# Conflict Resolution分歧解决技能规范

## 技能定义
**技能名称**: conflict-resolution  
**中文名称**: 研究分歧解决专家  
**应用场景**: 学术研究中的理论、方法论、解释、价值观等分歧解决

## 核心功能模块

### 1. 分歧类型识别模块（程序化规则）
```python
def identify_conflict_type(dispute_text, academic_domain):
    """
    程序化的分歧类型识别
    返回: {
        "conflict_type": "theoretical|methodological|interpretive|value_based",
        "confidence": float,
        "key_dimensions": [],
        "resolution_strategies": []
    }
    """
    conflict_patterns = {
        "theoretical": ["理论框架", "概念定义", "假设前提", "理论逻辑"],
        "methodological": ["研究方法", "数据收集", "分析技术", "验证标准"],
        "interpretive": ["结果解释", "意义建构", "结论推导", "证据权重"],
        "value_based": ["价值取向", "伦理立场", "文化背景", "社会影响"]
    }
```

### 2. 建设性对话框架（渐进式披露）
```python
class ConstructiveDialogueFramework:
    def __init__(self):
        self.dialogue_stages = [
            "perspective_clarification",  # 视角澄清
            "common_ground_identification", # 共同基础识别
            "difference_acknowledgment",   # 差异承认
            "integrative_synthesis",       # 整合综合
            "consensus_building"           # 共识建立
        ]
    
    def progressive_facilitation(self, conflict_data, engagement_level):
        """
        渐进式披露：根据参与程度提供不同层次的对话支持
        level=1: 基础问题引导
        level=2: 结构化对话模板
        level=3: 深度整合策略
        """
        if engagement_level == 1:
            return self.provide_questioning_framework(conflict_data)
        elif engagement_level == 2:
            return self.structured_dialogue_template(conflict_data)
        else:
            return self.integrative_synthesis_strategy(conflict_data)
```

### 3. 共识建立度量（定性定量结合）
```python
class ConsensusMetrics:
    def __init__(self):
        self.quantitative_indicators = [
            "position_convergence",     # 立场收敛度
            "argument_diversity",       # 论点多样性
            "evidence_agreement",       # 证据一致性
            "resolution_satisfaction"  # 解决方案满意度
        ]
        
        self.qualitative_assessments = [
            "dialogue_quality",         # 对话质量
            "mutual_understanding",     # 相互理解
            "intellectual_honesty",     # 知识诚实性
            "creative_potential"        # 创造性潜力
        ]
    
    def mixed_methods_evaluation(self, dialogue_history, consensus_outcome):
        """
        定性定量有机结合的共识评估
        """
        # 定量部分：可计算的收敛指标
        quant_metrics = self.calculate_convergence_metrics(dialogue_history)
        
        # 定性部分：基于规则的AI质量评估
        qual_context = self.prepare_dialogue_context(dialogue_history)
        qual_assessment = self.ai_quality_analysis(qual_context)
        
        return self.integrated_consensus_assessment(quant_metrics, qual_assessment)
```

## 渐进式披露设计

### 层次1：分歧基础识别
- **必需上下文**：分歧描述文本
- **输出**：分歧类型和关键维度
- **程序化程度**：90%

### 层次2：对话策略设计
- **必需上下文**：分歧双方立场
- **输出**：结构化对话框架
- **程序化程度**：70%

### 层次3：深度整合分析
- **必需上下文**：对话记录和论据
- **输出**：整合方案和评估
- **程序化程度**：50%

### 层次4：战略级解决方案
- **必需上下文**：完整分歧解决过程
- **输出**：长期共识策略
- **程序化程度**：30%

## 规则提示词模板

### 分歧分析提示词
```
你是一位学术分歧解决专家，正在分析以下学术争议：

**争议主题**: {dispute_topic}
**各方立场**: {positions}
**核心论据**: {arguments}

请从以下维度进行结构化分析：
1. 分歧根本原因（理论/方法/解释/价值）
2. 各立场合理性基础
3. 潜在的共同点或兼容性
4. 解决障碍和促进因素

基于建设性对话原则，提供：
- 中立的框架描述
- 无评判的立场呈现
- 寻找整合可能性的路径
```

### 对话促进提示词
```
基于分歧分析结果，设计建设性对话策略：

**分歧类型**: {conflict_type}
**核心争议点**: {core_issues}
**参与方背景**: {participant_background}

请设计层次化对话方案：
1. 开场问题设定（避免预设立场）
2. 渐进式深度探讨
3. 转换视角的引导技巧
4. 整合性思考的激发方式

重点关注：
- 如何建立信任氛围
- 如何避免防御性反应
- 如何促进深度倾听
- 如何寻找创造性解决方案
```

## 应用场景映射

### 理论分歧解决
```python
class TheoreticalConflictResolver(ConflictResolver):
    def specialized_strategies(self):
        return {
            "identification": [
                "概念定义差异",
                "理论假设冲突", 
                "逻辑框架对立",
                "解释层次不同"
            ],
            "resolution_approaches": [
                "概念澄清和重新定义",
                "理论边界划定",
                "多层次整合框架",
                "元理论对话"
            ]
        }
```

### 方法论分歧解决
```python
class MethodologicalConflictResolver(ConflictResolver):
    def specialized_strategies(self):
        return {
            "identification": [
                "研究范式差异",
                "数据收集方法冲突",
                "分析技术对立",
                "效度标准不同"
            ],
            "resolution_approaches": [
                "方法适用边界讨论",
                "混合方法设计",
                "三角验证策略",
                "方法互补框架"
            ]
        }
```

## 实现规范

### 技能接口
```python
def resolve_academic_conflict(
    dispute_description: str,
    participants_info: dict,
    resolution_goal: str = "mutual_understanding",
    facilitation_depth: int = 1,
    evaluation_focus: str = "balanced"
) -> dict:
    """
    学术分歧解决主入口
    
    Args:
        dispute_description: 分歧描述
        participants_info: 参与者信息
        resolution_goal: 解决目标类型
        facilitation_depth: 促进深度 (1-4)
        evaluation_focus: 评估重点
    
    Returns:
        dict: 结构化解决结果
    """
```

### 输出格式
```json
{
    "conflict_analysis": {
        "type": "theoretical|methodological|interpretive|value_based",
        "dimensions": [...],
        "key_positions": [...],
        "common_grounds": [...]
    },
    "dialogue_framework": {
        "stages": [...],
        "facilitation_questions": [...],
        "transition_strategies": [...]
    },
    "resolution_outcome": {
        "consensus_points": [...],
        "remaining_differences": [...],
        "integrative_insights": [...]
    },
    "evaluation_metrics": {
        "quantitative_indicators": {...},
        "qualitative_assessments": {...}
    }
}
```

## 质量保证

### 验证清单
- [ ] 分歧类型准确性
- [ ] 中立性保持
- [ ] 建设性导向
- [ ] 文化敏感性
- [ ] 可操作性评估

### 限制条件
- 复杂度限制：建议单一争议焦点
- 参与人数：建议2-5方
- 对话轮次：建议结构化8-12轮
- 时间框架：建议集中讨论2-4小时

## 工具集成

### 对话记录分析
```python
def analyze_dialogue_progress(dialogue_transcript, baseline_assessment):
    """
    分析对话进展和共识建立
    """
    return {
        "position_shifts": [...],
        "understanding_development": [...],
        "emergent_consensus": [...],
        "remaining_gaps": [...]
    }
```

### 解决方案质量评估
```python
def evaluate_resolution_quality(resolution_outcome, initial_conflict):
    """
    评估解决方案质量和可持续性
    """
    return {
        "completeness_score": float,
        "fairness_assessment": str,
        "sustainability_prediction": str,
        "learning_outcomes": [...]
    }
```