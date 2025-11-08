"""
Context Optimization Script
Implements the core functionality for context optimization using Context Engineering principles
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum


class OptimizationGoal(Enum):
    CLARITY = "clarity"
    RELEVANCE = "relevance" 
    COMPLETENESS = "completeness"
    CONCISENESS = "conciseness"
    CONSISTENCY = "consistency"


def optimize_clarity(context: str) -> Tuple[str, List[str]]:
    """
    Optimize context for clarity
    """
    issues = []
    optimized = context
    
    # Replace ambiguous terms with clearer alternatives
    ambiguous_replacements = {
        r'\bsome\b(?!\s+of)': 'a specific number of',
        r'\bcertain\b(?!\s+that)': 'specific',
        r'\bquite\b(?!\s+a)': 'rather',
        r'\bsort of\b': 'approximately',
        r'\tkind of\b': 'approximately',
        r'\ba bit\b(?!\s+of)': 'slightly',
        r'\setc\.?\b': 'and so on',
        r'\betc\b': 'and so on',
    }
    
    for pattern, replacement in ambiguous_replacements.items():
        optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
    
    # Improve sentence structure (simplify long sentences)
    sentences = re.split(r'([.!?]+)', optimized)
    new_sentences = []
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i] if i < len(sentences) else ""
        punctuation = sentences[i+1] if i+1 < len(sentences) else ""
        
        # Break up very long sentences
        if len(sentence) > 150:
            # Simple approach: split at conjunctions if the sentence is too long
            parts = re.split(r'\s+(?:and|or|but|so|yet|for|nor|while|although|since|because|if|when|where|before|after|as)\s+', sentence)
            clean_parts = [part.strip() for part in parts if part.strip()]
            
            if len(clean_parts) > 1:
                new_sentences.extend([part + punctuation for part in clean_parts])
                issues.append(f"Long sentence simplified into {len(clean_parts)} shorter sentences")
            else:
                new_sentences.append(sentence + punctuation)
        else:
            new_sentences.append(sentence + punctuation)
    
    optimized = ''.join(new_sentences)
    
    return optimized, issues


def optimize_relevance(context: str, topic_keywords: List[str] = None) -> Tuple[str, List[str]]:
    """
    Optimize context for relevance
    """
    issues = []
    optimized = context
    
    # In a real implementation, this would match content against the topic
    # For now, we'll just remove some obviously irrelevant patterns
    irrelevant_patterns = [
        r'\s+this is irrelevant\b',
        r'\s+this does not matter\b',
        r'\s+off topic information\b',
        r'\s+not related to the main point\b'
    ]
    
    for pattern in irrelevant_patterns:
        matches = re.findall(pattern, optimized, re.IGNORECASE)
        if matches:
            issues.extend([f"Removed irrelevant content: {m.strip()}" for m in matches])
            optimized = re.sub(pattern, '', optimized, flags=re.IGNORECASE)
    
    return optimized, issues


def optimize_completeness(context: str) -> Tuple[str, List[str]]:
    """
    Optimize context for completeness
    """
    issues = []
    optimized = context
    
    # Identify potentially missing elements based on common requirements
    required_elements = [
        ('goal', r'goal|objective|purpose|aim|target'),
        ('constraints', r'limitation|constraint|restriction|requirement|rule'),
        ('resources', r'resource|tool|access|capability'),
        ('timeline', r'timeline|schedule|deadline|duration')
    ]
    
    missing_elements = []
    context_lower = context.lower()
    
    for element_name, pattern in required_elements:
        if not re.search(pattern, context_lower):
            missing_elements.append(element_name)
    
    if missing_elements:
        # Add placeholder for missing elements - in a real app, these would be prompted for
        issues.append(f"Potentially missing elements: {', '.join(missing_elements)}")
        
        # Add section for missing elements (for demonstration)
        additions = []
        for element in missing_elements:
            additions.append(f"\n\n**{element.capitalize()}**: [Please specify {element} information]")
        
        optimized += ''.join(additions)
    
    return optimized, issues


def optimize_conciseness(context: str) -> Tuple[str, List[str]]:
    """
    Optimize context for conciseness
    """
    issues = []
    optimized = context
    
    # Remove redundant phrases
    redundancy_patterns = [
        r'\s+in order to\s+',  # Replace with 'to'
        r'\s+due to the fact that\s+',  # Replace with 'because'
        r'\s+at this point in time\s+',  # Replace with 'now'
        r'\s+in the event that\s+',  # Replace with 'if'
        r'\s+with regard to\s+',  # Replace with 'regarding'
        r'\s+prior to\s+',  # Replace with 'before'
        r'\s+subsequent to\s+',  # Replace with 'after'
        r'\s+regardless of the fact that\s+',  # Replace with 'although'
    ]
    
    for pattern in redundancy_patterns:
        optimized = re.sub(pattern, ' ', optimized, flags=re.IGNORECASE)
    
    # Remove duplicate sentences
    sentences = re.split(r'([.!?]+)', optimized)
    unique_sentences = []
    seen = set()
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i].strip() if i < len(sentences) else ""
        punctuation = sentences[i+1] if i+1 < len(sentences) and i+1 < len(sentences) else ""
        
        if sentence and sentence.lower() not in seen:
            unique_sentences.append(sentence + punctuation)
            seen.add(sentence.lower())
        elif sentence:
            issues.append(f"Removed duplicate sentence: '{sentence[:50]}...'")
    
    optimized = ''.join(unique_sentences) if unique_sentences else optimized
    
    return optimized, issues


def optimize_consistency(context: str) -> Tuple[str, List[str]]:
    """
    Optimize context for consistency
    """
    issues = []
    optimized = context
    
    # Check for inconsistent terminology (simplified approach)
    # Look for potential contradictions
    contradiction_patterns = [
        (r'\bmust\b.*\bcannot\b', "Found 'must' and 'cannot' in proximity"),
        (r'\balways\b.*\bnever\b', "Found 'always' and 'never' in proximity"),
        (r'\ball\b.*\bnone\b', "Found 'all' and 'none' in proximity"),
        (r'\bonly\b.*\balso\b', "Found 'only' and 'also' in proximity")
    ]
    
    for pattern, description in contradiction_patterns:
        matches = re.findall(pattern, optimized, re.IGNORECASE)
        if matches:
            issues.append(f"Potential contradiction: {description}")
    
    # Standardize some common terms
    consistency_replacements = {
        r'\butilize\b': 'use',
        r'\bfacility\b': 'facility|building|location',  # Could be more specific based on context
        r'\bindividual\b': 'person',
        r'\bcommence\b': 'start',
        r'\bterminate\b': 'end',
    }
    
    for pattern, replacement in consistency_replacements.items():
        optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
    
    return optimized, issues


def optimize_context(context: str, goals: List[OptimizationGoal] = None) -> Dict[str, Any]:
    """
    Main optimization function that applies specified optimization goals
    """
    if goals is None:
        goals = [OptimizationGoal.CLARITY, OptimizationGoal.RELEVANCE, 
                 OptimizationGoal.COMPLETENESS, OptimizationGoal.CONSISTENCY]
    
    original_context = context
    optimized_context = context
    all_issues = []
    
    optimization_functions = {
        OptimizationGoal.CLARITY: optimize_clarity,
        OptimizationGoal.RELEVANCE: optimize_relevance,
        OptimizationGoal.COMPLETENESS: optimize_completeness,
        OptimizationGoal.CONCISENESS: optimize_conciseness,
        OptimizationGoal.CONSISTENCY: optimize_consistency
    }
    
    for goal in goals:
        if goal in optimization_functions:
            optimized_context, issues = optimization_functions[goal](optimized_context)
            if issues:
                all_issues.extend([f"[{goal.value}] {issue}" for issue in issues])
    
    # Calculate improvement metrics
    original_length = len(original_context)
    optimized_length = len(optimized_context)
    
    return {
        "original_context": original_context,
        "optimized_context": optimized_context,
        "applied_optimizations": [goal.value for goal in goals],
        "improvement_metrics": {
            "length_change": optimized_length - original_length,
            "length_ratio": optimized_length / original_length if original_length > 0 else 0
        },
        "optimization_issues": all_issues,
        "original_analysis": {
            "length": original_length,
            "word_count": len(re.findall(r'\b\w+\b', original_context))
        },
        "optimized_analysis": {
            "length": optimized_length,
            "word_count": len(re.findall(r'\b\w+\b', optimized_context))
        }
    }


def format_optimization_report(result: Dict[str, Any]) -> str:
    """
    Format the optimization results into a readable report
    """
    report_parts = []
    
    report_parts.append("## Context Optimization Report")
    report_parts.append(f"**Applied Optimizations**: {', '.join(result['applied_optimizations'])}\n")
    
    report_parts.append(f"**Length Change**: {result['improvement_metrics']['length_change']} characters")
    report_parts.append(f"**Length Ratio**: {result['improvement_metrics']['length_ratio']:.2f}\n")
    
    if result['optimization_issues']:
        report_parts.append("**Issues Addressed**: ")
        for issue in result['optimization_issues']:
            report_parts.append(f"- {issue}")
    else:
        report_parts.append("**Issues Addressed**: No specific issues identified")
    
    report_parts.append("\n**Original Context Analysis**: ")
    report_parts.append(f"- Length: {result['original_analysis']['length']} characters")
    report_parts.append(f"- Word count: {result['original_analysis']['word_count']} words")
    
    report_parts.append("\n**Optimized Context Analysis**: ")
    report_parts.append(f"- Length: {result['optimized_analysis']['length']} characters")
    report_parts.append(f"- Word count: {result['optimized_analysis']['word_count']} words")
    
    report_parts.append(f"\n**Optimized Context**:\n{result['optimized_context']}")
    
    return "\n".join(report_parts)


if __name__ == "__main__":
    # Example usage
    test_context = """
    This is a complex document that needs to be improved for clarity. 
    The document should be clear and concise. Some parts may be redundant. 
    There could be inconsistencies in terminology. 
    The goal is to make the document better overall.
    """
    
    optimization_goals = [
        OptimizationGoal.CLARITY,
        OptimizationGoal.CONCISENESS,
        OptimizationGoal.CONSISTENCY
    ]
    
    result = optimize_context(test_context, optimization_goals)
    report = format_optimization_report(result)
    print(report)