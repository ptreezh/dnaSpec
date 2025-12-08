# Directory Capsule: test/

## Purpose
This directory (`test/`) is the central repository for all automated tests within the Dynamic Specification Growth System (DNASPEC). It is structured to support a comprehensive testing strategy, encompassing various levels and types of testing to ensure the quality, reliability, and performance of the DNASPEC. The primary purpose is to provide a robust safety net for development, validate functionalities, and prevent regressions.

## Key Modules/Files (Examples)
*   **`unit/`**: Contains unit tests, focusing on isolated components and functions to verify their correctness.
*   **`integration/`**: Houses integration tests, which validate the interactions between different modules and components.
*   **`e2e/`**: Stores end-to-end tests, simulating real-world user scenarios to ensure the entire system functions as expected.
*   **`performance/`**: Dedicated to performance tests, including benchmarks and stress tests, to evaluate system responsiveness and scalability.
*   **`security/`**: Contains security tests, such as penetration tests, to identify vulnerabilities.
*   **`chaos/`**: Implements chaos engineering experiments to test the system's resilience under turbulent conditions.
*   **`contract/`**: Holds tests specifically for validating API contracts, ensuring adherence to defined specifications.
*   **`FileHelper-tdd.test.ts`**: An example of a test file, likely part of a TDD cycle for a specific utility.

## Dependencies/Relationships
Tests within `test/` depend on the source code in `src/` and potentially configuration files in `config/`. They utilize testing frameworks (e.g., Jest, as indicated by `package.json`) and may rely on test utilities. The test suite is a critical feedback mechanism for developers and directly influences the quality of the codebase.

## Code Generation Guidelines
When generating new tests or test-related code within `test/`, adhere to the following principles:
*   **Test-Driven Development (TDD):** Where applicable, follow TDD principles by writing tests before implementing the corresponding code.
*   **Clear Naming Conventions:** Use descriptive names for test files and test cases to clearly indicate their purpose.
*   **Isolation:** Ensure unit tests are truly isolated, mocking external dependencies as needed.
*   **Coverage:** Strive for high code coverage, especially for critical paths and core functionalities.
*   **Maintainability:** Write clean, readable, and maintainable tests that are easy to understand and update.
*   **Performance (of tests):** Optimize test execution time to provide quick feedback to developers.
*   **BMAD-METHOD Context:** Any generated test code should be designed as a "code capsule" for its specific validation purpose. This includes clear descriptions of what is being tested, why it's important, and how it contributes to the overall system's quality assurance, making it easily consumable by AI agents for test analysis or generation.

## BMAD-METHOD Philosophy Link
This `_GEMINI_DIR_CAPSULE.md` for `test/` embodies the BMAD-METHOD's **Context-Engineered Development** by providing a clear, self-contained definition of the project's testing strategy. It acts as a "graded code capsule" for the entire testing layer, guiding AI agents and human developers on how to approach quality assurance, write effective tests, and understand the project's commitment to reliability. By explicitly defining the testing context, it minimizes "context loss" and facilitates more accurate test generation and analysis.
