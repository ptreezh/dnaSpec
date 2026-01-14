from typing import Dict, Any, Optional
from pathlib import Path
from .validator import ArchitectValidator
from .calculator import CoordinationCalculator
from .analyzer import CoordinationAnalyzer

class ArchitectExecutor:
    def __init__(self, skill_dir: Optional[Path] = None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent
        self.skill_dir = Path(skill_dir)
        self.prompts_dir = self.skill_dir / 'prompts'
        self.validator = ArchitectValidator()
        self.calculator = CoordinationCalculator()
        self.analyzer = CoordinationAnalyzer()
    
    def execute(self, request: str, context: Optional[Dict] = None, force_level: Optional[str] = None) -> Dict[str, Any]:
        validation = self.validator.validate(request, context)
        if not validation.is_valid:
            return {'success': False, 'validation': validation, 'error': '验证失败'}
        
        metrics = self.calculator.calculate(request, context)
        analysis = self.analyzer.analyze(request, context)
        level = force_level or metrics.recommended_level
        
        prompt = self._load_prompt(level)
        recommendations = metrics.recommendations + analysis.recommendations
        
        return {
            'success': True,
            'validation': validation,
            'metrics': metrics,
            'analysis': analysis,
            'prompt_level': level,
            'prompt_content': prompt,
            'recommendations': recommendations
        }
    
    def _load_prompt(self, level: str) -> str:
        filename_map = {'00': '00_context.md', '01': '01_basic.md', '02': '02_intermediate.md', '03': '03_advanced.md'}
        prompt_file = self.prompts_dir / filename_map.get(level, '00_context.md')
        if not prompt_file.exists():
            prompt_file = self.prompts_dir / '00_context.md'
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
