# DSGS Context Engineering Skills - 快速安装和使用指南

## 概述

DSGS Context Engineering Skills 是一个为AI CLI平台设计的上下文工程增强工具集，它利用AI模型的原生智能，通过标准化指令模板，实现上下文分析、优化和结构化功能。

## 安装

### 1. 克隆项目
```bash
git clone https://your-git-server/dsgs-context-engineering.git
cd dsgs-context-engineering
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -e .
```

## 配置AI模型API

### 1. Anthropic Claude
```bash
export ANTHROPIC_API_KEY=your-anthropic-api-key
```

### 2. Google Gemini  
```bash
export GOOGLE_API_KEY=your-google-api-key
```

### 3. OpenAI GPT
```bash
export OPENAI_API_KEY=your-openai-api-key
```

### 4. 阿里云通义千问
```bash
export DASHSCOPE_API_KEY=your-dashscope-api-key
```

## 快速使用示例

### 1. 在Python代码中使用

```python
from dsgs_context_engineering import analyze_context, optimize_context, apply_cognitive_template

# 设置API密钥
API_KEY = "your-api-key-here"

# 1. 分析上下文质量
context = "设计一个电商平台，支持用户注册、商品浏览、购物车、订单处理等功能。"
analysis = analyze_context(context, api_key=API_KEY, provider="anthropic")
print(analysis)

# 2. 优化上下文内容
optimized = optimize_context(
    context, 
    goals=['clarity', 'completeness'], 
    api_key=API_KEY, 
    provider="anthropic"
)
print(optimized)

# 3. 应用认知模板
result = apply_cognitive_template(
    "如何提高系统性能？", 
    template="chain_of_thought",
    api_key=API_KEY, 
    provider="anthropic"
)
print(result)
```

### 2. 使用技能系统

```python
from dsgs_context_engineering import create_context_engineering_system

# 创建系统实例
system = create_context_engineering_system("anthropic", "your-api-key")

# 使用技能管理器
result = system.skills_manager.execute_skill(
    'context-analysis',
    "需要开发一个任务管理系统", 
    {}
)
print(result)
```

### 3. 在AI CLI中使用

```bash
# 假设AI CLI支持DSL风格的技能调用
claude messages stream --model claude-3-haiku -s "使用DSGS上下文分析技能分析：设计一个电商系统，需要支持用户认证、商品管理、订单处理功能"
```

## 核心功能

### 1. Context Analysis Skill
- **功能**：分析上下文的5个维度质量
  - 清晰度 (Clarity)
  - 相关性 (Relevance) 
  - 完整性 (Completeness)
  - 一致性 (Consistency)
  - 效率 (Efficiency)
- **使用**：评估任何上下文的质量并获得优化建议

### 2. Context Optimization Skill  
- **功能**：基于分析结果优化上下文
  - 清晰度优化
  - 完整性补全
  - 相关性加强
  - 简洁性改进
- **使用**：改进上下文质量以获得更好的AI响应

### 3. Cognitive Template Skill
- **功能**：应用认知模板到任务
  - 思维链 (Chain of Thought)
  - 少示例学习 (Few-shot Learning)
  - 验证检查 (Verification Check)
  - 角色扮演 (Role Playing)
  - 理解框架 (Understanding Framework)
- **使用**：结构化复杂任务，提升推理质量

## 系统集成

### 与AI CLI平台集成
技能系统设计为可以与各种AI CLI平台集成：

- Claude CLI: 通过指令模板集成
- Gemini CLI: 通过Google API集成  
- 通义CLI: 通过DashScope API集成
- 其他平台: 通过通用API适配器集成

### 工作流程
1. 用户提供上下文
2. 选择适当技能
3. 系统构造AI指令模板
4. 发送到AI模型
5. 解析结构化响应
6. 返回结构化结果

## 性能指标

- **响应时间**: 通常在AI模型响应时间范围内（2-10秒）
- **准确性**: 依赖于底层AI模型的智能水平
- **兼容性**: 支持所有主流AI模型API
- **可扩展性**: 支持新的认知模板和优化策略

## 故障排除

### 常见问题
- **API密钥错误**: 确认环境变量正确设置
- **网络连接问题**: 检查网络连接和API服务状态
- **上下文过长**: 超过模型限制时会截断或报错

### 错误处理
系统提供详细的错误信息和状态码，便于调试集成问题。

## 许可证

MIT License - 详见 LICENSE 文件