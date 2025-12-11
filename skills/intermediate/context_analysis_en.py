"""
Context Analysis Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any
from ..skill_base_en import BaseSkill, DetailLevel
import re


class ContextAnalysisSkill(BaseSkill):
    """Context Analysis Skill"""
    
    def __init__(self):
        super().__init__(
            name="context-analysis",
            description="Analyze context quality and provide evaluation and improvement suggestions across five dimensions"
        )
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute context analysis logic"""
        # Perform context analysis
        clarity = self._analyze_clarity(input_text)
        relevance = self._analyze_relevance(input_text)
        completeness = self._analyze_completeness(input_text)
        consistency = self._analyze_consistency(input_text)
        efficiency = self._analyze_efficiency(input_text)
        
        overall_score = (clarity + relevance + completeness + consistency + efficiency) / 5
        
        # Generate suggestions
        suggestions = []
        if clarity < 0.7:
            suggestions.append("Add clearer terminology and goal statements")
        if completeness < 0.6:
            suggestions.append("Supplement constraints and specific requirements")
        if relevance < 0.7:
            suggestions.append("Clarify goal and task relevance")
        
        # Identify issues
        issues = []
        if "maybe" in input_text.lower() or "possibly" in input_text.lower() or "probably" in input_text.lower():
            issues.append("Contains uncertain terms: 'maybe', 'possibly', 'probably'")
        if len(input_text) < 20:
            issues.append("Context too short, insufficient information")
        if "but" in input_text.lower() and "therefore" not in input_text.lower():
            issues.append("Contains contrast but lacks logical conclusion")
        
        return {
            "context_length": len(input_text),
            "overall_score": round(overall_score, 2),
            "metrics": {
                "clarity": round(clarity, 2),
                "relevance": round(relevance, 2),
                "completeness": round(completeness, 2),
                "consistency": round(consistency, 2),
                "efficiency": round(efficiency, 2)
            },
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """Format output result based on detail level"""
        if detail_level == DetailLevel.BASIC:
            # Basic level returns core information only
            return {
                "overall_score": result_data["overall_score"],
                "main_issues": result_data["issues"][:3]  # Return only top 3 main issues
            }
        elif detail_level == DetailLevel.STANDARD:
            # Standard level returns standard information
            return {
                "overall_score": result_data["overall_score"],
                "metrics": result_data["metrics"],
                "issues": result_data["issues"],
                "suggestions": result_data["suggestions"][:5]  # Return only top 5 suggestions
            }
        else:  # DETAILED
            # Detailed level returns complete information
            detailed_analysis = {
                "context_length": result_data["context_length"],
                "metrics_breakdown": {
                    "clarity": {
                        "score": result_data["metrics"]["clarity"],
                        "analysis": "Clarity calculated based on explicit instruction words and sentence structure"
                    },
                    "relevance": {
                        "score": result_data["metrics"]["relevance"],
                        "analysis": "Relevance calculated based on task-related vocabulary"
                    },
                    "completeness": {
                        "score": result_data["metrics"]["completeness"],
                        "analysis": "Completeness calculated based on constraint and requirement vocabulary"
                    },
                    "consistency": {
                        "score": result_data["metrics"]["consistency"],
                        "analysis": "Consistency calculated based on logical contradiction detection"
                    },
                    "efficiency": {
                        "score": result_data["metrics"]["efficiency"],
                        "analysis": "Efficiency calculated based on information density"
                    }
                }
            }
            
            return {
                "overall_score": result_data["overall_score"],
                "metrics": result_data["metrics"],
                "issues": result_data["issues"],
                "suggestions": result_data["suggestions"],
                "detailed_analysis": detailed_analysis
            }
    
    def _analyze_clarity(self, context: str) -> float:
        """Analyze clarity"""
        clear_indicators = ['please', 'need', 'require', 'goal', 'task', 'implement', 'design', 'analyze', 'how', 'what']
        unclear_indicators = ['maybe', 'possibly', 'probably', 'seems', 'some', 'certain', 'part', 'etc']
        
        clear_count = sum(1 for indicator in clear_indicators if indicator in context.lower())
        unclear_count = sum(1 for indicator in unclear_indicators if indicator in context.lower())
        
        # Calculate clarity based on sentences and explicit instruction words
        sentences = re.split(r'[.!?;]', context)
        sentence_count = len([s for s in sentences if s.strip() and len(s.strip()) > 3])
        
        clarity_score = min(1.0, (clear_count * 0.3 + sentence_count * 0.05) if sentence_count > 0 else 0)
        unclear_penalty = min(0.5, unclear_count * 0.2)
        
        return max(0.0, clarity_score - unclear_penalty)
    
    def _analyze_relevance(self, context: str) -> float:
        """Analyze relevance"""
        task_indicators = ['system', 'function', 'task', 'goal', 'requirement', 'implement', 'develop', 'design', 'analyze', 'manage', 'process', 'support']
        
        task_count = sum(1 for indicator in task_indicators if indicator in context.lower())
        relevance_score = min(1.0, task_count * 0.15)
        
        return max(0.0, relevance_score)
    
    def _analyze_completeness(self, context: str) -> float:
        """Analyze completeness"""
        completeness_indicators = ['constraint', 'condition', 'requirement', 'standard', 'specification', 'limitation', 'assumption', 'premise', 'target', 'acceptance']
        
        completeness_count = sum(1 for indicator in completeness_indicators if indicator in context.lower())
        completeness_score = min(1.0, completeness_count * 0.15)
        
        return max(0.0, completeness_score)
    
    def _analyze_consistency(self, context: str) -> float:
        """Analyze consistency"""
        # Check for logical contradictions
        contradiction_pairs = [
            ('must', 'optional'),
            ('should', 'not necessary'),
            ('always', 'never'),
            ('all', 'part'),
            ('mandatory', 'arbitrary'),
            ('require', 'optional'),
            ('must', 'can')
        ]
        
        contradiction_count = 0
        for positive, negative in contradiction_pairs:
            if positive in context.lower() and negative in context.lower():
                contradiction_count += 1
        
        # Higher consistency means higher score, more contradictions mean lower score
        consistency_score = max(0.0, 1.0 - (contradiction_count * 0.2))
        
        return consistency_score
    
    def _analyze_efficiency(self, context: str) -> float:
        """Analyze efficiency (information density)"""
        if len(context) == 0:
            return 0.0
        
        # Calculate information density: effective word count / total character count
        words = [w for w in re.findall(r'[\w]+', context) if len(w) > 1]
        efficiency = len(words) / len(context) * 100
        
        # Normalize to 0-1 range (assume 25 effective words per 100 characters is ideal for full score)
        normalized_efficiency = min(1.0, efficiency / 25)
        
        return max(0.0, normalized_efficiency)