# Directory Capsule: scripts/

## Purpose
This directory (`scripts/`) is dedicated to housing various automation scripts that support the development, documentation, and maintenance workflows of the Dynamic Specification Growth System (DNASPEC). These scripts are designed to automate repetitive tasks, enforce project standards, and streamline common operations, contributing to increased efficiency and consistency across the development lifecycle.

## Key Modules/Files
*   **`docs-check.sh`**: A shell script likely used for validating documentation, ensuring compliance with standards, and potentially generating reports related to documentation quality.
*   **`install-hooks.sh`**: A script for installing Git hooks (e.g., pre-commit hooks) to automate checks and actions before commits, enforcing code quality and consistency.
*   **`uninstall-hooks.sh`**: A companion script to `install-hooks.sh` for removing the installed Git hooks.
*   **`update-project-state.ts`**: A TypeScript script likely responsible for updating the project's internal state or configuration, possibly related to build processes or deployment.

## Dependencies/Relationships
Scripts within `scripts/` may interact with various parts of the DNASPEC project, including source code (`src/`), documentation (`docs/`), and configuration files (`config/`). They often rely on external tools (e.g., `git`, `npm`, `tsc`) and the project's `package.json` scripts. These scripts are crucial for maintaining the health and integrity of the project.

## Code Generation Guidelines
When generating new scripts or modifying existing ones within `scripts/`, adhere to the following principles:
*   **Automation Focus:** Design scripts to automate tasks that are repetitive, error-prone, or require consistent execution.
*   **Robustness:** Ensure scripts are robust, handle errors gracefully, and provide clear feedback on their execution status.
*   **Idempotence:** Where applicable, design scripts to be idempotent, meaning running them multiple times produces the same result as running them once.
*   **Cross-Platform Compatibility:** Consider the target operating systems and ensure scripts are compatible or provide alternatives for different environments.
*   **Clarity and Documentation:** Scripts should be well-commented and their usage clearly documented, especially for complex operations.
*   **Security:** Be mindful of security implications, especially for scripts that modify system state or interact with sensitive data.
*   **BMAD-METHOD Context:** Any generated script should have a clear, well-defined purpose that can be easily encapsulated within its "code capsule" (i.e., its internal comments and this directory capsule). This ensures that its role in the overall automation context is immediately understandable and contributes to a more "context-engineered" development environment.

## BMAD-METHOD Philosophy Link
This `_GEMINI_DIR_CAPSULE.md` for `scripts/` embodies the BMAD-METHOD's **Context-Engineered Development** by providing a clear, self-contained definition of the project's automation layer. It acts as a "graded code capsule" for operational scripts, guiding AI agents and human developers on how to leverage automation for efficiency and consistency. By explicitly defining the purpose and usage of these scripts, it minimizes "context loss" and facilitates more effective project maintenance and evolution.
