# 模块化设计 - 中级场景

## 模块依赖管理

### 依赖关系类型

**层次依赖**：
```yaml
单向依赖 (推荐):
  表现层 → 业务层 → 数据层层 → 业务层 → 数据层
  低层模块不应该知道高层模块的存在
```

**共享依赖**：
```yaml
交叉依赖 (避免):
  A → B
  B → A
  解决方案: 提取公共接口C

正确方式:
  A → C ← B
```

### 依赖注入

**控制反转 (IoC)**：
```python
# 硬编码依赖 (不好)
class OrderService:
    def __init__(self):
        self.payment = PaymentService()  # 紧耦合

# 依赖注入 (好)
class OrderService:
    def __init__(self, payment: PaymentService):
        self.payment = payment  # 松耦合，可替换
```

**依赖倒置原则 (DIP)**：
```python
# 依赖抽象而非实现
class OrderService:
    def __init__(self, payment: IPaymentService):  # 接口
        self.payment = payment
```

---

## 模块通信模式

### 1. 同步通信

**直接调用**：
```python
# 简单直接
class OrderService:
    def create_order(self, user_id, product_id):
        user = self.user_service.get_user(user_id)
        product = self.product_service.get_product(product_id)
        # 处理订单...
```

**问题**：
- 紧耦合
- 难以扩展
- 性能瓶颈

### 2. 异步通信

**事件驱动**：
```python
# 发布-订阅模式
class OrderService:
    def create_order(self, user_id, product_id):
        order = self._create_order(user_id, product_id)
        # 发布事件，不关心谁处理
        event_bus.publish(OrderCreatedEvent(order))

class EmailService:
    @subscribe(OrderCreatedEvent)
    def send_confirmation(self, event):
        # 发送确认邮件
        pass

class InventoryService:
    @subscribe(OrderCreatedEvent)
    def update_inventory(self, event):
        # 更新库存
        pass
```

**优势**：
- 松耦合
- 易扩展
- 提高性能

### 3. 消息队列

**异步解耦**：
```yaml
场景: 订单创建后的后续处理

订单服务 → 消息队列 → [邮件服务, 库存服务, 物流服务]

优势:
  - 可靠性保证
  - 流量削峰
  - 异步处理
```

---

## 模块重构策略

### 识别"坏味道"

**信号模块**：
```python
# 症状: 一个模块被频繁修改
# 原因: 职责过多
# 解决: 拆分为多个模块
```

**特性蔓延**：
```python
# 症状: 模块逐渐增加不相关的功能
# 原因: 缺乏边界
# 解决: 提取新模块
```

**循环依赖**：
```python
# 症状: A依赖B，B依赖A
# 原因: 职责不清
# 解决: 提取公共模块或接口
```

### 重构步骤

**步骤1: 识别边界**
- 分析现有代码
- 识别职责
- 找出耦合点

**步骤2: 设计新结构**
- 定义新模块
- 设计接口
- 规划依赖关系

**步骤3: 渐进式迁移**
```python
# 旧代码
class OldService:
    def method(self):
        # 旧逻辑

# 新代码
class NewService:
    def method(self):
        # 新逻辑

# 适配器（过渡期）
class AdapterService:
    def __init__(self):
        self.old = OldService()
        self.new = NewService()

    def method(self):
        # 逐步切换到新逻辑
        if self.use_new:
            return self.new.method()
        else:
            return self.old.method()
```

**步骤4: 验证和优化**
- 单元测试
- 集成测试
- 性能测试
- 持续监控

---

## 模块测试策略

### 单元测试

**隔离测试**：
```python
def test_order_service():
    # 使用Mock对象隔离依赖
    mock_payment = Mock(spec=IPaymentService)
    mock_user = Mock(spec=UserService)

    service = OrderService(mock_payment, mock_user)

    # 测试订单逻辑
    order = service.create_order("user123", "product456")

    assert order.user_id == "user123"
    mock_payment.charge.assert_called_once()
```

### 集成测试

**模块间协作**：
```python
def test_order_to_payment_integration():
    # 真实场景测试
    order_service = OrderService(payment_service, user_service)

    # 测试完整流程
    result = order_service.create_order("user123", "product456")

    # 验证结果
    assert result.status == "paid"
    assert payment_service.was_called()
```

---

## 微服务模块化

### 什么时候拆分微服务？

**拆分信号**：
- 单体应用难以部署
- 不同模块需要不同技术栈
- 团队规模扩大
- 性能瓶颈

**拆分原则**：
```yaml
业务边界:
  - 按业务领域拆分 (DDD)
  - 每个服务对应一个业务能力

数据独立:
  - 每个服务有自己的数据库
  - 避免跨服务join

部署独立:
  - 独立部署、独立扩展
  - 故障隔离
```

**拆分示例**：
```yaml
单体应用:
  - 用户模块
  - 订单模块
  - 支付模块
  - 物流模块

微服务拆分:
  - 用户服务 (独立部署、独立数据库)
  - 订单服务 (独立部署、独立数据库)
  - 支付服务 (独立部署、独立数据库)
  - 物流服务 (独立部署、独立数据库)
```

---

*本层覆盖模块依赖管理、通信模式、重构策略和微服务拆分*
