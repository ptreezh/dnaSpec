# DSGS智能契约管理系统 - CLI协同工作流程

## 工作流程概述

基于Claude Code Skills的设计哲学和生物学有机体架构，建立CLI工具间的间接协同机制，通过共享项目目录和文件进行协作。

## 协作原则

### 1. 文件递交制协作
- 每个CLI工具在独立工作目录操作
- 通过共享项目目录进行状态同步
- 文件递交机制确保隔离和可追溯性

### 2. 渐次披露机制
- 信息按需逐步披露给相关工具
- 每个工具只接收必要的输入信息
- 通过文件内容传递上下文信息

### 3. 版本控制机制
- 每次文件递交都生成版本记录
- 支持回滚到历史版本
- 变更历史完整可追溯

## 工作区结构设计

```
/DNASPEC-Project/
├── /workspace/                    # 主工作区
│   ├── /source-analysis/         # 源码分析工作区
│   │   ├── /input/               # 输入源码文件
│   │   ├── /output/              # 分析结果输出
│   │   └── /logs/                # 分析日志
│   ├── /contract-generation/     # 契约生成工作区
│   │   ├── /input/               # 输入分析结果
│   │   ├── /output/              # 生成契约文件
│   │   └── /logs/                # 生成日志
│   ├── /contract-validation/     # 契约验证工作区
│   │   ├── /input/               # 输入契约文件
│   │   ├── /output/              # 验证结果输出
│   │   └── /logs/                # 验证日志
│   └── /version-management/      # 版本管理工作区
│       ├── /input/               # 输入契约文件
│       ├── /output/              # 版本管理输出
│       └── /logs/                # 版本管理日志
├── /delivery-registry/           # 递交记录登记处
│   ├── /source-analysis-deliveries/
│   ├── /contract-generation-deliveries/
│   ├── /contract-validation-deliveries/
│   └── /version-management-deliveries/
├── /common-resources/            # 只读共享资源
│   ├── /templates/               # 模板文件
│   ├── /schemas/                 # 模式定义
│   └── /examples/                # 示例文件
└── /project-config/              # 项目配置
    ├── config.yaml               # 项目配置文件
    └── workflow.yaml             # 工作流程定义
```

## CLI工具协同流程

### 第一阶段: 源码分析 (/analyze)
**参与者**: `dnaspec-analyze` CLI工具
**工作区**: `/workspace/source-analysis/`
**输入来源**: 用户提供的源码文件路径
**输出去向**: `/workspace/source-analysis/output/analysis.json`
**递交记录**: 登记到 `/delivery-registry/source-analysis-deliveries/`

**工作流程**:
```bash
# Python源码分析
dnaspec-analyze --source ./src/api.py --type python --output ./workspace/source-analysis/output/

# JavaScript源码分析
dnaspec-analyze --source ./src/routes.js --type javascript --output ./workspace/source-analysis/output/
```

**递交记录格式**:
```json
{
  "delivery_id": "src-20251101-001",
  "timestamp": "2025-11-01T10:30:00Z",
  "deliverer": "dnaspec-analyze",
  "receiver": "dnaspec-generate",
  "file_path": "/workspace/source-analysis/output/analysis.json",
  "content_summary": "Python API路由分析结果，包含3个端点定义",
  "version": "1.0.0"
}
```

### 第二阶段: 契约生成 (/generate)
**参与者**: `dnaspec-generate` CLI工具
**工作区**: `/workspace/contract-generation/`
**输入来源**: 从 `/delivery-registry/source-analysis-deliveries/` 获取分析结果
**输出去向**: `/workspace/contract-generation/output/spec.yaml`
**递交记录**: 登记到 `/delivery-registry/contract-generation-deliveries/`

**工作流程**:
```bash
# 契约生成
dnaspec-generate --input ./workspace/source-analysis/output/analysis.json --format openapi3 --output ./workspace/contract-generation/output/
```

### 第三阶段: 契约验证 (/validate)
**参与者**: `dnaspec-validate` CLI工具
**工作区**: `/workspace/contract-validation/`
**输入来源**: 从 `/delivery-registry/contract-generation-deliveries/` 获取契约文件
**输出去向**: `/workspace/contract-validation/output/validation-report.json`
**递交记录**: 登记到 `/delivery-registry/contract-validation-deliveries/`

**工作流程**:
```bash
# 契约验证
dnaspec-validate --spec ./workspace/contract-generation/output/spec.yaml --checks structure,types,compatibility --output ./workspace/contract-validation/output/
```

### 第四阶段: 版本管理 (/version)
**参与者**: `dnaspec-version` CLI工具
**工作区**: `/workspace/version-management/`
**输入来源**: 从 `/delivery-registry/contract-validation-deliveries/` 获取验证结果
**输出去向**: `/workspace/version-management/output/versioned-spec.yaml`
**递交记录**: 登记到 `/delivery-registry/version-management-deliveries/`

**工作流程**:
```bash
# 版本创建
dnaspec-version --spec ./workspace/contract-generation/output/spec.yaml --bump minor --output ./workspace/version-management/output/

# 版本比较
dnaspec-version --compare ./workspace/version-management/output/v1.0.0.yaml ./workspace/version-management/output/v1.1.0.yaml
```

## 文件递交机制

### 递交记录管理
每个CLI工具在完成任务后，需要创建递交记录：

```yaml
# 递交记录模板
delivery_record:
  delivery_id: ""           # 递交ID (自动生成)
  timestamp: ""             # 递交时间戳
  deliverer: ""             # 递交者工具名称
  receiver: ""              # 接收者工具名称
  file_path: ""             # 文件路径
  content_summary: ""       # 内容摘要
  version: ""               # 版本号
  status: "completed"       # 状态
  metadata: {}              # 元数据
```

### 递交记录存储
```bash
# 递交记录存储路径
/delivery-registry/
  ├── source-analysis-deliveries/
  │   ├── 20251101-001.json
  │   ├── 20251101-002.json
  │   └── latest.json       # 指向最新递交
  ├── contract-generation-deliveries/
  │   ├── 20251101-001.json
  │   ├── 20251101-002.json
  │   └── latest.json
  └── manifest.json          # 所有递交的清单
```

## 工作流程控制

### 工作流定义文件
```yaml
# workflow.yaml
workflow:
  name: "DSGS智能契约生成流程"
  version: "1.0.0"
  steps:
    - name: "源码分析"
      tool: "dnaspec-analyze"
      input: 
        - "source_files"
      output: 
        - "/workspace/source-analysis/output/analysis.json"
      dependencies: []
      
    - name: "契约生成"
      tool: "dnaspec-generate"
      input: 
        - "/workspace/source-analysis/output/analysis.json"
      output: 
        - "/workspace/contract-generation/output/spec.yaml"
      dependencies: ["源码分析"]
      
    - name: "契约验证"
      tool: "dnaspec-validate"
      input: 
        - "/workspace/contract-generation/output/spec.yaml"
      output: 
        - "/workspace/contract-validation/output/validation-report.json"
      dependencies: ["契约生成"]
      
    - name: "版本管理"
      tool: "dnaspec-version"
      input: 
        - "/workspace/contract-generation/output/spec.yaml"
      output: 
        - "/workspace/version-management/output/versioned-spec.yaml"
      dependencies: ["契约验证"]
```

### 流程执行器
```bash
# 工作流执行命令
dnaspec-workflow --config ./project-config/workflow.yaml --execute

# 单步执行
dnaspec-workflow --step "源码分析" --input ./src/api.py
```

## 质量控制机制

### 输入验证
每个CLI工具在处理前验证输入：
```bash
# 输入验证检查清单
- 文件存在性检查
- 文件格式验证
- 必需参数检查
- 权限验证
- 依赖项检查
```

### 输出验证
每个CLI工具在输出前验证结果：
```bash
# 输出验证检查清单
- 结果完整性检查
- 格式正确性验证
- 数据一致性检查
- 错误处理验证
- 性能指标记录
```

### 递交验证
递交前验证递交记录：
```bash
# 递交验证检查清单
- 递交ID唯一性检查
- 时间戳格式验证
- 文件路径有效性检查
- 内容摘要完整性检查
- 版本号格式验证
```

## 异常处理机制

### 错误分类
```bash
# 错误类型分类
1. 输入错误 - 文件不存在、格式错误、参数缺失
2. 处理错误 - 分析失败、生成错误、验证失败
3. 输出错误 - 写入失败、格式错误、权限不足
4. 递交错误 - 记录失败、路径错误、数据不完整
```

### 错误处理流程
```bash
# 错误处理步骤
1. 错误捕获和记录
2. 错误类型识别
3. 错误信息生成
4. 恢复建议提供
5. 错误日志写入
6. 用户通知发送
```

### 恢复机制
```bash
# 自动恢复策略
- 重试机制 (最多3次)
- 回滚到上一版本
- 使用默认配置
- 跳过错误步骤
- 生成错误报告
```

## 监控和日志

### 日志级别
```bash
# 日志级别定义
- DEBUG: 详细调试信息
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息
- CRITICAL: 严重错误
```

### 日志格式
```json
{
  "timestamp": "2025-11-01T10:30:00Z",
  "level": "INFO",
  "tool": "dnaspec-analyze",
  "message": "开始分析Python源码文件",
  "context": {
    "file": "./src/api.py",
    "size": "2.5KB"
  }
}
```

### 监控指标
```bash
# 性能监控指标
- 处理时间
- 内存使用
- CPU占用
- 文件数量
- 错误率
- 成功率
```

## 安全机制

### 访问控制
```bash
# 文件访问权限
- 只读访问: /common-resources/
- 读写访问: /workspace/*/input/
- 输出访问: /workspace/*/output/
- 记录访问: /delivery-registry/
```

### 数据保护
```bash
# 敏感数据处理
- 配置文件加密
- 日志信息脱敏
- 临时文件清理
- 权限最小化
```

这套CLI协同工作流程确保了工具间的松耦合协作，通过文件系统实现信息传递，既保证了各工具的独立性，又实现了高效的协同工作。