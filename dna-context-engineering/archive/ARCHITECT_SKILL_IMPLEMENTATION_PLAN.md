# TDD驱动的“Architect”技能实施计划 (V1)

**最终目标:** 实现一个简化版的 `architect` 技能。该技能接收一个关于系统需求的简单文本描述，并返回一个包含几个关键组件的、基于文本的架构图。

**示例:**
*   **输入:** `{"description": "一个简单的电商网站"}`
*   **输出:** `"[WebApp] -> [API Server] -> [Database]"`

---

#### **任务 1: 创建 `architect` 技能的骨架 (Skill Skeleton)**
*   **上下文:** 创建技能文件和基本的 `execute` 函数，作为我们开发的起点。
*   **任务:** 在 `src/dnaspec_spec_kit_integration/skills/` 目录下创建 `architect.py` 文件。
*   **核验标准:**
    *   [ ] 文件 `src/dnaspec_spec_kit_integration/skills/architect.py` 已创建。
    *   [ ] 文件中包含一个 `execute(args: dict)` 函数，目前可以暂时返回一个空字符串。

#### **任务 2: 创建 `architect` 技能的单元测试 (Unit Test - RED)**
*   **上下文:** 编写一个失败的单元测试来驱动 `architect` 技能的逻辑开发。
*   **任务:** 在 `tests/unit/` 目录下创建 `test_architect_skill.py` 文件，并编写一个测试用例，调用 `architect.execute` 函数并断言其返回值。
*   **核验标准:**
    *   [ ] 文件 `tests/unit/test_architect_skill.py` 已创建。
    *   [ ] 包含一个测试用例，例如 `test_architect_for_simple_ecommerce`。
    *   [ ] **(逻辑上)** 运行测试会失败，因为 `architect.execute` 的逻辑尚未实现。

#### **任务 3: 实现最小化的 `architect` 逻辑 (Minimal Logic - GREEN)**
*   **上下文:** 编写最少的代码，让 `architect` 技能的单元测试通过。
*   **任务:** 修改 `architect.py` 中的 `execute` 函数。实现一个简单的逻辑：如果输入的 `description` 包含 "电商"，就返回 `"[WebApp] -> [API Server] -> [Database]"`。
*   **核验标准:**
    *   [ ] **(逻辑上)** 再次运行单元测试，确认测试现在通过。

#### **任务 4: 重构与扩展 (Refactor & Extend)**
*   **上下文:** 基础逻辑通过后，我们可以稍微扩展功能，并使代码结构更清晰，以备未来进行更复杂的分析。
*   **任务:**
    1.  增加对另一种系统（例如 "博客"）的支持。
    2.  为新系统添加一个新的单元测试。
    3.  重构代码，使其更容易扩展（例如，使用字典来映射关键字和架构图）。
*   **核验标准:**
    *   [ ] `architect.py` 的代码结构更清晰。
    *   [ ] `test_architect_skill.py` 包含对 "博客" 系统的测试。
    *   [ ] **(逻辑上)** 所有单元测试都通过。
