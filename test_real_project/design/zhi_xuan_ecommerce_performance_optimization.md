# 智选电商平台性能优化策略

## 性能优化目标

智选电商平台的性能优化目标是确保95%的API请求在200ms内完成，支持10万QPS并发访问，实现高性能、低延迟的用户体验。

## 1. 整体性能架构优化

### 1.1 CDN加速策略

#### 静态资源CDN配置
```yaml
# cdn-configuration.yml
version: '3.8'

services:
  cdn-edge-server:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./cdn/nginx.conf:/etc/nginx/nginx.conf
      - ./cdn/ssl:/etc/ssl
      - /app/static:/var/www/static
    environment:
      - CDN_ORIGIN=http://api.zhixuan.com
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.labels.type == edge

# nginx.conf - CDN边缘节点配置
events {
    worker_connections 1024;
}

http {
    # 缓存配置
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=static_cache:10m 
                     max_size=10g inactive=60m use_temp_path=off;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript 
               text/xml application/xml application/xml+rss text/javascript;

    server {
        listen 80;
        server_name cdn.zhixuan.com;

        # 静态资源缓存
        location ~* \.(jpg|jpeg|png|gif|ico|svg|css|js|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            proxy_cache static_cache;
            proxy_cache_valid 200 1y;
            proxy_pass http://origin_servers;
        }

        # API请求代理
        location /api/ {
            proxy_pass http://api_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # 连接池优化
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            
            # 超时设置
            proxy_connect_timeout 5s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }
    }
}
```

### 1.2 负载均衡优化

#### 多级负载均衡架构
```
                    DNS负载均衡 (智能DNS)
                         │
                    CDN边缘节点 (L1缓存)
                         │
                    API网关 (L2负载均衡)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   用户服务集群      商品服务集群      订单服务集群
   (健康检查+路由)    (健康检查+路由)    (健康检查+路由)
```

#### Nginx负载均衡配置
```nginx
# nginx-load-balancer.conf
upstream user_service {
    least_conn;  # 最少连接算法，适合长连接
    server user-service-1:3001 max_fails=3 fail_timeout=30s;
    server user-service-2:3001 max_fails=3 fail_timeout=30s;
    server user-service-3:3001 max_fails=3 fail_timeout=30s;
    keepalive 32;  # 长连接池大小
}

upstream product_service {
    ip_hash;  # 会话保持
    server product-service-1:3002 max_fails=3 fail_timeout=30s;
    server product-service-2:3002 max_fails=3 fail_timeout=30s;
    server product-service-3:3002 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

upstream order_service {
    least_time;  # 最短响应时间算法
    server order-service-1:3003 max_fails=3 fail_timeout=30s;
    server order-service-2:3003 max_fails=3 fail_timeout=30s;
    server order-service-3:3003 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

# 主服务器配置
server {
    listen 80;
    server_name api.zhixuan.com;
    
    # 请求缓存
    location ~* /api/v1/products {
        proxy_cache product_cache;
        proxy_cache_valid 200 5m;
        proxy_cache_valid 404 1m;
        
        proxy_pass http://product_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # 响应头优化
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Response-Time $request_time;
    }
    
    # 动态请求
    location /api/ {
        proxy_pass http://$service_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 性能优化
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_connect_timeout 2s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
        
        # 压缩
        gzip on;
        gzip_types application/json text/plain;
    }
}
```

## 2. 数据库性能优化

### 2.1 查询优化策略

#### 索引优化
```sql
-- 用户表索引优化
CREATE INDEX idx_users_email_gin ON users USING gin(email gin_trgm_ops);
CREATE INDEX idx_users_created_at_btree ON users(created_at DESC);
CREATE INDEX idx_users_status_created_at ON users(status, created_at DESC);

-- 商品表复合索引
CREATE INDEX idx_products_category_status_price ON products(category_id, status, price ASC);
CREATE INDEX idx_products_name_gin ON products USING gin(to_tsvector('english', name));
CREATE INDEX idx_products_hot_new_recommend ON products(is_hot, is_new, is_recommend);

-- 订单表分区索引
CREATE INDEX idx_orders_user_status_created ON orders(user_id, status, created_at DESC);
CREATE INDEX idx_orders_created_at_brin ON orders USING brin(created_at) WITH (pages_per_range = 32);

-- 订单项表索引
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);
```

#### 查询优化示例
```sql
-- 优化前：全表扫描
SELECT * FROM products WHERE name LIKE '%手机%' AND price BETWEEN 1000 AND 5000;

-- 优化后：使用索引和覆盖索引
SELECT 
    product_id, 
    name, 
    price, 
    image_url,
    rating
FROM products 
WHERE to_tsvector('english', name) @@ to_tsquery('手机')
    AND price BETWEEN 1000 AND 5000
ORDER BY rating DESC
LIMIT 20;

-- 使用CTE优化复杂查询
WITH recent_orders AS (
    SELECT 
        order_id, 
        user_id, 
        total_amount, 
        created_at
    FROM orders 
    WHERE created_at >= NOW() - INTERVAL '30 days'
    AND status = 'completed'
),
user_stats AS (
    SELECT 
        user_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent,
        AVG(total_amount) as avg_order_value
    FROM recent_orders
    GROUP BY user_id
)
SELECT 
    u.username,
    u.email,
    us.order_count,
    us.total_spent,
    us.avg_order_value
FROM user_stats us
JOIN users u ON u.user_id = us.user_id
ORDER BY us.total_spent DESC
LIMIT 10;
```

### 2.2 连接池优化

#### PostgreSQL连接池配置
```typescript
// database-pool.service.ts
import { Injectable } from '@nestjs/common';
import { Pool } from 'pg';

@Injectable()
export class DatabasePoolService {
  private pools: Map<string, Pool> = new Map();

  constructor() {
    this.initPools();
  }

  private initPools() {
    const dbConfigs = {
      'user': {
        host: process.env.USER_DB_HOST || 'localhost',
        port: parseInt(process.env.USER_DB_PORT) || 5432,
        database: 'zhi_xuan_user',
        user: process.env.DB_USER || 'user',
        password: process.env.DB_PASSWORD || 'password',
      },
      'product': {
        host: process.env.PRODUCT_DB_HOST || 'localhost',
        port: parseInt(process.env.PRODUCT_DB_PORT) || 5432,
        database: 'zhi_xuan_product',
        user: process.env.DB_USER || 'user',
        password: process.env.DB_PASSWORD || 'password',
      },
      // ... 其他数据库配置
    };

    for (const [name, config] of Object.entries(dbConfigs)) {
      const pool = new Pool({
        ...config,
        // 连接池配置
        max: 50,  // 最大连接数
        min: 10,  // 最小连接数
        acquireTimeoutMillis: 2000,  // 获取连接超时时间
        createTimeoutMillis: 3000,   // 创建连接超时时间
        idleTimeoutMillis: 30000,    // 连接空闲超时时间
        Promise: require('bluebird'),
        
        // 连接健康检查
        verify: async (client) => {
          await client.query('SELECT 1');
        }
      });

      // 连接池事件监听
      pool.on('connect', (client) => {
        console.log(`Database pool: ${name} - New client connected`);
      });

      pool.on('acquire', (client) => {
        console.log(`Database pool: ${name} - Client acquired`);
      });

      pool.on('remove', (client) => {
        console.log(`Database pool: ${name} - Client removed`);
      });

      this.pools.set(name, pool);
    }
  }

  async executeQuery(dbName: string, query: string, params?: any[]) {
    const pool = this.pools.get(dbName);
    if (!pool) {
      throw new Error(`Database pool not found: ${dbName}`);
    }

    const start = Date.now();
    let client;
    
    try {
      client = await pool.connect();
      const result = await client.query(query, params);
      
      const duration = Date.now() - start;
      if (duration > 100) {
        console.warn(`Slow query detected: ${duration}ms - ${query}`);
      }
      
      return result;
    } finally {
      if (client) {
        client.release();
      }
    }
  }

  async executeTransaction(dbName: string, queries: Array<{query: string, params?: any[]}>) {
    const pool = this.pools.get(dbName);
    if (!pool) {
      throw new Error(`Database pool not found: ${dbName}`);
    }

    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      
      const results = [];
      for (const { query, params } of queries) {
        const result = await client.query(query, params);
        results.push(result);
      }
      
      await client.query('COMMIT');
      return results;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}
```

### 2.3 分库分表策略

#### 水平分表实现
```typescript
// sharding.service.ts
import { Injectable } from '@nestjs/common';

export interface ShardingConfig {
  tableName: string;
  shardKey: string;
  shardCount: number;
  algorithm: 'hash' | 'range' | 'date';
}

@Injectable()
export class ShardingService {
  private configs: Map<string, ShardingConfig> = new Map();

  constructor() {
    this.initShardingConfig();
  }

  private initShardingConfig() {
    // 用户表按用户ID哈希分表
    this.configs.set('users', {
      tableName: 'users',
      shardKey: 'user_id',
      shardCount: 8,
      algorithm: 'hash',
    });

    // 订单表按时间范围分表
    this.configs.set('orders', {
      tableName: 'orders',
      shardKey: 'created_at',
      shardCount: 12, // 按月分表
      algorithm: 'date',
    });
  }

  getShardTable(tableName: string, shardValue: any): string {
    const config = this.configs.get(tableName);
    if (!config) {
      return tableName; // 未配置分表的表返回原表名
    }

    const shardIndex = this.calculateShardIndex(config, shardValue);
    return `${tableName}_${shardIndex}`;
  }

  private calculateShardIndex(config: ShardingConfig, value: any): number {
    switch (config.algorithm) {
      case 'hash':
        // 简单哈希算法
        let hash = 0;
        const str = value.toString();
        for (let i = 0; i < str.length; i++) {
          hash = ((hash << 5) - hash) + str.charCodeAt(i);
          hash |= 0; // 转换为32位整数
        }
        return Math.abs(hash) % config.shardCount;

      case 'range':
        // 范围分片（简化实现）
        const numValue = Number(value);
        return Math.floor(numValue / (Number.MAX_SAFE_INTEGER / config.shardCount)) % config.shardCount;

      case 'date':
        // 按月分表
        const date = new Date(value);
        return date.getMonth();

      default:
        return 0;
    }
  }

  async executeShardedQuery(
    tableName: string, 
    query: string, 
    params?: any[], 
    shardValue?: any
  ) {
    const actualTable = this.getShardTable(tableName, shardValue);
    const modifiedQuery = query.replace(tableName, actualTable);
    
    // 这里应该调用数据库服务
    // return await this.databaseService.query(modifiedQuery, params);
  }

  async executeAllShardsQuery(tableName: string, query: string, params?: any[]) {
    const config = this.configs.get(tableName);
    if (!config) {
      // 未分表的表直接执行
      // return await this.databaseService.query(query, params);
    }

    // 在所有分片上执行查询
    const results = [];
    for (let i = 0; i < config.shardCount; i++) {
      const table = `${tableName}_${i}`;
      const modifiedQuery = query.replace(tableName, table);
      
      // const result = await this.databaseService.query(modifiedQuery, params);
      // results.push(result);
    }

    return this.mergeResults(results);
  }

  private mergeResults(results: any[]): any {
    // 合并分片查询结果
    // 这里需要根据具体的查询类型实现结果合并逻辑
    return results.flat();
  }
}
```

## 3. 缓存性能优化

### 3.1 多级缓存策略

#### L1缓存（进程内缓存）
```typescript
// l1-cache.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class L1CacheService {
  private cache: Map<string, { value: any; ttl: number; createdAt: number }> = new Map();
  private maxSize = 10000; // 最大缓存项数
  private ttl = 300; // 默认TTL: 5分钟

  set(key: string, value: any, customTtl?: number): void {
    if (this.cache.size >= this.maxSize) {
      // 使用LRU算法删除最久未使用的项
      this.evictLRU();
    }

    this.cache.set(key, {
      value,
      ttl: customTtl || this.ttl,
      createdAt: Date.now(),
    });
  }

  get<T = any>(key: string): T | null {
    const item = this.cache.get(key);
    if (!item) {
      return null;
    }

    // 检查是否过期
    if (Date.now() - item.createdAt > item.ttl * 1000) {
      this.cache.delete(key);
      return null;
    }

    return item.value as T;
  }

  has(key: string): boolean {
    const item = this.cache.get(key);
    if (!item) {
      return false;
    }

    // 检查是否过期
    if (Date.now() - item.createdAt > item.ttl * 1000) {
      this.cache.delete(key);
      return false;
    }

    return true;
  }

  delete(key: string): boolean {
    return this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }

  private evictLRU(): void {
    // 简化的LRU实现：删除最早添加的项
    const firstKey = this.cache.keys().next().value;
    if (firstKey) {
      this.cache.delete(firstKey);
    }
  }

  getStats(): { size: number; hitRate: number } {
    // 这里可以实现缓存统计功能
    return {
      size: this.cache.size,
      hitRate: 0, // 简化实现
    };
  }
}
```

#### L2缓存（Redis集群）
```typescript
// l2-cache.service.ts
import { Injectable } from '@nestjs/common';
import { Redis } from 'ioredis';

@Injectable()
export class L2CacheService {
  private redis: Redis;

  constructor() {
    this.redis = new Redis({
      cluster: {
        startupNodes: [
          { host: 'redis-node-1', port: 7001 },
          { host: 'redis-node-2', port: 7002 },
          { host: 'redis-node-3', port: 7003 },
        ],
        options: {
          redisOptions: {
            password: process.env.REDIS_PASSWORD,
            connectTimeout: 1000,
            retryDelayOnFailover: 100,
            maxRetriesPerRequest: 3,
          },
          scaleReads: 'slave', // 读取操作路由到从节点
        },
      },
    });
  }

  async set(key: string, value: any, ttl?: number): Promise<boolean> {
    try {
      const serializedValue = typeof value === 'string' ? value : JSON.stringify(value);
      
      if (ttl) {
        await this.redis.setex(key, ttl, serializedValue);
      } else {
        await this.redis.set(key, serializedValue);
      }
      
      return true;
    } catch (error) {
      console.error('L2 cache set error:', error);
      return false;
    }
  }

  async get<T = any>(key: string): Promise<T | null> {
    try {
      const value = await this.redis.get(key);
      if (value === null) {
        return null;
      }

      try {
        return JSON.parse(value);
      } catch {
        return value as T;
      }
    } catch (error) {
      console.error('L2 cache get error:', error);
      return null;
    }
  }

  async mget(keys: string[]): Promise<(any | null)[]> {
    try {
      const values = await this.redis.mget(keys);
      return values.map(value => {
        if (value === null) return null;
        try {
          return JSON.parse(value);
        } catch {
          return value;
        }
      });
    } catch (error) {
      console.error('L2 cache mget error:', error);
      return keys.map(() => null);
    }
  }

  async hget(hash: string, field: string): Promise<any> {
    try {
      const value = await this.redis.hget(hash, field);
      if (value === null) {
        return null;
      }

      try {
        return JSON.parse(value);
      } catch {
        return value;
      }
    } catch (error) {
      console.error('L2 cache hget error:', error);
      return null;
    }
  }

  async hset(hash: string, field: string, value: any): Promise<boolean> {
    try {
      const serializedValue = typeof value === 'string' ? value : JSON.stringify(value);
      await this.redis.hset(hash, field, serializedValue);
      return true;
    } catch (error) {
      console.error('L2 cache hset error:', error);
      return false;
    }
  }

  async exists(key: string): Promise<boolean> {
    try {
      const result = await this.redis.exists(key);
      return result === 1;
    } catch (error) {
      console.error('L2 cache exists error:', error);
      return false;
    }
  }

  async del(key: string | string[]): Promise<boolean> {
    try {
      if (Array.isArray(key)) {
        await this.redis.del(...key);
      } else {
        await this.redis.del(key);
      }
      return true;
    } catch (error) {
      console.error('L2 cache del error:', error);
      return false;
    }
  }

  async setWithCompression(key: string, value: any, ttl?: number): Promise<boolean> {
    // 对大数据进行压缩存储
    const serializedValue = JSON.stringify(value);
    
    if (serializedValue.length > 1024) { // 大于1KB时压缩
      try {
        // 这里可以使用gzip或其他压缩算法
        // const compressed = await this.compress(serializedValue);
        // await this.redis.setex(key, ttl || 3600, compressed);
        // return true;
      } catch (error) {
        // 压缩失败时存储原始数据
        return await this.set(key, value, ttl);
      }
    }
    
    return await this.set(key, value, ttl);
  }
}
```

### 3.2 缓存预热策略

#### 缓存预热服务
```typescript
// cache-warming.service.ts
import { Injectable, OnModuleInit } from '@nestjs/common';
import { L2CacheService } from './l2-cache.service';
import { DatabasePoolService } from './database-pool.service';

@Injectable()
export class CacheWarmingService implements OnModuleInit {
  constructor(
    private readonly cacheService: L2CacheService,
    private readonly dbService: DatabasePoolService,
  ) {}

  async onModuleInit() {
    // 应用启动时预热缓存
    await this.warmUpCache();
  }

  async warmUpCache(): Promise<void> {
    console.log('Starting cache warming...');
    
    const start = Date.now();
    
    try {
      // 预热热门商品
      await this.warmUpHotProducts();
      
      // 预热商品分类
      await this.warmUpCategories();
      
      // 预热系统配置
      await this.warmUpSystemConfig();
      
      // 预热用户会话配置
      await this.warmUpUserSessionConfig();
      
      const duration = Date.now() - start;
      console.log(`Cache warming completed in ${duration}ms`);
    } catch (error) {
      console.error('Cache warming failed:', error);
    }
  }

  private async warmUpHotProducts(): Promise<void> {
    console.log('Warming up hot products...');
    
    try {
      // 获取热门商品数据
      const hotProducts = await this.dbService.executeQuery('product', `
        SELECT 
          product_id, 
          name, 
          price, 
          image_url, 
          rating,
          stock_quantity
        FROM products 
        WHERE is_hot = true 
          AND status = 1
        ORDER BY rating DESC, sold_count DESC
        LIMIT 100
      `);

      // 批量设置缓存
      const pipeline = this.cacheService.createPipeline();
      
      for (const product of hotProducts.rows) {
        const key = `product:${product.product_id}`;
        await this.cacheService.set(key, product, 1800); // 30分钟TTL
      }
      
      console.log(`Warmed up ${hotProducts.rows.length} hot products`);
    } catch (error) {
      console.error('Failed to warm up hot products:', error);
    }
  }

  private async warmUpCategories(): Promise<void> {
    console.log('Warming up categories...');
    
    try {
      // 获取商品分类数据
      const categories = await this.dbService.executeQuery('product', `
        SELECT 
          category_id, 
          name, 
          slug, 
          image_url,
          parent_id
        FROM categories 
        WHERE status = 1
        ORDER BY sort_order ASC
      `);

      // 设置分类缓存
      for (const category of categories.rows) {
        const key = `category:${category.category_id}`;
        await this.cacheService.set(key, category, 3600); // 1小时TTL
      }
      
      // 设置分类树缓存
      const categoryTree = this.buildCategoryTree(categories.rows);
      await this.cacheService.set('category:tree', categoryTree, 3600);
      
      console.log(`Warmed up ${categories.rows.length} categories`);
    } catch (error) {
      console.error('Failed to warm up categories:', error);
    }
  }

  private async warmUpSystemConfig(): Promise<void> {
    console.log('Warming up system config...');
    
    try {
      // 获取系统配置
      const config = await this.dbService.executeQuery('user', `
        SELECT config_key, config_value 
        FROM system_config 
        WHERE status = 1
      `);

      const configMap = {};
      for (const row of config.rows) {
        try {
          configMap[row.config_key] = JSON.parse(row.config_value);
        } catch {
          configMap[row.config_key] = row.config_value;
        }
      }
      
      await this.cacheService.set('system:config', configMap, 7200); // 2小时TTL
      
      console.log('System config warmed up');
    } catch (error) {
      console.error('Failed to warm up system config:', error);
    }
  }

  private async warmUpUserSessionConfig(): Promise<void> {
    console.log('Warming up user session config...');
    
    try {
      // 预热用户会话相关配置
      const sessionConfig = {
        defaultPermissions: ['view_products', 'add_to_cart'],
        sessionTimeout: 1800, // 30分钟
        maxConcurrentSessions: 5,
      };
      
      await this.cacheService.set('user:session:config', sessionConfig, 3600);
      
      console.log('User session config warmed up');
    } catch (error) {
      console.error('Failed to warm up user session config:', error);
    }
  }

  private buildCategoryTree(categories: any[]): any[] {
    const categoryMap = new Map();
    const rootCategories = [];
    
    // 创建分类映射
    for (const category of categories) {
      categoryMap.set(category.category_id, { ...category, children: [] });
    }
    
    // 构建树结构
    for (const category of categories) {
      const cat = categoryMap.get(category.category_id);
      if (category.parent_id) {
        const parent = categoryMap.get(category.parent_id);
        if (parent) {
          parent.children.push(cat);
        }
      } else {
        rootCategories.push(cat);
      }
    }
    
    return rootCategories;
  }

  // 定时预热
  startScheduledWarming() {
    // 每小时预热一次
    setInterval(async () => {
      await this.warmUpHotProducts();
      await this.warmUpCategories();
    }, 3600000); // 1小时
    
    // 每天预热系统配置
    setInterval(async () => {
      await this.warmUpSystemConfig();
    }, 86400000); // 24小时
  }
}
```

## 4. 应用层性能优化

### 4.1 API响应优化

#### 响应压缩和分页优化
```typescript
// response-optimizer.service.ts
import { Injectable } from '@nestjs/common';
import * as zlib from 'zlib';
import { promisify } from 'util';

const gzip = promisify(zlib.gzip);
const deflate = promisify(zlib.deflate);

@Injectable()
export class ResponseOptimizerService {
  // 响应数据压缩
  async compressResponse(data: any, method: 'gzip' | 'deflate' = 'gzip'): Promise<Buffer> {
    const jsonString = JSON.stringify(data);
    
    // 对于小数据不压缩
    if (jsonString.length < 1024) {
      return Buffer.from(jsonString);
    }
    
    switch (method) {
      case 'gzip':
        return await gzip(jsonString, { level: 6 });
      case 'deflate':
        return await deflate(jsonString, { level: 6 });
      default:
        return Buffer.from(jsonString);
    }
  }

  // 智能分页
  createPaginatedResponse<T>(
    data: T[],
    page: number,
    limit: number,
    total: number,
    meta?: Record<string, any>
  ): any {
    const totalPages = Math.ceil(total / limit);
    const hasNextPage = page < totalPages;
    const hasPrevPage = page > 1;

    return {
      data,
      pagination: {
        current: page,
        pageSize: limit,
        total,
        totalPages,
        hasNextPage,
        hasPrevPage,
        nextPage: hasNextPage ? page + 1 : null,
        prevPage: hasPrevPage ? page - 1 : null,
      },
      meta: meta || {},
      timestamp: new Date().toISOString(),
    };
  }

  // 字段过滤和选择
  filterFields<T>(data: T, fields?: string[]): T {
    if (!fields || fields.length === 0) {
      return data;
    }

    if (Array.isArray(data)) {
      return data.map(item => this.filterFields(item, fields)) as any;
    }

    const filtered: any = {};
    for (const field of fields) {
      if ((data as any).hasOwnProperty(field)) {
        filtered[field] = (data as any)[field];
      }
    }
    return filtered;
  }

  // 数据脱敏
  sanitizeResponse(data: any, sensitiveFields: string[] = []): any {
    if (!data) return data;
    
    if (Array.isArray(data)) {
      return data.map(item => this.sanitizeResponse(item, sensitiveFields));
    }
    
    if (typeof data === 'object') {
      const sanitized: any = {};
      for (const [key, value] of Object.entries(data)) {
        if (sensitiveFields.includes(key)) {
          sanitized[key] = this.maskSensitiveData(value);
        } else if (typeof value === 'object' && value !== null) {
          sanitized[key] = this.sanitizeResponse(value, sensitiveFields);
        } else {
          sanitized[key] = value;
        }
      }
      return sanitized;
    }
    
    return data;
  }

  private maskSensitiveData(value: any): string {
    if (typeof value === 'string') {
      if (value.includes('@')) {
        // 邮箱脱敏
        const parts = value.split('@');
        if (parts[0].length > 2) {
          return parts[0].substring(0, 2) + '***@' + parts[1];
        }
        return '*@' + parts[1];
      } else if (value.length >= 11) {
        // 手机号脱敏
        return value.substring(0, 3) + '****' + value.substring(7);
      }
    }
    return '***';
  }

  // 响应时间优化
  async executeWithTimeout<T>(
    fn: () => Promise<T>, 
    timeout: number = 200  // 默认200ms超时
  ): Promise<T | null> {
    return Promise.race([
      fn(),
      new Promise<T>((_, reject) => 
        setTimeout(() => reject(new Error('Operation timeout')), timeout)
      )
    ]).catch(err => {
      if (err.message === 'Operation timeout') {
        console.warn('Operation timed out:', timeout, 'ms');
        return null;
      }
      throw err;
    });
  }
}
```

### 4.2 异步处理优化

#### 消息队列优化
```typescript
// message-queue.service.ts
import { Injectable } from '@nestjs/common';
import * as amqplib from 'amqplib';
import { v4 as uuidv4 } from 'uuid';

export interface QueueMessage {
  id: string;
  type: string;
  data: any;
  timestamp: number;
  priority?: number;
  retryCount?: number;
}

@Injectable()
export class MessageQueueService {
  private connection: amqplib.Connection;
  private channel: amqplib.Channel;
  private queues: Set<string> = new Set();

  async connect(): Promise<void> {
    this.connection = await amqplib.connect(process.env.RABBITMQ_URL || 'amqp://localhost:5672');
    this.channel = await this.connection.createChannel();
    
    // 确保交换机存在
    await this.channel.assertExchange('zhi_xuan_exchange', 'topic', { 
      durable: true 
    });
    
    console.log('Message queue connected');
  }

  async publish(
    routingKey: string, 
    message: QueueMessage,
    options: {
      priority?: number;
      expiration?: string;  // 毫秒
      persistent?: boolean;
    } = {}
  ): Promise<boolean> {
    try {
      const buffer = Buffer.from(JSON.stringify(message));
      
      const msgOptions = {
        persistent: options.persistent !== false,  // 默认持久化
        priority: options.priority || 0,
        expiration: options.expiration,
        timestamp: new Date(),
      };
      
      const result = this.channel.publish(
        'zhi_xuan_exchange',
        routingKey,
        buffer,
        msgOptions
      );
      
      if (result) {
        console.log(`Message published to ${routingKey}: ${message.id}`);
      }
      
      return result;
    } catch (error) {
      console.error('Failed to publish message:', error);
      return false;
    }
  }

  async consume(
    queueName: string,
    handler: (msg: amqplib.ConsumeMessage) => Promise<void>,
    options: {
      prefetch?: number;  // QoS设置
      durable?: boolean;
      autoDelete?: boolean;
    } = {}
  ): Promise<void> {
    // 确保队列存在
    await this.channel.assertQueue(queueName, {
      durable: options.durable !== false,
      autoDelete: options.autoDelete === true,
    });
    
    // 绑定队列到交换机
    await this.channel.bindQueue(queueName, 'zhi_xuan_exchange', queueName);
    
    // 设置QoS - 控制并发处理数
    await this.channel.prefetch(options.prefetch || 10);
    
    // 开始消费
    await this.channel.consume(queueName, async (msg) => {
      if (msg) {
        try {
          await handler(msg);
          this.channel.ack(msg); // 手动确认消息
        } catch (error) {
          console.error('Message processing failed:', error);
          // 根据错误类型决定是否重新入队
          if (this.shouldRetry(msg, error)) {
            this.channel.nack(msg, false, true); // 重新入队
          } else {
            this.channel.ack(msg); // 丢弃消息
          }
        }
      }
    });
    
    console.log(`Started consuming queue: ${queueName}`);
  }

  private shouldRetry(msg: amqplib.ConsumeMessage, error: any): boolean {
    // 解析消息获取重试次数
    const content = JSON.parse(msg.content.toString());
    const retryCount = content.retryCount || 0;
    
    // 最多重试3次
    if (retryCount >= 3) {
      return false;
    }
    
    // 对于某些错误类型不重试
    const nonRetryableErrors = ['ValidationError', 'AuthenticationError'];
    if (nonRetryableErrors.some(err => error.name?.includes(err))) {
      return false;
    }
    
    return true;
  }

  // 批量发布优化
  async batchPublish(
    routingKey: string,
    messages: QueueMessage[],
    batchSize: number = 100
  ): Promise<boolean> {
    if (messages.length === 0) return true;
    
    const pipeline = this.channel;
    let success = true;
    
    for (let i = 0; i < messages.length; i += batchSize) {
      const batch = messages.slice(i, i + batchSize);
      
      for (const message of batch) {
        const buffer = Buffer.from(JSON.stringify(message));
        const result = pipeline.publish(
          'zhi_xuan_exchange',
          routingKey,
          buffer,
          { persistent: true }
        );
        
        if (!result) {
          success = false;
        }
      }
    }
    
    return success;
  }

  // 延迟队列实现
  async publishDelayed(
    routingKey: string,
    message: QueueMessage,
    delayMs: number
  ): Promise<boolean> {
    // 使用RabbitMQ的延迟插件或TTL实现延迟消息
    const buffer = Buffer.from(JSON.stringify(message));
    
    // 创建延迟交换机
    await this.channel.assertExchange(`delayed_${routingKey}`, 'x-delayed-message', {
      durable: true,
      arguments: { 'x-delayed-type': 'topic' }
    });
    
    return this.channel.publish(
      `delayed_${routingKey}`,
      routingKey,
      buffer,
      {
        persistent: true,
        headers: { 'x-delay': delayMs }
      }
    );
  }
}
```

### 4.3 前端性能优化

#### React组件优化
```typescript
// performance-optimized-components.tsx
import React, { 
  memo, 
  useMemo, 
  useCallback, 
  useState, 
  useEffect 
} from 'react';

// 优化的商品列表组件
interface ProductListProps {
  products: Array<{
    id: string;
    name: string;
    price: number;
    image: string;
    rating: number;
  }>;;
  onAddToCart: (productId: string) => void;
  onPageChange: (page: number) => void;
  currentPage: number;
  totalPages: number;
}

const ProductList = memo(({ 
  products, 
  onAddToCart, 
  onPageChange, 
  currentPage, 
  totalPages 
}: ProductListProps) => {
  // 使用useMemo缓存计算结果
  const memoizedProducts = useMemo(() => {
    return products.map(product => ({
      ...product,
      displayPrice: `¥${product.price.toFixed(2)}`,
      displayRating: product.rating.toFixed(1)
    }));
  }, [products]);

  // 使用useCallback缓存函数
  const handleAddToCart = useCallback((productId: string) => {
    onAddToCart(productId);
  }, [onAddToCart]);

  return (
    <div className="product-grid">
      {memoizedProducts.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={handleAddToCart}
        />
      ))}
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={onPageChange}
      />
    </div>
  );
});

// 优化的商品卡片组件
interface ProductCardProps {
  product: {
    id: string;
    name: string;
    displayPrice: string;
    image: string;
    displayRating: string;
  };
  onAddToCart: (productId: string) => void;
}

const ProductCard = memo(({ product, onAddToCart }: ProductCardProps) => {
  const [isHovered, setIsHovered] = useState(false);

  // 防抖处理
  const debouncedAddToCart = useMemo(() => {
    let timeoutId: NodeJS.Timeout;
    return (productId: string) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        onAddToCart(productId);
      }, 300);
    };
  }, [onAddToCart]);

  return (
    <div 
      className={`product-card ${isHovered ? 'hovered' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <img 
        src={product.image} 
        alt={product.name}
        loading="lazy"  // 懒加载
        className="product-image"
      />
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <div className="product-rating">
          {'★'.repeat(Math.floor(parseFloat(product.displayRating)))}
          {'☆'.repeat(5 - Math.floor(parseFloat(product.displayRating)))}
          <span>{product.displayRating}</span>
        </div>
        <div className="product-price">{product.displayPrice}</div>
        <button 
          onClick={() => debouncedAddToCart(product.id)}
          className="add-to-cart-btn"
          disabled={!isHovered}
        >
          加入购物车
        </button>
      </div>
    </div>
  );
});

// 虚拟滚动列表 (用于大量数据渲染)
interface VirtualListProps<T> {
  items: T[];
  itemHeight: number;
  containerHeight: number;
  renderItem: (item: T, index: number) => React.ReactNode;
}

const VirtualList = <T extends {}>({ 
  items,
  itemHeight,
  containerHeight,
  renderItem
}: VirtualListProps<T>) => {
  const [scrollTop, setScrollTop] = useState(0);
  
  const visibleStart = Math.floor(scrollTop / itemHeight);
  const visibleCount = Math.ceil(containerHeight / itemHeight);
  const visibleEnd = Math.min(visibleStart + visibleCount, items.length);
  
  const visibleItems = items.slice(visibleStart, visibleEnd);
  
  const spacerStyle = {
    height: `${visibleStart * itemHeight}px`
  };
  
  const endSpacerStyle = {
    height: `${(items.length - visibleEnd) * itemHeight}px`
  };

  return (
    <div 
      className="virtual-list-container"
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.currentTarget.scrollTop)}
    >
      <div style={spacerStyle} />
      {visibleItems.map((item, index) => (
        <div 
          key={visibleStart + index}
          style={{ height: itemHeight }}
        >
          {renderItem(item, visibleStart + index)}
        </div>
      ))}
      <div style={endSpacerStyle} />
    </div>
  );
};

export { ProductList, VirtualList };
```

## 5. 性能监控与调优

### 5.1 性能指标监控

#### 性能监控服务
```typescript
// performance-monitoring.service.ts
import { Injectable } from '@nestjs/common';
import * as client from 'prom-client';

@Injectable()
export class PerformanceMonitoringService {
  private register: client.Registry;
  
  // 性能指标
  private apiResponseTime: client.Histogram<string>;
  private databaseQueryTime: client.Histogram<string>;
  private cacheHitRatio: client.Gauge<string>;
  private activeUsers: client.Gauge<string>;
  private requestRate: client.Gauge<string>;

  constructor() {
    this.register = new client.Registry();
    this.initMetrics();
  }

  private initMetrics() {
    // API响应时间直方图
    this.apiResponseTime = new client.Histogram({
      name: 'api_response_time_seconds',
      help: 'API response time in seconds',
      labelNames: ['endpoint', 'method', 'status'],
      buckets: [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10],
    });

    // 数据库查询时间直方图
    this.databaseQueryTime = new client.Histogram({
      name: 'database_query_time_seconds',
      help: 'Database query time in seconds',
      labelNames: ['query_type', 'table'],
      buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1],
    });

    // 缓存命中率
    this.cacheHitRatio = new client.Gauge({
      name: 'cache_hit_ratio',
      help: 'Cache hit ratio',
      labelNames: ['cache_type'],
    });

    // 活跃用户数
    this.activeUsers = new client.Gauge({
      name: 'active_users',
      help: 'Number of active users',
    });

    // 请求率
    this.requestRate = new client.Gauge({
      name: 'request_rate_per_second',
      help: 'Request rate per second',
    });

    // 注册指标
    this.register.registerMetric(this.apiResponseTime);
    this.register.registerMetric(this.databaseQueryTime);
    this.register.registerMetric(this.cacheHitRatio);
    this.register.registerMetric(this.activeUsers);
    this.register.registerMetric(this.requestRate);
  }

  // 记录API响应时间
  recordApiResponse(endpoint: string, method: string, status: number, duration: number) {
    this.apiResponseTime.observe(
      { endpoint, method, status: status.toString() },
      duration
    );
  }

  // 记录数据库查询时间
  recordDatabaseQuery(queryType: string, table: string, duration: number) {
    this.databaseQueryTime.observe(
      { query_type: queryType, table },
      duration
    );
  }

  // 更新缓存命中率
  updateCacheHitRatio(cacheType: string, ratio: number) {
    this.cacheHitRatio.set({ cache_type: cacheType }, ratio);
  }

  // 更新活跃用户数
  updateActiveUsers(count: number) {
    this.activeUsers.set(count);
  }

  // 更新请求率
  updateRequestRate(rate: number) {
    this.requestRate.set(rate);
  }

  // 性能分析装饰器
  performanceTrack(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function (...args: any[]) {
      const start = process.hrtime.bigint();
      
      try {
        const result = await originalMethod.apply(this, args);
        
        const duration = Number(process.hrtime.bigint() - start) / 1e9; // 转换为秒
        
        // 记录性能指标
        const endpoint = `${target.constructor.name}.${propertyKey}`;
        this.performanceMonitoringService?.recordApiResponse(
          endpoint,
          'INTERNAL',
          200,
          duration
        );
        
        return result;
      } catch (error) {
        const duration = Number(process.hrtime.bigint() - start) / 1e9;
        
        const endpoint = `${target.constructor.name}.${propertyKey}`;
        this.performanceMonitoringService?.recordApiResponse(
          endpoint,
          'INTERNAL',
          500,
          duration
        );
        
        throw error;
      }
    };
    
    return descriptor;
  }
}
```

### 5.2 性能调优脚本

#### 性能压测和调优
```bash
#!/bin/bash
# performance-tuning.sh - 性能调优脚本

# 性能测试配置
CONCURRENCY=${1:-100}  # 并发数
DURATION=${2:-60}      # 测试持续时间(秒)
TARGET_URL=${3:-"http://localhost:3000/api/v1/products"}

# 性能测试
run_performance_test() {
    echo "Running performance test..."
    echo "Target: $TARGET_URL"
    echo "Concurrency: $CONCURRENCY"
    echo "Duration: $DURATION seconds"
    
    # 使用wrk进行性能测试
    if command -v wrk &> /dev/null; then
        wrk -t$(nproc) -c$CONCURRENCY -d${DURATION}s $TARGET_URL
    else
        # 使用ab作为备选
        if command -v ab &> /dev/null; then
            ab -n 1000 -c $CONCURRENCY $TARGET_URL
        else
            echo "No performance testing tool found (wrk or ab)"
            return 1
        fi
    fi
}

# 数据库性能调优
optimize_database() {
    echo "Optimizing database performance..."
    
    # 分析查询性能
    psql -d zhi_xuan_product -c "
        SELECT 
            query,
            calls,
            total_time,
            mean_time,
            (total_time / calls) as avg_time
        FROM pg_stat_statements 
        ORDER BY total_time DESC 
        LIMIT 10;
    "
    
    # 检查缺失的索引
    psql -d zhi_xuan_product -c "
        SELECT 
            schemaname,
            tablename,
            attname,
            n_distinct,
            correlation
        FROM pg_stats
        WHERE schemaname = 'public'
        ORDER BY n_distinct ASC
        LIMIT 10;
    "
    
    # 统计信息更新
    echo "Updating table statistics..."
    psql -d zhi_xuan_product -c "ANALYZE;"
}

# 系统资源监控
monitor_system_resources() {
    echo "Monitoring system resources..."
    
    # CPU使用率
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1 "%"}'
    
    # 内存使用率
    echo "Memory Usage:"
    free -h | awk 'NR==2{printf "%.2f%%\n", $3*100/$2}'
    
    # 磁盘使用率
    echo "Disk Usage:"
    df -h | grep -E '^([A-Za-z]:|/)' | awk '{print $5 " " $6}'
    
    # 网络连接数
    echo "Active Connections:"
    ss -s
}

# JVM/Node.js参数调优 (示例)
optimize_nodejs() {
    echo "Optimizing Node.js performance..."
    
    # 建议的Node.js启动参数
    cat << EOF
Recommended Node.js startup parameters:
node --max-old-space-size=4096 \\
     --optimize-for-size \\
     --always-compact \\
     --expose-gc \\
     --max-semi-space-size=512 \\
     app.js
EOF
}

# 生成性能报告
generate_performance_report() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local report_dir="performance_reports"
    mkdir -p $report_dir
    
    local report_file="$report_dir/performance_report_$timestamp.txt"
    
    echo "Performance Report - $(date)" > $report_file
    echo "=================================" >> $report_file
    
    echo "System Resources:" >> $report_file
    echo "CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | awk -F'%' '{print $1}')" >> $report_file
    echo "Memory: $(free -h | awk 'NR==2{printf "%.2f%%", $3*100/$2})" >> $report_file
    echo "" >> $report_file
    
    echo "Database Performance:" >> $report_file
    echo "Slow queries (top 5):" >> $report_file
    psql -d zhi_xuan_product -c "
        SELECT query, mean_time 
        FROM pg_stat_statements 
        ORDER BY mean_time DESC 
        LIMIT 5;
    " >> $report_file 2>/dev/null || echo "Database not accessible" >> $report_file
    echo "" >> $report_file
    
    echo "Recommendations:" >> $report_file
    echo "- Consider adding indexes for slow queries" >> $report_file
    echo "- Optimize cache hit ratios" >> $report_file
    echo "- Review application code for performance bottlenecks" >> $report_file
    
    echo "Performance report generated: $report_file"
}

# 执行性能优化流程
echo "Starting performance optimization process..."
run_performance_test
monitor_system_resources
optimize_database
generate_performance_report

echo "Performance optimization completed."
```

## 6. 性能优化总结

通过实施以上性能优化策略，智选电商平台能够：

1. **API响应时间优化** - 通过多级缓存、数据库优化、CDN加速，确保95%的API请求在200ms内完成
2. **高并发处理能力** - 通过负载均衡、连接池优化、异步处理，支持10万QPS并发访问
3. **系统资源利用率优化** - 通过监控和调优，提高CPU、内存、网络等资源的使用效率
4. **用户体验优化** - 通过前端优化、响应压缩、虚拟滚动等技术，提升用户交互体验

这套性能优化策略从架构、数据库、缓存、应用、前端等多个层面确保了系统的高性能表现，满足智选电商平台的性能需求。
