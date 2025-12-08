# Project Overview: Dynamic Specification Growth System (DNASPEC)

The Dynamic Specification Growth System (DNASPEC) is a sophisticated software project designed to dynamically generate context-aware constraints for software development tasks. Its primary goal is to enhance code quality and consistency by providing minimal, task-specific constraints that evolve with the project's lifecycle.

**Key Features:**
*   **Dynamic Constraint Generation:** Automatically generates constraints based on task type and context.
*   **Hierarchical Specification Management:** Manages specifications from global rules to task-specific constraints.
*   **Real-time IDE Integration:** Seamless integration with MCP-compatible IDEs.
*   **Phased Evolution:** Supports incremental adoption of features.

**Technologies:**
DNASPEC is built primarily with **TypeScript** and **Node.js**, leveraging `npm` for package management and scripting. It utilizes `jest` for comprehensive testing.

**Architecture:**
The project follows a layered architecture with a clear separation of concerns:
*   `src/core/`: Contains the core business logic, including specification management, constraint generation, neural fields, cognitive tools, and protocol engine.
*   `src/integration/`: Handles external integrations, such as the MCP (Model Context Protocol) implementation and the command-line interface (CLI).
*   `src/utils/`: Provides common utility functions and helpers.
*   `docs/`: Stores project documentation and specifications.
*   `config/`: Contains configuration files, including those for contract management.
*   `test/`: Houses various types of tests (unit, integration, E2E, performance, chaos).

A significant aspect of the architecture is its **contract-driven development** approach, evident from the `config/contract.json` file, which outlines configurations for API contract generation, validation, publishing, and documentation.

# Building and Running

This section outlines the essential commands for setting up, building, and running the DNASPEC project.

## Installation

### From Source
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ptreezh/Dynamic-Specification-Growth-System-DNASPEC.git
    cd Dynamic-Specification-Growth-System-DNASPEC
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Building

To compile the TypeScript source code into JavaScript:
```bash
npm run build
```
This command also triggers contract generation (`npm run contract:generate`).

## Running

### Development Mode
For development with hot-reloading:
```bash
npm run dev
```

### Starting the Application
To run the compiled application:
```bash
npm start
```

## Testing

The project has a comprehensive testing suite.
*   **Run all tests:**
    ```bash
    npm test
    ```
*   **Run tests in watch mode:**
    ```bash
    npm run test:watch
    ```
*   **Generate coverage report:**
    ```bash
    npm run test:coverage
    ```
*   **Run specific test types:**
    *   Unit tests: `npm run test:unit`
    *   Integration tests: `npm run test:integration:full` (and other `test:integration:*` commands)
    *   Property-based tests: `npm run test:property` (and other `test:property:*` commands)
    *   Performance tests: `npm run test:performance`
    *   Chaos engineering tests: `npm run test:chaos`

## Other Useful Scripts

*   **Health Checks:**
    *   `npm run health:check`
    *   `npm run metrics:collect`
    *   `npm run alerts:status`
*   **Contract Management:**
    *   `npm run contract:generate`
    *   `npm run contract:validate`
    *   `npm run contract:publish`
    *   `npm run contract:docs`
    *   `npm run contract:init`
*   **Documentation Checks:** Various `npm run docs:*` commands for compliance, design, review, etc.

# Development Conventions

## TypeScript Configuration
The project enforces strict TypeScript practices, as configured in `tsconfig.json`. Key settings include:
*   `"strict": true`
*   `"noImplicitAny": true`
*   `"strictNullChecks": true`
*   `"strictFunctionTypes": true`
*   `"noImplicitThis": true`
*   `"noImplicitReturns": true`
*   `"noFallthroughCasesInSwitch": true`

## Path Aliases
For improved module resolution and readability, the following path aliases are configured:
*   `@core/*`: maps to `src/core/*`
*   `@integration/*`: maps to `src/integration/*`
*   `@utils/*`: maps to `src/utils/*`

## Testing Practices
DNASPEC employs a robust testing strategy encompassing:
*   **Unit Testing:** Focused on individual components.
*   **Integration Testing:** Verifying interactions between different modules.
*   **End-to-End Testing:** Simulating real-world user scenarios.
*   **Property-Based Testing:** Exploring a wide range of inputs to uncover edge cases.
*   **Performance Testing:** Benchmarking and identifying performance bottlenecks.
*   **Chaos Engineering:** Intentionally introducing failures to test system resilience.

## Contract-Driven Development
The project heavily relies on API contracts to ensure consistency and interoperability. This includes:
*   **Automated Contract Generation:** From source code.
*   **Contract Validation:** Against implementations.
*   **Contract Publishing:** To a central storage.
*   **Documentation Generation:** For API contracts.
*   **Integration with Build/Test Workflows:** Contracts are generated on build and validated on test.

## Documentation
The project emphasizes comprehensive documentation, with various scripts available to check and maintain documentation quality and compliance.

# AI Code Generation Principles

When dynamically generating specifications or code, the following principles **must** be strictly adhered to:

## Core Design Principles
*   **KISS (Keep It Simple, Stupid):** Favor simplicity and avoid unnecessary complexity.
*   **YAGNI (You Aren't Gonna Need It):** Do not add functionality until it is truly required.
*   **SOLID Principles:**
    *   **S**ingle Responsibility Principle: Each module/class/function should have only one reason to change.
    *   **O**pen/Closed Principle: Software entities should be open for extension, but closed for modification.
    *   **L**iskov Substitution Principle: Subtypes must be substitutable for their base types.
    *   **I**nterface Segregation Principle: Clients should not be forced to depend on interfaces they do not use.
    *   **D**ependency Inversion Principle: Depend upon abstractions, not concretions.

## Context and Scope Principles
*   **Self-Evident Principle (自明原则):** Generated specifications and code should be clear, understandable, and self-documenting, minimizing the need for external explanations. This aligns with the "code capsule" concept.
*   **Hierarchical Structuring Principle (层次结构化原则):** Each generated specification or code segment is strictly scoped. It applies *only* to the current directory and all its *first-level subdirectories*. It **must not** delve into or influence any deeper, next-level subdirectories. This reinforces the "Highest Constitutional Rule" for AI context.

## Interface and Encapsulation Principles (Capsule Principle)
*   **Directory Interface Encapsulation (胶囊原则):** Each directory's external interface is based on the "capsule principle." This means:
    *   Its public interfaces (e.g., exported functions, classes, or data structures) are designed to be self-contained and clearly defined.
    *   These interfaces are **only** callable or usable by scripts or modules located in the **parent directory** or **sibling directories** (same level).
    *   They **must not** be used by scripts or modules from other levels (e.g., deeper subdirectories) or cross-level directories. This enforces strict architectural boundaries and promotes clear dependency management at the directory level.

By adhering to these principles, the generated specifications and code will be robust, maintainable, and align with the project's architectural vision, while ensuring efficient and controlled AI interaction.