# 智选电商平台微服务架构设计方案

## 项目概述

智选电商平台是一个面向百万级用户的高并发电商平台，需要支持10万日活用户，双11大促期间支持10万并发请求，API请求95%需在200ms内完成，整体可用性达99.99%。

## 需求分析

### 性能需求
- 支持百万级用户规模
- 支持10万日活用户
- 双11大促期间支持10万QPS并发
- 99.99%系统可用性
- 95%的API响应时间在200ms内

### 功能需求
- 用户管理（注册、登录、个人中心）
- 商品管理（商品展示、搜索、分类）
- 订单管理（下单、支付、物流跟踪）
- 购物车功能
- 库存管理
- 营销活动
- 数据分析

## 总体架构设计

### 微服务划分

```
┌─────────────────────────────────────────────────────────────┐
│                    客户端层 (Client Layer)                    │
├─────────────────────────────────────────────────────────────┤
│  Web前端(React)  │  移动端App  │  小程序  │  管理后台        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    API网关层 (API Gateway)                   │
├─────────────────────────────────────────────────────────────┤
│                Nginx + Kong + 限流熔断                        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    服务发现层 (Service Discovery)            │
├─────────────────────────────────────────────────────────────┤
│                    Consul + 负载均衡                          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    微服务层 (Microservices)                 │
├─────────────────────────────────────────────────────────────┤
│ 用户服务 │ 商品服务 │ 订单服务 │ 支付服务 │ 库存服务 │ 营销服务 │
│ 通知服务 │ 搜索服务 │ 文件服务 │ 日志服务 │ 配置服务 │          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    数据存储层 (Data Storage)                │
├─────────────────────────────────────────────────────────────┤
│ PostgreSQL主从复制集群 │ Redis集群 │ Elasticsearch │         │
│        │         │      MongoDB      │         │           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    监控治理层 (Monitoring & Governance)     │
├─────────────────────────────────────────────────────────────┤
│  Prometheus + Grafana  │  Jaeger  │  ELK  │  Consul  │      │
└─────────────────────────────────────────────────────────────┘
```

## 前端架构设计 (React)

### 技术选型
- React 18+ (函数组件 + Hooks)
- TypeScript
- Redux Toolkit (状态管理)
- React Router 6 (路由管理)
- Ant Design / Material UI (UI组件库)
- Webpack 5 / Vite (构建工具)
- Axios (HTTP客户端)
- React Query (数据获取与缓存)

### 组件架构
```
src/
├── components/          # 通用组件
├── pages/              # 页面组件
├── hooks/              # 自定义Hooks
├── services/           # API服务
├── store/              # Redux状态管理
├── utils/              # 工具函数
├── types/              # TypeScript类型定义
└── assets/             # 静态资源
```

### 性能优化
- 代码分割 (Code Splitting)
- 组件懒加载 (Lazy Loading)
- 图片优化 (WebP格式、懒加载)
- HTTP缓存策略
- CDN加速静态资源

## 后端微服务架构 (Node.js)

### 服务划分

#### 1. 用户服务 (User Service)
- 负责用户注册、登录、个人信息管理
- 用户权限和角色管理
- JWT Token认证
- 技术栈：Node.js + Express/Koa + TypeScript

#### 2. 商品服务 (Product Service)
- 商品信息管理（CRUD）
- 商品分类管理
- 商品搜索和筛选
- 商品库存查询

#### 3. 订单服务 (Order Service)
- 订单创建、查询、修改
- 订单状态管理
- 订单支付流程
- 订单取消和退款

#### 4. 支付服务 (Payment Service)
- 支付网关集成
- 支付状态管理
- 退款处理
- 支付回调处理

#### 5. 库存服务 (Inventory Service)
- 库存管理
- 库存扣减和回滚
- 库存预警和补货

#### 6. 营销服务 (Marketing Service)
- 优惠券管理
- 活动管理
- 积分系统
- 会员等级

#### 7. 搜索服务 (Search Service)
- 商品全文搜索
- 搜索建议
- 搜索历史
- 搜索分析

#### 8. 通知服务 (Notification Service)
- 短信通知
- 邮件通知
- 站内信
- 推送通知

### 服务间通信
- REST API (同步通信)
- 消息队列 (异步通信，使用RabbitMQ/Kafka)
- gRPC (高性能服务间通信)

### Node.js微服务模板
```javascript
// 示例：用户服务结构
const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');

// 服务实例
const app = express();

// 数据库连接
const dbPool = new Pool({
  user: 'user',
  host: 'pg-cluster-primary',
  database: 'zhi_xuan_user',
  password: 'password',
  port: 5432,
  max: 20, // 连接池最大连接数
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Redis连接
const redisClient = redis.createClient({
  host: 'redis-cluster',
  port: 6379,
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

// 路由定义
app.use('/api/v1/users', require('./routes/users'));

// 启动服务
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`用户服务运行在端口 ${PORT}`);
});
```

## 数据库架构 (PostgreSQL主从复制)

### 数据库分片策略
- 按业务垂直分库
- 按用户ID水平分表

### 主从复制架构
```
                    Master (写入)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    Slave-1 (读)     Slave-2 (读)     Slave-3 (读)
     (北京)           (上海)           (深圳)
```

### 数据库配置
- 主库：高配置服务器，负责写入操作
- 从库：多个从库分担读取压力
- 读写分离：写操作到主库，读操作到从库
- 数据同步：异步复制，延迟<100ms

### 数据库设计原则
- 连接池管理 (pg-pool)
- 查询优化 (索引、分区表)
- 事务管理 (分布式事务处理)
- 备份策略 (每日全备+实时binlog)

## 缓存架构 (Redis集群)

### Redis集群架构
```
                    Redis Cluster (16384个哈希槽)
                    ├── Master-1 ── Slave-1
                    ├── Master-2 ── Slave-2
                    ├── Master-3 ── Slave-3
                    └── Master-4 ── Slave-4
```

### 缓存策略
1. **本地缓存 (L1)**
   - Node.js内存缓存
   - 存储热点数据
   - 缓存时间：5-10分钟

2. **分布式缓存 (L2)**
   - Redis集群
   - 存储用户会话、商品信息等
   - 缓存时间：30分钟-24小时

### 缓存数据结构设计
```javascript
// 用户会话
SET session:{sessionId} {userInfo} EX 1800

// 商品信息
HMSET product:{productId} name {name} price {price} stock {stock}

// 购物车
SADD cart:{userId} {productId}:{quantity}

// 热门商品
ZADD hot_products {score} {productId}
```

### 缓存更新策略
- Cache-Aside模式
- 写操作：先更新数据库，再删除缓存
- 读操作：先读缓存，缓存未命中则读数据库并写入缓存

## 服务治理和监控

### API网关 (Kong)
- 请求路由和负载均衡
- 身份认证和权限控制
- 限流和熔断
- 日志记录和监控

### 服务发现 (Consul)
- 服务注册与发现
- 健康检查
- 配置管理
- KV存储

### 监控系统
1. **应用性能监控 (APM)**
   - Prometheus + Grafana
   - 自定义指标收集
   - 性能告警

2. **分布式链路追踪**
   - Jaeger
   - 请求链路追踪
   - 性能瓶颈分析

3. **日志系统**
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - 结构化日志
   - 实时日志分析

### 容错与熔断
```javascript
// 熔断器示例
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failureCount = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}
```

## 高可用性保障措施

### 1. 多区域部署
- 北京、上海、深圳三个数据中心
- 数据同步和故障切换

### 2. 服务冗余
- 每个微服务至少部署2个实例
- 负载均衡和故障转移

### 3. 数据备份
- 数据库主从复制
- 每日全量备份 + 实时增量备份
- 跨区域备份

### 4. 容灾方案
- 故障自动检测和恢复
- 服务降级策略
- 灰度发布和回滚机制

### 5. SLA保障
- 99.99%可用性目标
- 服务级别协议监控
- 故障响应时间承诺

## 性能优化策略

### 1. 前端性能优化
- 资源压缩和合并
- 图片懒加载
- CDN加速
- 浏览器缓存策略

### 2. 后端性能优化
- 数据库查询优化
- Redis缓存策略
- 消息队列异步处理
- 连接池优化

### 3. 网络优化
- HTTP/2协议
- Gzip压缩
- 静态资源CDN分发

### 4. 数据库优化
- 索引优化
- 查询优化
- 分库分表
- 读写分离

## 部署架构

### 容器化部署
- Docker容器化微服务
- Kubernetes集群管理
- 服务编排和调度

### CI/CD流水线
- GitLab/GitHub Actions
- 自动化测试
- 蓝绿部署/滚动更新
- 回滚机制

### 监控告警
- Prometheus监控
- Grafana可视化
- 告警通知 (邮件、短信、钉钉)
- 自动恢复机制

## 安全设计

### 认证授权
- JWT Token认证
- OAuth2.0授权
- RBAC权限控制

### 数据安全
- 敏感数据加密
- 传输加密 (HTTPS)
- 数据脱敏

### 网络安全
- WAF防护
- DDoS防护
- 访问控制

## 总结

本架构方案通过微服务拆分、高可用设计、性能优化等手段，能够满足智选电商平台的高性能、高可用需求。通过合理的技术选型和架构设计，系统能够支持百万级用户、10万并发请求，并保证99.99%的可用性和200ms内的响应时间。