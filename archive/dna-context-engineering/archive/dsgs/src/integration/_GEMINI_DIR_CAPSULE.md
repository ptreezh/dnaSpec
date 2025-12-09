# Directory Capsule: src/integration/

## Purpose
This directory (`src/integration/`) is responsible for handling all external integrations of the Dynamic Specification Growth System (DNASPEC). It provides the necessary interfaces and logic for DNASPEC to communicate and interact with external systems, such as Command Line Interfaces (CLI) and Model Context Protocol (MCP) compatible environments (e.g., IDEs). Its primary goal is to expose DNASPEC functionalities to external consumers in a standardized and accessible manner.

## Key Modules/Files
*   **`cli/`**: Contains modules related to the Command Line Interface, allowing users to interact with DNASPEC functionalities via terminal commands.
*   **`mcp/`**: Houses the implementation of the Model Context Protocol (MCP), enabling seamless integration with IDEs and other development tools that support MCP. This is crucial for real-time context provision and constraint application within development environments.

## Dependencies/Relationships
Modules within `src/integration/` depend on the core business logic defined in `src/core/` to perform their operations. They act as adapters, translating external requests into calls to the core DNASPEC functionalities and formatting responses for external consumption. They may also utilize shared utilities from `src/utils/`.

## Code Generation Guidelines
When generating code within `src/integration/`, adhere to the following principles:
*   **External Interface Focus:** Prioritize clear, stable, and well-documented interfaces for external consumption.
*   **Robust Error Handling:** Implement comprehensive error handling to gracefully manage issues arising from external interactions.
*   **Protocol Adherence:** Strictly follow the specifications of the integrated protocols (e.g., MCP, CLI command structures).
*   **Security:** Ensure secure communication and data handling, especially when interacting with external systems.
*   **BMAD-METHOD Context:** Ensure that any generated integration code is designed to facilitate the flow of context. For example, CLI commands should clearly define their input context and expected output context, aligning with the "Context-Engineered Development" philosophy.

## BMAD-METHOD Philosophy Link
This `_GEMINI_DIR_CAPSULE.md` for `src/integration/` exemplifies the BMAD-METHOD's **Context-Engineered Development** by providing a clear, self-contained definition of this integration layer. It ensures that any AI agent or human developer working on external interfaces understands the specific context, protocols, and guidelines for building robust and context-aware integrations. This capsule helps maintain consistency and prevents "context loss" when extending DNASPEC's reach to various development environments and tools.
