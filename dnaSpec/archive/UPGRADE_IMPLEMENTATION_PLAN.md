# DNASPEC与spec.kit整合升级实施计划

## 1. 项目现状分析

### 1.1 当前架构
- **语言**: Python 3.8+
- **包管理**: pip + pyproject.toml
- **技能系统**: 已实现6个核心技能
  - dnaspec-architect (架构师)
  - dnaspec-agent-creator (智能体创建器)
  - dnaspec-task-decomposer (任务分解器)
  - dnaspec-constraint-generator (约束生成器)
  - dnaspec-dapi-checker (接口检查器)
  - dnaspec-modulizer (模块化器)
- **适配器系统**: 已实现spec.kit适配器基类和具体实现
- **命令接口**: /speckit.dnaspec.* 斜杠命令格式

### 1.2 当前问题
- 缺乏npm包管理支持
- 缺乏初始化工具
- 缺乏AI CLI自动检测和配置
- 缺乏统一的用户界面

## 2. 目标架构设计

### 2.1 双重包管理系统
```
项目结构
├── python/                    # Python包 (当前实现)
│   ├── src/
│   ├── pyproject.toml
│   └── README.md
├── node/                      # Node.js包 (新增)
│   ├── package.json
│   ├── bin/
│   ├── lib/
│   └── README.md
└── shared/                    # 共享资源
    ├── skills/
    ├── adapters/
    └── docs/
```

### 2.2 初始化工具设计
```bash
# npm安装后初始化
npx dnaspec-spec-kit init

# 交互式配置向导
1. 检测已安装的AI CLI工具
2. 选择要集成的平台
3. 配置技能映射
4. 生成配置文件
5. 验证集成
```

### 2.3 命令系统增强
```bash
# 全局命令
npx dnaspec-spec-kit init          # 初始化配置
npx dnaspec-spec-kit list          # 列出可用技能
npx dnaspec-spec-kit config        # 配置管理
npx dnaspec-spec-kit test          # 测试集成

# 技能调用 (与spec.kit兼容)
/speckit.dnaspec.architect         # 架构设计
/speckit.dnaspec.agent-creator     # 智能体创建
/speckit.dnaspec.task-decomposer   # 任务分解
```

## 3. 升级实施路线图

### 3.1 第一阶段：基础设施建设 (2周)
**目标**: 建立npm包管理和初始化工具

#### 任务清单
1. **创建Node.js包结构**
   - 创建package.json
   - 配置bin脚本入口
   - 设置npm发布配置

2. **开发初始化工具**
   - 系统环境检测
   - AI CLI工具检测
   - 交互式配置向导
   - 配置文件生成

3. **实现跨平台支持**
   - Windows、Linux、macOS兼容
   - 不同shell环境支持
   - 权限管理

#### 验收标准
- [ ] 可通过npm安装包
- [ ] 初始化工具可检测系统环境
- [ ] 支持至少3种AI CLI工具
- [ ] 生成标准配置文件

### 3.2 第二阶段：命令系统增强 (3周)
**目标**: 实现与spec.kit完全兼容的命令系统

#### 任务清单
1. **斜杠命令解析器**
   - 命令格式验证
   - 参数解析
   - 技能映射

2. **技能调用接口**
   - Python技能调用桥接
   - 结果格式化
   - 错误处理

3. **交互式Shell**
   - REPL环境
   - 命令历史
   - 自动补全

#### 验收标准
- [ ] 完全兼容spec.kit斜杠命令格式
- [ ] 支持所有6个核心技能调用
- [ ] 提供友好的错误提示
- [ ] 实现交互式命令行界面

### 3.3 第三阶段：智能集成 (2周)
**目标**: 实现自动检测和配置AI CLI工具

#### 任务清单
1. **AI CLI自动检测**
   - Claude CLI检测
   - Gemini CLI检测
   - Qwen CLI检测
   - 其他平台检测

2. **自动配置生成**
   - 根据检测结果生成配置
   - 自动创建技能注册文件
   - 验证配置有效性

3. **集成验证工具**
   - 集成状态检查
   - 性能测试
   - 兼容性验证

#### 验收标准
- [ ] 自动检测主流AI CLI工具
- [ ] 生成正确的配置文件
- [ ] 验证集成成功
- [ ] 提供详细的集成报告

### 3.4 第四阶段：文档和发布 (1周)
**目标**: 完善文档并发布到npm

#### 任务清单
1. **完善用户文档**
   - 安装指南
   - 使用教程
   - 故障排除

2. **API文档**
   - 命令参考
   - 配置选项
   - 开发指南

3. **发布到npm**
   - 版本管理
   - 发布流程
   - 更新通知

#### 验收标准
- [ ] 完整的用户文档
- [ ] 详细的API参考
- [ ] 成功发布到npm
- [ ] 可供普通用户使用

## 4. 技术规范

### 4.1 包管理规范
```json
{
  "name": "dnaspec-spec-kit",
  "version": "1.0.0",
  "description": "DNASPEC Skills for spec.kit integration",
  "bin": {
    "dnaspec-spec-kit": "./bin/cli.js"
  },
  "scripts": {
    "init": "node bin/init.js",
    "test": "node bin/test.js"
  },
  "dependencies": {
    "python-shell": "^3.0.0",
    "inquirer": "^8.0.0",
    "chalk": "^4.0.0"
  }
}
```

### 4.2 配置文件规范
```yaml
# .dnaspec/config.yaml
version: "1.0.0"
platforms:
  - name: "claude"
    enabled: true
    config_path: "~/.config/claude/skills/"
  - name: "gemini"
    enabled: false
    config_path: "~/.local/share/gemini/extensions/"
ai_cli_detection:
  claude: "claude --version"
  gemini: "gemini --version"
  qwen: "qwen --version"
skills:
  architect:
    command: "/speckit.dnaspec.architect"
    enabled: true
  agent-creator:
    command: "/speckit.dnaspec.agent-creator"
    enabled: true
```

### 4.3 命令接口规范
```javascript
// 命令解析规范
const commandSpec = {
  pattern: /^\/speckit\.dnaspec\.([a-zA-Z0-9-]+)(?:\s+(.+))?$/,
  groups: {
    skill: 1,
    params: 2
  }
};

// 技能映射规范
const skillMap = {
  "architect": "dnaspec-architect",
  "agent-creator": "dnaspec-agent-creator",
  "task-decomposer": "dnaspec-task-decomposer"
};
```

## 5. 风险评估和应对

### 5.1 技术风险
- **跨平台兼容性**: 不同操作系统可能有路径和权限差异
  - 应对: 使用跨平台库，充分测试

- **Python依赖管理**: 用户可能没有正确安装Python依赖
  - 应对: 提供自动安装脚本，详细错误提示

- **AI CLI版本兼容性**: 不同版本的AI CLI可能有API差异
  - 应对: 版本检测，兼容性层

### 5.2 项目风险
- **开发周期延长**: 功能复杂度可能超出预期
  - 应对: 分阶段交付，优先核心功能

- **用户接受度**: 用户可能不习惯新的命令方式
  - 应对: 提供迁移指南，保持向后兼容

## 6. 成功指标

### 6.1 技术指标
- 支持npm安装和使用
- 支持3个以上主流AI CLI平台
- 初始化过程少于5分钟
- 技能调用响应时间<2秒

### 6.2 用户体验指标
- 安装成功率>95%
- 初始化成功率>90%
- 用户满意度>4.5/5.0
- 文档完整性和准确性>95%

## 7. 时间计划

| 阶段 | 时间 | 里程碑 |
|------|------|--------|
| 基础设施建设 | 2周 | npm包可安装 |
| 命令系统增强 | 3周 | 命令系统完整 |
| 智能集成 | 2周 | 自动配置完成 |
| 文档和发布 | 1周 | npm发布成功 |

**总计**: 8周 (2个月)