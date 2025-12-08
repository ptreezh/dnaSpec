# DSGS文档系列概览

## 1. 文档结构

本目录包含DSGS (Dynamic Specification Growth System) 项目的完整需求文档系列，按照金字塔原则组织，从核心需求到具体功能实现：

### 1.1 主控文档
- **DNASPEC-Core-Requirements.md**: 核心需求文档，定义项目的顶层需求和架构
- **DNASPEC-Core-Requirements-BioInspired.md**: 生物学启发的核心需求文档
- **DNASPEC-Core-Requirements-BioInspired-Operational.md**: 生物学启发的操作级核心需求文档

### 1.2 功能细分文档
- **DNASPEC-Constraint-Engine-Requirements.md**: 约束生成引擎详细需求（基于生物学启发的时空展开机制）
- **DNASPEC-Template-Matcher-Requirements.md**: 模板匹配系统详细需求（基于生物学启发的基因表达机制）
- **DNASPEC-Specification-Management-Requirements.md**: 规范管理系统详细需求（基于生物学的基因组管理）
- **DNASPEC-Specification-Manager-Requirements.md**: 规范管理器详细需求
- **DNASPEC-TCC-System-Requirements.md**: 任务上下文胶囊系统详细需求（基于生物学启发的发育信号系统）
- **DNASPEC-Context-Engineering-Requirements.md**: 上下文工程集成需求
- **DNASPEC-Integration-Deployment-Requirements.md**: 集成与部署需求

### 1.3 工程化文档
- **DNASPEC-Engineering-Implementation-Guide.md**: 工程化实现指南（AI代码工程落地化）
- **DNASPEC-Engineering-Guide.md**: 工程化指南

### 1.4 历史文档
- **DSGS_Core_Requirements.md**: 早期版本的核心需求文档

## 2. 文档关系图

```
DNASPEC-Core-Requirements.md (顶层需求)
├── DNASPEC-Constraint-Engine-Requirements.md (约束生成)
├── DNASPEC-Template-Matcher-Requirements.md (模板匹配)
├── DNASPEC-Specification-Management-Requirements.md (规范管理)
├── DNASPEC-Specification-Manager-Requirements.md (规范管理器)
├── DNASPEC-TCC-System-Requirements.md (任务上下文)
├── DNASPEC-Context-Engineering-Requirements.md (上下文工程)
└── DNASPEC-Integration-Deployment-Requirements.md (集成部署)

DNASPEC-Engineering-Implementation-Guide.md (工程化实现)
```

## 3. 使用说明

### 3.1 阅读顺序
1. 首先阅读 **DNASPEC-Core-Requirements.md** 了解项目整体需求
2. 根据关注的功能模块选择相应的细分文档深入阅读
3. 参考 **DNASPEC-Engineering-Implementation-Guide.md** 了解工程化实现细节

### 3.2 维护要求
- 保持文档间引用关系的一致性
- 更新主控文档时同步更新相关细分文档
- 定期验证文档内容与代码实现的一致性

## 4. 版本信息

- **文档版本**: v1.0
- **创建日期**: 2025-09-02
- **维护状态**: 稳定版

## 5. 生物学启发映射关系

| DSGS组件 | 生物学类比 | 功能描述 |
|---------|-----------|---------|
| BSL | DNA | 系统核心约束原则 |
| TCC | 发育信号 | 任务上下文信息 |
| 约束模板 | 基因 | 可表达的约束规则 |
| 约束生成 | 基因表达 | 根据信号生成具体约束 |
| 模板匹配 | 基因调控 | 调控约束模板的表达 |
| 规范管理 | 基因组 | 管理所有约束规范 |