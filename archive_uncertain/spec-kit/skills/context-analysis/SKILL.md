---
name: context-analysis
description: Analyze context quality across multiple dimensions. Use when you need to evaluate the clarity, relevance, completeness, consistency, and efficiency of text content.
license: Apache 2.0
metadata:
  speckit-version: 1.0
  speckit-category: analysis
---

# Context Analysis

## Overview
Analyze context quality across multiple dimensions. This skill evaluates text content for clarity, relevance, completeness, consistency, and efficiency to help improve communication effectiveness.

## Analysis Dimensions

### 1. Clarity (0-1)
Measures how clearly information is expressed. Factors include:
- Use of precise language
- Logical flow of ideas
- Absence of ambiguous terms
- Clear structure and organization

### 2. Relevance (0-1)
Measures how well content aligns with the stated goals. Factors include:
- Direct relation to main topic
- Pertinence to intended audience
- Alignment with stated objectives
- Elimination of off-topic content

### 3. Completeness (0-1)
Measures whether key information is present. Factors include:
- Coverage of essential information
- Presence of all required elements
- Sufficient detail for understanding
- Absence of critical gaps

### 4. Consistency (0-1)
Measures logical and factual coherence. Factors include:
- Consistency of terminology
- Logical flow between ideas
- Absence of contradictions
- Factual coherence throughout

### 5. Efficiency (0-1)
Measures information density and conciseness. Factors include:
- Optimal length for content type
- Elimination of redundancy
- Effective use of space
- Clear signal-to-noise ratio

## Process

### Step 1: Content Input
Provide the context or text to be analyzed.

### Step 2: Multi-Dimensional Assessment
Evaluate the content across all relevant dimensions, scoring each from 0 to 1.

### Step 3: Issue Identification
Identify specific problems in each dimension where the score is low.

### Step 4: Improvement Suggestions
Provide actionable suggestions to address identified issues.

### Step 5: Structured Output
Return a structured analysis report with scores, issues, and suggestions.

## Examples
- "Analyze the clarity and relevance of this project specification"
- "Evaluate the completeness and consistency of this technical document"
- "Assess the efficiency of this proposal"

## Guidelines
- Provide numerical scores for each dimension (0-1 scale)
- Identify specific issues in low-scoring dimensions
- Offer concrete, actionable improvement suggestions
- Maintain objectivity in evaluation
- Focus on measurable aspects of quality
- Consider the context and purpose when evaluating