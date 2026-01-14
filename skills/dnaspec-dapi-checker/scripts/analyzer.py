from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class CheckAnalysis:
    check_level: str
    check_types: List[str]
    recommendations: List[str]

class DAPICheckerAnalyzer:
    def analyze(self, request: str, context: Optional[Dict] = None) -> CheckAnalysis:
        levels = []
        if '模块' in request:
            levels.append('module')
        if '子系统' in request:
            levels.append('subsystem')
        if '系统' in request:
            levels.append('system')
        return CheckAnalysis(levels[0] if levels else 'module', ['api_consistency'], [])
