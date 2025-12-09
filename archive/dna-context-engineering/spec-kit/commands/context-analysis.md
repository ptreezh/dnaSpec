---
allowed-tools: Bash(fs.createFile:*), Bash(fs.writeFile:*), Bash(fs.readFile:*)
argument-hint: [context-to-analyze]
description: Analyze context quality across multiple dimensions: clarity, relevance, completeness, consistency, and efficiency.
model: claude-3-5-sonnet-20241022
---

# Context Analysis Process

## Task
Analyze the following context: $ARGUMENTS

## Analysis Dimensions

### 1. Clarity (0-1)
Measures how clearly information is expressed. Evaluate:
- Use of precise language
- Logical flow of ideas
- Absence of ambiguous terms
- Clear structure and organization

### 2. Relevance (0-1)
Measures how well content aligns with the stated goals. Evaluate:
- Direct relation to main topic
- Pertinence to intended audience
- Alignment with stated objectives
- Elimination of off-topic content

### 3. Completeness (0-1)
Measures whether key information is present. Evaluate:
- Coverage of essential information
- Presence of all required elements
- Sufficient detail for understanding
- Absence of critical gaps

### 4. Consistency (0-1)
Measures logical and factual coherence. Evaluate:
- Consistency of terminology
- Logical flow between ideas
- Absence of contradictions
- Factual coherence throughout

### 5. Efficiency (0-1)
Measures information density and conciseness. Evaluate:
- Optimal length for content type
- Elimination of redundancy
- Effective use of space
- Clear signal-to-noise ratio

## Process to Follow
1. Provide numerical scores for each dimension (0-1 scale)
2. Identify specific issues in low-scoring dimensions
3. Offer concrete, actionable improvement suggestions
4. Maintain objectivity in evaluation
5. Focus on measurable aspects of quality
6. Consider the context and purpose when evaluating

## Output Requirements
Please provide:
- Numerical scores for each dimension (0-1 scale)
- Specific issues identified in each dimension
- Concrete, actionable improvement suggestions
- Brief explanation of the scoring rationale
- Structured format with clear sections