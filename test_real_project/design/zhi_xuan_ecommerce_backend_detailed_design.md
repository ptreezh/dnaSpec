# 智选电商平台后端微服务架构详细设计

## Node.js微服务技术栈

### 核心框架
- Express.js 4.x 或 Koa 2.x 作为Web框架
- TypeScript 提供类型安全
- NestJS 提供企业级架构支持
- PM2 进程管理
- Docker 容器化部署

### 依赖管理
```json
{
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/platform-express": "^10.0.0",
    "pg": "^8.11.0", 
    "redis": "^4.6.0",
    "amqplib": "^0.10.3",
    "joi": "^17.9.2",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.1",
    "helmet": "^7.0.0",
    "cors": "^2.8.5",
    "class-transformer": "^0.5.1",
    "class-validator": "^0.14.0"
  },
  "devDependencies": {
    "@nestjs/cli": "^10.0.0",
    "@nestjs/schematics": "^10.0.0",
    "@nestjs/testing": "^10.0.0",
    "@types/express": "^4.17.17",
    "@types/node": "^20.3.1",
    "typescript": "^5.0.0",
    "ts-node": "^10.9.1"
  }
}
```

## 微服务详细设计

### 1. 用户服务 (User Service)

#### 目录结构
```
user-service/
├── src/
│   ├── controllers/
│   │   └── user.controller.ts
│   ├── services/
│   │   └── user.service.ts
│   ├── models/
│   │   └── user.model.ts
│   ├── dtos/
│   │   ├── create-user.dto.ts
│   │   └── login.dto.ts
│   ├── middleware/
│   │   └── auth.middleware.ts
│   ├── utils/
│   │   └── password.util.ts
│   └── app.module.ts
├── docker/
│   └── Dockerfile
├── docker-compose.yml
└── package.json
```

#### 核心实现
```typescript
// user.service.ts
import { Injectable } from '@nestjs/common';
import { Pool } from 'pg';
import * as bcrypt from 'bcryptjs';
import * as jwt from 'jsonwebtoken';

@Injectable()
export class UserService {
  private readonly pool: Pool;

  constructor() {
    this.pool = new Pool({
      user: process.env.DB_USER || 'user',
      host: process.env.DB_HOST || 'localhost',
      database: process.env.DB_NAME || 'zhi_xuan_user',
      password: process.env.DB_PASSWORD || 'password',
      port: parseInt(process.env.DB_PORT) || 5432,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }

  async createUser(userData: CreateUserDto) {
    const hashedPassword = await bcrypt.hash(userData.password, 10);
    
    const query = `
      INSERT INTO users (username, email, password_hash, created_at, updated_at)
      VALUES ($1, $2, $3, NOW(), NOW())
      RETURNING user_id, username, email
    `;
    
    const result = await this.pool.query(query, [
      userData.username,
      userData.email,
      hashedPassword
    ]);
    
    return result.rows[0];
  }

  async findUserByEmail(email: string) {
    const query = 'SELECT * FROM users WHERE email = $1';
    const result = await this.pool.query(query, [email]);
    return result.rows[0];
  }

  async generateToken(user: any) {
    const payload = {
      userId: user.userId,
      email: user.email,
    };
    
    return jwt.sign(payload, process.env.JWT_SECRET || 'default_secret', {
      expiresIn: process.env.JWT_EXPIRES_IN || '24h',
    });
  }

  async validateUser(email: string, password: string) {
    const user = await this.findUserByEmail(email);
    if (!user) return null;
    
    const isValid = await bcrypt.compare(password, user.password_hash);
    if (!isValid) return null;
    
    // 移除密码字段
    const { password_hash, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }
}
```

#### API接口设计
```typescript
// user.controller.ts
import { Controller, Post, Get, Put, Delete, Body, Param, Query, UseGuards } from '@nestjs/common';
import { UserService } from './user.service';
import { CreateUserDto } from '../dtos/create-user.dto';
import { LoginDto } from '../dtos/login.dto';
import { AuthGuard } from '../middleware/auth.middleware';

@Controller('api/v1/users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('register')
  async register(@Body() createUserDto: CreateUserDto) {
    return await this.userService.createUser(createUserDto);
  }

  @Post('login')
  async login(@Body() loginDto: LoginDto) {
    const user = await this.userService.validateUser(
      loginDto.email, 
      loginDto.password
    );
    
    if (!user) {
      throw new Error('Invalid credentials');
    }
    
    const token = await this.userService.generateToken(user);
    return { user, token };
  }

  @UseGuards(AuthGuard)
  @Get(':id')
  async getUser(@Param('id') id: string) {
    // 实现获取用户信息逻辑
  }

  @UseGuards(AuthGuard)
  @Put(':id')
  async updateUser(@Param('id') id: string, @Body() userData: any) {
    // 实现更新用户信息逻辑
  }
}
```

### 2. 商品服务 (Product Service)

#### 核心实现
```typescript
// product.service.ts
import { Injectable } from '@nestjs/common';
import { Pool } from 'pg';

@Injectable()
export class ProductService {
  private readonly pool: Pool;

  constructor() {
    this.pool = new Pool({
      user: process.env.DB_USER || 'user',
      host: process.env.DB_HOST || 'localhost',
      database: process.env.DB_NAME || 'zhi_xuan_product',
      password: process.env.DB_PASSWORD || 'password',
      port: parseInt(process.env.DB_PORT) || 5432,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }

  async getProducts(page: number = 1, limit: number = 20, filters: any = {}) {
    // 构建查询条件
    let query = 'SELECT * FROM products WHERE 1=1';
    const params: any[] = [];
    
    if (filters.category) {
      params.push(filters.category);
      query += ` AND category_id = $${params.length}`;
    }
    
    if (filters.minPrice) {
      params.push(filters.minPrice);
      query += ` AND price >= $${params.length}`;
    }
    
    if (filters.maxPrice) {
      params.push(filters.maxPrice);
      query += ` AND price <= $${params.length}`;
    }
    
    if (filters.search) {
      params.push(`%${filters.search}%`);
      query += ` AND (name ILIKE $${params.length} OR description ILIKE $${params.length})`;
    }
    
    // 分页
    const offset = (page - 1) * limit;
    params.push(limit, offset);
    query += ` ORDER BY created_at DESC LIMIT $${params.length - 1} OFFSET $${params.length}`;
    
    const result = await this.pool.query(query, params);
    return result.rows;
  }

  async getProductById(id: string) {
    const query = 'SELECT * FROM products WHERE product_id = $1';
    const result = await this.pool.query(query, [id]);
    return result.rows[0];
  }

  async createProduct(productData: any) {
    const query = `
      INSERT INTO products (name, description, price, stock, category_id, images, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
      RETURNING *
    `;
    
    const result = await this.pool.query(query, [
      productData.name,
      productData.description,
      productData.price,
      productData.stock,
      productData.categoryId,
      productData.images
    ]);
    
    return result.rows[0];
  }
}
```

### 3. 订单服务 (Order Service)

#### 订单状态管理
```typescript
// order.service.ts
import { Injectable } from '@nestjs/common';
import { Pool } from 'pg';
import * as amqp from 'amqplib';

export enum OrderStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  PAID = 'paid',
  SHIPPED = 'shipped',
  DELIVERED = 'delivered',
  CANCELLED = 'cancelled',
  REFUNDED = 'refunded'
}

@Injectable()
export class OrderService {
  private readonly pool: Pool;
  private readonly rabbitmqConnection: amqp.Connection;

  constructor() {
    this.pool = new Pool({
      user: process.env.DB_USER || 'user',
      host: process.env.DB_HOST || 'localhost',
      database: process.env.DB_NAME || 'zhi_xuan_order',
      password: process.env.DB_PASSWORD || 'password',
      port: parseInt(process.env.DB_PORT) || 5432,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }

  async createOrder(orderData: any) {
    // 开始数据库事务
    const client = await this.pool.connect();
    
    try {
      await client.query('BEGIN');
      
      // 1. 创建订单
      const orderQuery = `
        INSERT INTO orders (user_id, total_amount, status, created_at, updated_at)
        VALUES ($1, $2, $3, NOW(), NOW())
        RETURNING order_id
      `;
      const orderResult = await client.query(orderQuery, [
        orderData.userId, 
        orderData.totalAmount, 
        OrderStatus.PENDING
      ]);
      
      const orderId = orderResult.rows[0].order_id;
      
      // 2. 创建订单项
      for (const item of orderData.items) {
        const orderItemQuery = `
          INSERT INTO order_items (order_id, product_id, quantity, price)
          VALUES ($1, $2, $3, $4)
        `;
        await client.query(orderItemQuery, [
          orderId,
          item.productId,
          item.quantity,
          item.price
        ]);
      }
      
      // 3. 扣减库存（通过消息队列异步处理）
      await this.publishToQueue('inventory.decrease', {
        orderId,
        items: orderData.items
      });
      
      await client.query('COMMIT');
      
      // 发布订单创建事件
      await this.publishToQueue('order.created', { orderId, ...orderData });
      
      return { orderId };
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  private async publishToQueue(queue: string, message: any) {
    // 实现消息队列发布逻辑
    console.log(`Publishing to queue ${queue}:`, message);
  }
}
```

## 服务间通信设计

### 1. REST API通信
```typescript
// http-client.service.ts
import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class HttpService {
  private readonly USER_SERVICE_URL = process.env.USER_SERVICE_URL || 'http://user-service:3000';
  private readonly PRODUCT_SERVICE_URL = process.env.PRODUCT_SERVICE_URL || 'http://product-service:3000';
  private readonly INVENTORY_SERVICE_URL = process.env.INVENTORY_SERVICE_URL || 'http://inventory-service:3000';

  async validateUserToken(token: string) {
    try {
      const response = await axios.get(`${this.USER_SERVICE_URL}/api/v1/users/validate`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      throw new Error('Token validation failed');
    }
  }

  async checkProductStock(productId: string, quantity: number) {
    try {
      const response = await axios.get(`${this.INVENTORY_SERVICE_URL}/api/v1/stock/${productId}`, {
        params: { quantity }
      });
      return response.data;
    } catch (error) {
      throw new Error('Stock check failed');
    }
  }
}
```

### 2. 消息队列通信 (RabbitMQ)
```typescript
// rabbitmq.service.ts
import { Injectable, OnModuleInit } from '@nestjs/common';
import * as amqp from 'amqplib';

@Injectable()
export class RabbitMQService implements OnModuleInit {
  private connection: amqp.Connection;
  private channel: amqp.Channel;

  async onModuleInit() {
    this.connection = await amqp.connect(process.env.RABBITMQ_URL || 'amqp://localhost:5672');
    this.channel = await this.connection.createChannel();
    
    // 确保交换机存在
    await this.channel.assertExchange('zhi_xuan_exchange', 'topic', { durable: true });
  }

  async publish(routingKey: string, message: any) {
    const buffer = Buffer.from(JSON.stringify(message));
    this.channel.publish('zhi_xuan_exchange', routingKey, buffer, { persistent: true });
  }

  async subscribe(routingKey: string, handler: (msg: amqp.ConsumeMessage) => void) {
    const queue = await this.channel.assertQueue('', { exclusive: true });
    await this.channel.bindQueue(queue.queue, 'zhi_xuan_exchange', routingKey);
    this.channel.consume(queue.queue, handler);
  }
}
```

## 性能优化实现

### 1. 连接池优化
```typescript
// config/database.config.ts
import { Pool } from 'pg';

export const createConnectionPool = (config: {
  host: string,
  port: number,
  database: string,
  user: string,
  password: string,
  max?: number,
  idleTimeoutMillis?: number,
  connectionTimeoutMillis?: number
}) => {
  return new Pool({
    host: config.host,
    port: config.port,
    database: config.database,
    user: config.user,
    password: config.password,
    max: config.max || 20,
    idleTimeoutMillis: config.idleTimeoutMillis || 30000,
    connectionTimeoutMillis: config.connectionTimeoutMillis || 2000,
    // 连接池健康检查
    verify: async (client) => {
      try {
        await client.query('SELECT 1');
      } catch (err) {
        throw new Error('Connection verification failed');
      }
    }
  });
};
```

### 2. 缓存中间件
```typescript
// middleware/cache.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import * as Redis from 'redis';

@Injectable()
export class CacheMiddleware implements NestMiddleware {
  private readonly redisClient = Redis.createClient({
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT) || 6379,
    retry_strategy: (options) => {
      if (options.error && options.error.code === 'ECONNREFUSED') {
        return new Error('Redis服务器拒绝连接');
      }
      if (options.total_retry_time > 1000 * 60 * 60) {
        return new Error('重试时间已用完');
      }
      if (options.attempt > 10) {
        return undefined;
      }
      return Math.min(options.attempt * 100, 3000);
    }
  });

  async use(req: Request, res: Response, next: NextFunction) {
    // 生成缓存键
    const cacheKey = `cache:${req.method}:${req.path}:${JSON.stringify(req.query)}`;
    
    try {
      // 尝试从缓存获取数据
      const cachedData = await this.redisClient.get(cacheKey);
      if (cachedData) {
        res.set('X-Cache', 'HIT');
        return res.json(JSON.parse(cachedData));
      }
    } catch (error) {
      console.error('Cache error:', error);
    }
    
    // 如果缓存未命中，继续执行后续中间件
    res.originalJson = res.json;
    res.json = (data) => {
      // 设置缓存
      this.redisClient.setex(cacheKey, 600, JSON.stringify(data)); // 缓存10分钟
      res.originalJson(data);
    };
    
    next();
  }
}
```

## Docker部署配置

### Dockerfile
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine

WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

EXPOSE 3000
CMD ["npm", "run", "start"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  user-service:
    build: ./user-service
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=user-db
      - DB_NAME=zhi_xuan_user
      - DB_USER=user
      - DB_PASSWORD=password
      - JWT_SECRET=your-jwt-secret
    depends_on:
      - user-db
      - redis-cluster
    restart: always
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  product-service:
    build: ./product-service
    ports:
      - "3002:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=product-db
      - DB_NAME=zhi_xuan_product
      - DB_USER=user
      - DB_PASSWORD=password
    depends_on:
      - product-db
      - redis-cluster
    restart: always

  order-service:
    build: ./order-service
    ports:
      - "3003:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=order-db
      - DB_NAME=zhi_xuan_order
      - DB_USER=user
      - DB_PASSWORD=password
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - order-db
      - rabbitmq
      - redis-cluster
    restart: always

  api-gateway:
    image: kong:latest
    ports:
      - "8000:8000"
      - "8443:8443"
      - "8001:8001"
      - "8444:8444"
    environment:
      - KONG_DATABASE=off
      - KONG_DECLARATIVE_CONFIG=/kong/declarative/kong.yml
    volumes:
      - ./kong:/kong/declarative
    depends_on:
      - user-service
      - product-service
      - order-service

  user-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=zhi_xuan_user
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - user-db-data:/var/lib/postgresql/data
      - ./init/user.sql:/docker-entrypoint-initdb.d/init.sql
    restart: always

  product-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=zhi_xuan_product
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - product-db-data:/var/lib/postgresql/data
      - ./init/product.sql:/docker-entrypoint-initdb.d/init.sql
    restart: always

  order-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=zhi_xuan_order
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - order-db-data:/var/lib/postgresql/data
      - ./init/order.sql:/docker-entrypoint-initdb.d/init.sql
    restart: always

  redis-cluster:
    image: redis:7-alpine
    command: redis-server --appendonly yes --cluster-enabled yes --cluster-config-file nodes.conf --port 6379
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: always

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=password
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    restart: always

volumes:
  user-db-data:
  product-db-data:
  order-db-data:
  redis-data:
  rabbitmq-data:
```

## API网关配置 (Kong)

```yaml
# kong.yml
_format_version: "2.1"

services:
  - name: user-service
    url: http://user-service:3000
    routes:
      - name: user-route
        paths:
          - /api/v1/users
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: redis
          redis_host: redis-cluster
          redis_port: 6379
      - name: jwt

  - name: product-service
    url: http://product-service:3000
    routes:
      - name: product-route
        paths:
          - /api/v1/products
    plugins:
      - name: rate-limiting
        config:
          minute: 1000
          policy: redis
          redis_host: redis-cluster
          redis_port: 6379

  - name: order-service
    url: http://order-service:3000
    routes:
      - name: order-route
        paths:
          - /api/v1/orders
    plugins:
      - name: rate-limiting
        config:
          minute: 500
          policy: redis
          redis_host: redis-cluster
          redis_port: 6379
      - name: jwt
```

## 健康检查和监控

### 健康检查端点
```typescript
// health.controller.ts
import { Controller, Get } from '@nestjs/common';
import { HealthCheck, HealthCheckService, TypeOrmHealthIndicator } from '@nestjs/terminus';

@Controller('health')
export class HealthController {
  constructor(
    private health: HealthCheckService,
    private db: TypeOrmHealthIndicator,
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      async () => this.db.pingCheck('database', { timeout: 300 }),
    ]);
  }
}
```

这个详细的后端微服务架构设计涵盖了：
1. Node.js微服务的技术栈选择
2. 各个核心服务的实现细节
3. 服务间通信机制
4. 性能优化策略
5. Docker部署配置
6. API网关配置
7. 健康检查和监控

架构设计确保了高可用性、高性能和可扩展性，满足智选电商平台的需求。