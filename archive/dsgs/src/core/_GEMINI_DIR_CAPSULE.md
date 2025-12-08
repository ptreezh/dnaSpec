# Directory Capsule: src/core/

## Purpose
This directory (`src/core/`) serves as the heart of the Dynamic Specification Growth System (DNASPEC). It encapsulates the fundamental business logic, algorithms, and core components responsible for dynamic constraint generation, context engineering, neural field operations, cognitive tools, and protocol engine management. Modules within this directory are designed to be highly cohesive and loosely coupled, forming the foundational layer upon which the rest of the DNASPEC system is built.

## Key Modules/Files
*   **`ContextEngineeringIntegration.ts`**: (Already has a code capsule) Manages the integration of context engineering principles, responsible for generating context-aware constraints.
*   **`neural-field/`**: Contains modules related to neural field operations, such as `ConstraintNeuralField` and `ConstraintAttractor`, which are crucial for advanced constraint modeling.
*   **`cognitive-tools/`**: Houses various cognitive tools like `ProblemUnderstandingTool`, `RelatedRecallTool`, etc., designed to assist in understanding and processing complex information for constraint generation.
*   **`protocol-engine/`**: Defines the `ProtocolEngine` and related components for managing and executing defined protocols within the system.
*   **`constraint/`**: Contains the core logic for constraint generation, including `TemplateMatcher`, `TemplateEvolver`, and `ConstraintGenerator`.
*   **`specification/`**: Manages the overall specification and its evolution within the DNASPEC.
*   **`types/`**: Defines shared TypeScript types and interfaces used across the core modules, such as `TaskContextCapsule`.
*   **`utils/`**: Provides core utility functions and factories specific to the `core` domain.

## Dependencies/Relationships
Modules within `src/core/` are generally independent of `src/integration/`, `src/modules/`, and `src/utils/` (except for shared utilities). They provide the core services consumed by the integration layer (e.g., CLI, MCP) and other higher-level modules. They primarily depend on each other for internal logic and shared types.

## Code Generation Guidelines
When generating code within `src/core/`, adhere to the following principles:
*   **High Cohesion, Low Coupling:** Ensure new components are focused on a single responsibility and minimize dependencies on external modules.
*   **Type Safety:** Strictly adhere to TypeScript's type system, leveraging interfaces and types defined in `src/core/types/`.
*   **Immutability:** Prefer immutable data structures where appropriate to enhance predictability and reduce side effects.
*   **Testability:** Design components with testability in mind, facilitating unit and integration testing.
*   **Performance:** Optimize for performance, especially in constraint generation and neural field operations, as these are critical path components.
*   **BMAD-METHOD Context:** Ensure that any generated code or new modules are designed with the intent of being easily "context-engineered" – meaning their purpose, dependencies, and usage can be clearly articulated and extracted for AI consumption (e.g., through well-structured comments or dedicated documentation).

## BMAD-METHOD Philosophy Link
This `_GEMINI_DIR_CAPSULE.md` file itself is an embodiment of the BMAD-METHOD's **Context-Engineered Development** principle applied at the directory level. By providing a comprehensive, self-contained overview of `src/core/`, it acts as a "graded code capsule" for this entire foundational layer. This ensures that any AI agent (or human developer) operating within or interacting with `src/core/` has immediate access to the necessary context, architectural guidance, and development conventions, thereby eliminating "context loss" and facilitating more accurate and aligned code generation.
