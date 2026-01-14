from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class AgentMetrics:
    token_count: int
    complexity_score: float
    has_code_agent: bool
    has_test_agent: bool
    has_doc_agent: bool
    recommended_level: str
    estimated_agents: int
    recommendations: List[str]

class AgentCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> AgentMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)
        
        has_code = any(kw in request.lower() for kw in ['代码', 'code', '审查', 'review'])
        has_test = any(kw in request.lower() for kw in ['测试', 'test'])
        has_doc = any(kw in request.lower() for kw in ['文档', 'doc'])
        
        level = '00' if complexity < 0.3 else '01' if complexity < 0.6 else '02'
        
        return AgentMetrics(
            token_count=token_count,
            complexity_score=complexity,
            has_code_agent=has_code,
            has_test_agent=has_test,
            has_doc_agent=has_doc,
            recommended_level=level,
            estimated_agents=1,
            recommendations=[]
        )
