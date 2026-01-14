# DNASPEC 架构 - Qwen 系统集成部署指南

## 概述

本指南详细介绍如何将 DNASPEC 架构部署并与 Qwen 系统集成。由于 Qwen 支持 MCP (Model Context Protocol)、扩展系统和工具系统，DNASPEC 架构可以很好地与其集成。

## 部署选项

### 选项 1: MCP 服务器部署（推荐）

这是与 Qwen 集成的最佳方式，因为 Qwen 原生支持 MCP。

#### 1.1 配置 MCP 服务器

```python
# mcp_setup.py
from src.mcp.mcp_server import MCPServer

def configure_dnaspec_mcp():
    """配置 DNASPEC MCP 服务器"""
    config = {
        'name': 'DNASPEC-MCP-Server',
        'capabilities': {
            'prompts': {
                'get': {'available': True}
            },
            'transports': {
                'pipe': True,
                'stdio': True
            }
        }
    }
    
    mcp_server = MCPServer(config)
    mcp_server.initialize()
    
    # 注册 DNASPEC 专用处理器
    async def context_analyze_handler(params):
        """上下文分析处理器"""
        from skill_adapter import execute_original_skill_as_tool
        return execute_original_skill_as_tool('context-analyzer', params)
    
    async def constraint_generate_handler(params):
        """约束生成处理器"""
        from skill_adapter import execute_original_skill_as_tool
        return execute_original_skill_as_tool('constraint-generator', params)
    
    async def modulizer_handler(params):
        """模块化处理器"""
        from skill_adapter import execute_original_skill_as_tool
        return execute_original_skill_as_tool('modulizer', params)
    
    # 注册处理器
    mcp_server.register_handler('dnaspec/context-analyze', context_analyze_handler)
    mcp_server.register_handler('dnaspec/generate-constraints', constraint_generate_handler)
    mcp_server.register_handler('dnaspec/modulize', modulizer_handler)
    
    return mcp_server

if __name__ == "__main__":
    server = configure_dnaspec_mcp()
    print("DNASPEC MCP Server configured and ready")
    print("Capabilities:", server.get_capabilities())
```

#### 1.2 启动 MCP 服务器

```bash
# 启动 DNASPEC MCP 服务器
python mcp_setup.py
```

#### 1.3 在 Qwen 中配置 MCP 服务器

在 Qwen 中使用 `/mcp` 命令配置 DNASPEC MCP 服务器：

```
/mcp list  # 查看已配置的 MCP 服务器
/mcp auth  # 如需要，进行认证
```

### 选项 2: 作为 Qwen 扩展部署

#### 2.1 创建扩展配置

```json
// qwen-extension.json
{
  "name": "dnaspec-extension",
  "version": "1.0.0",
  "displayName": "DNASPEC Skills Extension",
  "description": "Integrates DNASPEC context engineering skills into Qwen",
  "main": "./extension.js",
  "activationEvents": [
    "onCommand:dnaspec.context-analyze",
    "onCommand:dnaspec.generate-constraints",
    "onCommand:dnaspec.modulize"
  ],
  "contributes": {
    "commands": [
      {
        "command": "dnaspec.context-analyze",
        "title": "DNASPEC: Analyze Context Quality"
      },
      {
        "command": "dnaspec.generate-constraints",
        "title": "DNASPEC: Generate System Constraints"
      },
      {
        "command": "dnaspec.modulize",
        "title": "DNASPEC: Modularize System Design"
      }
    ]
  }
}
```

#### 2.2 实现扩展功能

```javascript
// extension.js
const { spawn } = require('child_process');
const path = require('path');

class DnaSpecExtension {
  constructor() {
    this.pythonPath = 'python';
    this.dnaspecDir = path.join(__dirname, '../..'); // DNASPEC 项目根目录
  }

  async activate() {
    console.log('DNASPEC Extension activated');
    // 初始化 DNASPEC 插件
    const { MyOpenCodePlugin } = require('./src/plugin');
    this.plugin = new MyOpenCodePlugin({
      name: 'Qwen-DNASPEC-Extension',
      version: '1.0.0'
    });
    this.plugin.initialize();
  }

  async deactivate() {
    if (this.plugin) {
      this.plugin.shutdown();
    }
  }

  async runContextAnalysis(context) {
    const result = await this.executeSkill('context-analyzer', { context });
    return result;
  }

  async runConstraintGeneration(requirement) {
    const result = await this.executeSkill('constraint-generator', { requirement });
    return result;
  }

  async runModulization(systemDesc) {
    const result = await this.executeSkill('modulizer', { system_description: systemDesc });
    return result;
  }

  async executeSkill(skillName, params) {
    // 通过 Python 子进程执行技能
    return new Promise((resolve, reject) => {
      const scriptPath = path.join(this.dnaspecDir, 'skill_executor.py');
      const child = spawn(this.pythonPath, [scriptPath, skillName, JSON.stringify(params)], {
        cwd: this.dnaspecDir
      });

      let output = '';
      let error = '';

      child.stdout.on('data', (data) => {
        output += data.toString();
      });

      child.stderr.on('data', (data) => {
        error += data.toString();
      });

      child.on('close', (code) => {
        if (code === 0) {
          resolve(JSON.parse(output));
        } else {
          reject(new Error(`Skill execution failed: ${error}`));
        }
      });
    });
  }
}

module.exports = DnaSpecExtension;
```

### 选项 3: 工具集成

#### 3.1 通过 Qwen 工具系统集成

```python
# qwen_tools_integration.py
from src.tools.tool_manager import ToolManager

def register_dnaspec_tools_with_qwen():
    """将 DNASPEC 工具注册到 Qwen 工具系统"""
    tool_manager = ToolManager()
    
    # 注册 DNASPEC 专用工具
    def qwen_context_analyzer_tool(params):
        """Qwen 专用的上下文分析工具"""
        context = params.get('context', '')
        # 使用 DNASPEC 的上下文分析能力
        from skill_adapter import execute_original_skill_as_tool
        return execute_original_skill_as_tool('context-analyzer', {'context': context})
    
    def qwen_constraint_generator_tool(params):
        """Qwen 专用的约束生成工具"""
        requirement = params.get('requirement', '')
        # 使用 DNASPEC 的约束生成能力
        from skill_adapter import execute_original_skill_as_tool
        return execute_original_skill_as_tool('constraint-generator', {'requirement': requirement})
    
    # 注册工具
    tool_manager.register_tool('qwen-context-analyzer', qwen_context_analyzer_tool)
    tool_manager.register_tool('qwen-constraint-generator', qwen_constraint_generator_tool)
    
    return tool_manager

# 使用示例
if __name__ == "__main__":
    tools = register_dnaspec_tools_with_qwen()
    print("Available DNASPEC tools for Qwen:", list(tools.tools.keys()))
```

## 部署步骤

### 步骤 1: 环境准备

```bash
# 确保 Python 3.8+ 已安装
python --version

# 安装依赖（如果有的话）
pip install -r requirements.txt
```

### 步骤 2: 选择部署方式

根据你的需求选择以下方式之一：

1. **MCP 部署** (推荐): 适用于需要深度集成的场景
2. **扩展部署**: 适用于需要 Qwen UI 集成的场景
3. **工具部署**: 适用于需要在 Qwen 工具系统中使用 DNASPEC 功能的场景

### 步骤 3: 配置集成

根据选择的部署方式，按照上述说明进行配置。

### 步骤 4: 验证集成

在 Qwen 中验证 DNASPEC 功能是否正常工作：

```
# 如果使用 MCP 集成
/qwen-mcp-command  # 使用 MCP 提供的命令

# 如果使用扩展集成
/dnaspec-analyze-context "your context here"

# 如果使用工具集成
/tools dnaspec-tools  # 查看可用的 DNASPEC 工具
```

## 最佳实践

1. **安全性**: 确保 MCP 服务器的安全配置
2. **性能**: 根据需要调整并发级别和资源限制
3. **监控**: 实施适当的日志记录和监控
4. **兼容性**: 定期验证与 Qwen 新版本的兼容性

## 故障排除

1. **MCP 连接问题**: 检查网络配置和防火墙设置
2. **工具不可用**: 验证工具是否正确注册到 Qwen
3. **性能问题**: 检查资源使用情况和并发设置