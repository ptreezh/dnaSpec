# DNASPEC Context Engineering Skills - 本地部署和使用指南

## 1. 系统要求

- Python 3.8 或更高版本
- Windows/macOS/Linux 操作系统
- 至少 500MB 可用磁盘空间
- 至少 1GB 可用内存

## 2. 安装步骤

### 2.1 克境准备
```bash
# 1. 进入项目目录
cd D:\DAIP\dnaSpec

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. 安装项目依赖
pip install -e .
```

### 2.2 验证安装
```bash
# 运行测试验证功能是否正常
python -m pytest tests/test_context_analysis_skill.py -v
python -m pytest tests/test_context_optimization_skill.py -v
python -m pytest tests/test_cognitive_template_skill.py -v
```

## 3. 系统功能概览

### 3.1 Context Analysis Skill
- **功能**: 自动分析上下文质量，评估清晰度、相关性、完整性等五个维度
- **应用场景**: 质量评估、输入验证、改进建议

### 3.2 Context Optimization Skill
- **功能**: 基于分析结果优化上下文内容
- **应用场景**: 上下文改进、清晰度提升、完整性补充

### 3.3 Cognitive Template Skill
- **功能**: 应用认知模板结构化复杂任务
- **应用场景**: 思维链、验证框架、少样本学习

## 4. 使用方法

### 4.1 在Python代码中使用

```python
# 导入所需技能
from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
from src.context_engineering_skills.context_optimization import ContextOptimizationSkill
from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill

# 1. 使用Context Analysis
skill = ContextAnalysisSkill()
result = skill.process_request("设计一个用户系统", {})
print(result.result)  # 输出分析结果

# 2. 使用Context Optimization
skill = ContextOptimizationSkill()
result = skill.process_request("系统要处理用户", {'optimization_goals': ['clarity', 'completeness']})
print(result.result['optimized_context'])  # 输出优化后的上下文

# 3. 使用Cognitive Template
skill = CognitiveTemplateSkill()
result = skill.process_request("如何设计系统？", {'template': 'chain_of_thought'})
print(result.result['enhanced_context'])  # 输出结构化后的上下文
```

### 4.2 直接函数调用

```python
from src.context_engineering_skills.context_analysis import execute as analysis_execute
from src.context_engineering_skills.context_optimization import execute as optimization_execute
from src.context_engineering_skills.cognitive_template import execute as template_execute

# 分析上下文
result = analysis_execute({"context": "系统设计要求"})

# 优化上下文
result = optimization_execute({"context": "待优化内容", "optimization_goals": "clarity,completeness"})

# 应用认知模板
result = template_execute({"context": "任务描述", "template": "chain_of_thought"})
```

## 5. 核心功能详解

### 5.1 Context Analysis 五个维度指标
- **Clarity (清晰度)**: 上下文表达的明确性
- **Relevance (相关性)**: 与目标任务的关联性
- **Completeness (完整性)**: 关键要素的完备性
- **Consistency (一致性)**: 陈述内容的逻辑一致性
- **Efficiency (效率)**: 信息密度和简洁性

### 5.2 Context Optimization 优化目标
- **Clarity**: 提高表达明确性
- **Completeness**: 补充缺失信息
- **Relevance**: 增强目标相关性
- **Conciseness**: 提高简洁性

### 5.3 Cognitive Template 类型
- **Chain of Thought**: 思维链推理模式
- **Few Shot**: 少样本学习模式
- **Verification**: 验证检查模式
- **Role Playing**: 角色扮演模式
- **Understanding**: 深入理解模式

## 6. 实际应用场景

### 6.1 AI 辅助开发
- 优化 prompt 质量
- 结构化复杂任务
- 提高 AI 输出质量

### 6.2 项目管理
- 任务分解优化
- 需求文档质量评估
- 项目上下文管理

### 6.3 内容创作
- 文章结构优化
- 逻辑梳理
- 内容完整性检查

## 7. 配置和自定义

### 7.1 默认配置文件位置
- 配置文件: `src/context_engineering_skills/config.py`
- 可以修改默认参数和阈值

### 7.2 自定义模板
- 在 `src/context_engineering_skills/templates/` 目录下添加自定义模板
- 遢照现有模板的格式创建新模板

## 8. 性能和限制

### 8.1 性能指标
- 小析速度: < 500ms (普通上下文)
- 优化速度: < 800ms (普通上下文)
- 模板应用: < 200ms

### 8.2 使用限制
- 上下文长度限制: < 50,000 字符
- 建议单次处理 < 10,000 字符

## 9. 故障排除

### 9.1 常见错误
- **ImportError**: 确保已激活虚拟环境
- **MemoryError**: 处理过长文本，请缩短输入
- **TimeoutError**: 检查系统资源使用情况

### 9.2 性能问题
- 使用缓存机制避免重复计算
- 对大文本进行分段处理
- 调整并发处理数量

## 10. 开发和扩展

### 10.1 添加新技能
1. 在 `src/context_engineering_skills/` 目录下创建新技能文件
2. 继承 `DNASpecSkill` 基类
3. 实现 `_execute_skill_logic` 方法
4. 添加对应的测试

### 10.2 贡献指南
- 编写单元测试
- 遢循代码风格规范
- 更新文档

## 11. 维护和支持

### 11.1 日志记录
- 系统日志位于 `logs/` 目录
- 记录所有技能执行情况

### 11.2 监控指标
- 执行时间
- 成功率
- 错误率

## 12. 安全注意事项

- 所有输入都会被验证
- 不存储敏感信息
- 遢循最小权限原则

---

**系统已成功部署，可以开始使用。**
**如遇问题，请参阅故障排除章节或联系技术支持。**