# 智选电商平台缓存架构设计 (Redis集群)

## 缓存架构概述

智选电商平台采用Redis集群作为主要缓存解决方案，通过多级缓存策略、数据分片和高可用部署，满足高并发访问需求，确保95%的API请求在200ms内完成。

## Redis集群架构设计

### 1. 集群拓扑
```
                    Redis Cluster (16384个哈希槽)
                    ├── Master-1 ── Slave-1 (北京)
                    ├── Master-2 ── Slave-2 (上海) 
                    ├── Master-3 ── Slave-3 (深圳)
                    └── Master-4 ── Slave-4 (备用)
                                │
                    应用服务器集群 (Node.js微服务)
```

### 2. 集群配置
```yaml
# redis-cluster.yml
version: '3.8'

services:
  redis-node-1:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "7001:7001"
      - "17001:17001"
    volumes:
      - redis-node-1-data:/data
      - ./redis-conf/node-1.conf:/usr/local/etc/redis/redis.conf
    networks:
      - redis-net

  redis-node-2:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "7002:7002"
      - "17002:17002"
    volumes:
      - redis-node-2-data:/data
      - ./redis-conf/node-2.conf:/usr/local/etc/redis/redis.conf
    networks:
      - redis-net

  redis-node-3:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "7003:7003"
      - "17003:17003"
    volumes:
      - redis-node-3-data:/data
      - ./redis-conf/node-3.conf:/usr/local/etc/redis/redis.conf
    networks:
      - redis-net

  redis-node-4:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "7004:7004"
      - "17004:17004"
    volumes:
      - redis-node-4-data:/data
      - ./redis-conf/node-4.conf:/usr/local/etc/redis/redis.conf
    networks:
      - redis-net

  redis-node-5:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "7005:7005"
      - "17005:17005"
    volumes:
      - redis-node-5-data:/data
      - ./redis-conf/node-5.conf:/usr/local/etc/redis/redis.conf
    networks:
      - redis-net

  redis-node-6:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "7006:7006"
      - "17006:17006"
    volumes:
      - redis-node-6-data:/data
      - ./redis-conf/node-6.conf:/usr/local/etc/redis/redis.conf
    networks:
      - redis-net

volumes:
  redis-node-1-data:
  redis-node-2-data:
  redis-node-3-data:
  redis-node-4-data:
  redis-node-5-data:
  redis-node-6-data:

networks:
  redis-net:
    driver: bridge
```

### 3. Redis节点配置文件

#### Master节点配置 (node-1.conf)
```conf
# 基本配置
port 7001
bind 0.0.0.0
timeout 0
tcp-keepalive 300

# 集群配置
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 15000
cluster-require-full-coverage no

# 持久化配置
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# 内存配置
maxmemory 2gb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# 日志配置
loglevel notice
logfile /var/log/redis/redis-server.log

# 安全配置
requirepass your_redis_password
masterauth your_redis_password

# 客户端配置
tcp-backlog 511
databases 1
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data

# 高可用配置
repl-timeout 60
repl-ping-replica-period 10
repl-backlog-size 10mb
repl-backlog-ttl 3600
slave-priority 100
```

## 缓存策略设计

### 1. 多级缓存架构
```
应用层
├── L1 Cache: Node.js进程内缓存 (5-10分钟)
├── L2 Cache: Redis集群 (30分钟-24小时)
└── L3 Cache: CDN (静态资源，24小时+)
```

### 2. 缓存数据分类

#### 热点数据 (TTL: 30分钟)
```javascript
// 用户会话数据
SET session:{sessionId} {userInfo} EX 1800

// 商品基本信息
HMSET product:{productId} name {name} price {price} category_id {categoryId} EX 1800

// 首页推荐商品
ZADD homepage_hot_products {score} {productId} EX 1800
```

#### 静态配置数据 (TTL: 24小时)
```javascript
// 商品分类数据
HMSET categories:{timestamp} {categoryData} EX 86400

// 平台配置信息
HMSET platform_config {configData} EX 86400
```

### 3. 缓存键命名规范
```javascript
// 用户相关
const cacheKeys = {
  // 用户会话
  session: (sessionId) => `session:${sessionId}`,
  
  // 用户信息
  userInfo: (userId) => `user:info:${userId}`,
  
  // 用户购物车
  userCart: (userId) => `cart:${userId}`,
  
  // 商品相关
  product: (productId) => `product:${productId}`,
  productDetail: (productId) => `product:detail:${productId}`,
  
  // 分类相关
  category: (categoryId) => `category:${categoryId}`,
  
  // 订单相关
  order: (orderId) => `order:${orderId}`,
  
  // 搜索相关
  searchResult: (keyword, page) => `search:${keyword}:${page}`,
  
  // 营销相关
  coupon: (couponId) => `coupon:${couponId}`,
  userCoupon: (userId) => `user:coupons:${userId}`,
  
  // 库存相关
  inventory: (productId) => `inventory:${productId}`,
  
  // 系统配置
  config: (key) => `config:${key}`
};
```

## Redis客户端实现

### 1. Redis集群客户端封装
```typescript
// redis-cluster.service.ts
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { Cluster, ClusterOptions, RedisOptions } from 'ioredis';

@Injectable()
export class RedisClusterService implements OnModuleInit, OnModuleDestroy {
  private cluster: Cluster;
  
  constructor() {
    const redisOptions: ClusterOptions = {
      startupNodes: [
        { host: process.env.REDIS_HOST_1 || 'localhost', port: 7001 },
        { host: process.env.REDIS_HOST_2 || 'localhost', port: 7002 },
        { host: process.env.REDIS_HOST_3 || 'localhost', port: 7003 },
      ],
      options: {
        redisOptions: {
          password: process.env.REDIS_PASSWORD || 'your_redis_password',
          connectTimeout: 30000,
          retryDelayOnFailover: 100,
          maxRetriesPerRequest: 3,
          enableReadyCheck: true,
        },
        scaleReads: 'all', // 读操作分布到所有节点（包括主从）
        slotsRefreshTimeout: 2000,
        dnsLookup: (address, callback) => callback(null, address),
      },
    };
    
    this.cluster = new Cluster(redisOptions.startupNodes, redisOptions.options);
    
    // 监听集群事件
    this.cluster.on('connect', () => {
      console.log('Redis cluster connected');
    });
    
    this.cluster.on('error', (error) => {
      console.error('Redis cluster error:', error);
    });
    
    this.cluster.on('close', () => {
      console.log('Redis cluster closed');
    });
    
    // 监听节点故障转移
    this.cluster.on('node error', (error) => {
      console.error('Redis node error:', error);
    });
  }

  async onModuleInit() {
    // 等待集群连接就绪
    await this.cluster.ping();
  }

  async onModuleDestroy() {
    await this.cluster.quit();
  }

  // 基础操作方法
  async get(key: string): Promise<string | null> {
    return await this.cluster.get(key);
  }

  async set(key: string, value: string, ttl?: number): Promise<'OK'> {
    if (ttl) {
      return await this.cluster.setex(key, ttl, value);
    }
    return await this.cluster.set(key, value);
  }

  async hget(hash: string, field: string): Promise<string | null> {
    return await this.cluster.hget(hash, field);
  }

  async hset(hash: string, field: string, value: string): Promise<number> {
    return await this.cluster.hset(hash, field, value);
  }

  async hgetall(hash: string): Promise<Record<string, string>> {
    return await this.cluster.hgetall(hash);
  }

  async del(key: string | string[]): Promise<number> {
    if (Array.isArray(key)) {
      return await this.cluster.del(...key);
    }
    return await this.cluster.del(key);
  }

  async exists(key: string): Promise<boolean> {
    const result = await this.cluster.exists(key);
    return result === 1;
  }

  async expire(key: string, seconds: number): Promise<boolean> {
    const result = await this.cluster.expire(key, seconds);
    return result === 1;
  }

  async ttl(key: string): Promise<number> {
    return await this.cluster.ttl(key);
  }

  // 批量操作
  async mget(keys: string[]): Promise<(string | null)[]> {
    return await this.cluster.mget(keys);
  }

  async mset(keyValuePairs: [string, string][]): Promise<'OK'> {
    const flattened = keyValuePairs.flat();
    return await this.cluster.mset(...flattened);
  }

  // 集合操作
  async sadd(key: string, ...members: string[]): Promise<number> {
    return await this.cluster.sadd(key, ...members);
  }

  async smembers(key: string): Promise<string[]> {
    return await this.cluster.smembers(key);
  }

  async zadd(key: string, score: number, member: string): Promise<number>;
  async zadd(key: string, ...scoreMembers: (number | string)[]): Promise<number>;
  async zadd(key: string, ...args: (number | string)[]): Promise<number> {
    return await this.cluster.zadd(key, ...args);
  }

  async zrange(key: string, start: number, stop: number): Promise<string[]> {
    return await this.cluster.zrange(key, start, stop);
  }

  async zrevrange(key: string, start: number, stop: number): Promise<string[]> {
    return await this.cluster.zrevrange(key, start, stop);
  }

  // 事务操作
  async multi(): Promise<any> {
    return this.cluster.multi();
  }

  // 管道操作
  async pipeline(): Promise<any> {
    return this.cluster.pipeline();
  }
}
```

### 2. 缓存管理服务
```typescript
// cache.service.ts
import { Injectable } from '@nestjs/common';
import { RedisClusterService } from './redis-cluster.service';

export interface CacheConfig {
  ttl?: number;        // 过期时间（秒）
  staleTtl?: number;   // 缓存标记过期但保留时间
  retryAttempts?: number; // 重试次数
  compress?: boolean;  // 是否压缩
}

@Injectable()
export class CacheService {
  constructor(private readonly redisService: RedisClusterService) {}

  async get<T = any>(key: string): Promise<T | null> {
    try {
      const cachedValue = await this.redisService.get(key);
      if (cachedValue) {
        return JSON.parse(cachedValue);
      }
      return null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  }

  async set<T = any>(key: string, value: T, config?: CacheConfig): Promise<void> {
    try {
      const ttl = config?.ttl || 3600; // 默认1小时
      const stringValue = JSON.stringify(value);
      await this.redisService.set(key, stringValue, ttl);
    } catch (error) {
      console.error('Cache set error:', error);
    }
  }

  async setHash(key: string, field: string, value: any, config?: CacheConfig): Promise<void> {
    try {
      const ttl = config?.ttl || 3600;
      await this.redisService.hset(key, field, JSON.stringify(value));
      
      // 设置整个hash的过期时间
      await this.redisService.expire(key, ttl);
    } catch (error) {
      console.error('Cache hash set error:', error);
    }
  }

  async getHash<T = any>(key: string, field: string): Promise<T | null> {
    try {
      const value = await this.redisService.hget(key, field);
      if (value) {
        return JSON.parse(value);
      }
      return null;
    } catch (error) {
      console.error('Cache hash get error:', error);
      return null;
    }
  }

  async getHashAll<T = any>(key: string): Promise<Record<string, T>> {
    try {
      const hash = await this.redisService.hgetall(key);
      const result: Record<string, T> = {};
      
      for (const [field, value] of Object.entries(hash)) {
        try {
          result[field] = JSON.parse(value);
        } catch (e) {
          result[field] = value as any;
        }
      }
      
      return result;
    } catch (error) {
      console.error('Cache hash get all error:', error);
      return {};
    }
  }

  async delete(key: string): Promise<void> {
    try {
      await this.redisService.del(key);
    } catch (error) {
      console.error('Cache delete error:', error);
    }
  }

  async deleteMany(keys: string[]): Promise<void> {
    try {
      if (keys.length > 0) {
        await this.redisService.del(keys);
      }
    } catch (error) {
      console.error('Cache delete many error:', error);
    }
  }

  // 带缓存穿透保护的查询
  async getOrSet<T = any>(
    key: string, 
    fetchFn: () => Promise<T>, 
    config?: CacheConfig
  ): Promise<T> {
    // 先从缓存获取
    let value = await this.get<T>(key);
    
    if (value !== null) {
      return value;
    }

    // 尝试获取分布式锁（防止缓存击穿）
    const lockKey = `${key}:lock`;
    const lockExpire = 10; // 锁过期时间10秒
    
    try {
      // 尝试获取分布式锁
      const lockResult = await this.redisService.set(lockKey, '1', lockExpire);
      
      if (lockResult === 'OK') {
        // 获取锁成功，执行查询
        value = await fetchFn();
        
        if (value !== null) {
          // 设置缓存
          await this.set(key, value, config);
        } else {
          // 防止缓存穿透，设置空值缓存
          await this.set(key, null, { ttl: 60 }); // 空值缓存1分钟
        }
        
        // 释放锁
        await this.redisService.del(lockKey);
        return value;
      } else {
        // 获取锁失败，等待一段时间后重试
        await new Promise(resolve => setTimeout(resolve, 50));
        return await this.getOrSet(key, fetchFn, config);
      }
    } catch (error) {
      console.error('Cache getOrSet error:', error);
      // 锁获取失败或执行异常，直接查询数据库
      return await fetchFn();
    }
  }

  // 缓存预热
  async warmUpCache(): Promise<void> {
    console.log('Starting cache warm-up...');
    
    // 预热热门商品
    await this.warmUpHotProducts();
    
    // 预热商品分类
    await this.warmUpCategories();
    
    // 预热系统配置
    await this.warmUpSystemConfig();
    
    console.log('Cache warm-up completed');
  }

  private async warmUpHotProducts(): Promise<void> {
    // 这里应该调用商品服务获取热门商品数据
    // 示例伪代码
    console.log('Warming up hot products...');
  }

  private async warmUpCategories(): Promise<void> {
    // 预热商品分类数据
    console.log('Warming up categories...');
  }

  private async warmUpSystemConfig(): Promise<void> {
    // 预热系统配置数据
    console.log('Warming up system config...');
  }

  // 缓存清理
  async clearPattern(pattern: string): Promise<void> {
    try {
      // 获取匹配模式的所有key
      const keys = await this.redisService.cluster.keys(pattern);
      
      if (keys.length > 0) {
        await this.redisService.del(keys);
      }
    } catch (error) {
      console.error('Cache clear pattern error:', error);
    }
  }
}
```

### 3. 缓存装饰器
```typescript
// cache.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const Cacheable = (options: {
  key: string;
  ttl?: number;
  condition?: (args: any[]) => boolean;
}) => SetMetadata('cache:options', options);

export const CacheEvict = (options: {
  key: string;
  beforeInvocation?: boolean; // 是否在方法执行前清除缓存
}) => SetMetadata('cache:evict', options);

export const CachePut = (options: {
  key: string;
  ttl?: number;
}) => SetMetadata('cache:put', options);
```

### 4. 缓存拦截器
```typescript
// cache.interceptor.ts
import { 
  Injectable, 
  NestInterceptor, 
  ExecutionContext, 
  CallHandler 
} from '@nestjs/common';
import { Observable, of } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { Reflector } from '@nestjs/core';
import { CacheService } from './cache.service';

@Injectable()
export class CacheInterceptor implements NestInterceptor {
  constructor(
    private readonly reflector: Reflector,
    private readonly cacheService: CacheService,
  ) {}

  async intercept(context: ExecutionContext, next: CallHandler): Promise<Observable<any>> {
    const cacheOptions = this.reflector.get('cache:options', context.getHandler());
    
    if (!cacheOptions) {
      return next.handle();
    }

    const { key, ttl, condition } = cacheOptions;
    const args = context.getArgs();
    
    // 检查缓存条件
    if (condition && !condition(args)) {
      return next.handle();
    }

    // 生成动态缓存键
    const cacheKey = this.generateCacheKey(key, args);
    
    // 尝试从缓存获取
    const cachedValue = await this.cacheService.get(cacheKey);
    
    if (cachedValue !== null) {
      return of(cachedValue);
    }

    // 执行原方法并缓存结果
    return next.handle().pipe(
      tap(async (result) => {
        await this.cacheService.set(cacheKey, result, { ttl });
      }),
      catchError((error) => {
        throw error;
      })
    );
  }

  private generateCacheKey(pattern: string, args: any[]): string {
    // 将参数嵌入到缓存键中
    let key = pattern;
    
    // 替换 {0}, {1} 等占位符
    args.forEach((arg, index) => {
      if (typeof arg === 'object') {
        key = key.replace(`{${index}}`, JSON.stringify(arg));
      } else {
        key = key.replace(`{${index}}`, arg);
      }
    });
    
    return key;
  }
}
```

## 缓存更新策略

### 1. Cache-Aside模式实现
```typescript
// cache-aside-pattern.service.ts
import { Injectable } from '@nestjs/common';
import { CacheService } from './cache.service';

@Injectable()
export class CacheAsideService {
  constructor(private readonly cacheService: CacheService) {}

  async getDataWithCache<T>(
    cacheKey: string,
    fetchFromSource: () => Promise<T>,
    ttl: number = 3600
  ): Promise<T> {
    // 1. 尝试从缓存获取
    let data = await this.cacheService.get<T>(cacheKey);
    
    if (data !== null) {
      console.log(`Cache hit for key: ${cacheKey}`);
      return data;
    }

    console.log(`Cache miss for key: ${cacheKey}, fetching from source...`);
    
    // 2. 缓存未命中，从数据源获取
    data = await fetchFromSource();
    
    // 3. 将数据写入缓存
    if (data !== null) {
      await this.cacheService.set(cacheKey, data, { ttl });
    }
    
    return data;
  }

  async updateDataWithCache<T>(
    cacheKey: string,
    updateInSource: () => Promise<T>,
    updateInCache: boolean = true
  ): Promise<T> {
    // 1. 更新数据源
    const updatedData = await updateInSource();
    
    // 2. 更新或删除缓存
    if (updateInCache) {
      await this.cacheService.set(cacheKey, updatedData);
    } else {
      await this.cacheService.delete(cacheKey);
    }
    
    return updatedData;
  }

  async deleteDataWithCache(
    cacheKey: string,
    deleteFromSource: () => Promise<void>
  ): Promise<void> {
    // 1. 删除数据源
    await deleteFromSource();
    
    // 2. 删除缓存
    await this.cacheService.delete(cacheKey);
  }
}
```

### 2. Write-Through模式实现
```typescript
// write-through-cache.service.ts
import { Injectable } from '@nestjs/common';
import { CacheService } from './cache.service';

@Injectable()
export class WriteThroughCacheService {
  constructor(private readonly cacheService: CacheService) {}

  async writeThrough<T>(
    cacheKey: string,
    data: T,
    writeToSource: (data: T) => Promise<void>,
    ttl: number = 3600
  ): Promise<void> {
    try {
      // 1. 先写入缓存
      await this.cacheService.set(cacheKey, data, { ttl });
      
      // 2. 再写入数据源
      await writeToSource(data);
      
      console.log(`Data written through cache and source for key: ${cacheKey}`);
    } catch (error) {
      console.error('Write-through failed:', error);
      
      // 写入失败时删除缓存，避免脏数据
      await this.cacheService.delete(cacheKey);
      
      throw error;
    }
  }
}
```

## 缓存监控与运维

### 1. 缓存监控服务
```typescript
// cache-monitor.service.ts
import { Injectable, OnModuleInit } from '@nestjs/common';
import { RedisClusterService } from './redis-cluster.service';

export interface CacheMetrics {
  hits: number;
  misses: number;
  hitRate: number;
  total: number;
  memoryUsage: number;
  connectedClients: number;
  opsPerSecond: number;
}

@Injectable()
export class CacheMonitorService implements OnModuleInit {
  private metrics: Map<string, CacheMetrics> = new Map();
  
  constructor(private readonly redisService: RedisClusterService) {}

  async onModuleInit() {
    // 启动监控定时任务
    this.startMonitoring();
  }

  private async startMonitoring() {
    setInterval(async () => {
      await this.collectMetrics();
    }, 30000); // 每30秒收集一次指标
  }

  async collectMetrics(): Promise<CacheMetrics> {
    try {
      // 获取Redis信息
      const info = await this.redisService.cluster.info();
      
      // 解析Redis信息
      const lines = info.split('\n');
      const infoMap: Record<string, string> = {};
      
      for (const line of lines) {
        if (line.startsWith('#') || !line.includes(':')) continue;
        const [key, value] = line.split(':');
        infoMap[key.trim()] = value.trim();
      }
      
      const metrics: CacheMetrics = {
        hits: parseInt(infoMap['keyspace_hits'] || '0'),
        misses: parseInt(infoMap['keyspace_misses'] || '0'),
        total: parseInt(infoMap['total_commands_processed'] || '0'),
        connectedClients: parseInt(infoMap['connected_clients'] || '0'),
        memoryUsage: parseInt(infoMap['used_memory'] || '0'),
        opsPerSecond: parseInt(infoMap['instantaneous_ops_per_sec'] || '0'),
        hitRate: 0
      };
      
      // 计算命中率
      if ((metrics.hits + metrics.misses) > 0) {
        metrics.hitRate = (metrics.hits / (metrics.hits + metrics.misses)) * 100;
      }
      
      // 更新指标
      this.updateMetrics(metrics);
      
      return metrics;
    } catch (error) {
      console.error('Failed to collect cache metrics:', error);
      return null;
    }
  }

  private updateMetrics(metrics: CacheMetrics) {
    // 存储指标历史
    const now = Date.now();
    const key = new Date().toISOString().split('T')[0]; // 按天分组
    
    if (!this.metrics.has(key)) {
      this.metrics.set(key, metrics);
    } else {
      // 更新现有指标
      const existing = this.metrics.get(key)!;
      existing.hits = metrics.hits;
      existing.misses = metrics.misses;
      existing.hitRate = metrics.hitRate;
      existing.total = metrics.total;
      existing.memoryUsage = metrics.memoryUsage;
      existing.connectedClients = metrics.connectedClients;
      existing.opsPerSecond = metrics.opsPerSecond;
    }
  }

  getMetrics(date?: string): CacheMetrics | Map<string, CacheMetrics> {
    if (date) {
      return this.metrics.get(date) || null;
    }
    return this.metrics;
  }

  async getDetailedInfo(): Promise<any> {
    try {
      const nodes = await this.redisService.cluster.nodes();
      const nodeInfo = {};
      
      for (const node of nodes) {
        try {
          const info = await node.info();
          const nodeId = await node.cluster('MYID');
          nodeInfo[nodeId] = info;
        } catch (error) {
          console.error(`Failed to get info from node:`, error);
        }
      }
      
      return nodeInfo;
    } catch (error) {
      console.error('Failed to get detailed cluster info:', error);
      return null;
    }
  }

  async getKeyStatistics(pattern: string = '*'): Promise<any> {
    try {
      // 获取所有匹配的key
      const keys = await this.redisService.cluster.keys(pattern);
      
      const stats = {
        totalKeys: keys.length,
        keyTypes: {},
        totalSize: 0
      };
      
      for (const key of keys) {
        try {
          const type = await this.redisService.cluster.type(key);
          const memoryUsage = await this.redisService.cluster.memory('USAGE', key);
          
          // 统计key类型
          if (!stats.keyTypes[type]) {
            stats.keyTypes[type] = 0;
          }
          stats.keyTypes[type]++;
          
          // 累计内存使用
          if (memoryUsage) {
            stats.totalSize += memoryUsage as number;
          }
        } catch (error) {
          console.error(`Failed to get stats for key ${key}:`, error);
        }
      }
      
      return stats;
    } catch (error) {
      console.error('Failed to get key statistics:', error);
      return null;
    }
  }
}
```

### 2. 缓存健康检查
```typescript
// cache-health.service.ts
import { Injectable } from '@nestjs/common';
import { HealthIndicator, HealthIndicatorResult, HealthCheckError } from '@nestjs/terminus';
import { RedisClusterService } from './redis-cluster.service';

@Injectable()
export class CacheHealthIndicator extends HealthIndicator {
  constructor(private readonly redisService: RedisClusterService) {
    super();
  }

  async cacheHealth(key: string): Promise<HealthIndicatorResult> {
    try {
      // 设置测试键
      const testValue = `healthcheck_${Date.now()}`;
      await this.redisService.set(key, testValue, 60);
      
      // 读取测试键
      const value = await this.redisService.get(key);
      
      // 验证值
      const isHealthy = value === testValue;
      
      const result = this.getStatus('redis_cache', isHealthy, {
        message: isHealthy ? 'Cache is healthy' : 'Cache is not responding',
        timestamp: new Date().toISOString(),
      });
      
      if (isHealthy) {
        return result;
      }
      
      throw new HealthCheckError('Cache check failed', result);
    } catch (error) {
      const result = this.getStatus('redis_cache', false, {
        message: error.message,
        timestamp: new Date().toISOString(),
      });
      
      throw new HealthCheckError('Cache check failed', result);
    }
  }

  async clusterHealth(): Promise<HealthIndicatorResult> {
    try {
      // 检查集群状态
      const clusterInfo = await this.redisService.cluster.cluster('INFO');
      const clusterNodes = await this.redisService.cluster.cluster('NODES');
      
      // 解析集群信息
      const isHealthy = clusterInfo.includes('cluster_state:ok');
      const nodeCount = clusterNodes.split('\n').filter(node => node.trim()).length;
      
      const result = this.getStatus('redis_cluster', isHealthy, {
        message: isHealthy ? 'Cluster is healthy' : 'Cluster is not healthy',
        nodeCount,
        timestamp: new Date().toISOString(),
      });
      
      if (isHealthy) {
        return result;
      }
      
      throw new HealthCheckError('Cluster check failed', result);
    } catch (error) {
      const result = this.getStatus('redis_cluster', false, {
        message: error.message,
        timestamp: new Date().toISOString(),
      });
      
      throw new HealthCheckError('Cluster check failed', result);
    }
  }
}
```

## 缓存性能优化

### 1. 连接池优化
```typescript
// redis-pool.config.ts
import { RedisOptions } from 'ioredis';

export const redisConfig: RedisOptions = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT) || 6379,
  password: process.env.REDIS_PASSWORD,
  db: parseInt(process.env.REDIS_DB) || 0,
  
  // 连接池配置
  maxRetriesPerRequest: 3,
  retryDelayOnFailover: 100,
  retryDelayOnClusterFailover: 100,
  maxLoadingTimeout: 2000,
  
  // 超时配置
  connectTimeout: 30000,
  commandTimeout: 20000,
  lazyConnect: true,
  
  // 故障转移配置
  enableReadyCheck: true,
  enableOfflineQueue: true,
  enableAutoPipelining: true,
  
  // 性能优化
  autoResendUnfulfilledCommands: true,
  keyPrefix: 'zhi_xuan:',
  
  // SSL配置（如果需要）
  tls: process.env.REDIS_USE_TLS === 'true' ? {
    rejectUnauthorized: false,
    requestCert: true,
    agent: false,
  } : undefined,
};
```

### 2. 数据压缩策略
```typescript
// compression.service.ts
import { Injectable } from '@nestjs/common';
import * as zlib from 'zlib';
import { promisify } from 'util';

const gzip = promisify(zlib.gzip);
const gunzip = promisify(zlib.gunzip);

@Injectable()
export class CompressionService {
  async compress(data: any): Promise<Buffer> {
    const jsonString = JSON.stringify(data);
    return await gzip(jsonString, { level: 6 }); // 中等压缩级别
  }

  async decompress(buffer: Buffer): Promise<any> {
    const jsonString = await gunzip(buffer);
    return JSON.parse(jsonString.toString());
  }

  async compressIfNeeded(data: any): Promise<string | Buffer> {
    const jsonString = JSON.stringify(data);
    
    // 如果数据较大，进行压缩
    if (jsonString.length > 1024) { // 1KB以上进行压缩
      const compressed = await gzip(jsonString, { level: 6 });
      // 使用Base64编码以便存储
      return compressed.toString('base64');
    }
    
    return jsonString;
  }

  async decompressIfNeeded(data: string | Buffer): Promise<any> {
    // 检查是否是压缩数据（通过base64检测）
    if (typeof data === 'string' && data.length > 1024) {
      try {
        const buffer = Buffer.from(data, 'base64');
        const decompressed = await gunzip(buffer);
        return JSON.parse(decompressed.toString());
      } catch (error) {
        // 如果解析失败，可能是普通字符串
        return JSON.parse(data);
      }
    }
    
    if (Buffer.isBuffer(data)) {
      const decompressed = await gunzip(data);
      return JSON.parse(decompressed.toString());
    }
    
    return JSON.parse(data as string);
  }
}
```

## 缓存安全配置

### 1. Redis安全配置
```conf
# redis-security.conf
# 绑定到特定IP
bind 127.0.0.1 10.0.0.0/8

# 设置密码
requirepass your_strong_password_here

# 限制客户端数量
maxclients 10000

# 设置请求大小限制
proto-max-bulk-len 512mb

# 禁用危险命令
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command EVAL ""
rename-command EVALSHA ""

# 日志级别
loglevel notice

# 审计日志
latency-monitor-threshold 100
```

### 2. 应用层安全
```typescript
// secure-cache.service.ts
import { Injectable } from '@nestjs/common';
import * as crypto from 'crypto';
import { RedisClusterService } from './redis-cluster.service';

@Injectable()
export class SecureCacheService {
  private readonly encryptionKey: Buffer;
  private readonly algorithm = 'aes-256-gcm';

  constructor(private readonly redisService: RedisClusterService) {
    // 从环境变量获取加密密钥
    const key = process.env.CACHE_ENCRYPTION_KEY;
    if (!key || key.length < 32) {
      throw new Error('CACHE_ENCRYPTION_KEY must be at least 32 characters long');
    }
    this.encryptionKey = Buffer.from(key, 'utf8').slice(0, 32);
  }

  async setSecure(key: string, value: any, ttl?: number): Promise<void> {
    try {
      // 加密数据
      const encryptedValue = await this.encrypt(JSON.stringify(value));
      
      // 存储加密后的数据
      if (ttl) {
        await this.redisService.set(key, encryptedValue, ttl);
      } else {
        await this.redisService.set(key, encryptedValue);
      }
    } catch (error) {
      console.error('Secure cache set error:', error);
      throw error;
    }
  }

  async getSecure<T = any>(key: string): Promise<T | null> {
    try {
      const encryptedValue = await this.redisService.get(key);
      if (!encryptedValue) {
        return null;
      }

      // 解密数据
      const decryptedValue = await this.decrypt(encryptedValue);
      return JSON.parse(decryptedValue);
    } catch (error) {
      console.error('Secure cache get error:', error);
      return null;
    }
  }

  private async encrypt(text: string): Promise<string> {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipher(this.algorithm, this.encryptionKey);
    const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
    const authTag = cipher.getAuthTag();
    
    // 返回: IV + AuthTag + 加密数据
    return Buffer.concat([iv, authTag, encrypted]).toString('base64');
  }

  private async decrypt(encryptedData: string): Promise<string> {
    const buffer = Buffer.from(encryptedData, 'base64');
    
    const iv = buffer.subarray(0, 16);
    const authTag = buffer.subarray(16, 32);
    const encrypted = buffer.subarray(32);
    
    const decipher = crypto.createDecipher(this.algorithm, this.encryptionKey);
    decipher.setAuthTag(authTag);
    
    const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
    return decrypted.toString('utf8');
  }

  // 验证缓存键的安全性
  private validateKey(key: string): boolean {
    // 检查是否包含非法字符
    const invalidChars = /[\r\n\t\0\x0B]/;
    if (invalidChars.test(key)) {
      return false;
    }
    
    // 检查长度限制
    if (key.length > 1024) {
      return false;
    }
    
    return true;
  }
}
```

这个缓存架构设计包含了：

1. Redis集群架构和配置
2. 多级缓存策略
3. 缓存客户端实现
4. 缓存管理服务
5. 缓存更新策略
6. 监控和运维工具
7. 性能优化措施
8. 安全配置

架构设计确保了缓存的高可用性、高性能和安全性，满足智选电商平台的性能需求。