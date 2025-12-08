---
name: dnaspec-dapi-checker
description: DNASPEC Distributed API Documentation Checker for verifying interface consistency and completeness across system components, validating implementation against API documentation. Use when checking interface consistency, validating distributed interfaces, verifying API documentation, or detecting interface inconsistencies.
license: Apache 2.0
allowed-tools: 
  - Bash(python:scripts/dapi_checker.py)
metadata:
  speckit-version: 1.0
  speckit-category: api-validation
---

# DNASPEC Distributed API Documentation Checker (DAPIcheck)

## Overview
DNASPEC Distributed API Documentation Checker is a specialized sub-skill of the DNASPEC Intelligent Architect system. It focuses on verifying interface consistency and completeness across system components, validating implementation against API documentation, and detecting interface-related issues. This skill ensures that distributed systems maintain proper interface contracts and communication integrity.

## Core Functions

### 1. Interface Definition Scanning
Systematically scan interface definitions across the system:
- External APIs exposed by components
- Internal abstract interface definitions
- Data transfer formats and protocols
- Communication protocols and message formats
- Service contracts and agreements

### 2. Consistency and Completeness Checking
Verify interface consistency and completeness:
- Check for interface definition completeness
- Validate interface consistency across components
- Identify missing interface definitions
- Assess interface documentation quality
- Verify interface standardization

### 3. Implementation-Documentation Validation
Validate implementation against documentation:
- Compare actual implementation to documented interfaces
- Identify implementation-documentation mismatches
- Verify parameter definitions and types
- Check response format consistency
- Validate error handling documentation

### 4. Dependency and Compatibility Analysis
Analyze interface dependencies and compatibility:
- Map interface dependencies across components
- Identify potential compatibility issues
- Assess backward compatibility
- Check version alignment across components
- Identify breaking changes and impacts

### 5. Reporting and Recommendations
Generate comprehensive consistency reports:
- Document all identified inconsistencies
- Provide prioritized fix recommendations
- Suggest refactoring strategies
- Highlight critical compatibility issues
- Provide prevention strategies

## Interface Checking Process

### Phase 1: System Scanning
- Identify all system components and their interfaces
- Collect interface definition documents
- Gather implementation code and specifications
- Map component relationships and dependencies
- Establish baseline for comparison

### Phase 2: Interface Analysis
- Analyze external API definitions
- Examine internal abstract interfaces
- Review data transfer protocols
- Assess communication interface designs
- Document interface characteristics

### Phase 3: Consistency Verification
- Compare interface definitions across components
- Verify parameter consistency and naming
- Check data type and format alignment
- Validate response structure consistency
- Assess error handling consistency

### Phase 4: Implementation Validation
- Compare implementation to documentation
- Verify parameter usage matches documentation
- Check actual responses against documented formats
- Validate error handling implementation
- Confirm interface behavior matches documentation

### Phase 5: Compatibility Assessment
- Analyze interface dependencies
- Identify potential breaking changes
- Assess compatibility impacts
- Evaluate version alignment
- Plan for compatibility maintenance

## Check Categories

### External Interface Consistency
- API endpoint definitions and paths
- Request/response parameter definitions
- Authentication and authorization requirements
- Rate limiting and throttling rules
- Error response formats and codes

### Internal Abstract Interface Consistency
- Method signatures and contracts
- Event definitions and structures
- Message format specifications
- Callback and handler definitions
- State transition patterns

### Data Interface Consistency
- Data model definitions and schemas
- Serialization format specifications
- Validation rules and constraints
- Data transformation patterns
- Format version compatibility

### Communication Interface Consistency
- Protocol specifications and versions
- Message format definitions
- Connection and handshake procedures
- Timeout and retry configurations
- Security and encryption specifications

## Advanced Features

### Automated Interface Discovery
- Automatic detection of API endpoints
- Interface definition extraction
- Dependency graph construction
- Interface usage pattern analysis
- Documentation gap identification

### Multi-Version Compatibility Checking
- Cross-version interface comparison
- Breaking change detection
- Backward compatibility verification
- Version migration path validation
- Compatibility matrix generation

### Real-Time Monitoring Integration
- Continuous interface monitoring
- Deviation alerting systems
- Performance impact assessment
- Anomaly detection for interface changes
- Automated reporting of inconsistencies

### Risk Assessment
- Evaluate impact of interface inconsistencies
- Prioritize issues based on severity
- Assess system stability risks
- Plan for mitigation strategies
- Estimate resolution effort

## Output Format

The interface checking will provide:

1. **Consistency Report**
   - List of interface inconsistencies
   - Implementation-documentation gaps
   - Missing interface definitions
   - Parameter mismatches
   - Type and format inconsistencies

2. **Dependency Analysis**
   - Interface dependency mapping
   - Component interdependency overview
   - Potential breaking changes
   - Compatibility issues

3. **Priority Recommendations**
   - Critical issues requiring immediate attention
   - High-priority fixes for stability
   - Medium-priority improvements
   - Low-priority optimization suggestions

4. **Fix Strategies**
   - Recommended resolution approaches
   - Implementation modification plans
   - Documentation update procedures
   - Testing strategies for fixes

5. **Prevention Measures**
   - Process improvements to prevent regressions
   - Automated checking recommendations
   - Documentation standards
   - Review procedures

## Examples
- "Check interface consistency across these microservices"
- "Verify API implementation matches documentation"
- "Identify interface inconsistencies in this distributed system"

## Guidelines
- Prioritize critical and breaking inconsistencies
- Verify interface changes across all dependent components
- Maintain backward compatibility where possible
- Document all identified issues clearly
- Plan fixes in coordinated releases
- Establish automated checking for ongoing consistency