"""
Context Analysis Script
Implements the core functionality for context analysis using Context Engineering principles
"""

import re
import json
from typing import Dict, Any, List, Tuple


def analyze_clarity(context: str) -> Tuple[float, List[str]]:
    """
    Analyze the clarity of the given context
    Returns a score (0-1) and a list of clarity issues
    """
    issues = []
    
    # Check for ambiguous words
    ambiguous_patterns = [
        r'\bsome\b', r'\bcertain\b', r'\bquite\b', r'\brather\b', 
        r'\bsort of\b', r'\tkind of\b', r'\ba bit\b'
    ]
    
    for pattern in ambiguous_patterns:
        matches = re.findall(pattern, context, re.IGNORECASE)
        if matches:
            issues.extend([f"Ambiguous term found: '{match}'" for match in matches[:3]])  # Limit to 3 examples
    
    # Check sentence structure
    sentences = re.split(r'[.!?]+', context)
    long_sentences = [s for s in sentences if len(s) > 200]
    if long_sentences:
        issues.append(f"Found {len(long_sentences)} long sentences that may reduce clarity")
    
    # Calculate clarity score (inverse of issues)
    max_issues = 10  # Assume 10+ issues = 0% clarity
    clarity_score = max(0, 1 - (len(issues) / max_issues))
    
    return round(clarity_score, 2), issues


def analyze_relevance(context: str, topic_keywords: List[str] = None) -> Tuple[float, List[str]]:
    """
    Analyze the relevance of the given context
    """
    if topic_keywords is None:
        # Default to some generic terms that might indicate relevance issues
        topic_keywords = ['relevant', 'topic', 'related', 'connection', 'connection']
    
    issues = []
    text_lower = context.lower()
    
    # In a real implementation, we would compare against a defined topic
    # For now, we'll just check for coherence
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Check for excessive repetition (might indicate lack of relevance)
    from collections import Counter
    word_counts = Counter(words)
    repeated_words = [word for word, count in word_counts.items() if count > len(words) * 0.05]  # >5% of text
    
    if repeated_words:
        issues.append(f"Words potentially overused (might indicate limited relevance): {repeated_words[:5]}")
    
    # Calculate relevance score (simplified)
    relevance_score = 0.7  # Default to medium relevance
    if len(issues) > 3:
        relevance_score = 0.3
    elif len(issues) > 0:
        relevance_score = 0.5
    
    return round(relevance_score, 2), issues


def analyze_completeness(context: str) -> Tuple[float, List[str]]:
    """
    Analyze the completeness of the given context
    """
    issues = []
    
    # Look for common elements that might be missing
    required_elements = [
        ('goal', r'goal|objective|purpose|aim|target|requirement'),
        ('constraints', r'constraint|limitation|restriction|boundary|condition'),
        ('resources', r'resource|tool|capability|support|access'),
        ('timeline', r'timeline|schedule|deadline|duration|when')
    ]
    
    missing_elements = []
    context_lower = context.lower()
    
    for element_name, pattern in required_elements:
        if not re.search(pattern, context_lower):
            missing_elements.append(element_name)
    
    if missing_elements:
        issues.append(f"Potentially missing elements: {', '.join(missing_elements)}")
    
    # Calculate completeness score
    completeness_score = 1.0 - (len(missing_elements) / len(required_elements))
    
    return round(completeness_score, 2), issues


def analyze_consistency(context: str) -> Tuple[float, List[str]]:
    """
    Analyze the consistency of the given context
    """
    issues = []
    
    # Check for potential contradictions
    contradiction_patterns = [
        (r'\bmust\b.*\bcannot\b', "Found 'must' and 'cannot' in proximity"),
        (r'\balways\b.*\bnever\b', "Found 'always' and 'never' in proximity"),
        (r'\ball\b.*\bnone\b', "Found 'all' and 'none' in proximity"),
        (r'\bonly\b.*\balso\b', "Found 'only' and 'also' in proximity")
    ]
    
    for pattern, description in contradiction_patterns:
        matches = re.findall(pattern, context, re.IGNORECASE)
        if matches:
            issues.append(f"Potential contradiction: {description}")
    
    # Check for consistent terminology
    # Look for different terms that may refer to the same concept
    context_lower = context.lower()
    if 'it' in context_lower and 'this' in context_lower:
        # Could be more sophisticated, but checking for overuse of pronouns
        pass
    
    # Calculate consistency score
    consistency_score = max(0.0, 1.0 - (len(issues) * 0.2))  # Each issue reduces score by 0.2
    
    return round(consistency_score, 2), issues


def analyze_efficiency(context: str) -> Tuple[float, List[str]]:
    """
    Analyze the efficiency (information density) of the given context
    """
    issues = []
    
    if not context.strip():
        return 0.0, ["Context is empty"]
    
    # Calculate basic metrics
    word_count = len(re.findall(r'\b\w+\b', context))
    char_count = len(context)
    
    # Check for redundancy
    sentences = re.split(r'[.!?]+', context)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Simple redundancy check - repeated similar sentences
    unique_sentences = set()
    repeated_sentences = 0
    
    for sentence in sentences:
        clean_sentence = re.sub(r'\s+', ' ', sentence.strip().lower())
        if clean_sentence and clean_sentence in unique_sentences:
            repeated_sentences += 1
        elif clean_sentence:
            unique_sentences.add(clean_sentence)
    
    if repeated_sentences > 0:
        issues.append(f"Found {repeated_sentences} potentially repeated sentences")
    
    # Efficiency score based on information density
    # A simple measure: fewer words to convey the same information = higher efficiency
    # This is a simplified calculation - real implementation may vary
    efficiency_score = min(1.0, word_count / (char_count * 0.1 + 1)) if char_count > 0 else 0.0
    # Adjust based on redundancy
    efficiency_score = max(0.1, efficiency_score - (repeated_sentences * 0.1))
    
    return round(min(efficiency_score, 1.0), 2), issues


def analyze_context(context: str) -> Dict[str, Any]:
    """
    Comprehensive context analysis using all metrics
    """
    # Perform all analyses
    clarity_score, clarity_issues = analyze_clarity(context)
    relevance_score, relevance_issues = analyze_relevance(context)
    completeness_score, completeness_issues = analyze_completeness(context)
    consistency_score, consistency_issues = analyze_consistency(context)
    efficiency_score, efficiency_issues = analyze_efficiency(context)
    
    # Compile results
    analysis = {
        "context_length": len(context),
        "word_count": len(re.findall(r'\b\w+\b', context)),
        "metrics": {
            "clarity": clarity_score,
            "relevance": relevance_score,
            "completeness": completeness_score,
            "consistency": consistency_score,
            "efficiency": efficiency_score
        },
        "detailed_issues": {
            "clarity": clarity_issues,
            "relevance": relevance_issues,
            "completeness": completeness_issues,
            "consistency": consistency_issues,
            "efficiency": efficiency_issues
        },
        "overall_score": round(sum([
            clarity_score, relevance_score, completeness_score, 
            consistency_score, efficiency_score
        ]) / 5, 2)
    }
    
    return analysis


def format_analysis_report(analysis: Dict[str, Any]) -> str:
    """
    Format the analysis results into a human-readable report
    """
    report_parts = []
    
    report_parts.append("## Context Analysis Report")
    report_parts.append(f"**Overall Score**: {analysis['overall_score']}/1.0\n")
    report_parts.append(f"**Length**: {analysis['context_length']} characters, {analysis['word_count']} words\n")
    
    report_parts.append("### Detailed Metrics:")
    for metric, score in analysis['metrics'].items():
        report_parts.append(f"- **{metric.title()}**: {score}/1.0")
    
    report_parts.append("\n### Identified Issues:")
    for metric, issues in analysis['detailed_issues'].items():
        if issues:
            report_parts.append(f"**{metric.title()} Issues:**")
            for issue in issues:
                report_parts.append(f"  - {issue}")
    
    return "\n".join(report_parts)


if __name__ == "__main__":
    # Example usage
    test_context = """
    This is a sample context for testing purposes. The goal is to determine 
    if the content provides enough information to be clear and relevant. 
    There should be no contradictions and the information needs to be 
    presented efficiently. Some requirements need to be specified, but 
    constraints might limit what can be achieved. The timeline is important 
    for planning purposes.
    """
    
    analysis = analyze_context(test_context)
    report = format_analysis_report(analysis)
    print(report)