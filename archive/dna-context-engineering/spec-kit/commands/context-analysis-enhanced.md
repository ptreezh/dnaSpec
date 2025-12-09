---
allowed-tools: Bash(fs.createFile:*), Bash(fs.writeFile:*), Bash(fs.readFile:*)
argument-hint: [context-to-analyze]
description: Enhanced context analysis using Context Engineering methodology. Analyze context quality with detailed metrics for clarity, relevance, completeness, consistency, and efficiency.
model: claude-3-5-sonnet-20241022
---

# Enhanced Context Analysis Process

## Task
Analyze the following context using Context Engineering methodology: $ARGUMENTS

## Analysis Framework
Please evaluate the provided context across multiple dimensions:

### 1. Clarity Analysis (0-1)
- How clearly is information expressed?
- Are there ambiguous terms or phrases?
- Is the structure logical and organized?
- Can the main points be easily identified?

### 2. Relevance Assessment (0-1)
- How well does the content align with its stated purpose?
- Are there off-topic elements?
- Is the content appropriate for the intended audience?
- Does it stay focused on the main theme?

### 3. Completeness Evaluation (0-1)
- Are all necessary elements present?
- Are there information gaps?
- Is the context sufficient for understanding?
- Are prerequisites adequately covered?

### 4. Consistency Check (0-1)
- Are there any contradictory statements?
- Is terminology used consistently?
- Do ideas flow logically between sections?
- Are there factual coherence issues?

### 5. Efficiency Measurement (0-1)
- Is the information-to-noise ratio optimal?
- Are there redundant elements?
- Is the content appropriately sized for its purpose?
- Does it avoid unnecessary complexity?

## Context Engineering Analysis
In addition to the above metrics, please evaluate:

### Token Budget Optimization
- Is the context efficient in its token usage?
- Are there opportunities for more economical formulations?
- Does it balance information density with clarity?

### Memory Integration Considerations
- How well does this content fit into larger context windows?
- Are there potential memory conflicts?
- Is it optimized for multi-turn interactions?

### Reasoning Architecture Compatibility
- How well does the content support reasoning operations?
- Are there structures that enable cognitive tool application?
- Is it designed for multi-step processing?

## Output Requirements
Please provide:
1. Numerical scores for each dimension (0-1 scale)
2. Specific issues identified in each dimension
3. Actionable recommendations for improvement
4. Relevant Context Engineering patterns that could be applied
5. Expected improvement impact from recommendations

Structure your response clearly with these elements and provide detailed, actionable feedback.