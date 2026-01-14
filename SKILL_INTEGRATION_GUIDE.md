# DNASPEC 技能包新架构集成指南

## 概述

本文档详细说明了原有 dnaspec 技能如何在新的架构中工作。新架构通过适配器模式将原有技能无缝集成到 Hook 系统、Agent 系统、Tool 系统和上下文共享机制中。

## 原有技能映射到新架构

### 1. Agent 系统集成

原有技能被包装成专门的 Agent，可以在 Sisyphus 编排器中被调用：

#### Context Analyzer 技能
- **新位置**: `ContextAnalyzerAgent`
- **功能**: 分析上下文质量和结构
- **调用方式**: 
  ```python
  agent = agent_manager.get_agent('context-analyzer')
  result = await agent.process({'context': '待分析的上下文'})
  ```

#### Constraint Generator 技能
- **新位置**: `ConstraintGeneratorAgent`
- **功能**: 为系统设计生成约束条件
- **调用方式**:
  ```python
  agent = agent_manager.get_agent('constraint-generator')
  result = await agent.process({'requirement': '系统需求描述'})
  ```

#### Modulizer 技能
- **新位置**: `ModulizerAgent`
- **功能**: 将系统分解为模块
- **调用方式**:
  ```python
  agent = agent_manager.get_agent('modulizer')
  result = await agent.process({'system_description': '系统描述'})
  ```

### 2. Tool 系统集成

原有技能也可以作为工具使用：

#### Context Analyzer 作为工具
- **调用方式**:
  ```python
  tool_manager = ToolManager()
  result = tool_manager.execute_tool('context-analyzer', {'context': '待分析的上下文'})
  ```

#### Constraint Generator 作为工具
- **调用方式**:
  ```python
  result = tool_manager.execute_tool('constraint-generator', {'requirement': '系统需求描述'})
  ```

### 3. Hook 系统集成

原有技能可以通过 Hook 系统在特定事件发生时自动执行：

#### 示例：在技能执行后运行分析
```python
def post_skill_analysis(context: HookContext):
    if context.hook_name == 'skill_after_invoke':
        # 在技能执行后进行额外处理
        skill_result = context.data.get('result')
        # 执行后分析逻辑
```

## 新架构中的工作流程

### 1. 传统技能调用流程
```
用户请求 -> 技能接口 -> 技能执行 -> 返回结果
```

### 2. 新架构中的技能调用流程
```
用户请求 -> Sisyphus编排器 -> Agent/Tool选择 -> Hook触发 -> 结果返回
```

### 3. 具体示例：Context Analysis 工作流程

1. **请求进入**: 用户请求进行上下文分析
2. **编排器调度**: SisyphusOrchestrator 接收请求并调度
3. **Agent执行**: ContextAnalyzerAgent 处理请求
4. **Hook触发**: 
   - `agent_before_process`: 代理处理前Hook
   - `agent_context_updated`: 上下文更新Hook
   - `agent_after_process`: 代理处理后Hook
5. **结果返回**: 返回结构化分析结果

## 适配器模式详解

### DnaSpecSkillAdapter 类

该类负责将原有技能适配到新架构中：

```python
skill_adapter = DnaSpecSkillAdapter()
```

#### 主要功能：
1. `_register_skills_as_agents()`: 将技能注册为Agent
2. `_register_skills_as_tools()`: 将技能注册为Tool
3. `_register_skills_as_hooks()`: 将技能注册为Hook回调

## 向后兼容性

新架构保持了对原有技能的向后兼容性：

1. **API兼容**: 原有的技能调用接口仍然有效
2. **参数兼容**: 原有的参数格式不变
3. **结果兼容**: 原有的结果格式保持一致

## 扩展性

新架构允许轻松添加新的技能：

1. **创建新Agent**: 继承BaseAgent类
2. **注册到系统**: 使用AgentManager注册
3. **Hook集成**: 可选地注册相关Hook

## 性能优化

1. **异步支持**: 所有Agent和Hook都支持异步执行
2. **并发控制**: BackgroundTaskManager管理并发任务
3. **资源管理**: ContextWindowMonitor监控资源使用

## 总结

新架构通过适配器模式将原有技能无缝集成，同时提供了更强的扩展性、更好的模块化和更丰富的功能。原有技能的功能得到保留，同时获得了新架构的所有优势。