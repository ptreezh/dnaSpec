# DNASPEC iflow 技能测试指南

## 可用的 DNASPEC 命令

项目中已安装以下 dnaspec 命令（位于 `.iflow\commands\` 目录）：

### 1. dnaspec-task-decomposer
**命令**: `/dnaspec.task-decomposer`
**用途**: 将复杂任务分解为可管理的步骤

**测试示例**:
```bash
iflow "/dnaspec.task-decomposer 将开发一个REST API分解为具体任务"
```

### 2. dnaspec-architect
**命令**: `/dnaspec.architect`
**用途**: 系统架构设计和规划

**测试示例**:
```bash
iflow "/dnaspec.architect 为电商平台设计微服务架构"
```

### 3. dnaspec-agent-creator
**命令**: `/dnaspec.agent-creator`
**用途**: 创建智能代理

**测试示例**:
```bash
iflow "/dnaspec.agent-creator 创建一个代码审查自动化代理"
```

### 4. dnaspec-constraint-generator
**命令**: `/dnaspec.constraint-generator`
**用途**: 生成系统约束和规则

**测试示例**:
```bash
iflow "/dnaspec.constraint-generator 为支付API生成安全约束"
```

### 5. dnaspec-modulizer
**命令**: `/dnaspec.modulizer`
**用途**: 代码模块化和重构

**测试示例**:
```bash
iflow "/dnaspec.modulizer 将这个代码库重构为模块化结构"
```

### 6. dnaspec-dapi-checker
**命令**: `/dnaspec.dapi-checker`
**用途**: API接口验证

**测试示例**:
```bash
iflow "/dnaspec.dapi-checker 验证这个REST API规范"
```

### 7. dnaspec-cache-manager
**命令**: `/dnaspec.cache-manager`
**用途**: 缓存策略和数据优化

**测试示例**:
```bash
iflow "/dnaspec.cache-manager 优化这个应用的缓存策略"
```

### 8. dnaspec-git-operations
**命令**: `/dnaspec.git-operations`
**用途**: Git仓库清理和维护

**测试示例**:
```bash
iflow "/dnaspec.git-operations 清理仓库中的临时文件"
```

## 启动 iflow 交互式会话

### 方法1: 直接运行命令
```bash
cd "D:\DAIP\dnaSpec"
iflow
```
然后在交互式会话中输入：
```
/dnaspec.task-decomposer 帮我规划一个项目的实施步骤
```

### 方法2: 单次执行模式
```bash
cd "D:\DAIP\dnaSpec"
iflow -p "/dnaspec.architect 设计一个任务管理系统的架构"
```

### 方法3: 继续上次会话
```bash
cd "D:\DAIP\dnaSpec"
iflow -c
```

## 测试步骤

1. **列出可用命令**
   ```bash
   iflow -p "列出所有可用的 dnaspec 命令"
   ```

2. **测试任务分解**
   ```bash
   iflow -p "/dnaspec.task-decomposer 将开发一个博客系统分解为具体任务"
   ```

3. **测试架构设计**
   ```bash
   iflow -p "/dnaspec.architect 为一个在线教育平台设计系统架构"
   ```

4. **测试代理创建**
   ```bash
   iflow -p "/dnaspec.agent-creator 创建一个自动化测试代理"
   ```

## 参数说明

iflow 命令行参数：
- `-p, --prompt`: 单次执行模式，执行命令后退出
- `-i, --prompt-interactive`: 执行命令后进入交互模式
- `-c, --continue`: 继续上次的会话
- `-m, --model`: 指定使用的模型
- `-d, --debug`: 启用调试模式
- `-a, --all-files`: 包含所有文件到上下文中

## 实际测试场景

### 场景1: 完整项目规划
```bash
iflow -p "/dnaspec.task-decomposer 将开发一个电商网站分解为完整的开发任务"
```

### 场景2: 架构优化
```bash
iflow -p "/dnaspec.architect 分析现有系统架构并提出优化建议"
```

### 场景3: 组合使用多个命令
```bash
iflow
# 在交互式会话中：
/dnaspec.task-decomposer 设计一个用户认证系统
/dnaspec.architect 为这个认证系统设计架构
/dnaspec.constraint-generator 生成安全约束
```

## 注意事项

1. 确保在 `D:\DAIP\dnaSpec` 目录下运行命令
2. 命令文件位于 `.iflow\commands\` 目录
3. 使用中文或英文都可以与 dnaspec 交互
4. 可以使用 `-a` 或 `--all-files` 参数包含所有项目文件到上下文中
5. 使用 `-d` 参数可以看到详细的调试信息

## 验证命令是否正确加载

```bash
cd "D:\DAIP\dnaSpec"
iflow -p "列出你认识的所有 /dnaspec 开头的命令"
```

如果命令正确加载，iflow 应该能够识别并执行这些命令。
