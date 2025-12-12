# DNASPEC 卸载指南

## 📋 概述

DNASPEC 提供了完整的卸载工具，可以清理所有安装过程中生成的文件、配置和依赖。

## 🚀 卸载方法

### 方法1: 使用 NPM 卸载 (推荐)

```bash
# 全局卸载 (自动运行清理脚本)
npm uninstall -g dnaspec

# 本地卸载
npm uninstall dnaspec
```

### 方法2: 手动运行卸载脚本

```bash
# 直接运行卸载脚本
node uninstall.js

# 或使用 NPM 脚本
npm run cleanup

# 或使用安装的命令
dnaspec-uninstall
```

### 方法3: 使用包管理器

```bash
# 如果使用 yarn
yarn global remove dnaspec

# 如果使用 pnpm
pnpm uninstall -g dnaspec
```

## 🧹 清理内容

卸载脚本会清理以下内容：

### 📁 文件和目录
- 临时目录: `dnaspec-install-tmp`, `dnaspec-temp-*`
- Python 缓存: `__pycache__`, `*.pyc`, `*.pyo`
- 构建文件: `build`, `dist`, `*.egg-info`
- 配置文件: `.dnaspec-config.json`, `.dna-spec-integration.json`

### 🐍 Python 包
- `dnaspec-context-engineering-skills`
- `dna-context-engineering-skills`
- `dna-spec-kit-integration`
- `dnaspec-spec-kit-integration`

### 📦 NPM 包
- `dnaspec`
- `stigmergy` (仅 DNASPEC 相关配置)

### 🔧 平台配置
- **Claude**: `.claude/` 目录中的 DNASPEC 相关文件
- **Cursor**: `.cursor/`, `.cursorrules` 中的配置
- **Copilot**: `.copilot/` 中的配置
- **Qwen**: `.qwen/` 中的配置
- **Gemini**: `.gemini/` 中的配置
- **其他平台**: 对应的配置目录

### ⚙️ 系统配置
- NPM 配置中的 DNASPEC 相关设置
- 临时工作空间和缓存

## ⚠️ 注意事项

### 手动清理项目
卸载后，您可能还需要手动清理：

1. **环境变量**:
   ```bash
   # 检查并删除以下环境变量
   NPM_AUTH_TOKEN
   DNASPEC_*
   DNA_SPEC_*
   ```

2. **AI 工具配置**:
   - 检查 Claude、Cursor、Copilot 等工具中的自定义命令
   - 删除 `/speckit.dnaspec.*` 相关的命令配置

3. **项目配置**:
   - 检查项目根目录的配置文件
   - 删除 `.claude/` 目录 (如果不包含其他重要内容)

## 📊 卸载报告

卸载完成后，会在当前目录生成 `dnaspec-uninstall-report.json` 文件，包含：

- 清理时间戳
- 成功删除的项目列表
- 失败的项目和错误信息
- 详细的清理记录

## 🔍 验证卸载

卸载完成后，可以通过以下方式验证：

```bash
# 检查 NPM 包
npm list -g | grep dnaspec

# 检查 Python 包
pip list | grep dnaspec

# 检查残留文件
find ~ -name "*dnaspec*" -type f 2>/dev/null

# 检查配置
ls -la ~/.claude/ | grep dnaspec
```

## 🆘 故障排除

### 常见问题

1. **权限错误**
   ```bash
   # 使用管理员权限运行
   sudo npm uninstall -g dnaspec
   ```

2. **文件正在使用**
   ```bash
   # 关闭相关 IDE 和终端后重试
   ```

3. **网络问题**
   ```bash
   # 使用 --no-verify 跳过网络验证
   npm uninstall -g dnaspec --no-verify
   ```

### 强制清理

如果需要强制清理，可以手动删除：

```bash
# 删除全局 NPM 包
rm -rf $(npm root -g)/dnaspec

# 删除 Python 包
pip uninstall -y dnaspec-context-engineering-skills

# 清理配置
rm -rf ~/.claude/dnaspec*
rm -rf ~/.cursor/dnaspec*
```

## 📞 支持

如果遇到问题，请：

1. 查看 `dnaspec-uninstall-report.json` 了解详细错误信息
2. 访问 [GitHub Issues](https://github.com/ptreezh/dnaSpec/issues) 报告问题
3. 提供详细的错误日志和系统信息

---

**注意**: 卸载是不可逆操作，请确保您备份了重要的配置和数据。