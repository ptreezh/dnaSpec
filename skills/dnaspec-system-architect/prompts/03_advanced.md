# 系统架构设计 - 高级应用

## 企业级架构治理

### 架构决策记录 (ADR)

**什么是ADR**：
```yaml
ADR (Architecture Decision Record):
  - 记录重要的架构决策
  - 说明决策原因
  - 记录决策背景
  - 跟踪决策状态

格式:
  - 标题
  - 状态（提议/接受/废弃）
  - 背景
  - 决策
  - 后果
```

**示例ADR**：
```markdown
# ADR-001: 选择PostgreSQL作为主数据库

## 状态
已接受

## 背景
我们需要一个关系型数据库来存储核心业务数据。
候选方案：MySQL、PostgreSQL、MongoDB

## 决策
选择PostgreSQL作为主数据库。

## 原因
1. 支持复杂查询和JSON类型
2. ACID事务保证
3. 开源且社区活跃
4. 团队有相关经验

## 后果
正面：
- 数据一致性有保障
- 查询功能强大

负面：
- 学习成本
- 需要DBA支持
```

### 架构审查机制

**定期架构审查**：
```yaml
审查周期:
  - 季度审查
  - 重大变更审查

审查内容:
  - 架构符合度
  - 技术债务
  - 性能指标
  - 安全风险

审查产出:
  - 架构健康报告
  - 改进建议
  - 行动计划
```

---

## 领域驱动设计 (DDD)

### 战略设计

**领域建模**：
```yaml
核心域 (Core Domain):
  - 业务核心竞争力
  - 最大投入
  - 例: 订单系统、支付系统

支撑域 (Supporting Domain):
  - 支持核心业务
  - 适度投入
  - 例: 用户管理、库存管理

通用域 (Generic Domain):
  - 通用功能
  - 可用现成方案
  - 例: 日志、监控
```

**限界上下文**：
```yaml
电商系统限界上下文:

  用户上下文:
    - 用户注册、登录
    - 用户信息管理
    - 权限管理
    - 概念: User、Role、Permission

  订单上下文:
    - 订单创建、支付
    - 订单状态流转
    - 订单查询
    - 概念: Order、OrderItem、Payment

上下文映射:
  - 共享内核 (Shared Kernel)
  - 客户方供应 (OHS)
  - 防腐层 (ACL)
  - 合作关系 (PC)
```

### 战术设计

**聚合根**：
```python
# Order是聚合根
class Order:
    def __init__(self, order_id: str, user_id: str):
        self.order_id = order_id
        self.user_id = user_id
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING

    def add_item(self, product_id: str, quantity: int, price: Decimal):
        """通过聚合根操作，保证一致性"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("只能修改待处理订单")

        # 检查是否已存在
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                return

        # 添加新项
        self.items.append(OrderItem(product_id, quantity, price))

    def calculate_total(self) -> Decimal:
        """计算总金额"""
        return sum(item.subtotal() for item in self.items)

    def confirm(self):
        """确认订单"""
        if len(self.items) == 0:
            raise ValueError("订单为空")
        self.status = OrderStatus.CONFIRMED
```

**值对象**：
```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    """金额值对象 - 不可变"""
    amount: Decimal
    currency: str = "CNY"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("金额不能为负数")

    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("货币类型不同")
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> 'Money':
        return Money(self.amount * factor, self.currency)

@dataclass(frozen=True)
class Email:
    """邮箱值对象"""
    value: str

    def __post_init__(self):
        if not self._is_valid():
            raise ValueError("邮箱格式无效")

    def _is_valid(self) -> bool:
        import re
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.value))
```

**领域服务**：
```python
class PaymentDomainService:
    """支付领域服务 - 不属于任何实体"""

    def process_payment(
        self,
        order: Order,
        payment_method: PaymentMethod
    ) -> PaymentResult:
        """处理支付 - 复杂的领域逻辑"""

        # 1. 验证订单状态
        if order.status != OrderStatus.CONFIRMED:
            raise PaymentError("订单状态错误")

        # 2. 计算手续费
        fee = self._calculate_fee(order.calculate_total(), payment_method)

        # 3. 调用支付网关
        result = self.payment_gateway.charge(
            order.calculate_total() + fee,
            payment_method
        )

        # 4. 返回结果
        return PaymentResult(
            transaction_id=result.transaction_id,
            amount=result.amount,
            status=result.status
        )
```

---

## 事件驱动架构

### 事件风暴

**领域事件**：
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any
import json

@dataclass
class DomainEvent:
    """领域事件基类"""
    event_id: str
    aggregate_id: str
    aggregate_type: str
    event_type: str
    occurred_at: datetime
    payload: dict

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "payload": self.payload
        }

# 具体事件
class OrderCreatedEvent(DomainEvent):
    def __init__(self, order_id: str, user_id: str, items: list):
        super().__init__(
            event_id=str(uuid.uuid4()),
            aggregate_id=order_id,
            aggregate_type="Order",
            event_type="OrderCreated",
            occurred_at=datetime.utcnow(),
            payload={
                "user_id": user_id,
                "items": items
            }
        )

class OrderPaidEvent(DomainEvent):
    def __init__(self, order_id: str, payment_id: str):
        super().__init__(
            event_id=str(uuid.uuid4()),
            aggregate_id=order_id,
            aggregate_type="Order",
            event_type="OrderPaid",
            occurred_at=datetime.utcnow(),
            payload={
                "payment_id": payment_id
            }
        )
```

**事件存储**：
```python
class EventStore:
    """事件存储"""

    async def append_event(self, event: DomainEvent):
        """追加事件"""
        await self.db.execute(
            """INSERT INTO event_store
               (event_id, aggregate_id, aggregate_type,
                event_type, occurred_at, payload)
               VALUES ($1, $2, $3, $4, $5, $6)""",
            event.event_id, event.aggregate_id, event.aggregate_type,
            event.event_type, event.occurred_at, json.dumps(event.payload)
        )

    async def get_events(
        self,
        aggregate_id: str
    ) -> List[DomainEvent]:
        """获取聚合的所有事件"""
        rows = await self.db.fetch(
            "SELECT * FROM event_store WHERE aggregate_id = $1 ORDER BY occurred_at",
            aggregate_id
        )
        return [self._deserialize(row) for row in rows]
```

### CQRS模式

**命令查询职责分离**：
```python
# 写模型（Command）
class OrderCommandHandler:
    async def create_order(self, command: CreateOrderCommand):
        """创建订单命令"""
        order = Order.create(command.user_id, command.items)

        # 保存到写库
        await self.write_db.save(order)

        # 发布事件
        await self.event_publisher.publish(
            OrderCreatedEvent(order.id, order.user_id, order.items)
        )

# 读模型（Query）
class OrderQueryHandler:
    async def get_order(self, query: GetOrderQuery) -> OrderView:
        """查询订单 - 从读库"""
        return await self.read_db.find_one(
            "order_views",
            {"order_id": query.order_id}
        )

    async def list_user_orders(self, query: ListUserOrdersQuery) -> List[OrderView]:
        """查询用户订单列表"""
        return await self.read_db.find(
            "order_views",
            {"user_id": query.user_id},
            sort=[("created_at", -1)]
        )

# 事件处理器 - 更新读模型
class OrderProjector:
    @subscribe(OrderCreatedEvent)
    async def on_order_created(self, event: OrderCreatedEvent):
        """订单创建后，更新读模型"""
        order_view = OrderView(
            order_id=event.aggregate_id,
            user_id=event.payload["user_id"],
            items=event.payload["items"],
            status="pending",
            created_at=event.occurred_at
        )
        await self.read_db.insert("order_views", order_view)
```

---

## 云原生架构

### 容器化

**Docker化**：
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Kubernetes部署**：
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: order-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 服务网格

**Istio配置**：
```yaml
# 虚拟服务
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: order-service
        subset: v2
      weight: 100
  - route:
    - destination:
        host: order-service
        subset: v1
      weight: 90
    - destination:
        host: order-service
        subset: v2
      weight: 10
```

### 无服务器架构

**Serverless函数**：
```python
# AWS Lambda
import json
import boto3

def lambda_handler(event, context):
    """处理订单创建事件"""

    # 解析事件
    order_data = json.loads(event['body'])

    # 处理业务逻辑
    order = create_order(order_data)

    # 返回响应
    return {
        'statusCode': 200,
        'body': json.dumps({
            'order_id': order.id,
            'status': order.status
        })
    }
```

---

## 前沿技术趋势

### AI驱动的架构设计

**AI辅助架构决策**：
```yaml
AI分析:
  输入:
    - 业务需求文档
    - 性能要求
    - 团队技能
    - 预算约束

AI输出:
  - 推荐技术栈
  - 架构模式选择
  - 风险评估
  - 成本估算

人工审核:
  - 验证推荐合理性
  - 调整细节
  - 最终决策
```

### 边缘计算架构

```yaml
边缘计算场景:
  物联网:
    - 数据本地处理
    - 减少云端传输
    - 实时响应

  内容分发:
    - 就近处理
    - 降低延迟
    - 节省带宽

架构:
  - 边缘节点
  - 边缘集群
  - 云边协同
```

### Web3架构

```yaml
区块链集成:
  智能合约:
    - 业务逻辑上链
    - 不可篡改

  去中心化存储:
    - IPFS
    - Filecoin

  去中心化身份:
    - DID
    - NFT身份
```

---

## 总结

**企业级架构设计的关键**：
1. 架构治理（ADR、架构审查）
2. DDD指导（领域建模、限界上下文）
3. 事件驱动（事件风暴、CQRS）
4. 云原生（容器化、服务网格、无服务器）
5. 持续创新（AI辅助、边缘计算、Web3）

**目标**：构建灵活、可靠、可演化的企业级技术架构。

---

*本层覆盖企业级架构治理、DDD、事件驱动架构、云原生和前沿趋势*
