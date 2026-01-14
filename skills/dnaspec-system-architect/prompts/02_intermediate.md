# 系统架构设计 - 中级场景

## 微服务架构

### 1. 何时拆分微服务？

**拆分信号**：
```yaml
单体应用瓶颈:
  - 部署时间长
  - 修改影响面大
  - 扩展困难
  - 技术栈固化

团队规模:
  - > 20人
  - 多团队协作
  - 独立发布需求

业务需求:
  - 不同模块性能要求不同
  - 需要不同技术栈
  - 高可用性要求
```

### 2. 微服务拆分策略

**按业务能力拆分**：
```yaml
电商系统微服务:
  用户服务 (User Service):
    - 用户注册、登录
    - 个人信息管理
    - 独立数据库

  商品服务 (Product Service):
    - 商品管理
    - 库存管理
    - 独立数据库

  订单服务 (Order Service):
    - 订单创建
    - 订单查询
    - 独立数据库

  支付服务 (Payment Service):
    - 支付处理
    - 退款处理
    - 独立数据库
```

**数据库拆分原则**：
```yaml
每个服务独立数据库:
  优势:
    - 独立部署
    - 技术选型灵活
    - 故障隔离

  挑战:
    - 分布式事务
    - 数据一致性
    - 跨服务查询

解决:
  - 最终一致性
  - 事件驱动
  - CQRS模式
```

### 3. 服务间通信

**同步通信**：
```python
# HTTP/REST
import httpx

async def get_user(user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://user-service/users/{user_id}")
        return response.json()
```

**异步通信**：
```python
# 消息队列
from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://localhost:5672")
app = FastStream(broker)

@broker.publisher("order.created")
async def order_created_event(order: Order):
    """发布订单创建事件"""
    await broker.publish(order, "order.created")

@broker.subscriber("order.created")
async def handle_order_created(order: Order):
    """处理订单创建事件"""
    # 更新库存
    await update_inventory(order.product_id, order.quantity)
```

**API网关**：
```yaml
网关职责:
  - 路由转发
  - 认证授权
  - 限流熔断
  - 日志监控

实现:
  - Kong
  - Nginx
  - Spring Cloud Gateway
```

---

## 分布式架构

### 1. 负载均衡

```yaml
负载均衡策略:
  轮询 (Round Robin):
    - 依次分配请求
    - 简单公平

  最少连接 (Least Connections):
    - 分配给连接数最少的服务器
    - 动态适应

  IP哈希 (IP Hash):
    - 根据客户端IP分配
    - 会话保持

实现:
  硬件: F5、A10
  软件: Nginx、HAProxy、LVS
```

### 2. 缓存架构

**多级缓存**：
```yaml
浏览器缓存:
  - 静态资源
  - HTTP缓存头

CDN缓存:
  - 全球分发
  - 高可用

应用缓存:
  - Redis / Memcached
  - 热点数据

数据库缓存:
  - 查询缓存
  - 索引缓存
```

**缓存策略**：
```python
# Cache-Aside模式
async def get_user(user_id: str):
    # 1. 先查缓存
    user = await redis.get(f"user:{user_id}")
    if user:
        return json.loads(user)

    # 2. 缓存未命中，查数据库
    user = await db.get_user(user_id)

    # 3. 写入缓存
    await redis.setex(f"user:{user_id}", 3600, json.dumps(user))

    return user
```

### 3. 分布式事务

**Saga模式**：
```python
# 订单Saga
class OrderSaga:
    async def create_order(self, order_data):
        # 步骤1: 创建订单
        order = await self.create_order_record(order_data)

        try:
            # 步骤2: 扣减库存
            await self.inventory_service.deduct(
                order.product_id, order.quantity
            )

            # 步骤3: 处理支付
            await self.payment_service.charge(
                order.user_id, order.amount
            )

            # 成功，完成订单
            await self.complete_order(order.id)

        except Exception as e:
            # 失败，执行补偿操作
            await self.compensate_order(order)
            raise e
```

**TCC模式**：
```yaml
Try阶段:
  - 检查资源
  - 预留资源

Confirm阶段:
  - 确认执行
  - 提交事务

Cancel阶段:
  - 取消执行
  - 释放资源
```

---

## 性能优化

### 1. 数据库优化

**索引优化**：
```sql
-- 创建索引
CREATE INDEX idx_user_email ON users(email);

-- 复合索引
CREATE INDEX idx_order_user_status ON orders(user_id, status);

-- 覆盖索引
CREATE INDEX idx_order_user_status_amount
ON orders(user_id, status) INCLUDE (amount);
```

**查询优化**：
```sql
-- 避免SELECT *
SELECT id, name, email FROM users WHERE id = 123;

-- 使用JOIN而非子查询
SELECT u.name, o.order_id
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- 分页查询
SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;
```

### 2. 应用优化

**异步处理**：
```python
import asyncio

async def process_order(order_id: str):
    # 并行执行多个任务
    tasks = [
        validate_order(order_id),
        check_inventory(order_id),
        calculate_price(order_id)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

**连接池**：
```python
from sqlalchemy.ext.asyncio import create_async_engine

# 连接池配置
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,        # 连接池大小
    max_overflow=10,     # 最大溢出
    pool_timeout=30,     # 连接超时
    pool_recycle=3600    # 连接回收时间
)
```

### 3. 架构优化

**读写分离**：
```yaml
主库 (Master):
  - 处理写操作
  - 数据同步到从库

从库 (Slave):
  - 处理读操作
  - 多个从库负载均衡

中间件:
  - ProxySQL
  - MaxScale
  - 自定义路由
```

**分库分表**：
```yaml
水平分片:
  - 按用户ID分片
  - 按时间分片
  - 按地理位置分片

垂直分片:
  - 按业务模块
  - 按数据访问频率
```

---

## 安全架构

### 1. 认证授权

**JWT认证**：
```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
```

**OAuth2.0**：
```yaml
授权流程:
  1. 用户登录
  2. 授权码获取
  3. Access Token获取
  4. 访问受保护资源

实现:
  - Auth0
  - Keycloak
  - 自建OAuth服务
```

### 2. 数据安全

**加密存储**：
```python
from cryptography.fernet import Fernet

# 加密
cipher = Fernet(ENCRYPTION_KEY)
encrypted = cipher.encrypt(plaintext.encode())

# 解密
decrypted = cipher.decrypt(encrypted).decode()
```

**传输加密**：
```yaml
HTTPS:
  - SSL/TLS证书
  - 强制HTTPS
  - HSTS头

API安全:
  - 请求签名
  - 时间戳验证
  - 防重放攻击
```

### 3. 防护措施

**限流**：
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.post("/api/users")
@limiter.limit("10/minute")  # 每分钟10次
async def create_user(request: Request):
    pass
```

**熔断降级**：
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_external_service():
    # 失败超过5次，熔断60秒
    response = await httpx.get("https://external-api")
    return response.json()
```

---

## 监控运维

### 1. 日志管理

```yaml
结构化日志:
  - JSON格式
  - 统一字段
  - 便于查询

日志级别:
  DEBUG: 调试信息
  INFO: 一般信息
  WARNING: 警告
  ERROR: 错误
  CRITICAL: 严重错误

日志聚合:
  - ELK Stack
  - Loki
  - CloudWatch
```

### 2. 指标监控

**关键指标**：
```yaml
业务指标:
  - QPS / TPS
  - 响应时间
  - 错误率

系统指标:
  - CPU使用率
  - 内存使用率
  - 磁盘I/O
  - 网络流量

自定义指标:
  - 业务成功率
  - 用户活跃度
  - 订单转化率
```

### 3. 链路追踪

```yaml
分布式追踪:
  OpenTelemetry:
    - 生成Trace ID
    - 记录Span
    - 上下文传播

后端存储:
  - Jaeger
  - Zipkin
  - Datadog

可视化:
  - 请求链路图
  - 性能分析
  - 瓶颈识别
```

---

*本层覆盖微服务架构、分布式架构、性能优化、安全架构和监控运维*
