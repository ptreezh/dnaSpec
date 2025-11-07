# DSGS智能契约管理系统 - 核心技能定义

## 系统概述

基于Claude Skills设计哲学和Context Engineering生物学有机体架构，定义DSGS智能契约管理系统的核心技能集合。每个技能都是独立的、可组合的模块，通过CLI接口协同工作。

## 核心技能分类

### 1. 源码分析技能族

#### `/analyze.python` - Python源码分析技能
**目的**: 分析Python源码文件，提取API端点、装饰器和类型信息

**使用示例**: 
```
/analyze.python source=@app/api/routes.py extract=decorators,types,output=analysis.json
```

**工作流程**:
- **context_mapping**: 解析输入参数和源码文件路径
- **source_parsing**: 使用AST解析Python源码结构
- **decorator_extraction**: 识别并提取Flask/FastAPI装饰器信息
- **type_analysis**: 解析函数签名、参数类型和返回类型
- **result_output**: 生成结构化JSON分析报告

**核心能力**:
- Python AST语法树解析
- 路由装饰器识别 (`@app.route`, `@api.get`, `@router.post`)
- 类型注解处理 (PEP 484, Pydantic模型)
- 函数签名和文档字符串解析
- 异常处理和错误定位

**工具集成**:
- `python_ast_parser`: Python源码解析工具
- `decorator_extractor`: 装饰器提取工具
- `type_analyzer`: 类型分析工具
- `json_generator`: JSON结果生成工具

#### `/analyze.js` - JavaScript源码分析技能
**目的**: 分析JavaScript/TypeScript源码，提取API路由和JSDoc信息

**使用示例**:
```
/analyze.js source=@src/routes/api.js extract=routes,jsdoc,output=analysis.json
```

**工作流程**:
- **syntax_parsing**: 解析JS/TS源码语法结构
- **route_identification**: 提取Express/Koa路由定义
- **jsdoc_parsing**: 解析JSDoc注释和类型信息
- **interface_extraction**: 提取TypeScript接口和类型定义
- **output_generation**: 生成结构化分析结果

**核心能力**:
- JavaScript/TypeScript语法解析
- Express/Koa路由识别 (`app.get`, `router.post`)
- JSDoc注释解析和参数提取
- TypeScript接口和类型定义提取
- 异步函数和Promise处理分析

**工具集成**:
- `js_parser`: JavaScript语法解析工具
- `route_extractor`: 路由提取工具
- `jsdoc_processor`: JSDoc处理工具
- `ts_interface_parser`: TypeScript接口解析工具

### 2. 契约生成技能族

#### `/contract.generate` - 契约生成技能
**目的**: 从源码分析结果生成OpenAPI 3.0契约

**使用示例**:
```
/contract.generate analysis=@analysis.json format=openapi3,title="My API",version=1.0.0,output=spec.yaml
```

**工作流程**:
- **data_loading**: 加载源码分析结果数据
- **model_building**: 构建数据模型和API路径定义
- **contract_assembly**: 组装完整的OpenAPI契约文档
- **example_generation**: 自动生成请求/响应示例
- **validation_output**: 验证并输出生成的契约

**核心能力**:
- OpenAPI 3.0规范契约生成
- 数据模型自动构建和优化
- API路径和操作定义生成
- 请求/响应示例自动生成
- 错误响应格式标准化

**工具集成**:
- `openapi_builder`: OpenAPI契约构建工具
- `model_generator`: 数据模型生成工具
- `example_creator`: 示例数据创建工具
- `validator`: 契约验证工具

#### `/contract.enhance` - 契约增强技能
**目的**: 增强现有契约，添加详细描述和示例

**使用示例**:
```
/contract.enhance spec=@basic.yaml enhance=descriptions,examples,security,output=enhanced.yaml
```

**工作流程**:
- **spec_loading**: 加载现有契约文件
- **description_enhancement**: 为API端点添加详细描述
- **example_generation**: 生成更丰富的示例数据
- **security_definition**: 添加安全方案定义
- **output_creation**: 生成增强后的契约文件

**核心能力**:
- API描述自动生成和优化
- 多样化示例数据生成
- 安全方案定义和集成
- 契约文档质量提升
- 多语言支持

**工具集成**:
- `description_enhancer`: 描述增强工具
- `example_generator`: 示例生成工具
- `security_adder`: 安全定义添加工具
- `quality_checker`: 质量检查工具

### 3. 契约验证技能族

#### `/contract.validate` - 契约验证技能
**目的**: 验证契约的结构、类型和兼容性

**使用示例**:
```
/contract.validate spec=@api.yaml check=structure,types,compatibility,report=detailed,output=validation.json
```

**工作流程**:
- **contract_loading**: 加载待验证的契约文件
- **structure_validation**: 检查契约结构完整性
- **type_validation**: 验证数据类型一致性
- **compatibility_check**: 评估版本兼容性
- **report_generation**: 生成详细的验证报告

**核心能力**:
- OpenAPI结构完整性验证
- 数据类型和格式验证
- 版本兼容性评估
- 错误定位和修复建议
- 验证报告生成

**工具集成**:
- `structure_validator`: 结构验证工具
- `type_checker`: 类型检查工具
- `compatibility_analyzer`: 兼容性分析工具
- `report_generator`: 报告生成工具

#### `/contract.compare` - 契约对比技能
**目的**: 比较两个版本契约的差异

**使用示例**:
```
/contract.compare old=@v1.0.yaml new=@v2.0.yaml output=diff.json format=json
```

**工作流程**:
- **version_loading**: 加载两个版本的契约文件
- **diff_analysis**: 分析API路径和模型变更
- **impact_assessment**: 评估变更对兼容性的影响
- **breaking_changes`: 识别破坏性变更
- **report_output**: 生成差异分析报告

**核心能力**:
- 精确的契约差异分析
- 破坏性变更检测
- 兼容性影响评估
- 变更统计和分类
- 差异报告生成

**工具集成**:
- `diff_analyzer`: 差异分析工具
- `breaking_change_detector`: 破坏性变更检测工具
- `impact_assessor`: 影响评估工具
- `comparison_reporter`: 对比报告工具

### 4. 版本管理技能族

#### `/contract.version` - 版本管理技能
**目的**: 管理契约版本和变更历史

**使用示例**:
```
/contract.version create --from=@current.yaml --bump=minor --changelog=auto,output=version.json
```

**工作流程**:
- **version_analysis**: 分析当前契约版本信息
- **bump_calculation**: 计算新版本号(语义化版本)
- **changelog_generation`: 自动生成变更日志
- **version_creation`: 创建新版本记录
- **registry_update`: 更新版本注册表

**核心能力**:
- 语义化版本管理 (SemVer)
- 自动变更日志生成
- 版本历史追踪
- 版本回滚支持
- 多版本并行管理

**工具集成**:
- `version_manager`: 版本管理工具
- `changelog_generator`: 变更日志生成工具
- `history_tracker`: 历史追踪工具
- `registry_updater`: 注册表更新工具

#### `/contract.release` - 版本发布技能
**目的**: 准备和执行契约版本发布

**使用示例**:
```
/contract.release version=2.1.0 spec=@api.yaml docs=true,changelog=@changelog.md,output=release.zip
```

**工作流程**:
- **release_preparation**: 准备发布所需文件
- **documentation_generation`: 生成发布文档
- **package_creation`: 创建发布包
- **validation_check`: 执行发布前验证
- **release_output`: 生成最终发布文件

**核心能力**:
- 完整发布包生成
- 自动化文档生成
- 发布前质量检查
- 多格式输出支持
- 发布流程自动化

**工具集成**:
- `release_preparer`: 发布准备工具
- `doc_generator`: 文档生成工具
- `package_creator`: 包创建工具
- `quality_assurance`: 质量保证工具

### 5. 文档生成技能族

#### `/doc.generate` - 文档生成技能
**目的**: 从契约生成多种格式的API文档

**使用示例**:
```
/doc.generate spec=@api.yaml format=html,markdown,postman,output=./docs/
```

**工作流程**:
- **spec_loading**: 加载API契约文件
- **template_selection`: 选择文档模板
- **content_generation`: 生成文档内容
- **format_conversion`: 转换为指定格式
- **output_publishing`: 发布文档文件

**核心能力**:
- 多格式文档生成 (HTML, Markdown, PDF)
- 交互式API文档支持
- 代码示例自动生成
- 搜索和导航功能
- 响应式设计支持

**工具集成**:
- `template_engine`: 模板引擎工具
- `content_generator`: 内容生成工具
- `format_converter`: 格式转换工具
- `publisher`: 发布工具

#### `/doc.publish` - 文档发布技能
**目的**: 发布API文档到指定平台

**使用示例**:
```
/doc.publish docs=@./docs/ target=github-pages,postman,output=publish-report.json
```

**工作流程**:
- **doc_validation**: 验证文档完整性和质量
- **target_preparation`: 准备目标平台环境
- **content_upload`: 上传文档内容
- **link_generation`: 生成访问链接
- **publish_confirmation`: 确认发布成功

**核心能力**:
- 多平台文档发布支持
- 自动化发布流程
- 发布状态监控
- 错误恢复机制
- 发布报告生成

**工具集成**:
- `doc_validator`: 文档验证工具
- `platform_adapter`: 平台适配工具
- `uploader`: 上传工具
- `link_generator`: 链接生成工具

## 技能协作机制

### 1. 管道操作
技能可以通过管道操作组合使用：

```bash
# 源码分析 → 契约生成 → 契约验证
/analyze.python source=@api.py | /contract.generate input=- | /contract.validate spec=-

# 契约对比 → 版本管理 → 文档生成
/contract.compare old=@v1.yaml new=@v2.yaml | /contract.version create --from=- | /doc.generate spec=-
```

### 2. 工作区协作
每个技能在独立工作区运行，通过文件系统交换数据：

```
/project-root/
├── /analyze-workspace/
│   ├── /input/
│   ├── /output/
│   └── /logs/
├── /generate-workspace/
│   ├── /input/
│   ├── /output/
│   └── /logs/
├── /validate-workspace/
│   ├── /input/
│   ├── /output/
│   └── /logs/
└── /delivery-registry/
    ├── /analyses/
    ├── /contracts/
    ├── /validations/
    └── /documents/
```

### 3. 递归优化
技能支持自我优化和迭代改进：

```python
def skill_optimization_cycle(context, state=None, depth=0, max_depth=3):
    """
    技能递归优化循环
    """
    # 执行技能核心功能
    result = execute_core_functionality(context, state)
    
    # 质量评估
    quality_score = assess_quality(result)
    
    # 检查是否需要改进
    if depth < max_depth and quality_score < THRESHOLD:
        # 获取改进建议
        improvement_suggestions = get_improvement_suggestions(context, result, quality_score)
        # 更新上下文
        improved_context = update_context(context, improvement_suggestions)
        # 递归执行改进
        return skill_optimization_cycle(improved_context, state, depth + 1, max_depth)
    
    return result
```

## 认知工具集成

### 1. 源码理解认知工具
```python
def understand_source_code(source_file):
    """
    理解源码结构的认知工具
    """
    return {
        "understand": "识别主要API端点和路由结构",
        "extract": "提取关键的装饰器、类型和注释信息",
        "highlight": "标记重要的函数和类定义",
        "apply": "应用适当的分析策略和工具",
        "validate": "验证提取信息的完整性和准确性"
    }
```

### 2. 契约验证认知工具
```python
def validate_contract(contract):
    """
    验证契约质量的认知工具
    """
    return {
        "understand": "理解契约结构和规范要求",
        "extract": "提取验证规则和约束条件",
        "highlight": "标记潜在问题和不一致之处",
        "apply": "执行多层次验证检查",
        "validate": "确认验证结果的可靠性和完整性"
    }
```

### 3. 版本管理认知工具
```python
def manage_versions(old_contract, new_contract):
    """
    管理版本变更的认知工具
    """
    return {
        "understand": "理解版本变更的语义和影响",
        "extract": "识别新增、修改和删除的API元素",
        "highlight": "标记兼容性风险和破坏性变更",
        "apply": "应用版本管理策略和规则",
        "validate": "确认版本变更的合理性和正确性"
    }
```

## 字段理论应用

### 语义场操作
- **吸引子**: API设计模式、契约结构模式
- **共振**: 相似API端点的语义强化
- **持久性**: 重要契约元素的信息保持
- **边界**: 不同版本间的清晰分界

### 协议壳层
```yaml
protocol: contract-lifecycle-v1
operations:
  - analyze_source
  - generate_contract
  - validate_contract
  - manage_versions
  - generate_docs
measurement:
  resonance_score: 0.85
  attractor_strength: 0.90
  field_coherence: 0.88
  boundary_clarity: 0.92
```

## 质量保证机制

### 验证标准
- 源码分析准确率 > 95%
- 契约生成完整性 100%
- 类型推断准确率 > 98%
- 错误检测率 > 90%
- 兼容性评估准确率 > 95%

### 审计日志
每个技能执行都生成完整的审计日志：
- 输入参数和配置
- 执行过程和中间结果
- 性能指标和资源使用
- 错误信息和异常处理
- 输出结果和质量评估

---

*本技能定义基于Claude Code Skills的交互模式和Context Engineering的生物学有机体架构，为DSGS智能契约管理系统提供完整的技能体系框架。*