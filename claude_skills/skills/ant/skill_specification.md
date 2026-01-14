# ANT行动者网络理论技能规范

## 技能定义
**技能名称**: ant  
**中文名称**: 行动者网络理论分析专家  
**应用场景**: 科技政策、医疗健康、环境治理、数字化转型等领域的ANT分析

## 核心功能模块

### 1. 行动者识别模块（程序化规则）
```python
def identify_actors(context_text, domain_type):
    """
    程序化的行动者识别规则
    返回: {
        "human_actors": [],
        "nonhuman_actors": [],
        "controversy_points": []
    }
    """
    # 确定性规则：基于关键词和语法模式识别
    patterns = {
        "human": ["专家", "决策者", "用户", "研究者", "管理者"],
        "nonhuman": ["技术", "法规", "数据", "设备", "标准"],
        "controversy": ["争议", "冲突", "矛盾", "博弈", "协商"]
    }
```

### 2. 转译过程分析（渐进式披露）
```python
class TranslationAnalyzer:
    def __init__(self):
        self.stages = [
            "problematisation",  # 问题化
            "interessement",     # 激励
            "enrollment",        # 招募
            "mobilization"       # 动员
        ]
    
    def progressive_analysis(self, actors_network, depth=1):
        """
        渐进式披露：根据深度需求逐步加载分析层次
        depth=1: 基础转译阶段识别
        depth=2: 阶段间关系分析
        depth=3: 权力动态和策略分析
        """
        if depth == 1:
            return self.identify_stages(actors_network)
        elif depth == 2:
            return self.analyze_transitions(actors_network)
        else:
            return self.analyze_power_dynamics(actors_network)
```

### 3. 网络构建追踪（定性定量结合）
```python
class NetworkTracker:
    def __init__(self):
        self.quantitative_metrics = [
            "network_density",      # 网络密度
            "centrality_measures",  # 中心性测量
            "path_length",         # 路径长度
            "clustering_coeff"     # 聚类系数
        ]
        
        self.qualitative_aspects = [
            "actor_legitimacy",     # 行动者合法性
            "controversy_intensity", # 争议强度
            "stability_level",      # 稳定性水平
            "enrollment_strategies" # 招募策略
        ]
    
    def mixed_methods_analysis(self, network_data):
        """
        定性定量有机结合分析
        """
        # 定量部分：确定性计算
        quant_results = self.calculate_metrics(network_data)
        
        # 定性部分：基于规则提示词的AI分析
        qual_context = self.prepare_qualitative_context(network_data)
        qual_results = self.ai_qualitative_analysis(qual_context)
        
        return self.integrate_findings(quant_results, qual_results)
```

## 渐进式披露设计

### 层次1：基础行动者识别
- **必需上下文**：最小文本片段
- **输出**：行动者清单和基本分类
- **程序化程度**：80%

### 层次2：转译阶段分析
- **必需上下文**：行动者互动描述
- **输出**：转译过程阶段图
- **程序化程度**：60%

### 层次3：网络动态分析
- **必需上下文**：完整案例描述
- **输出**：网络演化轨迹
- **程序化程度**：40%

### 层次4：策略性洞察
- **必需上下文**：历史+背景信息
- **输出**：策略建议和预测
- **程序化程度**：20%

## 规则提示词模板

### 定性分析提示词
```
你是一位ANT理论专家，正在分析以下行动者网络：

**行动者清单**: {actors_list}
**关系数据**: {relations_data}
**背景信息**: {background}

请从以下角度进行定性分析：
1. 行动者合法性基础
2. 争议焦点和权力不平衡
3. 转译策略的有效性
4. 网络稳定性评估

基于ANT理论框架，提供结构化分析，重点关注：
- 异质性如何被管理
- 黑箱化过程
- 不可逆点的形成
```

### 定量验证提示词
```
基于以下网络指标：
- 网络密度: {density}
- 中心性分布: {centrality}
- 聚类系数: {clustering}

请验证以下假设：
1. 网络是否呈现核心-边缘结构
2. 是否存在关键节点依赖
3. 网络脆弱性点在哪里

结合定性发现，解释这些指标的意义。
```

## 应用场景映射

### 科技政策分析
```python
class TechPolicyANT(ANTAnalyzer):
    def specialized_patterns(self):
        return {
            "actors": ["政策制定者", "技术公司", "研究机构", "用户群体"],
            "controversies": ["技术伦理", "数据隐私", "技术标准"],
            "translation_points": ["政策制定", "标准设立", "市场接受"]
        }
```

### 医疗健康分析
```python
class HealthcareANT(ANTAnalyzer):
    def specialized_patterns(self):
        return {
            "actors": ["医生", "患者", "设备", "药品", "监管机构"],
            "controversies": ["治疗方案", "资源分配", "医疗伦理"],
            "translation_points": ["诊断标准", "治疗协议", "健康管理"]
        }
```

## 实现规范

### 技能接口
```python
def execute_ant_analysis(
    input_text: str,
    analysis_depth: int = 1,
    domain_context: str = "general",
    quantitative_focus: bool = False
) -> dict:
    """
    ANT分析主入口
    
    Args:
        input_text: 待分析文本
        analysis_depth: 分析深度 (1-4)
        domain_context: 领域上下文
        quantitative_focus: 是否侧重定量分析
    
    Returns:
        dict: 结构化分析结果
    """
```

### 输出格式
```json
{
    "actors": {
        "human": [...],
        "nonhuman": [...],
 "key_controversy_points": [...]
    },
    "translation_stages": {
        "problematisation": {...},
        "interessement": {...},
        "enrollment": {...},
        "mobilization": {...}
    },
    "network_metrics": {
        "quantitative": {...},
        "qualitative_assessments": {...}
    },
    "strategic_insights": [...],
    "confidence_score": 0.85
}
```

## 质量保证

### 验证清单
- [ ] 行动者异质性充分体现
- [ ] 转译过程完整性
- [ ] 定性定量逻辑一致性
- [ ] 渐进式披露适当性
- [ ] 领域适配准确性

### 限制条件
- 最大文本长度: 50,000字符
- 建议分析深度: 从1开始渐进
- 网络规模: 建议<100个节点
- 时间范围: 单个案例完整周期