# 智选电商平台高可用性保障措施

## 高可用性目标

智选电商平台的目标是实现99.99%的系统可用性，即全年停机时间不超过52.6分钟。为实现这一目标，需要从架构、部署、监控、容灾等多个维度制定全面的高可用保障措施。

## 1. 系统架构高可用设计

### 1.1 微服务无单点故障设计

#### 多实例部署策略
```
应用层高可用
├── 用户服务集群 (3+实例，跨可用区部署)
├── 商品服务集群 (3+实例，跨可用区部署) 
├── 订单服务集群 (3+实例，跨可用区部署)
├── 支付服务集群 (3+实例，跨可用区部署)
└── API网关集群 (2+实例，负载均衡)
```

#### 负载均衡策略
```yaml
# ingress-nginx 配置示例
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: zhi-xuan-ingress
  annotations:
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "route"
    nginx.ingress.kubernetes.io/session-cookie-hash: "sha1"
    nginx.ingress.kubernetes.io/upstream-hash-by: "$request_uri"
spec:
  rules:
  - host: api.zhixuan.com
    http:
      paths:
      - path: /api/v1/users
        pathType: Prefix
        backend:
          service:
            name: user-service
            port:
              number: 3001
      - path: /api/v1/products
        pathType: Prefix
        backend:
          service:
            name: product-service
            port:
              number: 3002
```

### 1.2 数据库高可用架构

#### PostgreSQL主从复制 + 故障转移
```bash
#!/bin/bash
# pg_failover.sh - PostgreSQL故障转移脚本

MASTER_HOST="pg-master.zhixuan.internal"
SLAVE_HOSTS=("pg-slave-1.zhixuan.internal" "pg-slave-2.zhixuan.internal")
VIP="10.0.0.100"  # 虚拟IP
CLUSTER_NAME="zhi_xuan_db_cluster"

# 检查主库健康状态
check_master_health() {
    pg_isready -h $MASTER_HOST -p 5432
    return $?
}

# 检查从库健康状态
check_slave_health() {
    local slave_host=$1
    pg_isready -h $slave_host -p 5432
    return $?
}

# 提升从库为新主库
promote_slave() {
    local slave_host=$1
    echo "Promoting $slave_host to master..."
    
    # 提升从库
    psql -h $slave_host -p 5432 -U postgres -c "SELECT pg_promote();"
    
    # 配置VIP漂移
    if command -v keepalived &> /dev/null; then
        # 使用Keepalived进行VIP漂移
        systemctl reload keepalived
    else
        # 手动配置VIP
        ip addr add $VIP/24 dev eth0
    fi
    
    # 通知应用层配置变更
    update_app_config $slave_host
}

# 更新应用配置
update_app_config() {
    local new_master=$1
    echo "Updating application database configuration..."
    
    # 更新配置文件
    sed -i "s/$MASTER_HOST/$new_master/g" /app/config/database.json
    
    # 重新加载配置
    pkill -HUP -f app-process
}

# 执行故障转移
perform_failover() {
    echo "Starting failover procedure..."
    
    # 确认主库确实故障
    if check_master_health; then
        echo "Master is still alive, aborting failover"
        return 1
    fi
    
    # 检查从库状态，选择最好的从库进行提升
    for slave in "${SLAVE_HOSTS[@]}"; do
        if check_slave_health $slave; then
            # 检查复制延迟
            REPLICATION_DELAY=$(psql -h $slave -p 5432 -U postgres -t -c "
                SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()));
            " 2>/dev/null)
            
            if [ $? -eq 0 ] && [ $(echo "$REPLICATION_DELAY < 30" | bc) -eq 1 ]; then
                promote_slave $slave
                echo "Failover completed successfully"
                return 0
            fi
        fi
    done
    
    echo "No healthy slave found, failover failed"
    return 1
}

# 监控脚本
while true; do
    if ! check_master_health; then
        echo "$(date): Master database is down, initiating failover..."
        perform_failover
        break
    fi
    sleep 10
done
```

#### Redis集群高可用
```yaml
# redis-cluster-failover.yml
version: '3.8'

services:
  redis-sentinel:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26379:26379"
      - "26380:26380"
      - "26381:26381"
    volumes:
      - ./sentinel.conf:/etc/redis/sentinel.conf
    networks:
      - redis-net
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.labels.zone == beijing
          - node.labels.zone == shanghai
          - node.labels.zone == shenzhen

  redis-master:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis-master.conf:/etc/redis/redis.conf
    networks:
      - redis-net
    deploy:
      placement:
        constraints:
          - node.labels.zone == beijing

  redis-slave-1:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis-slave.conf:/etc/redis/redis.conf
    networks:
      - redis-net
    deploy:
      placement:
        constraints:
          - node.labels.zone == shanghai

  redis-slave-2:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - ./redis-slave.conf:/etc/redis/redis.conf
    networks:
      - redis-net
    deploy:
      placement:
        constraints:
          - node.labels.zone == shenzhen

networks:
  redis-net:
    driver: overlay
    attachable: true
```

## 2. 多数据中心容灾策略

### 2.1 多区域部署架构
```
                    用户请求
                         │
        ┌────────────────┼────────────────┐
        │                │                │
  北京数据中心       上海数据中心       深圳数据中心
  (主数据中心)      (热备数据中心)      (灾备数据中心)
        │                │                │
     应用集群          应用集群          应用集群
     数据库主          数据库从          数据库从
     Redis主           Redis从           Redis从
```

### 2.2 数据同步策略

#### 异步复制配置
```sql
-- PostgreSQL异步流复制配置
-- 主库 postgresql.conf
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
synchronous_commit = off  -- 异步复制，提高性能
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/archive/%f'

-- 从库 recovery.conf
standby_mode = 'on'
primary_conninfo = 'host=pg-master port=5432 user=replicator password=replicator'
recovery_target_timeline = 'latest'
```

#### Redis数据同步
```bash
#!/bin/bash
# redis-sync.sh - Redis数据同步脚本

REDIS_MASTER="redis-master.zhixuan.internal:6379"
REDIS_SLAVES=("redis-slave-1.zhixuan.internal:6379" "redis-slave-2.zhixuan.internal:6379")

# Redis数据备份
backup_redis_data() {
    local backup_dir="/data/redis-backup/$(date +%Y%m%d_%H%M%S)"
    mkdir -p $backup_dir
    
    # 执行BGSAVE
    redis-cli -h $REDIS_MASTER -p 6379 BGSAVE
    
    # 等待RDB文件生成
    sleep 10
    
    # 复制RDB文件
    cp /var/lib/redis/dump.rdb $backup_dir/
    
    # 压缩备份
    tar -czf $backup_dir/redis_backup.tar.gz -C $backup_dir dump.rdb
    rm $backup_dir/dump.rdb
    
    echo "Redis backup completed: $backup_dir/redis_backup.tar.gz"
}

# Redis数据恢复
restore_redis_data() {
    local backup_file=$1
    local target_slave=$2
    
    # 解压备份文件
    local temp_dir="/tmp/redis-restore-$(date +%s)"
    mkdir -p $temp_dir
    tar -xzf $backup_file -C $temp_dir
    
    # 停止Redis服务
    ssh $target_slave "sudo systemctl stop redis"
    
    # 替换RDB文件
    scp $temp_dir/dump.rdb $target_slave:/var/lib/redis/dump.rdb
    
    # 启动Redis服务
    ssh $target_slave "sudo systemctl start redis"
    
    # 清理临时文件
    rm -rf $temp_dir
    
    echo "Redis restore completed on $target_slave"
}

# 数据同步监控
monitor_sync_status() {
    for slave in "${REDIS_SLAVES[@]}"; do
        local status=$(redis-cli -h $slave --raw INFO replication | grep "master_link_status:")
        if [[ "$status" != *"master_link_status:up"* ]]; then
            echo "Redis replication broken for $slave"
            # 触发告警
            trigger_alert "Redis replication broken: $slave"
        fi
    done
}
```

### 2.3 容灾切换流程

#### 自动故障检测与切换
```typescript
// disaster-recovery.service.ts
import { Injectable } from '@nestjs/common';
import * as dns from 'dns/promises';

export enum RegionStatus {
  PRIMARY = 'primary',
  SECONDARY = 'secondary',
  FAILOVER = 'failover',
}

@Injectable()
export class DisasterRecoveryService {
  private regions: Map<string, {
    status: RegionStatus;
    health: boolean;
    lastCheck: Date;
    failoverCount: number;
  }> = new Map();

  constructor() {
    this.regions.set('beijing', { 
      status: RegionStatus.PRIMARY, 
      health: true, 
      lastCheck: new Date(),
      failoverCount: 0
    });
    this.regions.set('shanghai', { 
      status: RegionStatus.SECONDARY, 
      health: true, 
      lastCheck: new Date(),
      failoverCount: 0
    });
    this.regions.set('shenzhen', { 
      status: RegionStatus.SECONDARY, 
      health: true, 
      lastCheck: new Date(),
      failoverCount: 0
    });
  }

  async monitorRegions(): Promise<void> {
    const checkPromises = Array.from(this.regions.keys()).map(region => 
      this.checkRegionHealth(region)
    );
    
    const results = await Promise.allSettled(checkPromises);
    
    for (let i = 0; i < results.length; i++) {
      const region = Array.from(this.regions.keys())[i];
      const result = results[i];
      
      if (result.status === 'fulfilled') {
        this.regions.get(region)!.health = result.value;
        this.regions.get(region)!.lastCheck = new Date();
      } else {
        this.regions.get(region)!.health = false;
        console.error(`Health check failed for region ${region}:`, result.reason);
      }
    }
    
    await this.evaluateFailover();
  }

  private async checkRegionHealth(region: string): Promise<boolean> {
    try {
      // 检查DNS解析
      await dns.resolve4(`api.${region}.zhixuan.internal`);
      
      // 检查API服务可用性
      const response = await fetch(`http://${region}.zhixuan.internal:8080/health`, {
        timeout: 5000,
      });
      
      return response.ok;
    } catch (error) {
      console.error(`Region health check failed for ${region}:`, error);
      return false;
    }
  }

  private async evaluateFailover(): Promise<void> {
    const primaryRegion = Array.from(this.regions.entries())
      .find(([_, config]) => config.status === RegionStatus.PRIMARY);
    
    if (!primaryRegion || !primaryRegion[1].health) {
      console.log('Primary region is unhealthy, initiating failover...');
      
      // 寻找最健康的备用区域
      const healthySecondary = Array.from(this.regions.entries())
        .filter(([_, config]) => 
          config.status === RegionStatus.SECONDARY && config.health
        )
        .sort((a, b) => b[1].lastCheck.getTime() - a[1].lastCheck.getTime())[0];
      
      if (healthySecondary) {
        await this.performFailover(healthySecondary[0]);
      } else {
        console.error('No healthy secondary region found for failover');
      }
    }
  }

  private async performFailover(targetRegion: string): Promise<void> {
    console.log(`Performing failover to region: ${targetRegion}`);
    
    // 1. 更新区域状态
    for (const [region, config] of this.regions) {
      if (region === targetRegion) {
        config.status = RegionStatus.PRIMARY;
      } else if (config.status === RegionStatus.PRIMARY) {
        config.status = RegionStatus.FAILOVER;
        config.failoverCount++;
      }
    }
    
    // 2. 更新DNS记录
    await this.updateDnsRecords(targetRegion);
    
    // 3. 更新应用配置
    await this.updateApplicationConfig(targetRegion);
    
    // 4. 通知相关服务
    await this.notifyServices(targetRegion);
    
    console.log(`Failover to ${targetRegion} completed successfully`);
  }

  private async updateDnsRecords(targetRegion: string): Promise<void> {
    // 这里应该调用DNS提供商的API来更新DNS记录
    console.log(`Updating DNS records to point to ${targetRegion}`);
    
    // 示例：更新主域名解析
    // await dnsProvider.updateRecord('api.zhixuan.com', `${targetRegion}.internal`);
  }

  private async updateApplicationConfig(targetRegion: string): Promise<void> {
    // 更新应用配置以指向新的主区域
    console.log(`Updating application config to use ${targetRegion} as primary`);
    
    // 这里可以更新配置中心的配置
    // await configService.updateConfig('primary-region', targetRegion);
  }

  private async notifyServices(targetRegion: string): Promise<void> {
    // 通知所有服务配置变更
    console.log(`Notifying services about region change to ${targetRegion}`);
    
    // 可以通过消息队列或API调用通知其他服务
    // await messageQueue.publish('region_change', { newPrimary: targetRegion });
  }
}
```

## 3. 服务级别保障措施

### 3.1 服务熔断与降级

#### 熔断器配置
```typescript
// circuit-breaker.config.ts
export interface CircuitBreakerConfig {
  name: string;
  failureThreshold: number;    // 失败阈值
  timeout: number;             // 熔断器开启后等待时间(毫秒)
  successThreshold: number;    // 半开状态成功阈值
  requestVolumeThreshold: number; // 启用熔断的最小请求数
  errorPercentageThreshold: number; // 错误率阈值(%)
}

export const CIRCUIT_BREAKER_CONFIGS: Record<string, CircuitBreakerConfig> = {
  'user-service': {
    name: 'user-service',
    failureThreshold: 5,
    timeout: 60000,
    successThreshold: 3,
    requestVolumeThreshold: 10,
    errorPercentageThreshold: 50,
  },
  'product-service': {
    name: 'product-service',
    failureThreshold: 3,
    timeout: 30000,
    successThreshold: 2,
    requestVolumeThreshold: 20,
    errorPercentageThreshold: 60,
  },
  'order-service': {
    name: 'order-service',
    failureThreshold: 2,
    timeout: 120000,
    successThreshold: 1,
    requestVolumeThreshold: 5,
    errorPercentageThreshold: 40,
  },
};
```

#### 降级策略实现
```typescript
// fallback.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class FallbackService {
  // 用户服务降级
  async userFallback(userId: string) {
    // 返回缓存的用户信息或默认信息
    console.log(`User service is down, returning fallback for user: ${userId}`);
    
    // 尝试从缓存获取
    const cachedUser = await this.getUserFromCache(userId);
    if (cachedUser) {
      return cachedUser;
    }
    
    // 返回默认用户信息
    return {
      userId,
      username: 'default_user',
      email: 'user@fallback.com',
      avatar: '/images/default-avatar.png',
      isFallback: true,
    };
  }

  // 商品服务降级
  async productFallback(productId: string) {
    console.log(`Product service is down, returning fallback for product: ${productId}`);
    
    // 返回缓存的商品信息
    const cachedProduct = await this.getProductFromCache(productId);
    if (cachedProduct) {
      return cachedProduct;
    }
    
    // 返回默认商品信息
    return {
      productId,
      name: 'Product Unavailable',
      price: 0,
      stock: 0,
      images: ['/images/unavailable.png'],
      isFallback: true,
    };
  }

  // 订单服务降级
  async orderFallback(orderId: string) {
    console.log(`Order service is down, returning fallback for order: ${orderId}`);
    
    // 返回简化订单信息
    return {
      orderId,
      status: 'SERVICE_UNAVAILABLE',
      totalAmount: 0,
      items: [],
      isFallback: true,
    };
  }

  private async getUserFromCache(userId: string) {
    // 实现从缓存获取用户信息的逻辑
    return null; // 示例返回
  }

  private async getProductFromCache(productId: string) {
    // 实现从缓存获取商品信息的逻辑
    return null; // 示例返回
  }
}
```

### 3.2 限流与过载保护

#### 令牌桶限流算法
```typescript
// rate-limiter.service.ts
import { Injectable } from '@nestjs/common';

export interface RateLimitConfig {
  tokensPerInterval: number;  // 每个时间间隔的令牌数
  interval: number;           // 时间间隔(毫秒)
}

@Injectable()
export class RateLimiterService {
  private rateLimiters: Map<string, {
    tokens: number;
    lastRefill: number;
    config: RateLimitConfig;
  }> = new Map();

  async isAllowed(key: string, config: RateLimitConfig): Promise<boolean> {
    const limiter = this.getOrCreateLimiter(key, config);
    
    // 补充令牌
    this.refillTokens(limiter);
    
    if (limiter.tokens > 0) {
      limiter.tokens--;
      return true;
    }
    
    return false;
  }

  private getOrCreateLimiter(key: string, config: RateLimitConfig) {
    if (!this.rateLimiters.has(key)) {
      this.rateLimiters.set(key, {
        tokens: config.tokensPerInterval,
        lastRefill: Date.now(),
        config,
      });
    }
    return this.rateLimiters.get(key)!;
  }

  private refillTokens(limiter: {
    tokens: number;
    lastRefill: number;
    config: RateLimitConfig;
  }) {
    const now = Date.now();
    const timePassed = now - limiter.lastRefill;
    const intervalsPassed = Math.floor(timePassed / limiter.config.interval);
    
    if (intervalsPassed > 0) {
      const newTokens = Math.min(
        limiter.config.tokensPerInterval,
        limiter.tokens + (intervalsPassed * limiter.config.tokensPerInterval)
      );
      
      limiter.tokens = newTokens;
      limiter.lastRefill = now;
    }
  }

  // API限流中间件
  createRateLimitMiddleware(config: RateLimitConfig) {
    return async (req: any, res: any, next: any) => {
      const key = this.getClientKey(req);
      const allowed = await this.isAllowed(key, config);
      
      if (!allowed) {
        res.status(429).json({
          error: 'Too Many Requests',
          message: 'Rate limit exceeded',
        });
        return;
      }
      
      next();
    };
  }

  private getClientKey(req: any): string {
    // 基于IP地址、用户ID等生成限流键
    return req.headers['x-forwarded-for'] || 
           req.connection.remoteAddress || 
           req.ip ||
           'unknown';
  }
}
```

## 4. 监控告警体系

### 4.1 关键指标监控

#### Prometheus监控指标
```typescript
// monitoring.constants.ts
export const MONITORING_METRICS = {
  // 系统指标
  HTTP_REQUEST_DURATION: 'http_request_duration_seconds',
  HTTP_REQUEST_TOTAL: 'http_requests_total',
  ACTIVE_USERS: 'active_users_count',
  API_RESPONSE_TIME: 'api_response_time_seconds',
  DATABASE_QUERY_DURATION: 'database_query_duration_seconds',
  CACHE_HIT_RATIO: 'cache_hit_ratio',
  
  // 业务指标
  ORDER_COUNT: 'order_count',
  USER_REGISTRATION: 'user_registration_count',
  PRODUCT_VIEW: 'product_view_count',
  PAYMENT_SUCCESS: 'payment_success_count',
  PAYMENT_FAILURE: 'payment_failure_count',
  
  // 健康指标
  SERVICE_HEALTH: 'service_health_status',
  DATABASE_CONNECTIONS: 'database_connections',
  REDIS_CONNECTIONS: 'redis_connections',
  QUEUE_SIZE: 'message_queue_size',
};
```

#### 告警规则配置
```yaml
# alert_rules.yml
groups:
- name: zhi_xuan_alerts
  rules:
  # 系统健康告警
  - alert: ServiceDown
    expr: up{job="user-service"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Service {{ $labels.instance }} is down"
      description: "Service {{ $labels.instance }} has been down for more than 1 minute"

  # 性能告警
  - alert: HighHTTPErrorRate
    expr: 100 * sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 5
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High error rate on {{ $labels.instance }}"
      description: "HTTP error rate is above 5% for the past 5 minutes"

  # 响应时间告警
  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 3m
    labels:
      severity: warning
    annotations:
      summary: "High response time on {{ $labels.instance }}"
      description: "95th percentile response time is above 1 second"

  # 资源使用告警
  - alert: HighCPUUsage
    expr: 100 * (1 - avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m]))) > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage on {{ $labels.instance }}"
      description: "CPU usage is above 80%"

  # 数据库告警
  - alert: DatabaseDown
    expr: up{job="postgres-exporter"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Database {{ $labels.instance }} is down"
      description: "Database connection failed"

  # 缓存告警
  - alert: RedisDown
    expr: up{job="redis-exporter"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Redis {{ $labels.instance }} is down"
      description: "Redis connection failed"

  # 业务指标告警
  - alert: LowCacheHitRatio
    expr: cache_hit_ratio < 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Low cache hit ratio"
      description: "Cache hit ratio is below 80%"
```

### 4.2 告警通知机制

#### 多渠道告警通知
```typescript
// alert-notification.service.ts
import { Injectable } from '@nestjs/common';

export enum AlertSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

export interface Alert {
  id: string;
  title: string;
  description: string;
  severity: AlertSeverity;
  timestamp: Date;
  service: string;
  metrics?: Record<string, any>;
}

@Injectable()
export class AlertNotificationService {
  async sendAlert(alert: Alert): Promise<void> {
    // 根据严重程度选择通知渠道
    const channels = this.getNotificationChannels(alert.severity);
    
    const sendPromises = channels.map(channel => 
      this.sendToChannel(alert, channel)
    );
    
    await Promise.allSettled(sendPromises);
  }

  private getNotificationChannels(severity: AlertSeverity): string[] {
    switch (severity) {
      case AlertSeverity.CRITICAL:
        return ['email', 'sms', 'wechat', 'phone'];
      case AlertSeverity.HIGH:
        return ['email', 'sms', 'wechat'];
      case AlertSeverity.MEDIUM:
        return ['email', 'wechat'];
      case AlertSeverity.LOW:
        return ['email'];
      default:
        return ['email'];
    }
  }

  private async sendToChannel(alert: Alert, channel: string): Promise<void> {
    switch (channel) {
      case 'email':
        await this.sendEmail(alert);
        break;
      case 'sms':
        await this.sendSMS(alert);
        break;
      case 'wechat':
        await this.sendWeChat(alert);
        break;
      case 'phone':
        await this.makePhoneCall(alert);
        break;
      default:
        console.warn(`Unknown notification channel: ${channel}`);
    }
  }

  private async sendEmail(alert: Alert): Promise<void> {
    console.log(`Sending email alert: ${alert.title}`);
    // 实现邮件发送逻辑
  }

  private async sendSMS(alert: Alert): Promise<void> {
    console.log(`Sending SMS alert: ${alert.title}`);
    // 实现短信发送逻辑
  }

  private async sendWeChat(alert: Alert): Promise<void> {
    console.log(`Sending WeChat alert: ${alert.title}`);
    // 实现微信推送逻辑
  }

  private async makePhoneCall(alert: Alert): Promise<void> {
    console.log(`Making phone call alert: ${alert.title}`);
    // 实现电话呼叫逻辑
  }
}
```

## 5. 备份与恢复策略

### 5.1 数据备份策略

#### 全量与增量备份
```bash
#!/bin/bash
# backup-strategy.sh - 备份策略脚本

BACKUP_BASE_DIR="/data/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
DAILY_RETENTION=7
WEEKLY_RETENTION=4
MONTHLY_RETENTION=12

# PostgreSQL备份函数
backup_postgresql() {
    local db_name=$1
    local backup_dir="$BACKUP_BASE_DIR/postgresql/$db_name"
    
    mkdir -p "$backup_dir/daily"
    mkdir -p "$backup_dir/weekly"
    mkdir -p "$backup_dir/monthly"
    
    # 全量备份
    pg_dump -h localhost -U backup_user -d "$db_name" -Fc -f "$backup_dir/daily/${db_name}_${DATE}.dump"
    
    if [ $? -eq 0 ]; then
        echo "PostgreSQL backup completed for $db_name"
        
        # 设置备份文件权限
        chmod 600 "$backup_dir/daily/${db_name}_${DATE}.dump"
        
        # 验证备份文件
        pg_restore --list "$backup_dir/daily/${db_name}_${DATE}.dump" > /dev/null
        if [ $? -eq 0 ]; then
            echo "Backup verification successful for $db_name"
        else
            echo "Backup verification failed for $db_name"
        fi
    else
        echo "PostgreSQL backup failed for $db_name"
        return 1
    fi
}

# Redis备份函数
backup_redis() {
    local backup_dir="$BACKUP_BASE_DIR/redis"
    mkdir -p "$backup_dir"
    
    # 触发Redis BGSAVE
    redis-cli -h localhost -p 6379 BGSAVE
    
    # 等待RDB文件生成
    sleep 10
    
    # 复制RDB文件
    local rdb_file="/var/lib/redis/dump.rdb"
    if [ -f "$rdb_file" ]; then
        cp "$rdb_file" "$backup_dir/redis_backup_${DATE}.rdb"
        chmod 600 "$backup_dir/redis_backup_${DATE}.rdb"
        echo "Redis backup completed"
    else
        echo "Redis backup failed: RDB file not found"
        return 1
    fi
}

# 文件系统备份
backup_files() {
    local backup_dir="$BACKUP_BASE_DIR/files"
    mkdir -p "$backup_dir"
    
    # 备份重要配置文件和上传文件
    tar -czf "$backup_dir/config_backup_${DATE}.tar.gz" \
        -C /app/config . 2>/dev/null
    
    if [ -d "/app/uploads" ]; then
        tar -czf "$backup_dir/uploads_backup_${DATE}.tar.gz" \
            -C /app/uploads . 2>/dev/null
    fi
    
    echo "File backup completed"
}

# 清理过期备份
cleanup_old_backups() {
    local current_date=$(date +%s)
    
    # 清理过期的每日备份
    find "$BACKUP_BASE_DIR" -name "*.dump" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_BASE_DIR" -name "*.rdb" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_BASE_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    echo "Old backups cleaned up"
}

# 执行备份
echo "Starting backup process..."
backup_postgresql "zhi_xuan_user"
backup_postgresql "zhi_xuan_product"
backup_postgresql "zhi_xuan_order"
backup_postgresql "zhi_xuan_inventory"
backup_postgresql "zhi_xuan_marketing"
backup_redis
backup_files
cleanup_old_backups

# 上传到远程存储（可选）
if [ -n "$REMOTE_STORAGE_URL" ]; then
    echo "Uploading backups to remote storage..."
    # 实现远程存储上传逻辑
fi

echo "Backup process completed at $(date)"
```

### 5.2 灾难恢复流程

#### 恢复脚本
```bash
#!/bin/bash
# disaster-recovery.sh - 灾难恢复脚本

RESTORE_BASE_DIR="/data/backups"
RESTORE_DATE=${1:-$(date +%Y%m%d_%H%M%S)}

# 恢复PostgreSQL数据库
restore_postgresql() {
    local db_name=$1
    local backup_file=$2
    
    if [ ! -f "$backup_file" ]; then
        echo "Backup file not found: $backup_file"
        return 1
    fi
    
    echo "Restoring database $db_name from $backup_file"
    
    # 检查数据库是否存在，不存在则创建
    if ! psql -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        createdb -O app_user "$db_name"
        echo "Database $db_name created"
    fi
    
    # 执行恢复
    pg_restore -h localhost -U restore_user -d "$db_name" --clean --if-exists "$backup_file"
    
    if [ $? -eq 0 ]; then
        echo "Database $db_name restored successfully"
    else
        echo "Database restore failed for $db_name"
        return 1
    fi
}

# 恢复Redis数据
restore_redis() {
    local backup_file=$1
    
    if [ ! -f "$backup_file" ]; then
        echo "Redis backup file not found: $backup_file"
        return 1
    fi
    
    echo "Restoring Redis from $backup_file"
    
    # 停止Redis服务
    systemctl stop redis
    
    # 复制RDB文件
    cp "$backup_file" /var/lib/redis/dump.rdb
    
    # 设置权限
    chown redis:redis /var/lib/redis/dump.rdb
    chmod 600 /var/lib/redis/dump.rdb
    
    # 启动Redis服务
    systemctl start redis
    
    echo "Redis restored successfully"
}

# 恢复文件
restore_files() {
    local files_backup=$1
    
    if [ ! -f "$files_backup" ]; then
        echo "Files backup not found: $files_backup"
        return 1
    fi
    
    echo "Restoring files from $files_backup"
    
    # 恢复配置文件
    if [[ "$files_backup" == *"config_backup"* ]]; then
        mkdir -p /app/config
        tar -xzf "$files_backup" -C /app/config
    fi
    
    # 恢复上传文件
    if [[ "$files_backup" == *"uploads_backup"* ]]; then
        mkdir -p /app/uploads
        tar -xzf "$files_backup" -C /app/uploads
    fi
    
    echo "Files restored successfully"
}

# 完整恢复流程
perform_full_recovery() {
    echo "Starting full disaster recovery..."
    
    # 1. 恢复数据库
    for db in user product order inventory marketing; do
        backup_file=$(find "$RESTORE_BASE_DIR/postgresql/zhi_xuan_$db" -name "zhi_xuan_$db*.dump" -newest -print -quit 2>/dev/null)
        if [ -n "$backup_file" ]; then
            restore_postgresql "zhi_xuan_$db" "$backup_file"
        fi
    done
    
    # 2. 恢复Redis
    redis_backup=$(find "$RESTORE_BASE_DIR/redis" -name "redis_backup*.rdb" -newest -print -quit 2>/dev/null)
    if [ -n "$redis_backup" ]; then
        restore_redis "$redis_backup"
    fi
    
    # 3. 恢复文件
    config_backup=$(find "$RESTORE_BASE_DIR/files" -name "config_backup*.tar.gz" -newest -print -quit 2>/dev/null)
    if [ -n "$config_backup" ]; then
        restore_files "$config_backup"
    fi
    
    uploads_backup=$(find "$RESTORE_BASE_DIR/files" -name "uploads_backup*.tar.gz" -newest -print -quit 2>/dev/null)
    if [ -n "$uploads_backup" ]; then
        restore_files "$uploads_backup"
    fi
    
    # 4. 重启应用服务
    echo "Restarting application services..."
    systemctl restart user-service
    systemctl restart product-service
    systemctl restart order-service
    systemctl restart api-gateway
    
    echo "Full disaster recovery completed"
}

# 执行恢复
perform_full_recovery
```

## 6. 高可用性测试与演练

### 6.1 故障演练计划

#### 演练脚本
```typescript
// chaos-engineering.service.ts
import { Injectable } from '@nestjs/common';

export interface ChaosTestConfig {
  testName: string;
  targetService: string;
  faultType: 'latency' | 'error' | 'kill' | 'network' | 'disk';
  duration: number; // 持续时间(秒)
  probability: number; // 故障概率(0-1)
}

@Injectable()
export class ChaosEngineeringService {
  private runningTests: Map<string, NodeJS.Timeout> = new Map();

  async startChaosTest(config: ChaosTestConfig): Promise<string> {
    const testId = this.generateTestId();
    
    console.log(`Starting chaos test: ${config.testName} (ID: ${testId})`);
    
    switch (config.faultType) {
      case 'latency':
        this.injectLatency(config, testId);
        break;
      case 'error':
        this.injectError(config, testId);
        break;
      case 'kill':
        this.killService(config, testId);
        break;
      case 'network':
        this.injectNetworkFault(config, testId);
        break;
      case 'disk':
        this.injectDiskFault(config, testId);
        break;
    }
    
    // 设置定时器自动停止测试
    const timeoutId = setTimeout(() => {
      this.stopChaosTest(testId);
    }, config.duration * 1000);
    
    this.runningTests.set(testId, timeoutId);
    
    return testId;
  }

  async stopChaosTest(testId: string): Promise<boolean> {
    if (this.runningTests.has(testId)) {
      const timeoutId = this.runningTests.get(testId)!;
      clearTimeout(timeoutId);
      this.runningTests.delete(testId);
      
      console.log(`Chaos test ${testId} stopped`);
      return true;
    }
    
    return false;
  }

  private injectLatency(config: ChaosTestConfig, testId: string) {
    // 模拟服务响应延迟
    console.log(`Injecting latency fault for ${config.targetService}`);
    
    // 实现延迟注入逻辑
    // 可以通过中间件或代理实现
  }

  private injectError(config: ChaosTestConfig, testId: string) {
    // 模拟服务错误
    console.log(`Injecting error fault for ${config.targetService}`);
    
    // 实现错误注入逻辑
  }

  private killService(config: ChaosTestConfig, testId: string) {
    // 模拟服务崩溃
    console.log(`Injecting service kill fault for ${config.targetService}`);
    
    // 实现服务终止逻辑
  }

  private injectNetworkFault(config: ChaosTestConfig, testId: string) {
    // 模拟网络故障
    console.log(`Injecting network fault for ${config.targetService}`);
    
    // 实现网络故障注入逻辑
  }

  private injectDiskFault(config: ChaosTestConfig, testId: string) {
    // 模拟磁盘故障
    console.log(`Injecting disk fault for ${config.targetService}`);
    
    // 实现磁盘故障注入逻辑
  }

  private generateTestId(): string {
    return `chaos-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  getRunningTests(): string[] {
    return Array.from(this.runningTests.keys());
  }
}
```

### 6.2 可用性指标计算

#### SLA监控
```typescript
// sla-monitor.service.ts
import { Injectable } from '@nestjs/common';

export interface SlaMetrics {
  availability: number; // 可用性百分比
  responseTimeP95: number; // 95%响应时间
  errorRate: number; // 错误率
  uptime: number; // 正常运行时间
  downtime: number; // 停机时间
}

@Injectable()
export class SlaMonitorService {
  private requestCounts: Map<string, number> = new Map();
  private errorCounts: Map<string, number> = new Map();
  private responseTimes: Map<string, number[]> = new Map();
  private startTime: Date = new Date();

  async updateMetrics(
    service: string, 
    responseTime: number, 
    isError: boolean
  ): Promise<void> {
    // 更新请求数
    const currentRequests = this.requestCounts.get(service) || 0;
    this.requestCounts.set(service, currentRequests + 1);
    
    // 更新错误数
    if (isError) {
      const currentErrors = this.errorCounts.get(service) || 0;
      this.errorCounts.set(service, currentErrors + 1);
    }
    
    // 更新响应时间
    const times = this.responseTimes.get(service) || [];
    times.push(responseTime);
    // 限制数组大小，避免内存溢出
    if (times.length > 10000) {
      times.shift();
    }
    this.responseTimes.set(service, times);
  }

  getSlaMetrics(service: string): SlaMetrics {
    const totalRequests = this.requestCounts.get(service) || 0;
    const errorRequests = this.errorCounts.get(service) || 0;
    const responseTimes = this.responseTimes.get(service) || [];
    
    const uptime = this.calculateUptime();
    const downtime = this.calculateDowntime();
    
    const availability = totalRequests > 0 
      ? ((totalRequests - errorRequests) / totalRequests) * 100 
      : 100;
    
    const errorRate = totalRequests > 0 
      ? (errorRequests / totalRequests) * 100 
      : 0;
    
    const responseTimeP95 = this.calculatePercentile(responseTimes, 0.95);
    
    return {
      availability: parseFloat(availability.toFixed(4)),
      responseTimeP95: parseFloat(responseTimeP95.toFixed(3)),
      errorRate: parseFloat(errorRate.toFixed(4)),
      uptime,
      downtime,
    };
  }

  private calculateUptime(): number {
    const now = new Date();
    return (now.getTime() - this.startTime.getTime()) / 1000;
  }

  private calculateDowntime(): number {
    // 这里应该从监控系统获取实际的停机时间
    // 简化实现，返回0
    return 0;
  }

  private calculatePercentile(arr: number[], percentile: number): number {
    if (arr.length === 0) return 0;
    
    const sorted = [...arr].sort((a, b) => a - b);
    const index = Math.ceil(percentile * sorted.length) - 1;
    return sorted[Math.max(0, Math.min(index, sorted.length - 1))];
  }

  async generateSlaReport(): Promise<any> {
    const services = Array.from(this.requestCounts.keys());
    const report: Record<string, SlaMetrics> = {};
    
    for (const service of services) {
      report[service] = this.getSlaMetrics(service);
    }
    
    return {
      timestamp: new Date(),
      report,
      summary: this.calculateOverallSla(report),
    };
  }

  private calculateOverallSla(report: Record<string, SlaMetrics>): any {
    const services = Object.values(report);
    
    if (services.length === 0) {
      return {
        overallAvailability: 100,
        overallErrorRate: 0,
        overallResponseTimeP95: 0,
      };
    }
    
    const totalAvailability = services.reduce((sum, service) => sum + service.availability, 0);
    const totalErrorRate = services.reduce((sum, service) => sum + service.errorRate, 0);
    const responseTimes = services.map(s => s.responseTimeP95).filter(t => t > 0);
    
    const avgResponseTime = responseTimes.length > 0 
      ? responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length
      : 0;
    
    return {
      overallAvailability: parseFloat((totalAvailability / services.length).toFixed(4)),
      overallErrorRate: parseFloat((totalErrorRate / services.length).toFixed(4)),
      overallResponseTimeP95: parseFloat(avgResponseTime.toFixed(3)),
    };
  }
}
```

## 7. 高可用性保障措施总结

通过上述全面的高可用性保障措施，智选电商平台能够：

1. **实现99.99%可用性** - 通过多区域部署、故障转移、熔断降级等措施
2. **快速故障恢复** - 通过自动化监控、告警和恢复机制
3. **业务连续性** - 通过数据备份、容灾演练确保业务不中断
4. **性能保障** - 通过限流、缓存、负载均衡确保响应时间

这套高可用性保障体系从架构设计、部署策略、监控告警、备份恢复、故障演练等多个维度确保了系统的高可用性，满足智选电商平台的业务需求。