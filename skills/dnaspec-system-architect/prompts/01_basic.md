# 系统架构设计 - 基本应用

## 常见架构模式

### 1. 分层架构

**经典三层架构**：
```yaml
表现层 (Presentation):
  职责: 用户交互、数据展示
  技术: React/Vue/Angular
  接口: REST API / GraphQL

业务层 (Business):
  职责: 业务逻辑、工作流
  技术: Node.js/Python/Java
  模块: 用户服务、订单服务

数据层 (Data):
  职责: 数据存储、访问
  技术: PostgreSQL/MongoDB/Redis
  接口: ORM / SQL
```

**适用场景**：
- 中小型应用
- 团队规模 < 20人
- 业务需求清晰

### 2. MVC架构

**模型-视图-控制器**：
```yaml
Model (模型):
  - 数据结构
  - 业务逻辑
  - 数据访问

View (视图):
  - 用户界面
  - 数据展示
  - 用户输入

Controller (控制器):
  - 处理请求
  - 调用模型
  - 返回视图
```

**实现示例**：
```python
# Controller
class UserController:
    def create_user(self, request):
        # 1. 验证输入
        data = request.validate()

        # 2. 调用模型
        user = UserModel.create(data)

        # 3. 返回响应
        return View.render(user)
```

### 3. 前后端分离

**分离架构**：
```yaml
前端应用:
  - 独立部署
  - 单页应用 (SPA)
  - 通过API与后端通信

后端API:
  - RESTful API
  - 认证授权
  - 业务逻辑

优势:
  - 前后端独立开发
  - 技术栈灵活
  - 便于扩展
```

---

## 技术栈选择

### 1. 后端技术栈

**按语言分类**：

**Python栈**：
```yaml
框架: Django / FastAPI / Flask
数据库: PostgreSQL / MongoDB
缓存: Redis / Memcached
消息队列: Celery / RabbitMQ
适用: 数据分析、AI、快速开发
```

**Node.js栈**：
```yaml
框架: Express / NestJS / Koa
数据库: PostgreSQL / MongoDB
缓存: Redis
实时: WebSocket / Socket.io
适用: 高并发、实时应用
```

**Java栈**：
```yaml
框架: Spring Boot / Spring Cloud
数据库: PostgreSQL / MySQL
缓存: Redis
消息: Kafka / RabbitMQ
适用: 企业级、高可靠
```

**Go栈**：
```yaml
框架: Gin / Echo / Beego
数据库: PostgreSQL / MySQL
缓存: Redis
适用: 高性能、微服务
```

### 2. 前端技术栈

**主流框架**：
```yaml
React:
  生态: 最丰富
  学习: 中等
  适用: 大型应用

Vue:
  生态: 完善
  学习: 简单
  适用: 快速开发

Angular:
  生态: 完整
  学习: 复杂
  适用: 企业级应用
```

### 3. 数据库选择

**关系型数据库**：
```yaml
PostgreSQL:
  特点: 功能强大、开源
  适用: 复杂查询、事务

MySQL:
  特点: 流行、稳定
  适用: Web应用
```

**NoSQL数据库**：
```yaml
MongoDB:
  特点: 文档型、灵活
  适用: 快速迭代、非结构化数据

Redis:
  特点: 键值存储、高性能
  适用: 缓存、会话
```

---

## 模块划分方法

### 1. 按功能划分

```yaml
电商系统功能模块:
  用户模块: 注册、登录、个人中心
  商品模块: 商品列表、详情、搜索
  订单模块: 下单、支付、查询
  物流模块: 配送、跟踪
  评价模块: 评价、反馈
```

### 2. 按层次划分

```yaml
技术层次模块:
  API层: 接口定义、路由
  服务层: 业务逻辑
  数据层: 数据访问
  工具层: 通用工具
```

### 3. 按领域划分

```yaml
DDD领域模块:
  用户领域: 用户、权限、角色
  订单领域: 订单、支付、物流
  商品领域: 商品、库存、分类
```

---

## 接口设计

### 1. RESTful API设计

**资源命名**：
```yaml
# 好的设计
GET /users          # 获取用户列表
GET /users/123      # 获取特定用户
POST /users         # 创建用户
PUT /users/123      # 更新用户
DELETE /users/123   # 删除用户

# 不好的设计
GET /getUsers
POST /createUser
GET /user?id=123
```

**响应格式**：
```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "张三"
  },
  "message": "操作成功"
}
```

### 2. 数据验证

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

    class Config:
        schema_extra = {
            "example": {
                "name": "张三",
                "email": "zhangsan@example.com",
                "age": 25
            }
        }
```

---

## 实际案例

### 案例: 中型Web应用架构

```yaml
技术栈:
  前端: React + TypeScript
  后端: Node.js + NestJS
  数据库: PostgreSQL
  缓存: Redis

架构:
  ┌─────────────┐
  │   Nginx     │  反向代理
  └─────────────┘
       ↓
  ┌─────────────┐
  │  React App  │  前端应用
  └─────────────┘
       ↓
  ┌─────────────┐
  │   NestJS    │  后端API
  └─────────────┘
       ↓
  ┌─────────────┬─────────────┐
  │ PostgreSQL  │   Redis     │  数据存储
  └─────────────┴─────────────┘
```

**模块划分**：
```yaml
用户模块:
  - 用户注册、登录
  - 个人信息管理
  - 权限控制

内容模块:
  - 内容发布
  - 内容管理
  - 评论系统

通知模块:
  - 邮件通知
  - 站内消息
  - 推送通知
```

---

*本层覆盖常见架构模式、技术栈选择、模块划分和接口设计*
