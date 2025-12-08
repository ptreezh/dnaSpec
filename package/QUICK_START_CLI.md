# DNASPEC Context Engineering Skills - CLI快速开始指南

## 一键自动配置

DNASPEC Context Engineering Skills 提供了强大的自动配置功能，能够在一次安装后自动识别和配置本地的AI CLI工具。

### 安装步骤

1. **克隆并安装项目**
   ```bash
   git clone https://github.com/ptreezh/dnaSpec.git
   cd dnaSpec
   pip install -e .
   ```

2. **运行自动配置**
   ```bash
   python run_auto_config.py
   ```

   这将自动：
   - 检测系统中安装的AI CLI工具（Claude, Qwen, Gemini, Copilot, Cursor等）
   - 生成相应的配置文件
   - 验证所有集成
   - 创建验证报告

### 自动配置功能详解

#### 1. 自动检测
系统会自动检测以下AI CLI工具：
- Claude CLI (`claude --version`)
- Qwen CLI (`qwen --version`)
- Gemini CLI (`gemini --version`)
- GitHub Copilot (`gh copilot --version`)
- Cursor（如果提供CLI命令）

#### 2. 自动配置
- 根据检测结果生成 `./.dnaspec/config.yaml` 配置文件
- 配置所有可用的DNASPEC技能
- 设置平台特定的配置选项

#### 3. 自动验证
- 验证每个平台的集成状态
- 生成 `./dnaspec-validation-report.md` 验证报告
- 测试基本技能执行功能

### 使用已配置的CLI命令

配置完成后，您可以在支持的AI CLI工具中使用以下命令：

#### 上下文工程命令
- `/speckit.dnaspec.context-analysis [上下文]` - 分析上下文质量
- `/speckit.dnaspec.context-optimization [上下文] [优化目标]` - 优化上下文
- `/speckit.dnaspec.cognitive-template [任务] template=[模板类型]` - 应用认知模板

#### 专业分析命令
- `/speckit.dnaspec.architect [需求]` - 系统架构设计
- `/speckit.dnaspec.agent-creator [描述]` - 智能体创建
- `/speckit.dnaspec.task-decomposer [任务]` - 任务分解
- `/speckit.dnaspec.constraint-generator [系统]` - 约束生成
- `/speckit.dnaspec.dapi-checker [接口]` - 接口检查
- `/speckit.dnaspec.modulizer [系统]` - 模块化设计

### 高级配置选项

#### 交互式配置
```bash
# 运行交互式配置向导
python -c "from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator; ac = AutoConfigurator(); ac.interactive_configure()"
```

#### 更新现有配置
```bash
# 当安装新CLI工具后更新配置
python -c "from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator; ac = AutoConfigurator(); ac.update_configuration('./.dnaspec/config.yaml')"
```

#### 检查当前状态
```bash
# 查看当前检测到的工具
python -c "from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator; ac = AutoConfigurator(); print(ac.get_status())"
```

### 故障排除

1. **CLI工具未被检测到**
   - 确保工具已正确安装并添加到系统PATH
   - 检查是否可以运行 `tool-name --version`

2. **配置文件未生成**
   - 检查 `.dnaspec` 目录的写入权限
   - 确保有足够的磁盘空间

3. **技能无法执行**
   - 查看 `dnaspec-validation-report.md` 获取详细信息
   - 确保Python环境配置正确

### 验证安装

配置完成后，可以在CLI工具中执行以下测试命令：
```
/speckit.dnaspec.context-analysis "测试配置是否成功"
```

如果返回上下文分析结果，则说明配置成功！

### 更新配置

当您安装了新的AI CLI工具后，重新运行：
```bash
python run_auto_config.py
```

系统将检测新安装的工具并更新配置。

---

DNASPEC Context Engineering Skills - 让AI CLI工具配置变得简单高效