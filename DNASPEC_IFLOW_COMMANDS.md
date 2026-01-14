# DNASPEC iflow 命令使用指南

## 📋 可用的 DNASPEC 命令

项目已安装以下 8 个 DNASPEC 命令：

### 1️⃣ /dnaspec.task-decomposer
**描述**: 将复杂任务分解为可管理的步骤
**用途**: 项目规划、任务拆分、工作分解结构

**测试示例**:
```bash
iflow -p "/dnaspec.task-decomposer 将'开发一个待办事项应用'分解为具体任务"
```

---

### 2️⃣ /dnaspec.architect
**描述**: 设计系统架构和技术规范
**用途**: 系统架构设计、技术选型、模块设计

**测试示例**:
```bash
iflow -p "/dnaspec.architect 为一个博客系统设计系统架构"
```

---

### 3️⃣ /dnaspec.agent-creator
**描述**: 为特定任务和领域创建智能代理
**用途**: AI代理设计、自动化工具创建

**测试示例**:
```bash
iflow -p "/dnaspec.agent-creator 创建一个代码审查自动化代理"
```

---

### 4️⃣ /dnaspec.constraint-generator
**描述**: 生成约束和验证规则
**用途**: 安全约束、业务规则、验证规则

**测试示例**:
```bash
iflow -p "/dnaspec.constraint-generator 为支付API生成安全约束"
```

---

### 5️⃣ /dnaspec.modulizer
**描述**: 模块化和重构代码库
**用途**: 代码重构、模块提取、架构优化

**测试示例**:
```bash
iflow -p "/dnaspec.modulizer 将这个代码库重构为模块化结构"
```

---

### 6️⃣ /dnaspec.dapi-checker
**描述**: 验证API接口设计
**用途**: API规范检查、接口验证

**测试示例**:
```bash
iflow -p "/dnaspec.dapi-checker 验证这个REST API规范"
```

---

### 7️⃣ /dnaspec.cache-manager
**描述**: 缓存策略和数据优化
**用途**: 缓存设计、性能优化

**测试示例**:
```bash
iflow -p "/dnaspec.cache-manager 优化这个应用的缓存策略"
```

---

### 8️⃣ /dnaspec.git-operations
**描述**: Git仓库清理和维护
**用途**: 仓库清理、污染预防

**测试示例**:
```bash
iflow -p "/dnaspec.git-operations 清理仓库中的临时文件"
```

---

## 🚀 快速开始

### 方法 1: 使用批处理脚本（推荐）

直接运行提供的测试脚本：
```cmd
test_iflow_commands.bat
```

脚本会提供交互式菜单让你选择测试不同的命令。

### 方法 2: 单次命令执行

在命令行中快速测试：
```cmd
cd D:\DAIP\dnaSpec
iflow -p "/dnaspec.task-decomposer 你的任务描述"
```

### 方法 3: 交互式会话

进入 iflow 交互模式：
```cmd
cd D:\DAIP\dnaSpec
iflow
```

然后在交互式会话中输入命令：
```
/dnaspec.architect 为电商平台设计微服务架构
/dnaspec.constraint-generator 生成数据安全约束
```

---

## 📝 实际测试场景

### 场景 1: 完整项目规划
```cmd
iflow -p "/dnaspec.task-decomposer 将开发一个电商网站分解为完整的开发任务"
```

### 场景 2: 架构设计
```cmd
iflow -p "/dnaspec.architect 为在线教育平台设计系统架构，需要支持视频直播、即时通讯和支付功能"
```

### 场景 3: 安全约束生成
```cmd
iflow -p "/dnaspec.constraint-generator 为用户认证系统生成安全约束，包括密码策略、会话管理和防暴力破解"
```

### 场景 4: 代理创建
```cmd
iflow -p "/dnaspec.agent-creator 创建一个自动化测试代理，能够生成测试用例并执行测试"
```

### 场景 5: 代码模块化
```cmd
iflow -p "/dnaspec.modulizer 分析当前代码库并提出模块化重构建议"
```

---

## 🛠️ iflow 命令参数

| 参数 | 说明 |
|------|------|
| `-p, --prompt` | 单次执行模式，执行后退出 |
| `-i, --prompt-interactive` | 执行命令后进入交互模式 |
| `-c, --continue` | 继续上次的会话 |
| `-m, --model` | 指定使用的模型 |
| `-a, --all-files` | 包含所有文件到上下文 |
| `-d, --debug` | 启用调试模式 |
| `--max-tokens` | 限制最大token数 |

---

## 💡 使用技巧

### 1. 验证命令是否加载
```cmd
iflow -p "列出所有 /dnaspec 开头的命令"
```

### 2. 使用调试模式
如果命令不工作，启用调试模式查看详情：
```cmd
iflow -d -p "/dnaspec.task-decomposer 测试任务"
```

### 3. 包含项目文件
如果需要分析项目代码：
```cmd
iflow -a -p "/dnaspec.modulizer 分析并优化当前项目结构"
```

### 4. 限制输出长度
```cmd
iflow -p "/dnaspec.architect 设计简单架构" --max-tokens 1000
```

---

## ⚠️ 常见问题

### 问题: 命令无法识别
**解决方案**:
1. 确保在 `D:\DAIP\dnaSpec` 目录下
2. 检查 `.iflow\commands\` 目录是否存在
3. 尝试列出命令: `iflow commands list`

### 问题: 输出过长
**解决方案**:
使用 `--max-tokens` 参数限制输出长度

### 问题: 需要分析项目代码
**解决方案**:
使用 `-a` 或 `--all-files` 参数包含所有文件

---

## 📚 相关文档

- `test_iflow_dnaspec.md` - 详细测试指南
- `test_iflow_commands.bat` - 交互式测试脚本
- `.iflow\commands\` - 命令定义文件目录

---

## 🎯 推荐测试流程

1. **快速验证**: 先测试简单的任务分解命令
   ```cmd
   iflow -p "/dnaspec.task-decomposer 列出开发一个TODO应用的基本步骤"
   ```

2. **架构测试**: 测试架构设计能力
   ```cmd
   iflow -p "/dnaspec.architect 设计一个简单博客的架构"
   ```

3. **综合测试**: 组合使用多个命令
   ```cmd
   iflow -i "/dnaspec.task-decomposer 规划一个CRM系统"
   ```
   然后在交互模式中继续使用其他命令

4. **进入交互模式**: 进行深度测试
   ```cmd
   iflow
   ```

---

生成时间: 2025-12-25
项目: DNASPEC
工具: iflow CLI
