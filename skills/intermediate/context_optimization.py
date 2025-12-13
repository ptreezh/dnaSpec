"""
Context Optimization Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any, List
from ..skill_base import BaseSkill, DetailLevel
import re


class ContextOptimizationSkill(BaseSkill):
    """Context Optimization Skill"""

    def __init__(self):
        super().__init__(
            name="context-optimization",
            description="Optimize context quality, enhance dimensions such as clarity, relevance, completeness, etc."
        )
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel,
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute context optimization logic"""
        # Get optimization goals
        optimization_goals = options.get("optimization_goals", ["clarity", "completeness"])
        if isinstance(optimization_goals, str):
            optimization_goals = [g.strip() for g in optimization_goals.split(",") if g.strip()]

        # Execute context optimization
        optimized_context = input_text
        applied_optimizations = []

        # Execute optimization based on goals
        if 'clarity' in optimization_goals:
            optimized_context, clarity_ops = self._apply_clarity_optimization(optimized_context)
            applied_optimizations.extend(clarity_ops)

        if 'relevance' in optimization_goals:
            optimized_context, relevance_ops = self._apply_relevance_optimization(optimized_context)
            applied_optimizations.extend(relevance_ops)

        if 'completeness' in optimization_goals:
            optimized_context, completeness_ops = self._apply_completeness_optimization(optimized_context)
            applied_optimizations.extend(completeness_ops)

        if 'conciseness' in optimization_goals:
            optimized_context, conciseness_ops = self._apply_conciseness_optimization(optimized_context)
            applied_optimizations.extend(conciseness_ops)

        # Calculate improvement metrics
        improvement_metrics = self._calculate_improvements(input_text, optimized_context, applied_optimizations)

        return {
            "original_context": input_text,
            "optimized_context": optimized_context,
            "original_length": len(input_text),
            "optimized_length": len(optimized_context),
            "applied_optimizations": applied_optimizations,
            "improvement_metrics": improvement_metrics
        }
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """Format output result based on detail level"""
        if detail_level == DetailLevel.BASIC:
            # Basic level returns only core information
            return {
                "optimized_context": result_data["optimized_context"],
                "main_optimizations": result_data["applied_optimizations"][:3],  # Return only first 3 main optimizations
                "length_improvement": result_data["optimized_length"] - result_data["original_length"]
            }
        elif detail_level == DetailLevel.STANDARD:
            # Standard level returns standard information
            return {
                "optimized_context": result_data["optimized_context"],
                "applied_optimizations": result_data["applied_optimizations"],
                "improvement_metrics": result_data["improvement_metrics"]
            }
        else:  # DETAILED
            # Detailed level returns complete information
            optimization_summary = {
                "total_optimizations": len(result_data["applied_optimizations"]),
                "length_change": {
                    "original": result_data["original_length"],
                    "optimized": result_data["optimized_length"],
                    "difference": result_data["optimized_length"] - result_data["original_length"]
                },
                "optimization_categories": self._categorize_optimizations(result_data["applied_optimizations"])
            }

            return {
                "original_context": result_data["original_context"],
                "optimized_context": result_data["optimized_context"],
                "applied_optimizations": result_data["applied_optimizations"],
                "improvement_metrics": result_data["improvement_metrics"],
                "optimization_summary": optimization_summary
            }
    
    def _apply_clarity_optimization(self, context: str) -> tuple:
        """Apply clarity optimization"""
        optimizations = []
        optimized = context

        # Replace ambiguous terms with clear expressions
        replacements = {
            '需要': 'please specify need for',
            '大概': 'specifically',
            '可能': 'under specific conditions',
            '也许': 'in certain cases',
            '一些': 'specific quantity of',
            '某些': 'specific'
        }

        for old_word, new_phrase in replacements.items():
            if old_word in context:
                optimized = optimized.replace(old_word, new_phrase)
                optimizations.append(f"Improve clarity: Replace '{old_word}' with '{new_phrase}'")

        # Add clear instruction prefix
        if not any(indicator in optimized for indicator in ['请', '要求', '目标']):
            optimized = f"Please specify {optimized}"
            optimizations.append("Add clear instruction prefix: Add 'Please specify'")

        return optimized, optimizations
    
    def _apply_relevance_optimization(self, context: str) -> tuple:
        """Apply relevance optimization"""
        optimizations = []
        optimized = context

        # Add goal-related expressions
        if '系统' in context and '目标' not in context:
            optimized += " The goal is to create an efficient and reliable system."
            optimizations.append("Enhance relevance: Add system goal statement")

        if '功能' in context and '用户' not in context and '客户' not in context:
            optimized += " Mainly consider user needs and experience."
            optimizations.append("Enhance relevance: Add user perspective")

        return optimized, optimizations
    
    def _apply_completeness_optimization(self, context: str) -> tuple:
        """Apply completeness optimization"""
        optimizations = []
        optimized = context

        # Add missing common elements
        if not any(indicator in context for indicator in ['约束', '要求', '条件', '限制']):
            optimized += "\n\nConstraints: Must complete within specified time period"
            optimizations.append("Add constraints")

        if not any(indicator in context for indicator in ['目标', '目的', '成功标准', '验收标准']):
            optimized += "\nClear goal: Implement expected functionality and meet quality requirements"
            optimizations.append("Add clear goal")

        if not any(indicator in context for indicator in ['假设', '前提', '基础条件']):
            optimized += "\nPrerequisite assumptions: Have necessary development resources and technical support"
            optimizations.append("Add prerequisite assumptions")

        return optimized, optimizations
    
    def _apply_conciseness_optimization(self, context: str) -> tuple:
        """Apply conciseness optimization"""
        optimizations = []
        optimized = context

        # Remove duplicate content (simple implementation)
        sentences = re.split(r'([。！？.!?]+)', context)

        # Merge sentences and punctuation
        parts = []
        for i in range(0, len(sentences), 2):
            if i + 1 < len(sentences):
                parts.append(sentences[i] + sentences[i+1])
            elif i < len(sentences):
                parts.append(sentences[i])

        # Remove duplicate sentences (simple deduplication)
        unique_parts = []
        seen = set()
        for part in parts:
            clean_part = re.sub(r'\s+', ' ', part.strip())
            if clean_part and clean_part not in seen:
                unique_parts.append(part)
                seen.add(clean_part)

        if len(unique_parts) < len(parts):
            optimized = ''.join(unique_parts)
            optimizations.append("Remove duplicate content")

        # Simplify verbose expressions
        simplifications = [
            ('尽可能的', ''),
            ('最大程度上', ''),
            ('在某种程度上', ''),
            ('可以说', ''),
            ('基本上', '')
        ]

        for old_expr, new_expr in simplifications:
            original_len = len(optimized)
            optimized = optimized.replace(old_expr, new_expr)
            if len(optimized) < original_len:
                optimizations.append(f"Simplify expression: Remove '{old_expr}'")

        return optimized, optimizations
    
    def _calculate_improvements(self, original: str, optimized: str, applied_optimizations: List[str]) -> Dict[str, float]:
        """
        Calculate optimization improvement metrics
        """
        # Simplified implementation: evaluate improvements based on optimization measures' quantity and type
        improvements = {}

        optimization_types = [op.split(':')[0] for op in applied_optimizations]

        improvements['clarity'] = 0.0
        improvements['relevance'] = 0.0
        improvements['completeness'] = 0.0
        improvements['conciseness'] = 0.0

        for opt_type in optimization_types:
            if '清晰度' in opt_type or '明确' in opt_type:
                improvements['clarity'] += 0.15
            elif '相关性' in opt_type:
                improvements['relevance'] += 0.1
            elif '完整性' in opt_type or '补充' in opt_type:
                improvements['completeness'] += 0.2
            elif '简洁性' in opt_type or '简化' in opt_type or '移除' in opt_type:
                # Conciseness improvement: based on length change
                improvements['conciseness'] = (len(original) - len(optimized)) / len(original) if original else 0

        # Limit improvement values within reasonable range
        for key in improvements:
            improvements[key] = max(-0.5, min(0.5, improvements[key]))

        return improvements
    
    def _categorize_optimizations(self, applied_optimizations: List[str]) -> Dict[str, int]:
        """Categorize and count optimization measures"""
        categories = {
            "clarity": 0,
            "relevance": 0,
            "completeness": 0,
            "conciseness": 0,
            "other": 0
        }

        for opt in applied_optimizations:
            if '清晰度' in opt or '明确' in opt:
                categories["clarity"] += 1
            elif '相关性' in opt:
                categories["relevance"] += 1
            elif '完整性' in opt or '补充' in opt:
                categories["completeness"] += 1
            elif '简洁性' in opt or '简化' in opt or '移除' in opt:
                categories["conciseness"] += 1
            else:
                categories["other"] += 1

        return categories