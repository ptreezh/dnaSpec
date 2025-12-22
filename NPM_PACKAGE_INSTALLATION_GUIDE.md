# DNASPEC v2.0.0 NPM包安装和使用指南

## 🎉 包构建完成

NPM包已成功构建，生成文件：`dnaspec-2.0.0.tgz`

## 📦 更新内容

### 1. 构建系统改进
- **完整构建脚本**: `npm run build` 现在包含实际构建逻辑
- **验证脚本**: 自动验证项目结构
- **文档生成**: 自动生成文档准备标识
- **发布钩子**: `prepublishOnly`, `prepublish`, `prepack` 钩子

### 2. CLI工具增强
- **智能CLI**: `bin/dnaspec-cli.js` 支持完整和简化模式
- **依赖回退**: 在缺少依赖时自动切换到简化模式
- **版本一致性**: 所有CLI工具显示版本 2.0.0
- **帮助信息**: 完整的命令帮助和使用示例

### 3. 安装后提示系统
- **自动提示**: `bin/dnaspec-init.js` 在安装后自动运行
- **环境检测**: 自动检测Python、Git、Node.js等环境
- **交互式设置**: 可选的用户交互式配置向导
- **使用指南**: 详细的部署和使用说明

### 4. 包结构优化
- **BIN目录**: 包含所有CLI入口文件
- **标准配置**: 符合NPM包标准
- **版本管理**: 统一的版本号管理

## 🚀 安装和使用

### 安装包
```bash
# 从本地包安装
npm install dnaspec-2.0.0.tgz

# 或全局安装
npm install -g dnaspec-2.0.0.tgz
```

### 使用CLI
```bash
# 查看帮助
dnaspec --help

# 查看版本
dnaspec --version

# 列出技能
dnaspec list

# 显示使用提示
dnaspec tips

# 使用技能
dnaspec slash context-analysis "分析这段文本"
```

### 安装后自动配置
包安装后会自动运行 `dnaspec-init.js` 进行：
1. 🔍 检测已安装的AI CLI工具
2. 🐍 检查Python环境
3. 📦 安装Python依赖（可选）
4. ⚙️ 生成配置文件
5. 📋 显示部署指南

## 🔧 双部署系统支持

### 标准化部署（Claude Code兼容）
```bash
# 创建技能目录
mkdir -p .claude/skills

# 复制技能文件
cp -r skills/* .claude/skills/
```

### CLI模式部署
```bash
# 直接使用Slash命令
dnaspec slash <技能名> [参数]
```

### Stigmergy集成
```bash
# 检查可用平台
dnaspec integrate --list

# 启用集成
dnaspec integrate --stigmergy
```

## 📋 可用技能

| 技能名称 | 功能描述 | 使用示例 |
|---------|---------|----------|
| context-analysis | 分析上下文质量 | `dnaspec slash context-analysis "待分析文本"` |
| context-optimization | 优化上下文 | `dnaspec slash context-optimization "待优化文本"` |
| cognitive-template | 认知模板应用 | `dnaspec slash cognitive-template "应用模板"` |
| agent-creator | 创建AI智能体 | `dnaspec slash agent-creator "创建数据分析助手"` |
| task-decomposer | 分解复杂任务 | `dnaspec slash task-decomposer "分解这个任务"` |
| constraint-generator | 生成约束 | `dnaspec slash constraint-generator "生成系统约束"` |
| api-checker | API接口检查 | `dnaspec slash api-checker "检查API接口"` |
| modulizer | 系统模块化 | `dnaspec slash modulizer "模块化系统"` |
| system-architect | 系统架构设计 | `dnaspec slash system-architect "设计系统架构"` |
| git-operations | Git操作技能 | `dnaspec slash git-operations "operation=status"` |

## 🛠️ 故障排除

### 依赖问题
如果遇到依赖缺失警告，CLI会自动切换到简化模式：
```bash
# 安装完整依赖
npm install
```

### Python环境
确保Python 3.8+已安装并在PATH中：
```bash
python --version
pip --version
```

### 权限问题
全局安装可能需要sudo权限（Linux/Mac）：
```bash
sudo npm install -g dnaspec-2.0.0.tgz
```

## 📖 更多信息

- **项目地址**: https://github.com/ptreezh/dnaSpec
- **文档**: https://github.com/ptreezh/dnaSpec#readme
- **问题反馈**: https://github.com/ptreezh/dnaSpec/issues
- **版本**: v2.0.0
- **许可证**: MIT

## 🎯 快速开始

1. **安装包**: `npm install -g dnaspec-2.0.0.tgz`
2. **查看提示**: `dnaspec tips`
3. **列出技能**: `dnaspec list`
4. **开始使用**: `dnaspec slash context-analysis "你好世界"`

---

**DNASPEC v2.0.0** - 上下文工程技能系统  
专业的AI辅助开发工具套件，支持双部署系统