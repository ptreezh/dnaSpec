# DNASPEC Init Skill - 优化规范

## 技能概述

DNASPEC Init技能是DNASPEC协调框架的核心管理工具，负责项目协调机制的初始化、状态检测、配置管理和优雅重置。该技能完全符合agentskills.io规范，支持在Claude CLI环境中自动加载和使用。

## 功能特性

### 核心功能
1. **项目状态检测** - 自动检测项目是否已初始化协调机制
2. **协调机制初始化** - 为项目设置DNASPEC协调框架
3. **配置管理** - 生成和管理项目配置文件
4. **状态查询** - 检查协调机制的健康状态
5. **优雅重置** - 安全地重置协调配置并备份原有设置

### 智能特性
- **自动类型识别** - 基于项目文件自动检测项目类型和开发工具
- **多类型支持** - 支持project、team、enterprise、solo、auto五种初始化类型
- **功能模块化** - 支持caching、git_hooks、ci_cd等功能模块的独立启用
- **优雅降级** - 当协调不可用时自动降级到独立模式

## 技能接口规范

### 输入模式
```json
{
  "operation": "detect|initialize|reset|get-config|status",
  "init_type": "project|team|enterprise|solo|auto",
  "project_type": "web_application|mobile_app|api_service|desktop_app|library|microservice|data_science|ml_project|generic",
  "features": ["caching", "git_hooks", "ci_cd"],
  "force": true|false,
  "confirm": true|false
}
```

### 支持的操作

#### 1. detect（检测）
检测项目当前状态，包括：
- 协调机制初始化状态
- 现有配置文件
- 检测到的项目类型
- 开发工具识别

#### 2. initialize（初始化）
为项目初始化DNASPEC协调机制，包括：
- 创建.目录结构
- 生成PROJECT_CONSTITUTION.md文件
- 生成config.json配置文件
- 启用指定的功能模块

#### 3. reset（重置）
安全重置协调机制：
- 备份现有配置
- 清理协调文件
- 提供恢复指引

#### 4. get-config（获取配置）
读取并返回当前配置信息

#### 5. status（状态）
与detect操作相同，提供状态查询

## 使用指南

### 在Claude CLI中的调用

```bash
# 检测项目状态
/dnaspec-init "operation=detect"

# 初始化项目（自动检测）
/dnaspec-init "operation=initialize"

# 初始化为团队项目，启用缓存和Git钩子
/dnaspec-init "operation=initialize init_type=team features=caching,git_hooks"

# 查看配置信息
/dnaspec-init "operation=get-config"

# 重置协调机制（需要确认）
/dnaspec-init "operation=reset confirm=true"

# 强制重新初始化
/dnaspec-init "operation=initialize force=true"
```

### 集成工作流

```bash
# 1. 检测当前状态
/dnaspec-init "operation=detect"

# 2. 初始化协调机制
/dnaspec-init "operation=initialize init_type=auto"

# 3. 使用其他DNASPEC技能
/architect "system_type=web_application"
/task-decomposer "input=implement_user_login"
/constraint-generator "requirements=security_requirements"

# 4. 定期检查状态
/dnaspec-init "operation=status"
```

## 输出格式

### 成功响应
```json
{
  "success": true,
  "operation": "detect",
  "message": "项目状态检测完成",
  "result": {
    "status": "complete|partial|not_initialized",
    "existing_files": [...],
    "missing_files": [...],
    "detected_types": [...],
    "detected_tools": {...}
  },
  "timestamp": "2025-12-21T21:41:00.000Z"
}
```

### 错误响应
```json
{
  "success": false,
  "error": "错误描述",
  "operation": "unknown_operation",
  "timestamp": "2025-12-21T21:41:00.000Z"
}
```

## 生成的文件结构

初始化后项目将包含以下结构：

```
project_root/
├── PROJECT_CONSTITUTION.md     # 项目协调宪法
├── .dnaspec/                   # DNASPEC协调目录
│   ├── config.json            # 协调配置文件
│   ├── cache/                 # 缓存目录
│   │   ├── config.json        # 缓存配置
│   │   ├── temp/              # 临时缓存
│   │   ├── staging/           # 暂存缓存
│   │   └── meta/              # 元数据缓存
│   ├── meta/                  # 元数据目录
│   ├── hooks/                 # Git钩子目录
│   └── logs/                  # 日志目录
└── .git/hooks/                # Git钩子（如果启用）
    └── pre-commit             # 预提交钩子
```

## 协调机制特性

### 自动检测
- 检测Git版本控制系统
- 识别构建工具（npm、pip、Docker）
- 检测团队协作工具（GitHub Actions、GitLab CI）
- 识别企业工具（Kubernetes、Terraform）

### 智能初始化
- 基于项目特征选择初始化类型
- 自动配置技能优先级
- 生成最佳实践配置

### 优雅降级
- 协调机制不可用时自动使用独立模式
- 提供降级原因说明
- 支持手动重新启用协调

## 性能优化

### 缓存策略
- 文件系统缓存：TTL 3600秒
- 内存缓存：TTL 1800秒
- 分布式缓存：按需启用

### 资源限制
- 最大并发任务：5
- 执行超时：300秒
- 内存限制：1024MB

## 错误处理

### 常见错误场景
1. **权限不足** - 无法创建目录或文件
2. **磁盘空间不足** - 无法写入配置文件
3. **网络问题** - 无法访问远程资源
4. **配置冲突** - 现有配置与新配置冲突

### 错误恢复
- 自动重试机制
- 详细错误信息
- 恢复建议提供
- 备份机制保护

## 安全考虑

### 数据保护
- 敏感配置加密存储
- 备份文件自动清理
- 操作日志记录

### 访问控制
- 只在项目目录内操作
- 不访问系统敏感文件
- Git凭据安全处理

## 维护指南

### 定期维护
- 清理过期缓存文件
- 检查配置文件完整性
- 监控磁盘空间使用

### 升级流程
1. 备份当前配置
2. 运行重置操作
3. 重新初始化
4. 验证功能正常

## 故障排除

### 常见问题

**Q: 初始化失败怎么办？**
A: 检查项目目录权限，确保有写入权限

**Q: 协调模式未启用？**
A: 运行`/dnaspec-init "operation=detect"`检查状态

**Q: 配置文件错误？**
A: 检查`.dnaspec/config.json`格式，或重新初始化

### 日志查看
```bash
# 查看DNASPEC日志
cat .dnaspec/logs/*.log

# 检查Git钩子状态
cat .git/hooks/pre-commit
```

## 扩展开发

### 添加新功能模块
1. 在`_setup_xxx_system()`函数中添加逻辑
2. 更新`_generate_configuration()`配置生成
3. 修改宪法模板包含新功能说明

### 自定义初始化类型
1. 在操作枚举中添加新类型
2. 实现相应的初始化逻辑
3. 更新类型检测算法

---

**版本**: 1.0.0  
**维护者**: DNASPEC团队  
**最后更新**: 2025-12-21  
**兼容性**: agentskills.io v1 规范