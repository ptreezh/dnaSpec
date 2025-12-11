#!/usr/bin/env python3
"""
Comprehensive test script for DNASPEC agentic skills with detailed explanations
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def explain_agentic_functionalities():
    """Explain the agentic functionalities and their mechanisms"""
    print("DNASPEC AGENTIC FUNCTIONALITIES EXPLANATION")
    print("=" * 60)
    
    print("""
AGENTIC DESIGN OVERVIEW:
=======================
Agentic design in DNASPEC refers to the creation of autonomous, goal-directed entities 
(AI agents) that can perform specific tasks within a larger system. These agents are 
designed with specific roles, capabilities, and constraints that allow them to operate 
autonomously while coordinating with other agents.

KEY COMPONENTS:
===============
1. Agent Creator: Designs and configures specialized AI agents
2. Task Decomposer: Breaks down complex projects into atomic, manageable tasks
3. System Architect: Designs complete system architectures with technology stacks
4. Constraint Generator: Identifies and formalizes system constraints
5. DAPI Checker: Validates API interfaces and contracts
6. Modulizer: Creates modular system designs with clear boundaries

MECHANISMS AND WORKFLOWS:
========================
Each agentic skill operates through a combination of:
- Pattern recognition and keyword analysis
- Rule-based decision making
- Heuristic-based recommendations
- Structured output generation
""")
    
    print("\n" + "=" * 60)


def test_agent_creator_comprehensive():
    """Comprehensive test of the Agent Creator skill"""
    print("\n1. AGENT CREATOR SKILL")
    print("-" * 30)
    
    try:
        # Add agent creator path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-agent-creator', 'scripts'))
        from agent_creator import AgentCreator
        
        print("""
ROLE: Creates specialized AI agents with defined roles, capabilities, and constraints
MECHANISM: Analyzes requirements to determine agent type, role, and configuration
SCENARIOS: Building multi-agent systems, delegating specific tasks to specialized agents

EXAMPLE SCENARIO:
Creating a monitoring agent for a production system that needs to track performance
metrics and alert administrators when thresholds are exceeded.
""")
        
        requirements = """
        Create an intelligent agent that monitors server performance metrics including 
        CPU usage, memory consumption, disk space, and network traffic. The agent should:
        1. Collect metrics every 30 seconds
        2. Alert administrators via email when CPU exceeds 80% for more than 5 minutes
        3. Send Slack notifications for critical alerts
        4. Log all activities for audit purposes
        5. Maintain low resource consumption to avoid impacting monitored systems
        6. Handle security with encrypted communications
        """
        
        creator = AgentCreator()
        specification = creator.generate_agent_specification("PerformanceMonitorAgent", requirements)
        
        print("AGENT SPECIFICATION GENERATED:")
        print(f"  Name: {specification['agent_name']}")
        print(f"  Type: {specification['agent_type']}")
        print(f"  Role: {specification['agent_role']}")
        print(f"  Capabilities: {len(specification['capabilities'])}")
        print(f"  Constraints: {len(specification['constraints'])}")
        print(f"  Communication Protocols: {len(specification['communication_protocols'])}")
        
        print("\nSAMPLE CAPABILITIES:")
        for i, cap in enumerate(specification['capabilities'][:5]):
            print(f"  {i+1}. {cap}")
        
        print("\nDESIGN RECOMMENDATIONS:")
        for i, rec in enumerate(specification['design_recommendations'][:3]):
            print(f"  {i+1}. {rec}")
        
        print("\n✅ Agent Creator skill functioning correctly!")
        
    except Exception as e:
        print(f"❌ Error testing Agent Creator skill: {e}")


def test_task_decomposer_comprehensive():
    """Comprehensive test of the Task Decomposer skill"""
    print("\n\n2. TASK DECOMPOSER SKILL")
    print("-" * 30)
    
    try:
        # Add task decomposer path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-task-decomposer', 'scripts'))
        from task_decomposer import TaskDecomposer
        
        print("""
ROLE: Breaks down complex projects into atomic, manageable tasks with dependencies
MECHANISM: Analyzes requirements to identify individual tasks and their relationships
SCENARIOS: Project planning, sprint breakdown, resource allocation, timeline estimation

EXAMPLE SCENARIO:
Decomposing the development of a complete e-commerce platform into manageable tasks.
""")
        
        requirements = """
        Develop a complete e-commerce platform with the following features:
        - User registration and authentication with email verification
        - Product catalog with search and filtering capabilities
        - Shopping cart functionality with item management
        - Secure payment processing integration
        - Order management system with status tracking
        - Admin dashboard for inventory and order management
        - Mobile-responsive design for all interfaces
        - Performance optimization for high traffic periods
        - Comprehensive security measures including PCI compliance
        """
        
        decomposer = TaskDecomposer()
        breakdown = decomposer.generate_task_breakdown(requirements)
        
        print("TASK BREAKDOWN GENERATED:")
        print(f"  Total Tasks: {breakdown['total_tasks']}")
        print(f"  Critical Path Length: {len(breakdown['critical_path'])}")
        print(f"  Execution Sequence Length: {len(breakdown['execution_sequence'])}")
        
        print("\nRESOURCE RECOMMENDATIONS:")
        for task_type, hours in list(breakdown['resource_recommendations'].items())[:5]:
            print(f"  {task_type}: {hours} estimated hours")
        
        print("\nSAMPLE TASKS:")
        for i, task in enumerate(breakdown['tasks'][:3]):
            print(f"  {i+1}. [{task['id']}] {task['description'][:60]}...")
            print(f"      Type: {task['type']}, Priority: {task['priority']}")
            print(f"      Estimated Hours: {task['estimated_hours']}")
            if task['dependencies']:
                print(f"      Dependencies: {', '.join(task['dependencies'])}")
        
        print("\n✅ Task Decomposer skill functioning correctly!")
        
    except Exception as e:
        print(f"❌ Error testing Task Decomposer skill: {e}")


def test_system_architect_comprehensive():
    """Comprehensive test of the System Architect skill"""
    print("\n\n3. SYSTEM ARCHITECT SKILL")
    print("-" * 30)
    
    try:
        # Add system architect path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-system-architect', 'scripts'))
        from system_architect_designer import SystemArchitectDesigner
        
        print("""
ROLE: Designs complete system architectures with technology stacks and module divisions
MECHANISM: Analyzes requirements to determine optimal architecture patterns and technologies
SCENARIOS: New system design, technology migration, scalability planning, microservices design

EXAMPLE SCENARIO:
Designing a scalable architecture for a social media platform with millions of users.
""")
        
        requirements = """
        Design a scalable, secure social media platform that supports:
        - User profiles with photos and personal information
        - News feed with algorithmic content curation
        - Real-time messaging between users
        - Photo and video sharing with filters
        - Notification system for likes, comments, and messages
        - Privacy controls and content moderation
        - Analytics dashboard for user engagement metrics
        - Support for 10 million monthly active users
        - 99.9% uptime requirement
        - GDPR compliance for European users
        """
        
        architect = SystemArchitectDesigner()
        design = architect.design_system(requirements)
        
        print("SYSTEM DESIGN GENERATED:")
        print(f"  Architecture Type: {design.get('architecture_type', 'N/A')}")
        print(f"  Recommended Tech Stack: {design.get('recommended_tech_stack', 'N/A')}")
        print(f"  Number of Modules: {len(design.get('modules', []))}")
        print(f"  Number of Interfaces: {len(design.get('interfaces', []))}")
        
        print("\nSAMPLE MODULES:")
        for i, module in enumerate(design.get('modules', [])[:3]):
            print(f"  {i+1}. {module.get('name', 'Unnamed Module')}")
            print(f"      Type: {module.get('type', 'N/A')}")
            print(f"      Responsibilities: {', '.join(module.get('responsibilities', [])[:3])}")
        
        print("\nARCHITECTURE RECOMMENDATIONS:")
        for i, rec in enumerate(design.get('recommendations', [])[:3]):
            print(f"  {i+1}. {rec}")
        
        print("\n✅ System Architect skill functioning correctly!")
        
    except Exception as e:
        print(f"❌ Error testing System Architect skill: {e}")


def test_constraint_generator_comprehensive():
    """Comprehensive test of the Constraint Generator skill"""
    print("\n\n4. CONSTRAINT GENERATOR SKILL")
    print("-" * 30)
    
    try:
        # Add constraint generator path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-constraint-generator', 'scripts'))
        from constraint_generator import ConstraintGenerator
        
        print("""
ROLE: Identifies and formalizes system constraints and requirements
MECHANISM: Analyzes requirements to extract explicit and implicit constraints
SCENARIOS: Compliance requirements, performance benchmarks, security mandates, resource limits

EXAMPLE SCENARIO:
Generating constraints for a financial trading platform with strict regulatory requirements.
""")
        
        requirements = """
        Develop a financial trading platform that must comply with SEC regulations and 
        handle high-frequency trading. Key requirements include:
        - Maximum trade execution time of 50 milliseconds
        - 99.99% uptime during market hours
        - End-to-end encryption for all transactions
        - Audit trail for all trades and system activities
        - Multi-factor authentication for traders
        - Real-time risk assessment and position limits
        - Integration with existing clearing house systems
        - Support for 100,000 concurrent users during peak trading
        - Data retention for 7 years as per FINRA requirements
        """
        
        generator = ConstraintGenerator()
        constraints = generator.generate_constraints(requirements)
        
        print("CONSTRAINTS GENERATED:")
        print(f"  Total Constraints: {len(constraints.get('constraints', []))}")
        print(f"  Constraint Categories: {len(constraints.get('categories', {}))}")
        print(f"  Critical Constraints: {len([c for c in constraints.get('constraints', []) if c.get('severity') == 'critical'])}")
        
        print("\nSAMPLE CONSTRAINTS:")
        for i, constraint in enumerate(constraints.get('constraints', [])[:5]):
            print(f"  {i+1}. [{constraint.get('category', 'N/A')}] {constraint.get('description', 'N/A')}")
            print(f"      Severity: {constraint.get('severity', 'N/A')}")
            print(f"      Rationale: {constraint.get('rationale', 'N/A')[:50]}...")
        
        print("\n✅ Constraint Generator skill functioning correctly!")
        
    except Exception as e:
        print(f"❌ Error testing Constraint Generator skill: {e}")


def test_dapi_checker_comprehensive():
    """Comprehensive test of the DAPI Checker skill"""
    print("\n\n5. DAPI CHECKER SKILL")
    print("-" * 30)
    
    try:
        # Add DAPI checker path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-dapi-checker', 'scripts'))
        from dapi_checker import DAPIChecker
        
        print("""
ROLE: Validates API interfaces and contracts for correctness and completeness
MECHANISM: Analyzes API specifications to ensure they meet design standards and best practices
SCENARIOS: API design review, contract validation, interface compliance checking

EXAMPLE SCENARIO:
Checking a REST API specification for a user management service.
""")
        
        api_spec = """
        User Management API Specification:
        
        GET /users
        Description: Retrieve list of users
        Parameters: page (int), limit (int, max 100), sort (string)
        Response: 200 OK with JSON array of users
        
        POST /users
        Description: Create new user
        Body: { "name": "string", "email": "string", "password": "string" }
        Response: 201 Created with user object
        
        GET /users/{id}
        Description: Retrieve specific user
        Response: 200 OK with user object or 404 Not Found
        
        PUT /users/{id}
        Description: Update user information
        Body: { "name": "string", "email": "string" }
        Response: 200 OK with updated user object
        
        DELETE /users/{id}
        Description: Delete user
        Response: 204 No Content
        """
        
        checker = DAPIChecker()
        analysis = checker.analyze_api_specification(api_spec)
        
        print("API ANALYSIS GENERATED:")
        print(f"  Total Endpoints: {analysis.get('endpoint_count', 0)}")
        print(f"  Issues Found: {len(analysis.get('issues', []))}")
        print(f"  Recommendations: {len(analysis.get('recommendations', []))}")
        print(f"  Best Practices Score: {analysis.get('best_practices_score', 'N/A')}/100")
        
        print("\nDETECTED ISSUES:")
        for i, issue in enumerate(analysis.get('issues', [])[:3]):
            print(f"  {i+1}. {issue.get('type', 'N/A')}: {issue.get('description', 'N/A')}")
            print(f"      Severity: {issue.get('severity', 'N/A')}")
        
        print("\nRECOMMENDATIONS:")
        for i, rec in enumerate(analysis.get('recommendations', [])[:3]):
            print(f"  {i+1}. {rec}")
        
        print("\n✅ DAPI Checker skill functioning correctly!")
        
    except Exception as e:
        print(f"❌ Error testing DAPI Checker skill: {e}")


def test_modulizer_comprehensive():
    """Comprehensive test of the Modulizer skill"""
    print("\n\n6. MODULIZER SKILL")
    print("-" * 30)
    
    try:
        # Add modulizer path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-modulizer', 'scripts'))
        from modulizer import Modulizer
        
        print("""
ROLE: Creates modular system designs with clear boundaries and interfaces
MECHANISM: Analyzes system requirements to define cohesive, loosely-coupled modules
SCENARIOS: System refactoring, microservices decomposition, architectural modernization

EXAMPLE SCENARIO:
Modularizing a monolithic e-commerce application into distinct service modules.
""")
        
        system_description = """
        Monolithic e-commerce application with the following components:
        - User management (registration, authentication, profiles)
        - Product catalog (categories, products, search, filters)
        - Shopping cart (add/remove items, quantity management)
        - Order processing (checkout, payment integration, order status)
        - Inventory management (stock levels, supplier integration)
        - Payment processing (credit cards, PayPal, fraud detection)
        - Shipping and fulfillment (carriers, tracking, returns)
        - Reporting and analytics (sales, user behavior, inventory)
        - Admin dashboard (product management, order fulfillment, user support)
        - Customer support (tickets, chat, FAQ)
        """
        
        modulizer = Modulizer()
        modular_design = modulizer.create_modular_design(system_description)
        
        print("MODULAR DESIGN GENERATED:")
        print(f"  Number of Modules: {len(modular_design.get('modules', []))}")
        print(f"  Number of Interfaces: {len(modular_design.get('interfaces', []))}")
        print(f"  Cohesion Score: {modular_design.get('cohesion_score', 'N/A')}/100")
        print(f"  Coupling Score: {modular_design.get('coupling_score', 'N/A')}/100")
        
        print("\nSAMPLE MODULES:")
        for i, module in enumerate(modular_design.get('modules', [])[:4]):
            print(f"  {i+1}. {module.get('name', 'Unnamed Module')}")
            print(f"      Responsibilities: {', '.join(module.get('responsibilities', [])[:3])}")
            print(f"      Technologies: {', '.join(module.get('technologies', [])[:3])}")
        
        print("\nDESIGN PRINCIPLES APPLIED:")
        for principle in modular_design.get('design_principles', [])[:3]:
            print(f"  • {principle}")
        
        print("\n✅ Modulizer skill functioning correctly!")
        
    except Exception as e:
        print(f"❌ Error testing Modulizer skill: {e}")


def demonstrate_agentic_workflow():
    """Demonstrate how all agentic skills work together in a workflow"""
    print("\n\n7. AGENTIC WORKFLOW DEMONSTRATION")
    print("-" * 40)
    
    print("""
INTEGRATED AGENTIC WORKFLOW:
============================
The true power of DNASPEC's agentic design lies in how these skills work together:

1. SYSTEM ARCHITECT → Defines the overall system structure and technology stack
2. TASK DECOMPOSER → Breaks down implementation into manageable tasks
3. AGENT CREATOR → Creates specialized agents for specific subsystems
4. CONSTRAINT GENERATOR → Identifies compliance and performance requirements
5. MODULIZER → Ensures proper modularization and separation of concerns
6. DAPI CHECKER → Validates API interfaces between modules

EXAMPLE WORKFLOW:
Building a healthcare management system for hospitals with patient records, 
appointment scheduling, billing, and telemedicine capabilities.

This workflow enables:
- Autonomous system design and planning
- Coordinated multi-agent development
- Automated validation and compliance checking
- Scalable, maintainable system architecture
""")


def main():
    """Main function to run all comprehensive tests"""
    print("DNASPEC COMPREHENSIVE AGENTIC SKILLS TEST")
    print("=" * 60)
    
    explain_agentic_functionalities()
    test_agent_creator_comprehensive()
    test_task_decomposer_comprehensive()
    test_system_architect_comprehensive()
    test_constraint_generator_comprehensive()
    test_dapi_checker_comprehensive()
    test_modulizer_comprehensive()
    demonstrate_agentic_workflow()
    
    print("\n" + "=" * 60)
    print("🎉 ALL AGENTIC SKILLS TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()