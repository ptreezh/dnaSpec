# DNASPEC智能契约管理系统 - Claude Skills风格设计规范

## 设计哲学

基于Claude Code Skills的设计理念，结合Context Engineering框架的生物学有机体架构原则，构建模块化、可组合的智能体技能系统。

## 核心设计原则

### 1. 生物学隐喻架构
```
atoms → molecules → cells → organs → neural systems → neural fields
  │        │         │        │             │              │
基础命令   参数组合   状态管理  多步流程    认知工具      语义场持续性
```

### 2. 技能组织结构
每个技能遵循标准化的Markdown格式，包含以下核心部分：

```markdown
# /技能名称 - 技能描述

## 目的
技能的核心功能和应用场景

## 使用示例
具体的命令使用方式和参数示例

## 工作流程
- **阶段1**: 描述第一个处理阶段
- **阶段2**: 描述第二个处理阶段
- **阶段3**: 描述第三个处理阶段

## 核心能力
技能具备的关键能力列表

## 工具集成
需要调用的外部工具和内部功能
```

## 技能分类体系

### 基础分析技能 (Atoms - Molecules)
处理单个文件或简单任务的原子级技能

#### 1. `/analyze.python` - Python源码分析技能
**目的**: 分析Python源码文件，提取API端点、装饰器和类型信息

**使用示例**: 
```
/analyze.python source=@app/api/routes.py extract=decorators,types
```

**工作流程**:
- **源码解析**: 使用AST解析Python源码结构
- **装饰器提取**: 识别并提取路由装饰器信息
- **类型分析**: 解析函数签名和类型注解
- **结果输出**: 生成结构化分析报告

**核心能力**:
- Python AST解析
- 装饰器识别 (`@app.route`, `@api.doc`)
- 类型注解处理
- 函数签名分析

#### 2. `/analyze.js` - JavaScript源码分析技能
**目的**: 分析JavaScript/TypeScript源码，提取API路由和JSDoc信息

**使用示例**:
```
/analyze.js source=@src/routes/api.js extract=routes,jsdoc
```

**工作流程**:
- **语法解析**: 解析JS/TS源码结构
- **路由识别**: 提取Express路由定义
- **注释解析**: 解析JSDoc注释信息
- **接口提取**: 提取TypeScript接口定义

**核心能力**:
- JavaScript语法解析
- Express路由识别
- JSDoc注释解析
- TypeScript接口提取

### 组合技能 (Cells - Organs)
处理复杂任务，组合多个基础技能的多步流程技能

#### 3. `/contract.generate` - 契约生成技能
**目的**: 从源码分析结果生成OpenAPI契约

**使用示例**:
```
/contract.generate analysis=@analysis.json format=openapi3 output=spec.yaml
```

**工作流程**:
- **数据加载**: 加载源码分析结果
- **模型构建**: 构建数据模型和API路径
- **契约组装**: 组装OpenAPI契约文档
- **验证输出**: 验证生成契约的完整性

**核心能力**:
- OpenAPI 3.0规范生成
- 数据模型构建
- API路径定义
- 示例数据生成

#### 4. `/contract.validate` - 契约验证技能
**目的**: 验证契约的结构、类型和兼容性

**使用示例**:
```
/contract.validate spec=@api.yaml check=structure,types,compatibility
```

**工作流程**:
- **契约加载**: 加载待验证的契约文件
- **结构验证**: 检查契约结构完整性
- **类型验证**: 验证数据类型一致性
- **兼容性检查**: 评估版本兼容性
- **报告生成**: 生成验证结果报告

**核心能力**:
- OpenAPI结构验证
- 数据类型检查
- 版本兼容性评估
- 错误检测和报告

### 认知工具技能 (Neural Systems)
提供高级推理和分析能力的复杂技能

#### 5. `/analyze.compatibility` - 兼容性分析技能
**目的**: 分析不同版本契约间的兼容性变更

**使用示例**:
```
/analyze.compatibility old=@v1.0.yaml new=@v2.0.yaml report=detailed
```

**工作流程**:
- **版本加载**: 加载两个版本的契约文件
- **差异分析**: 识别API路径和模型变更
- **影响评估**: 评估变更对兼容性的影响
- **风险识别**: 识别破坏性变更风险
- **建议生成**: 提供版本迁移建议

**核心能力**:
- 版本差异分析
- 破坏性变更检测
- 兼容性风险评估
- 迁移策略建议

#### 6. `/optimize.contract` - 契约优化技能
**目的**: 优化契约结构和性能

**使用示例**:
```
/optimize.contract spec=@api.yaml strategy=minimize,standardize
```

**工作流程**:
- **性能分析**: 分析契约文件大小和复杂度
- **冗余识别**: 识别重复和冗余定义
- **结构优化**: 优化数据模型结构
- **标准统一**: 统一命名和格式规范
- **输出生成**: 生成优化后的契约

**核心能力**:
- 契约性能分析
- 冗余代码识别
- 数据模型优化
- 标准化处理

### 场景化应用技能 (Neural Fields)
针对特定应用场景的完整解决方案技能

#### 7. `/project.setup` - 项目初始化技能
**目的**: 初始化DNASPEC智能契约管理项目

**使用示例**:
```
/project.setup name=my-api-project type=python,js workspace=./contracts
```

**工作流程**:
- **目录创建**: 创建项目工作区结构
- **配置生成**: 生成项目配置文件
- **模板部署**: 部署基础模板文件
- **工具安装**: 安装必要的依赖工具
- **文档生成**: 生成项目使用文档

**核心能力**:
- 项目结构初始化
- 配置文件生成
- 模板系统部署
- 依赖管理

#### 8. `/release.prepare` - 版本发布准备技能
**目的**: 准备契约版本发布所需的所有文件

**使用示例**:
```
/release.prepare version=2.1.0 spec=@api.yaml docs=true changelog=auto
```

**工作流程**:
- **版本验证**: 验证新版本号的正确性
- **契约打包**: 打包契约文件和相关资源
- **文档生成**: 生成版本文档和示例
- **变更记录**: 自动生成变更日志
- **发布准备**: 准备发布所需的所有文件

**核心能力**:
- 版本管理
- 文件打包
- 文档自动生成
- 变更日志管理

## 技能交互机制

### 1. 参数传递
技能间通过参数传递数据，支持文件引用和直接值传递：

```bash
# 文件引用
/analyze.python source=@app/api.py

# 直接值传递
/contract.generate title="My API" version="1.0.0"

# 组合使用
/analyze.python source=@api.py | /contract.generate input=- format=openapi3
```

### 2. 工作区隔离
每个技能在独立的工作目录中运行，通过文件系统进行数据交换：

```
/workspace/
├── /analyze-python-workspace/
│   ├── /input/
│   ├── /output/
│   └── /logs/
├── /contract-generate-workspace/
│   ├── /input/
│   ├── /output/
│   └── /logs/
└── /delivery-registry/
    ├── /analysis-results/
    └── /contract-files/
```

### 3. 递归改进
技能支持自我优化和迭代改进：

```python
def skill_improvement_cycle(context, state=None, depth=0, max_depth=3):
    # 执行技能核心功能
    result = execute_skill(context, state)
    
    # 检查是否需要改进
    if depth < max_depth and needs_improvement(result):
        # 获取改进建议
        improved_context = get_improvement_suggestions(context, result)
        # 递归执行改进
        return skill_improvement_cycle(improved_context, state, depth + 1, max_depth)
    
    return result
```

## 技能开发规范

### 1. 文件命名规范
- 基础技能: `动词.名词.md` (如: `analyze.python.md`)
- 组合技能: `功能.操作.md` (如: `contract.generate.md`)
- 场景技能: `场景.动作.md` (如: `project.setup.md`)

### 2. 参数设计原则
- **必需参数**: 使用`<参数名>`格式
- **可选参数**: 使用`[参数名=默认值]`格式
- **文件参数**: 使用`@文件路径`格式
- **布尔参数**: 使用`true/false`值

### 3. 错误处理机制
每个技能都需要包含错误处理和恢复机制：

```markdown
## 错误处理
- **源码解析错误**: 返回详细的错误位置和原因
- **文件不存在**: 提供文件查找建议
- **格式不支持**: 列出支持的格式类型
- **权限不足**: 指导用户如何解决权限问题

## 恢复建议
针对每种错误类型提供具体的恢复步骤
```

### 4. 性能优化要求
- 单个技能执行时间 < 5秒
- 内存使用 < 256MB
- 支持并发执行
- 提供进度反馈

## 质量保证标准

### 功能完整性
- [ ] 技能描述准确完整
- [ ] 使用示例真实有效
- [ ] 工作流程清晰可执行
- [ ] 错误处理机制完善

### 性能要求
- [ ] 执行时间符合预期
- [ ] 资源使用在合理范围内
- [ ] 支持大文件处理
- [ ] 提供性能监控

### 用户体验
- [ ] 命令语法简单直观
- [ ] 参数说明清晰明确
- [ ] 错误信息友好详细
- [ ] 帮助文档完整

### 安全性
- [ ] 文件访问权限控制
- [ ] 敏感信息处理安全
- [ ] 输入数据验证完整
- [ ] 操作日志记录完整

---

*本设计规范基于Claude Code Skills的交互模式和Context Engineering的理论框架，为DNASPEC智能契约管理系统提供标准化的技能开发指南。*