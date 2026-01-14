# Network Computation社会网络计算分析技能规范

## 技能定义
**技能名称**: network-computation  
**中文名称**: 社会网络计算分析专家  
**应用场景**: 网络构建、中心性测量、社区检测、网络可视化等完整的网络分析支持

## 核心功能模块

### 1. 网络类型识别与构建（程序化规则）
```python
def identify_and_construct_network(data_source, network_context):
    """
    程序化的网络类型识别和构建
    返回: {
        "network_type": "social|organizational|knowledge|communication",
        "construction_method": "co-occurrence|interaction|affiliation|citation",
        "network_structure": {...},
        "quality_metrics": {...}
    }
    """
    network_types = {
        "social_network": {
            "data_sources": ["friendship", "family", "colleague", "community"],
            "edge_types": ["strong_tie", "weak_tie", "multiplex", "directed"],
            "construction_rules": ["frequency_threshold", "reciprocity_check", "temporal_consistency"]
        },
        "organizational_network": {
            "data_sources": ["formal_hierarchy", "informal_collaboration", "resource_flow"],
            "edge_types": ["reporting", "collaboration", "knowledge_sharing", "influence"],
            "construction_rules": ["organizational_boundaries", "role_consistency", "resource_threshold"]
        },
        "knowledge_network": {
            "data_sources": ["co_authorship", "citation", "knowledge_transfer", "expertise"],
            "edge_types": ["knowledge_flow", "collaboration", "influence", "similarity"],
            "construction_rules": ["knowledge_domains", "expertise_level", "temporal_decay"]
        }
    }
```

### 2. 渐进式网络分析（渐进式披露）
```python
class ProgressiveNetworkAnalysis:
    def __init__(self):
        self.analysis_levels = [
            "basic_descriptives",      # 基础描述性分析
            "centrality_analysis",     # 中心性分析
            "community_detection",     # 社区检测
            "structural_dynamics",      # 结构动态分析
            "network_interpretation"   # 网络解释
        ]
    
    def tiered_analysis(self, network_data, research_objectives, analysis_depth):
        """
        渐进式披露：根据深度需求提供不同层次的网络分析
        depth=1: 基础网络描述和可视化
        depth=2: 中心性分析和关键节点识别
        depth=3: 社区结构和子群分析
        depth=4: 网络动力学和演化分析
        depth=5: 深度社会学解释
        """
        if analysis_depth == 1:
            return self.basic_network_descriptives(network_data)
        elif analysis_depth == 2:
            return self.centrality_and_position_analysis(network_data)
        elif analysis_depth == 3:
            return self.community_and_subgroup_analysis(network_data)
        elif analysis_depth == 4:
            return self.network_dynamics_analysis(network_data, research_objectives)
        else:
            return self.comprehensive_network_interpretation(network_data, research_objectives)
```

### 3. 中心性与权力分析（定性定量结合）
```python
class CentralityPowerAnalysis:
    def __init__(self):
        self.quantitative_measures = {
            "degree_centrality": {
                "calculation": "standard",
                "interpretation": "local_importance",
                "applications": ["influence_spread", "vulnerability_assessment"]
            },
            "betweenness_centrality": {
                "calculation": "standard|weighted",
                "interpretation": "brokerage_control",
                "applications": ["information_control", "structural_holes"]
            },
            "eigenvector_centrality": {
                "calculation": "iterative",
                "interpretation": "prestige_importance",
                "applications": ["influence_amplitude", "network_elites"]
            },
            "closeness_centrality": {
                "calculation": "inverse_shortest_path",
                "interpretation": "access_efficiency",
                "applications": ["information_speed", "resource_optimization"]
            }
        }
        
        self.qualitative_insights = {
            "power_structures": ["centralization_patterns", "hierarchical_organization", "elite_cohesion"],
            "control_mechanisms": ["gatekeeping", "agenda_setting", "resource_distribution"],
            "vulnerability_points": ["critical_nodes", "network_bottlenecks", "cascading_risks"]
        }
    
    def mixed_methods_centrality_analysis(self, network_data, social_context):
        """
        定性定量有机结合的中心性分析
        """
        # 定量部分：标准中心性计算
        quant_results = self.calculate_all_centralities(network_data)
        
        # 定性部分：基于规则的社会学权力分析
        qual_context = self.prepare_power_context(network_data, social_context)
        qual_insights = self.ai_power_structure_analysis(qual_context)
        
        return self.integrated_power_analysis(quant_results, qual_insights)
```

### 4. 社区检测与结构分析（程序化+定性）
```python
class CommunityDetection:
    def __init__(self):
        self.detection_algorithms = {
            "modularity_based": ["louvain", "leiden", "walktrap"],
            "hierarchical": ["agnes", "diana", "hierarchical_clustering"],
            "density_based": ["clique_percolation", "core_periphery", "k_core"],
            "spectral": ["spectral_clustering", "normalized_cut", "markov_clustering"]
        }
        
        self.community_properties = {
            "structural": ["modularity", "conductance", "expansion", "internal_density"],
            "semantic": ["thematic_cohesion", "identity_alignment", "shared_goals"],
            "functional": ["collaboration_patterns", "resource_sharing", "knowledge_flow"]
        }
    
    def comprehensive_community_analysis(self, network_data, detection_parameters, interpretation_context):
        """
        综合性社区检测和结构分析
        """
        structural_communities = self.detect_communities_structural(network_data, detection_parameters)
        semantic_communities = self.detect_communities_semantic(network_data, interpretation_context)
        functional_communities = self.detect_communities_functional(network_data, interpretation_context)
        
        return {
            "structural_clusters": structural_communities,
            "semantic_groups": semantic_communities,
            "functional_communities": functional_communities,
            "integrated_interpretation": self.integrate_community_findings(...)
        }
```

## 渐进式披露设计

### 层次1：基础网络描述
- **必需上下文**：边和节点列表
- **输出**：网络基本统计和简单可视化
- **程序化程度**：95%

### 层次2：中心性位置分析
- **必需上下文**：完整网络结构
- **输出**：各种中心性指标和关键节点
- **程序化程度**：85%

### 层次3：社区结构识别
- **必需上下文**：网络+节点属性
- **输出**：社区结构和子群特征
- **程序化程度**：70%

### 层次4：网络动力学分析
- **必需上下文**：时间序列网络数据
- **输出**：网络演化模式和趋势
- **程序化程度**：50%

### 层次5：社会学深度解释
- **必需上下文**：网络数据+社会背景
- **输出**：权力结构和机制解释
- **程序化程度**：30%

## 大规模网络处理策略

### 分层计算方法
```python
class LargeScaleNetworkProcessing:
    def __init__(self):
        self.scaling_strategies = {
            "sampling_methods": ["node_sampling", "edge_sampling", "snowball_sampling"],
            "approximation_algorithms": ["approximate_centrality", "streaming_algorithms", "parallel_processing"],
            "decomposition_methods": ["community_decomposition", "core_periphery_split", "layered_analysis"]
        }
    
    def scalable_analysis(self, large_network, computational_constraints):
        """
        大规模网络的可扩展分析
        """
        network_size = len(large_network.nodes())
        if network_size > 100000:
            return self.distributed_analysis(large_network)
        elif network_size > 10000:
            return self.approximate_analysis(large_network)
        else:
            return self.exact_analysis(large_network)
```

### 内存优化算法
```python
class MemoryOptimizedNetworkAnalysis:
    def memory_efficient_algorithms(self):
        return {
            "streaming_centrality": "增量中心性计算",
            "incremental_clustering": "动态社区检测",
            "sparse_matrix_operations": "稀疏矩阵优化",
            "network_compression": "网络压缩技术"
        }
```

## 规则提示词模板

### 网络构建提示词
```
你是一位社会网络分析专家，正在从以下数据构建网络：

**数据来源**: {data_source}
**网络背景**: {network_context}
**分析目标**: {analysis_objectives}

请确定：
1. 这是什么类型的网络？（社交/组织/知识/传播）
2. 如何定义节点和边？
3. 网络构建的合理阈值是什么？
4. 如何处理网络的质量问题？

基于网络分析原则，提供：
- 节点和边的操作化定义
- 数据清洗和处理建议
- 网络质量评估标准
- 构建方法的理论依据
```

### 网络解释提示词
```
基于网络分析结果，提供社会学深度解释：

**网络指标**: {network_metrics}
**关键节点**: {key_nodes}
**社区结构**: {community_structure}
**社会背景**: {social_context}

请解释：
1. 网络结构的形成机制
2. 权力关系的分布特征
3. 资源流动的模式和障碍
4. 网络演化的潜在趋势

结合社会学理论，分析：
- 社会资本的形成和分布
- 结构洞的机会和约束
- 网络闭合与桥接的平衡
- 网络效应的边界条件
```

## 应用场景映射

### 组织网络分析
```python
class OrganizationalNetworkAnalysis(NetworkComputation):
    def specialized_methods(self):
        return {
            "formal_structure": ["hierarchy_analysis", "span_of_control", "departmental_boundaries"],
            "informal_networks": ["friendship_ties", "advice_seeking", "communication_patterns"],
            "performance_analysis": ["innovation_diffusion", "knowledge_sharing", "collaborative_effectiveness"],
            "change_management": ["network_resilience", "influence_identification", "barrier_analysis"]
        }
```

### 学术合作网络
```python
class AcademicCollaborationNetwork(NetworkComputation):
    def specialized_methods(self):
        return {
            "co_authorship_analysis": ["collaboration_patterns", "interdisciplinary_links", "institutional_boundaries"],
            "citation_networks": ["knowledge_flow", "influence_patterns", "field_evolution"],
            "expertise_networks": ["knowledge_domains", "specialization_patterns", "expertise_diffusion"],
            "innovation_analysis": ["breakthrough_detection", "trend_identification", "emerging_topics"]
        }
```

## 实现规范

### 技能接口
```python
def conduct_network_analysis(
    network_data: dict,
    analysis_objectives: list,
    analysis_depth: int = 1,
    network_type: str = "auto_detect",
    computational_constraints: dict = {}
) -> dict:
    """
    社会网络分析主入口
    
    Args:
        network_data: 网络数据源
        analysis_objectives: 分析目标列表
        analysis_depth: 分析深度 (1-5)
        network_type: 网络类型
        computational_constraints: 计算约束条件
    
    Returns:
        dict: 结构化网络分析结果
    """
```

### 输出格式
```json
{
    "network_construction": {
        "network_type": "...",
        "construction_method": "...",
        "quality_metrics": {...},
        "nodes_and_edges_summary": {...}
    },
    "descriptive_statistics": {
        "basic_measures": {...},
        "density_metrics": {...},
        "connectivity_properties": {...},
        "structural_characteristics": {...}
    },
    "centrality_analysis": {
        "degree_centralities": {...},
        "betweenness_centralities": {...},
        "eigenvector_centralities": {...},
        "key_players_identification": {...}
    },
    "community_structure": {
        "detection_results": {...},
        "community_characteristics": {...},
        "inter_community_relations": {...},
        "functional_interpretations": {...}
    },
    "network_dynamics": {
        "temporal_patterns": {...},
        "evolution_trends": {...},
        "stability_assessment": {...},
        "predictive_indicators": {...}
    },
    "sociological_interpretation": {
        "power_structures": {...},
        "social_capital_distribution": {...},
        "structural_holes_analysis": {...},
        "network_mechanisms": {...}
    }
}
```

## 质量保证

### 验证清单
- [ ] 网络构建有效性
- [ ] 算法选择适当性
- [ ] 结果解释准确性
- [ ] 社会学理论一致性
- [ ] 计算效率评估

### 限制条件
- 网络规模：需要考虑计算复杂度
- 数据质量：边和节点的完整性要求
- 因果推断：网络结构≠因果关系
- 隐私保护：敏感节点和边处理

## 工具集成

### 网络可视化引擎
```python
def generate_network_visualization(network_data, visualization_parameters):
    """
    生成网络可视化
    """
    return {
        "layout_algorithms": ["force_directed", "circular", "hierarchical", "community_based"],
        "interactive_features": ["node_selection", "path_highlighting", "community_exploration"],
        "visual_encodings": ["size_encoding", "color_encoding", "shape_encoding", "edge_weight"]
    }
```

### 网络比较工具
```python
def compare_networks(network_list, comparison_metrics):
    """
    多网络比较分析
    """
    return {
        "structural_similarity": {...},
        "role_equivalence": {...},
        "evolution_patterns": {...},
        "cross_network_insights": {...}
    }
```