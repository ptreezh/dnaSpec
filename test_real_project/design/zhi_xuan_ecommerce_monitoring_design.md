# 智选电商平台服务治理和监控组件设计

## 服务治理与监控架构概述

智选电商平台采用完整的微服务治理和监控体系，包括API网关、服务发现、配置中心、分布式追踪、性能监控、日志聚合等组件，确保系统高可用性、可观测性和可维护性。

## 服务治理架构

### 1. 服务注册与发现 (Consul)

#### 架构设计
```
                    Consul Cluster (3节点)
                    ├── Node-1 (Leader) - 北京
                    ├── Node-2 (Follower) - 上海
                    └── Node-3 (Follower) - 深圳
                              │
                    微服务节点 (自动注册/发现)
                    ├── 用户服务 (多实例)
                    ├── 商品服务 (多实例)
                    ├── 订单服务 (多实例)
                    └── 网关服务 (多实例)
```

#### Consul配置
```hcl
# consul-config.hcl
datacenter = "beijing"
data_dir = "/opt/consul/data"
log_level = "INFO"
node_name = "consul-server-01"
bind_addr = "0.0.0.0"
client_addr = "0.0.0.0"
ports {
  http = 8500
  grpc = 8502
  serf_lan = 8301
  server = 8300
}
retry_join = ["consul-server-02", "consul-server-03"]
server = true
bootstrap_expect = 3
ui = true
raft_protocol = 3
performance {
  raft_multiplier = 1
}
connect {
  enabled = true
}
```

#### 服务定义文件 (user-service.json)
```json
{
  "service": {
    "name": "user-service",
    "tags": ["api", "user", "v1"],
    "port": 3001,
    "checks": [
      {
        "id": "user-service-api-check",
        "name": "User Service API Health Check",
        "http": "http://localhost:3001/health",
        "method": "GET",
        "interval": "10s",
        "timeout": "1s",
        "deregister_critical_service_after": "30m"
      },
      {
        "id": "user-service-memory-check",
        "name": "User Service Memory Check",
        "script": "/bin/check-memory.sh",
        "interval": "30s",
        "timeout": "5s"
      }
    ],
    "meta": {
      "version": "1.0.0",
      "team": "user-service-team",
      "owner": "zhi_xuan_user_service"
    }
  }
}
```

#### Node.js服务注册实现
```typescript
// service-registration.service.ts
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import * as Consul from 'consul';

@Injectable()
export class ServiceRegistrationService implements OnModuleInit, OnModuleDestroy {
  private consul: Consul;
  private serviceId: string;

  constructor() {
    this.consul = new Consul({
      host: process.env.CONSUL_HOST || 'localhost',
      port: parseInt(process.env.CONSUL_PORT) || 8500,
      promisify: true,
    });
    
    this.serviceId = `${process.env.SERVICE_NAME}-${process.env.HOSTNAME || 'localhost'}-${Date.now()}`;
  }

  async onModuleInit() {
    await this.registerService();
    this.startHealthCheck();
  }

  async onModuleDestroy() {
    await this.deregisterService();
  }

  private async registerService() {
    try {
      const registration = {
        id: this.serviceId,
        name: process.env.SERVICE_NAME || 'unknown-service',
        address: process.env.SERVICE_HOST || 'localhost',
        port: parseInt(process.env.SERVICE_PORT) || 3000,
        tags: [process.env.SERVICE_ENV || 'development'],
        meta: {
          version: process.env.SERVICE_VERSION || '1.0.0',
          node_version: process.version,
          platform: process.platform,
        },
        check: {
          http: `http://${process.env.SERVICE_HOST || 'localhost'}:${process.env.SERVICE_PORT || 3000}/health`,
          interval: '10s',
          timeout: '5s',
          deregistercriticalserviceafter: '30m',
        },
      };

      await this.consul.agent.service.register(registration);
      console.log(`Service ${this.serviceId} registered successfully`);
    } catch (error) {
      console.error('Service registration failed:', error);
      throw error;
    }
  }

  private async deregisterService() {
    try {
      await this.consul.agent.service.deregister(this.serviceId);
      console.log(`Service ${this.serviceId} deregistered successfully`);
    } catch (error) {
      console.error('Service deregistration failed:', error);
    }
  }

  private startHealthCheck() {
    // 定期检查服务健康状态
    setInterval(async () => {
      try {
        await this.consul.agent.checks();
        console.log('Health check passed');
      } catch (error) {
        console.error('Health check failed:', error);
      }
    }, 30000); // 每30秒检查一次
  }

  async discoverService(serviceName: string): Promise<Consul.Agent.Service[]> {
    try {
      const services = await this.consul.catalog.service.nodes(serviceName);
      return services.filter(service => service.Checks?.every(check => check.Status === 'passing'));
    } catch (error) {
      console.error(`Service discovery failed for ${serviceName}:`, error);
      return [];
    }
  }

  async getKeyValue(key: string): Promise<string | null> {
    try {
      const result = await this.consul.kv.get(key);
      return result ? result.Value : null;
    } catch (error) {
      console.error(`KV get failed for ${key}:`, error);
      return null;
    }
  }

  async putKeyValue(key: string, value: string): Promise<boolean> {
    try {
      await this.consul.kv.set(key, value);
      return true;
    } catch (error) {
      console.error(`KV put failed for ${key}:`, error);
      return false;
    }
  }
}
```

### 2. API网关 (Kong)

#### Kong配置
```yaml
# kong.yml - 声明式配置
_format_version: "2.1"

# 服务定义
services:
  - name: user-service
    url: http://user-service:3000
    routes:
      - name: user-route
        paths:
          - /api/v1/users
        methods:
          - GET
          - POST
          - PUT
          - DELETE
        strip_path: true
        preserve_host: false
    plugins:
      - name: rate-limiting
        config:
          minute: 1000
          hour: 5000
          policy: redis
          redis_host: redis-cluster
          redis_port: 6379
          redis_password: your_redis_password
      - name: jwt
      - name: cors
        config:
          origins:
            - "https://zhixuan.com"
            - "https://www.zhixuan.com"
          methods:
            - GET
            - POST
            - PUT
            - DELETE
            - OPTIONS
          headers:
            - Accept
            - Content-Type
            - Authorization
          credentials: true

  - name: product-service
    url: http://product-service:3000
    routes:
      - name: product-route
        paths:
          - /api/v1/products
        strip_path: true
      - name: product-search-route
        paths:
          - /api/v1/search
        strip_path: true
    plugins:
      - name: rate-limiting
        config:
          minute: 5000
          hour: 30000
          policy: redis
          redis_host: redis-cluster
          redis_port: 6379
      - name: jwt
      - name: response-ratelimiting
        config:
          limits:
            global_minute:
              minute: 10000
            global_hour:
              hour: 50000

  - name: order-service
    url: http://order-service:3000
    routes:
      - name: order-route
        paths:
          - /api/v1/orders
        strip_path: true
    plugins:
      - name: rate-limiting
        config:
          minute: 2000
          hour: 10000
          policy: redis
          redis_host: redis-cluster
          redis_port: 6379
      - name: jwt
      - name: request-transformer
        config:
          add:
            headers:
              - "X-Authenticated-UserId:"

# 上游定义
upstreams:
  - name: user-service
    algorithm: round-robin
    healthchecks:
      active:
        type: http
        timeout: 1
        concurrency: 10
        http_path: /health
        healthy:
          http_statuses:
            - 200
            - 302
          interval: 10
          successes: 3
        unhealthy:
          http_statuses:
            - 429
            - 404
            - 500
            - 501
            - 502
            - 503
            - 504
          interval: 10
          tcp_failures: 3
          timeouts: 3
      passive:
        type: http
        healthy:
          http_statuses:
            - 200
            - 201
            - 202
            - 203
            - 204
            - 205
            - 206
            - 207
            - 208
            - 226
            - 300
            - 301
            - 302
            - 303
            - 304
            - 305
            - 306
            - 307
            - 308
          successes: 3
        unhealthy:
          http_statuses:
            - 429
            - 500
            - 503
            - 504
          tcp_failures: 3
          timeouts: 3
          http_failures: 3

# 插件定义
plugins:
  - name: prometheus
    config: {}
```

#### Kong Docker Compose
```yaml
# docker-compose.kong.yml
version: '3.8'

services:
  kong-database:
    image: postgres:15
    environment:
      POSTGRES_DB: kong
      POSTGRES_USER: kong
      POSTGRES_PASSWORD: kong
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "kong"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - kong-database-data:/var/lib/postgresql/data

  kong-migrate:
    image: kong:latest
    command: kong migrations bootstrap
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kong
    depends_on:
      kong-database:
        condition: service_healthy

  kong:
    image: kong:latest
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kong
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001, 0.0.0.0:8444 ssl
    ports:
      - "8000:8000"
      - "8443:8443"
      - "8001:8001"
      - "8444:8444"
    depends_on:
      kong-database:
        condition: service_healthy
      kong-migrate:
        condition: service_completed_successfully
    healthcheck:
      test: ["CMD", "curl", "-f", "http://kong:8001"]
      interval: 30s
      timeout: 10s
      retries: 3

  konga:
    image: pantsel/konga:latest
    environment:
      DB_ADAPTER: postgres
      DB_HOST: kong-database
      DB_PORT: 5432
      DB_USER: kong
      DB_PASSWORD: kong
      DB_DATABASE: konga
      NODE_ENV: production
    ports:
      - "1337:1337"
    depends_on:
      kong-database:
        condition: service_healthy

volumes:
  kong-database-data:
```

### 3. 配置中心 (Spring Cloud Config / Consul KV)

#### 配置管理实现
```typescript
// config.service.ts
import { Injectable, OnModuleInit } from '@nestjs/common';
import * as Consul from 'consul';
import * as fs from 'fs';
import * as yaml from 'js-yaml';

@Injectable()
export class ConfigService implements OnModuleInit {
  private consul: Consul;
  private configCache: Map<string, any> = new Map();

  constructor() {
    this.consul = new Consul({
      host: process.env.CONSUL_HOST || 'localhost',
      port: parseInt(process.env.CONSUL_PORT) || 8500,
      promisify: true,
    });
  }

  async onModuleInit() {
    await this.loadConfigurations();
    this.startConfigWatcher();
  }

  private async loadConfigurations() {
    try {
      // 从Consul KV获取配置
      const serviceConfig = await this.getConfig(`config/${process.env.SERVICE_NAME || 'default'}`);
      if (serviceConfig) {
        this.configCache.set('service', serviceConfig);
      }

      // 从本地文件获取默认配置
      const defaultConfigPath = process.env.DEFAULT_CONFIG_PATH || './config/default.yaml';
      if (fs.existsSync(defaultConfigPath)) {
        const defaultConfig = yaml.load(fs.readFileSync(defaultConfigPath, 'utf8'));
        this.configCache.set('default', defaultConfig);
      }
    } catch (error) {
      console.error('Failed to load configurations:', error);
    }
  }

  private startConfigWatcher() {
    // 监听配置变更
    setInterval(async () => {
      try {
        const currentConfig = await this.getConfig(`config/${process.env.SERVICE_NAME || 'default'}`);
        const cachedConfig = this.configCache.get('service');
        
        if (JSON.stringify(currentConfig) !== JSON.stringify(cachedConfig)) {
          console.log('Configuration changed, updating...');
          this.configCache.set('service', currentConfig);
          
          // 触发配置变更事件
          this.onConfigChange(currentConfig);
        }
      } catch (error) {
        console.error('Config watcher error:', error);
      }
    }, 30000); // 每30秒检查一次
  }

  private async getConfig(key: string): Promise<any> {
    try {
      const result = await this.consul.kv.get(key);
      if (result && result.Value) {
        try {
          return JSON.parse(result.Value);
        } catch {
          return result.Value;
        }
      }
      return null;
    } catch (error) {
      console.error(`Failed to get config for key ${key}:`, error);
      return null;
    }
  }

  private onConfigChange(newConfig: any) {
    // 配置变更处理逻辑
    console.log('Configuration updated:', newConfig);
    
    // 这里可以触发其他服务的配置更新
    // 比如更新数据库连接池配置、缓存策略等
  }

  get<T = any>(key: string, defaultValue?: T): T {
    // 优先从配置缓存获取
    const cached = this.configCache.get(key);
    if (cached !== undefined) {
      return cached;
    }

    // 从环境变量获取
    const envValue = process.env[key.toUpperCase().replace(/[^A-Z0-9_]/g, '_')];
    if (envValue !== undefined) {
      try {
        return JSON.parse(envValue);
      } catch {
        return envValue as any;
      }
    }

    // 返回默认值
    return defaultValue;
  }

  async updateConfig(key: string, value: any): Promise<boolean> {
    try {
      const serializedValue = typeof value === 'string' ? value : JSON.stringify(value);
      await this.consul.kv.set(key, serializedValue);
      
      // 更新本地缓存
      this.configCache.set(key, value);
      
      return true;
    } catch (error) {
      console.error(`Failed to update config for key ${key}:`, error);
      return false;
    }
  }
}
```

## 分布式追踪 (Jaeger)

### Jaeger架构
```yaml
# jaeger-docker-compose.yml
version: '3.8'

services:
  jaeger-collector:
    image: jaegertracing/jaeger-collector:latest
    command: ["--config-file=/etc/jaeger/config/config.yaml"]
    environment:
      - SPAN_STORAGE_TYPE=elasticsearch
      - ES_SERVER_URLS=http://elasticsearch:9200
      - ES_USERNAME=elastic
      - ES_PASSWORD=elastic
    ports:
      - "14268:14268"
      - "14269:14269"
      - "14250:14250"
    volumes:
      - ./jaeger-config.yaml:/etc/jaeger/config/config.yaml
    depends_on:
      - elasticsearch

  jaeger-query:
    image: jaegertracing/jaeger-query:latest
    environment:
      - SPAN_STORAGE_TYPE=elasticsearch
      - ES_SERVER_URLS=http://elasticsearch:9200
      - ES_USERNAME=elastic
      - ES_PASSWORD=elastic
    ports:
      - "16686:16686"
      - "16687:16687"
    depends_on:
      - elasticsearch

  jaeger-agent:
    image: jaegertracing/jaeger-agent:latest
    command: ["--reporter.grpc.host-port=jaeger-collector:14250"]
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
    depends_on:
      - jaeger-collector

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch-data:
```

### Jaeger配置
```yaml
# jaeger-config.yaml
collector:
  queue:
    size: 2000
    num-workers: 10
  grpc-server:
    host-port: :14250
  http-server:
    host-port: :14268
  sampling:
    strategy-store:
      type: "file"
      file:
        name: "/etc/jaeger/sampling_strategies.json"
```

### Node.js分布式追踪实现
```typescript
// tracing.service.ts
import { Injectable, OnModuleInit } from '@nestjs/common';
import * as opentracing from 'opentracing';
import { initTracerFromEnv } from 'jaeger-client';

@Injectable()
export class TracingService implements OnModuleInit {
  private tracer: opentracing.Tracer;

  async onModuleInit() {
    this.initTracer();
  }

  private initTracer() {
    const config = {
      serviceName: process.env.SERVICE_NAME || 'zhi_xuan_service',
      sampler: {
        type: 'const',
        param: 1,
      },
      reporter: {
        logSpans: true,
        agentHost: process.env.JAEGER_AGENT_HOST || 'localhost',
        agentPort: parseInt(process.env.JAEGER_AGENT_PORT) || 6832,
      },
    };

    const options = {
      tags: {
        'service.version': process.env.SERVICE_VERSION || '1.0.0',
        'environment': process.env.NODE_ENV || 'development',
      },
      baggagePrefix: 'zhi_xuan.',
    };

    this.tracer = initTracerFromEnv(config, options);
  }

  startSpan(operationName: string, parentSpan?: opentracing.Span): opentracing.Span {
    const options: opentracing.SpanOptions = {};
    
    if (parentSpan) {
      options.childOf = parentSpan;
    }
    
    return this.tracer.startSpan(operationName, options);
  }

  inject(span: opentracing.Span, format: opentracing.FORMAT_HTTP_HEADERS | opentracing.FORMAT_TEXT_MAP): any {
    const carrier = {};
    this.tracer.inject(span, format, carrier);
    return carrier;
  }

  extract(format: opentracing.FORMAT_HTTP_HEADERS | opentracing.FORMAT_TEXT_MAP, carrier: any): opentracing.SpanContext | null {
    return this.tracer.extract(format, carrier);
  }

  getTracer(): opentracing.Tracer {
    return this.tracer;
  }

  createTracingInterceptor() {
    return (req, res, next) => {
      const operationName = `${req.method} ${req.path}`;
      const span = this.startSpan(operationName);
      
      // 设置Span标签
      span.setTag(opentracing.Tags.HTTP_METHOD, req.method);
      span.setTag(opentracing.Tags.HTTP_URL, req.url);
      span.setTag('user.agent', req.get('User-Agent'));
      
      // 从请求头提取父Span
      const parentSpan = this.extract(opentracing.FORMAT_HTTP_HEADERS, req.headers);
      if (parentSpan) {
        span.addReference(opentracing.REFERENCE_CHILD_OF, parentSpan);
      }
      
      // 注入Span上下文到请求对象
      req.span = span;
      
      // 监听响应结束事件
      res.on('finish', () => {
        span.setTag(opentracing.Tags.HTTP_STATUS_CODE, res.statusCode);
        
        if (res.statusCode >= 500) {
          span.setTag(opentracing.Tags.ERROR, true);
        }
        
        span.finish();
      });
      
      next();
    };
  }
}
```

## 性能监控 (Prometheus + Grafana)

### Prometheus配置
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'user-service'
    scrape_interval: 5s
    metrics_path: /metrics
    static_configs:
      - targets: ['user-service:3001']
    relabel_configs:
      - source_labels: [__address__]
        target_label: service_name
        replacement: user-service

  - job_name: 'product-service'
    scrape_interval: 5s
    metrics_path: /metrics
    static_configs:
      - targets: ['product-service:3002']
    relabel_configs:
      - source_labels: [__address__]
        target_label: service_name
        replacement: product-service

  - job_name: 'order-service'
    scrape_interval: 5s
    metrics_path: /metrics
    static_configs:
      - targets: ['order-service:3003']
    relabel_configs:
      - source_labels: [__address__]
        target_label: service_name
        replacement: order-service

  - job_name: 'kong'
    scrape_interval: 5s
    static_configs:
      - targets: ['kong:8001']
    metrics_path: /metrics

  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['redis-exporter:9121']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### Node.js服务监控实现
```typescript
// metrics.service.ts
import { Injectable } from '@nestjs/common';
import * as client from 'prom-client';

@Injectable()
export class MetricsService {
  private register: client.Registry;
  
  // 业务指标
  private httpRequestDurationHistogram: client.Histogram<string>;
  private httpRequestTotal: client.Counter<string>;
  private activeUsers: client.Gauge<string>;
  private apiResponseTime: client.Histogram<string>;
  private databaseQueryDuration: client.Histogram<string>;
  private cacheHitRatio: client.Gauge<string>;

  constructor() {
    this.register = new client.Registry();
    
    // 初始化指标
    this.initMetrics();
    
    // 注册指标收集器
    this.register.setDefaultLabels({
      app: 'zhi_xuan_ecommerce',
      version: process.env.SERVICE_VERSION || '1.0.0',
    });
  }

  private initMetrics() {
    // HTTP请求持续时间直方图
    this.httpRequestDurationHistogram = new client.Histogram({
      name: 'http_request_duration_seconds',
      help: 'Duration of HTTP requests in seconds',
      labelNames: ['method', 'route', 'status_code'],
      buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
    });

    // HTTP请求总数计数器
    this.httpRequestTotal = new client.Counter({
      name: 'http_requests_total',
      help: 'Total number of HTTP requests',
      labelNames: ['method', 'route', 'status_code'],
    });

    // 活跃用户数
    this.activeUsers = new client.Gauge({
      name: 'active_users_count',
      help: 'Number of active users',
      labelNames: ['service'],
    });

    // API响应时间
    this.apiResponseTime = new client.Histogram({
      name: 'api_response_time_seconds',
      help: 'API response time in seconds',
      labelNames: ['api', 'method'],
      buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
    });

    // 数据库查询持续时间
    this.databaseQueryDuration = new client.Histogram({
      name: 'database_query_duration_seconds',
      help: 'Database query duration in seconds',
      labelNames: ['query_type', 'table'],
      buckets: [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1],
    });

    // 缓存命中率
    this.cacheHitRatio = new client.Gauge({
      name: 'cache_hit_ratio',
      help: 'Cache hit ratio',
      labelNames: ['cache_type'],
    });

    // 注册所有指标
    this.register.registerMetric(this.httpRequestDurationHistogram);
    this.register.registerMetric(this.httpRequestTotal);
    this.register.registerMetric(this.activeUsers);
    this.register.registerMetric(this.apiResponseTime);
    this.register.registerMetric(this.databaseQueryDuration);
    this.register.registerMetric(this.cacheHitRatio);
  }

  // 记录HTTP请求指标
  recordHttpRequest(
    method: string, 
    route: string, 
    statusCode: number, 
    duration: number
  ) {
    this.httpRequestTotal.inc({ method, route, status_code: statusCode.toString() });
    this.httpRequestDurationHistogram.observe({ 
      method, 
      route, 
      status_code: statusCode.toString() 
    }, duration);
  }

  // 记录API响应时间
  recordApiResponseTime(api: string, method: string, duration: number) {
    this.apiResponseTime.observe({ api, method }, duration);
  }

  // 记录数据库查询时间
  recordDatabaseQuery(queryType: string, table: string, duration: number) {
    this.databaseQueryDuration.observe({ query_type: queryType, table }, duration);
  }

  // 更新缓存命中率
  updateCacheHitRatio(cacheType: string, ratio: number) {
    this.cacheHitRatio.set({ cache_type: cacheType }, ratio);
  }

  // 更新活跃用户数
  updateActiveUsers(service: string, count: number) {
    this.activeUsers.set({ service }, count);
  }

  // 获取指标注册表
  getRegister(): client.Registry {
    return this.register;
  }

  // 获取指标字符串
  async getMetrics(): Promise<string> {
    return await this.register.metrics();
  }

  // 收集业务指标
  collectBusinessMetrics() {
    // 这里可以添加业务特定的指标收集逻辑
    // 例如：订单量、用户注册数、商品浏览量等
    
    // 模拟一些业务指标
    // this.orderCount.inc({ status: 'completed' });
    // this.userRegistrationCount.inc();
  }
}
```

### 监控中间件
```typescript
// metrics.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { MetricsService } from './metrics.service';

@Injectable()
export class MetricsMiddleware implements NestMiddleware {
  constructor(private readonly metricsService: MetricsService) {}

  use(req: Request, res: Response, next: NextFunction) {
    const start = Date.now();
    
    res.on('finish', () => {
      const duration = (Date.now() - start) / 1000; // 转换为秒
      
      // 记录HTTP请求指标
      this.metricsService.recordHttpRequest(
        req.method,
        req.route?.path || req.path,
        res.statusCode,
        duration
      );
    });
    
    next();
  }
}
```

## 日志聚合 (ELK Stack)

### ELK架构配置
```yaml
# elk-stack.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
      - cluster.routing.allocation.disk.threshold_enabled=false
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    environment:
      ELASTICSEARCH_URL: http://elasticsearch:9200
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
    ports:
      - "5044:5044"
      - "5000:5000/tcp"
      - "5000:5000/udp"
      - "9600:9600"
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      - ./logstash/config:/usr/share/logstash/config
    depends_on:
      elasticsearch:
        condition: service_healthy

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      elasticsearch:
        condition: service_healthy

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    user: root
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./logs:/app/logs:ro
    depends_on:
      elasticsearch:
        condition: service_healthy

volumes:
  elasticsearch-data:
```

### Logstash配置
```ruby
# logstash/pipeline/logstash.conf
input {
  beats {
    port => 5044
  }
  
  http {
    port => 5000
    codec => json
  }
}

filter {
  if [type] == "user-service" or [service] == "user-service" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:loglevel}\] %{GREEDYDATA:content}" }
    }
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
  
  if [type] == "product-service" or [service] == "product-service" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:loglevel}\] %{GREEDYDATA:content}" }
    }
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
  
  # 添加服务名称标签
  if [message] =~ /user/ {
    mutate {
      add_tag => [ "user-service" ]
    }
  }
  
  if [message] =~ /product/ {
    mutate {
      add_tag => [ "product-service" ]
    }
  }
  
  if [message] =~ /order/ {
    mutate {
      add_tag => [ "order-service" ]
    }
  }
  
  # 解析JSON格式日志
  if [message] =~ /^\{.*\}$/ {
    json {
      source => "message"
    }
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "zhi_xuan-%{+YYYY.MM.dd}"
    template_name => "zhi_xuan"
    template_pattern => "zhi_xuan-*"
  }
  
  stdout {
    codec => rubydebug
  }
}
```

### Node.js结构化日志实现
```typescript
// logger.service.ts
import { Injectable } from '@nestjs/common';
import * as winston from 'winston';
import * as Transport from 'winston-transport';

// 自定义传输：发送日志到Logstash
class LogstashTransport extends Transport {
  private logstashUrl: string;

  constructor(options = {}) {
    super(options);
    this.logstashUrl = process.env.LOGSTASH_URL || 'http://localhost:5000';
  }

  async log(info: any, callback: () => void) {
    try {
      const logData = {
        ...info,
        service: process.env.SERVICE_NAME || 'unknown-service',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development',
      };

      // 发送到Logstash
      await fetch(this.logstashUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(logData),
      });

      callback();
    } catch (error) {
      console.error('Logstash transport error:', error);
      callback();
    }
  }
}

@Injectable()
export class LoggerService {
  private logger: winston.Logger;

  constructor() {
    this.logger = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.splat(),
        winston.format.json()
      ),
      defaultMeta: { 
        service: process.env.SERVICE_NAME || 'unknown-service',
        version: process.env.SERVICE_VERSION || '1.0.0',
      },
      transports: [
        // 控制台输出
        new winston.transports.Console({
          format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
          ),
        }),
        
        // 文件输出
        new winston.transports.File({ 
          filename: 'logs/error.log', 
          level: 'error',
          maxsize: 5242880, // 5MB
          maxFiles: 5,
        }),
        
        new winston.transports.File({ 
          filename: 'logs/combined.log',
          maxsize: 5242880, // 5MB
          maxFiles: 5,
        }),
        
        // Logstash输出
        new LogstashTransport(),
      ],
    });
  }

  info(message: string, meta?: any) {
    this.logger.info(message, meta);
  }

  warn(message: string, meta?: any) {
    this.logger.warn(message, meta);
  }

  error(message: string, meta?: any) {
    this.logger.error(message, meta);
  }

  debug(message: string, meta?: any) {
    if (process.env.NODE_ENV === 'development') {
      this.logger.debug(message, meta);
    }
  }

  // 记录API请求日志
  logRequest(method: string, url: string, statusCode: number, duration: number, userId?: string) {
    this.logger.info('API Request', {
      type: 'api_request',
      method,
      url,
      statusCode,
      duration,
      userId,
      service: process.env.SERVICE_NAME,
    });
  }

  // 记录数据库操作日志
  logDatabaseOperation(operation: string, table: string, duration: number, success: boolean) {
    this.logger.info('Database Operation', {
      type: 'database_operation',
      operation,
      table,
      duration,
      success,
      service: process.env.SERVICE_NAME,
    });
  }

  // 记录缓存操作日志
  logCacheOperation(operation: string, key: string, hit: boolean) {
    this.logger.info('Cache Operation', {
      type: 'cache_operation',
      operation,
      key,
      hit,
      service: process.env.SERVICE_NAME,
    });
  }

  // 记录错误日志（包含追踪ID）
  logErrorWithTrace(error: Error, traceId: string, additionalInfo?: any) {
    this.logger.error('Error with Trace', {
      type: 'error_with_trace',
      error: error.message,
      stack: error.stack,
      traceId,
      additionalInfo,
      service: process.env.SERVICE_NAME,
    });
  }
}
```

## 健康检查和熔断器

### 健康检查实现
```typescript
// health-check.service.ts
import { Injectable } from '@nestjs/common';
import { HealthIndicator, HealthIndicatorResult, HealthCheckError } from '@nestjs/terminus';
import * as Redis from 'ioredis';
import { Pool } from 'pg';

@Injectable()
export class CustomHealthIndicator extends HealthIndicator {
  constructor(
    private readonly redis: Redis,
    private readonly dbPool: Pool,
  ) {
    super();
  }

  async databaseHealth(key: string): Promise<HealthIndicatorResult> {
    try {
      await this.dbPool.query('SELECT 1');
      return this.getStatus(key, true);
    } catch (error) {
      throw new HealthCheckError('Database check failed', this.getStatus(key, false));
    }
  }

  async redisHealth(key: string): Promise<HealthIndicatorResult> {
    try {
      await this.redis.ping();
      return this.getStatus(key, true);
    } catch (error) {
      throw new HealthCheckError('Redis check failed', this.getStatus(key, false));
    }
  }
}

// health.controller.ts
import { Controller, Get } from '@nestjs/common';
import { HealthCheckService, HealthCheck, TypeOrmHealthIndicator } from '@nestjs/terminus';
import { CustomHealthIndicator } from './health-check.service';

@Controller('health')
export class HealthController {
  constructor(
    private health: HealthCheckService,
    private customHealth: CustomHealthIndicator,
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      () => this.customHealth.databaseHealth('database'),
      () => this.customHealth.redisHealth('redis'),
      async () => {
        // 检查外部服务
        const response = await fetch('http://external-service:3000/health');
        const isHealthy = response.ok;
        return this.customHealth.getStatus('external-service', isHealthy);
      },
    ]);
  }
}
```

### 熔断器实现
```typescript
// circuit-breaker.service.ts
import { Injectable } from '@nestjs/common';

export enum CircuitState {
  CLOSED = 'CLOSED',
  OPEN = 'OPEN',
  HALF_OPEN = 'HALF_OPEN',
}

export interface CircuitBreakerOptions {
  failureThreshold?: number;  // 失败次数阈值
  timeout?: number;           // 熔断器开启后等待时间（毫秒）
  successThreshold?: number;  // 半开状态下成功次数阈值
}

@Injectable()
export class CircuitBreakerService {
  private circuitStates: Map<string, {
    state: CircuitState;
    failureCount: number;
    lastFailureTime: number | null;
    timeoutId: NodeJS.Timeout | null;
  }> = new Map();

  execute<T>(
    name: string,
    fn: () => Promise<T>,
    options: CircuitBreakerOptions = {}
  ): Promise<T> {
    const circuit = this.getCircuit(name, options);
    
    if (circuit.state === CircuitState.OPEN) {
      if (Date.now() - (circuit.lastFailureTime || 0) < (options.timeout || 60000)) {
        return Promise.reject(new Error('Circuit breaker is OPEN'));
      } else {
        // 超时后进入半开状态
        circuit.state = CircuitState.HALF_OPEN;
      }
    }

    return fn()
      .then(result => {
        this.onSuccess(name, options);
        return result;
      })
      .catch(error => {
        this.onFailure(name, options);
        throw error;
      });
  }

  private getCircuit(name: string, options: CircuitBreakerOptions) {
    if (!this.circuitStates.has(name)) {
      this.circuitStates.set(name, {
        state: CircuitState.CLOSED,
        failureCount: 0,
        lastFailureTime: null,
        timeoutId: null,
      });
    }
    return this.circuitStates.get(name)!;
  }

  private onSuccess(name: string, options: CircuitBreakerOptions) {
    const circuit = this.circuitStates.get(name)!;
    
    if (circuit.state === CircuitState.HALF_OPEN) {
      // 半开状态下成功，重置为关闭状态
      circuit.state = CircuitState.CLOSED;
      circuit.failureCount = 0;
      circuit.lastFailureTime = null;
    }
  }

  private onFailure(name: string, options: CircuitBreakerOptions) {
    const circuit = this.circuitStates.get(name)!;
    
    circuit.failureCount++;
    circuit.lastFailureTime = Date.now();
    
    const failureThreshold = options.failureThreshold || 5;
    
    if (circuit.failureCount >= failureThreshold) {
      circuit.state = CircuitState.OPEN;
      
      // 设置定时器，过期后进入半开状态
      if (circuit.timeoutId) {
        clearTimeout(circuit.timeoutId);
      }
      
      circuit.timeoutId = setTimeout(() => {
        circuit.state = CircuitState.HALF_OPEN;
      }, options.timeout || 60000);
    }
  }

  reset(name: string) {
    const circuit = this.circuitStates.get(name);
    if (circuit) {
      circuit.state = CircuitState.CLOSED;
      circuit.failureCount = 0;
      circuit.lastFailureTime = null;
      if (circuit.timeoutId) {
        clearTimeout(circuit.timeoutId);
        circuit.timeoutId = null;
      }
    }
  }

  getStatus(name: string) {
    return this.circuitStates.get(name)?.state || CircuitState.CLOSED;
  }
}
```

## 服务治理和监控总结

这个服务治理和监控组件设计包含了：

1. 服务注册与发现（Consul）
2. API网关（Kong）
3. 配置中心
4. 分布式追踪（Jaeger）
5. 性能监控（Prometheus + Grafana）
6. 日志聚合（ELK Stack）
7. 健康检查和熔断器

这套完整的治理和监控体系确保了智选电商平台的高可用性、可观测性和可维护性，满足99.99%可用性和性能要求。