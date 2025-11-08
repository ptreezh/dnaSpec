---
name: speckit-plan
description: Create technical implementation plans including technology stack choices, architecture decisions, and development approach. Use when planning how to implement project specifications.
license: Apache 2.0
metadata:
  speckit-version: 1.0
  speckit-category: planning
---

# SpecKit - Technical Planning

## Overview
This skill helps create comprehensive technical implementation plans by selecting appropriate technologies, defining architecture, and outlining development approach based on project specifications.

## Process

### 1. Analyze Specifications
First, review the project specifications to understand:
- Functional requirements
- Non-functional requirements
- Constraints and limitations
- Success criteria
- Performance requirements

### 2. Select Technology Stack
Consider and document:

#### 2.1 Frontend Technologies (if applicable)
- Framework selection (React, Vue, Angular, etc.)
- UI component libraries
- State management solutions
- Build tools and bundlers

#### 2.2 Backend Technologies (if applicable)
- Programming language selection
- Framework choice
- Database technology
- API design approach (REST, GraphQL, etc.)
- Authentication and authorization

#### 2.3 Infrastructure
- Hosting platform
- Deployment strategy
- Containerization (Docker, etc.)
- CI/CD pipeline
- Monitoring and logging

#### 2.4 Third-party Services
- External APIs
- Payment processors
- Analytics services
- Email/SMS services

### 3. Define Architecture
Create architectural decisions including:
- High-level system design
- Component interactions
- Data flow diagrams
- Security considerations
- Scalability approach

### 4. Outline Development Approach
Define the development methodology:
- Project management approach (Agile, Scrum, etc.)
- Development phases
- Testing strategy
- Code review process
- Deployment strategy

## Examples
- When planning a web application: "Plan the technology stack and architecture for a user dashboard including React frontend, Node.js backend, PostgreSQL database, and AWS hosting"
- When planning an API: "Plan the technical implementation for a RESTful API including Express.js framework, MongoDB database, authentication with JWT, and Docker containerization"
- When planning a data pipeline: "Plan the technical approach for processing large datasets including Apache Spark, Kafka for streaming, and cloud-based infrastructure"

## Guidelines
- Align technology choices with project requirements
- Consider team expertise and learning curve
- Account for scalability and maintenance
- Include security considerations from the start
- Plan for testing and monitoring
- Document trade-offs and decision rationales
- Consider cost implications of technology choices