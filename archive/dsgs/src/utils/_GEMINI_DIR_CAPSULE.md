# Directory Capsule: src/utils/

## Purpose
This directory (`src/utils/`) is dedicated to housing general utility functions, helper classes, and shared type definitions that are used across various modules and components of the Dynamic Specification Growth System (DSGS). Its primary purpose is to promote code reusability, reduce redundancy, and provide common functionalities that do not belong to any specific core logic, integration, or functional module.

## Key Modules/Files
*   **`error/`**: Contains custom error classes and error handling utilities, ensuring consistent and structured error reporting throughout the application.
*   **`types/`**: Houses shared TypeScript type definitions and interfaces that are utilized by multiple parts of the DSGS, promoting type safety and consistency across the codebase. This includes common data structures, enums, and interface definitions.

## Dependencies/Relationships
Modules within `src/utils/` are designed to be highly independent and have minimal dependencies on other parts of the DSGS project. They are consumed by `src/core/`, `src/integration/`, and `src/modules/` to provide common services. They should not introduce circular dependencies.

## Code Generation Guidelines
When generating code within `src/utils/`, adhere to the following principles:
*   **Generality:** Ensure that utilities are generic enough to be useful in multiple contexts without being tied to specific business logic.
*   **Purity:** Prefer pure functions where possible, avoiding side effects and making them easier to test and reason about.
*   **Testability:** All utility functions and types should be easily testable in isolation.
*   **Performance:** Optimize utility functions for performance, as they may be called frequently across the application.
*   **Clear Documentation:** Provide clear and concise JSDoc comments for all functions, classes, and types, explaining their purpose, parameters, and return values.
*   **BMAD-METHOD Context:** Any new utility should be designed with a clear, well-defined purpose that can be easily encapsulated within its "code capsule" (i.e., its internal documentation and potentially a `_GEMINI_DIR_CAPSULE.md` if it becomes a subdirectory). This ensures that its role in the overall system context is immediately understandable.

## BMAD-METHOD Philosophy Link
This `_GEMINI_DIR_CAPSULE.md` for `src/utils/` exemplifies the BMAD-METHOD's **Context-Engineered Development** by providing a clear, self-contained definition of the utility layer. It acts as a "graded code capsule" for common functionalities, guiding AI agents and human developers on how to create reusable, well-documented, and context-aware utilities. This approach minimizes "context loss" by ensuring that the purpose and usage of shared components are explicitly defined and easily accessible, contributing to a more predictable and maintainable codebase.
