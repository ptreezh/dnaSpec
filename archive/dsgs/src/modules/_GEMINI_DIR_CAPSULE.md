# Directory Capsule: src/modules/

## Purpose
This directory (`src/modules/`) is dedicated to housing distinct, self-contained functional modules of the Dynamic Specification Growth System (DSGS). Each subdirectory within `src/modules/` represents a specific domain or feature area, designed to operate with a clear separation of concerns. This modular approach enhances maintainability, scalability, and allows for independent development and deployment of features.

## Key Modules/Files
*   **`contract/`**: Contains the implementation for contract management, including generation, validation, publishing, and documentation of API contracts. This module is crucial for ensuring interoperability and consistency across different parts of the system and external integrations.
*   **`monitoring/`**: Houses functionalities related to system monitoring, health checks, metrics collection, and alert management. This module provides insights into the operational status and performance of the DSGS.

## Dependencies/Relationships
Modules within `src/modules/` typically depend on the core business logic defined in `src/core/` to perform their specialized functions. They may also interact with the `src/integration/` layer to expose their functionalities externally (e.g., via CLI commands or MCP methods). Shared utilities from `src/utils/` are also commonly used. Each module aims to be as independent as possible from other modules within `src/modules/` to minimize inter-module dependencies.

## Code Generation Guidelines
When generating code within `src/modules/`, adhere to the following principles:
*   **Domain-Driven Design:** Focus on encapsulating specific domain logic within each module, ensuring clear boundaries and responsibilities.
*   **Modularity:** Design new features as independent modules where appropriate, promoting reusability and reducing coupling.
*   **Clear APIs:** Define clear and stable internal APIs for interaction between modules and with the core/integration layers.
*   **Test Coverage:** Ensure high test coverage for each module's specific functionalities.
*   **Scalability:** Consider the scalability of the module's design, especially for features that might experience high load or complexity.
*   **BMAD-METHOD Context:** When generating code for a new module, ensure its "code capsule" (i.e., its `_GEMINI_DIR_CAPSULE.md` and internal documentation) clearly defines its domain, responsibilities, and how it contributes to the overall DSGS context.

## BMAD-METHOD Philosophy Link
This `_GEMINI_DIR_CAPSULE.md` for `src/modules/` embodies the BMAD-METHOD's **Context-Engineered Development** by providing a high-level overview of the modular structure. It acts as a "graded code capsule" for the entire modules layer, guiding AI agents and human developers on how to approach the development of new features as distinct, context-rich modules. This approach minimizes "context loss" by ensuring that the purpose and boundaries of each functional area are explicitly defined and easily accessible.
