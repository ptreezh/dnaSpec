from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class CheckMetrics:
    token_count: int
    complexity_score: float
    has_module_check: bool
    has_subsystem_check: bool
    has_system_check: bool
    recommended_level: str
    recommendations: List[str]

class DAPICheckerCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> CheckMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)
        has_module = '模块' in request or 'module' in request.lower()
        has_subsystem = '子系统' in request or 'subsystem' in request.lower()
        has_system = '系统' in request or 'system' in request.lower()
        level = '00' if complexity < 0.3 else '01' if complexity < 0.6 else '02'
        return CheckMetrics(token_count, complexity, has_module, has_subsystem, has_system, level, [])
