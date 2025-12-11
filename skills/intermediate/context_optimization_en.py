"""
Context Optimization Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any, List
from ..skill_base_en import BaseSkill, DetailLevel
import re


class ContextOptimizationSkill(BaseSkill):
    """Context Optimization Skill"""
    
    def __init__(self):
        super().__init__(
            name="context-optimization",
            description="Optimize context quality to enhance clarity, relevance, completeness and other dimensions"
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
        
        # Apply optimization based on goals
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
            # Basic level returns core information only
            return {
                "optimized_context": result_data["optimized_context"],
                "main_optimizations": result_data["applied_optimizations"][:3],  # Return only top 3 main optimizations
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
        
        # Replace vague terms with explicit statements
        replacements = {
            'need': 'please clearly specify',
            'maybe': 'specifically',
            'possibly': 'under specific conditions',
            'perhaps': 'in certain cases',
            'some': 'specific quantity of',
            'certain': 'specific'
        }
        
        for old_word, new_phrase in replacements.items():
            if old_word in context.lower():
                # Case-insensitive replacement
                pattern = re.compile(re.escape(old_word), re.IGNORECASE)
                optimized = pattern.sub(new_phrase, optimized)
                optimizations.append(f"Enhance clarity: Replace '{old_word}' with '{new_phrase}'")
        
        # Add explicit instruction prefix
        if not any(indicator in optimized.lower() for indicator in ['please', 'require', 'goal']):
            optimized = f"Please clearly specify {optimized}"
            optimizations.append("Add explicit instruction prefix: Added 'Please clearly specify'")
        
        return optimized, optimizations
    
    def _apply_relevance_optimization(self, context: str) -> tuple:
        """Apply relevance optimization"""
        optimizations = []
        optimized = context
        
        # Add relevance statements
        if 'system' in context.lower() and 'goal' not in context.lower():
            optimized += " The goal is to create an efficient and reliable system."
            optimizations.append("Enhance relevance: Supplement system goal description")
        
        if 'function' in context.lower() and 'user' not in context.lower() and 'customer' not in context.lower():
            optimized += " Main consideration is user requirements and experience."
            optimizations.append("Enhance relevance: Supplement user perspective")
        
        return optimized, optimizations
    
    def _apply_completeness_optimization(self, context: str) -> tuple:
        """Apply completeness optimization"""
        optimizations = []
        optimized = context
        
        # Supplement common missing elements
        if not any(indicator in context.lower() for indicator in ['constraint', 'requirement', 'condition', 'limitation']):
            optimized += "\n\nConstraints: Must be completed within specified time frame"
            optimizations.append("Supplement constraints")
        
        if not any(indicator in context.lower() for indicator in ['goal', 'purpose', 'success criteria', 'acceptance criteria']):
            optimized += "\nClear objective: Achieve expected functionality and meet quality requirements"
            optimizations.append("Supplement clear objectives")
        
        if not any(indicator in context.lower() for indicator in ['assumption', 'premise', 'basic condition']):
            optimized += "\nPrerequisites: Necessary development resources and technical support available"
            optimizations.append("Supplement prerequisites")
        
        return optimized, optimizations
    
    def _apply_conciseness_optimization(self, context: str) -> tuple:
        """Apply conciseness optimization"""
        optimizations = []
        optimized = context
        
        # Remove duplicate content (simple implementation)
        sentences = re.split(r'([.!?]+)', context)
        
        # Combine sentences and punctuation
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
            ('as much as possible', ''),
            ('to the greatest extent', ''),
            ('to some extent', ''),
            ('it can be said that', ''),
            ('basically', '')
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
        # Simplified implementation: Evaluate improvements based on optimization measures count and type
        improvements = {}
        
        optimization_types = [op.split(':')[0] for op in applied_optimizations]
        
        improvements['clarity'] = 0.0
        improvements['relevance'] = 0.0
        improvements['completeness'] = 0.0
        improvements['conciseness'] = 0.0
        
        for opt_type in optimization_types:
            if 'clarity' in opt_type.lower() or 'clear' in opt_type.lower():
                improvements['clarity'] += 0.15
            elif 'relevance' in opt_type.lower():
                improvements['relevance'] += 0.1
            elif 'completeness' in opt_type.lower() or 'supplement' in opt_type.lower():
                improvements['completeness'] += 0.2
            elif 'conciseness' in opt_type.lower() or 'simplify' in opt_type.lower() or 'remove' in opt_type.lower():
                # Conciseness improvement: Based on length change
                improvements['conciseness'] = (len(original) - len(optimized)) / len(original) if original else 0
        
        # Limit improvement values to reasonable range
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
            if 'clarity' in opt.lower() or 'clear' in opt.lower():
                categories["clarity"] += 1
            elif 'relevance' in opt.lower():
                categories["relevance"] += 1
            elif 'completeness' in opt.lower() or 'supplement' in opt.lower():
                categories["completeness"] += 1
            elif 'conciseness' in opt.lower() or 'simplify' in opt.lower() or 'remove' in opt.lower():
                categories["conciseness"] += 1
            else:
                categories["other"] += 1
        
        return categories