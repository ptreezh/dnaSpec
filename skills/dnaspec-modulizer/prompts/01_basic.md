# 模块化设计 - 基本应用

## 常见模块划分方法

### 1. 按层次分层

**经典三层架构**：
```yaml
表现层 (Presentation):
  职责: 用户交互、数据展示
  模块: UI组件、路由、状态管理

业务层 (Business):
  职责: 业务逻辑、工作流
  模块: 用户服务、订单服务、支付服务

数据层 (Data):
  职责: 数据存储、访问
  模块: 数据库访问、缓存、文件存储
```

### 2. 按功能划分

**功能模块化**：
```yaml
用户模块:
  - 用户注册
  - 用户登录
  - 用户信息管理
  - 权限验证

订单模块:
  - 创建订单
  - 查询订单
  - 订单状态更新
  - 订单取消

支付模块:
  - 支付处理
  - 退款处理
  - 支付回调
```

### 3. 按技术组件

**技术模块化**：
```yaml
认证模块:
  - JWT令牌管理
  - OAuth集成
  - 会话管理

日志模块:
  - 日志记录
  - 日志聚合
  - 日志分析

缓存模块:
  - 缓存策略
  - 缓存失效
  - 缓存预热
```

---

## 模块化工作流程

### 步骤1: 识别功能

**输入**：需求文档或功能列表

**方法**：
- 列出所有功能点
- 按相关性分组
- 识别共享功能

### 步骤2: 设计模块边界

**原则**：
- 单一职责：一个模块做一件事
- 高内聚：相关功能放在一起
- 低耦合：最小化模块间依赖

**检查清单**：
- [ ] 模块职责明确吗？
- [ ] 模块内部功能相关吗？
- [ ] 模块间接口清晰吗？
- [ ] 可以独立测试吗？

### 步骤3: 定义接口

**接口设计**：
```python
# 清晰的模块接口
class UserService:
    def create_user(self, data: UserDTO) -> User:
        """创建用户"""

    def get_user(self, user_id: str) -> User:
        """获取用户"""

    def update_user(self, user_id: str, data: UserDTO) -> User:
        """更新用户"""
```

### 步骤4: 评估质量

**度量指标**：
- **内聚度**：模块内部功能的相关性 (0-1)
- **耦合度**：模块间的依赖程度 (0-1)
- **复杂度**：模块的复杂性 (0-1)

**目标**：高内聚 (>0.7) + 低耦合 (<0.3)

---

## 实际案例

### 案例: 电商系统模块化

**原始需求**：
```
系统需要支持用户注册登录、商品浏览、购物车、
下单支付、订单查询、物流跟踪、评价反馈
```

**模块划分**：
```yaml
用户模块 (User):
  - 注册登录
  - 个人信息

商品模块 (Product):
  - 商品浏览
  - 商品搜索
  - 商品详情

交易模块 (Transaction):
  - 购物车
  - 订单管理
  - 支付处理

物流模块 (Logistics):
  - 物流跟踪
  - 配送管理

评价模块 (Review):
  - 评价反馈
  - 评分统计
```

**模块依赖关系**：
```
Transaction → User (下单需要用户信息)
Transaction → Product (下单需要商品信息)
Transaction → Logistics (订单需要物流)
Review → Transaction (评价需要订单)
```

---

## 常见反模式

### ❌ 糟糕的模块化

```python
# God Object - 一个模块做所有事
class SystemManager:
    def handle_user(self): pass
    def handle_order(self): pass
    def handle_payment(self): pass
    def handle_logistics(self): pass
    # ... 100+ 个方法
```

### ✅ 好的模块化

```python
# 单一职责的模块
class UserService: pass
class OrderService: pass
class PaymentService: pass
class LogisticsService: pass
```

---

*本层覆盖常见的模块划分方法和基本工作流程*
