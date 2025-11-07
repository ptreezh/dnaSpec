# TDD驱动的“纵向切片”实施计划

**最终目标:** 实现一个最小化的端到端工作流，通过调用一个简单的 `'liveness'` 技能来验证整个系统的核心架构。

**核心原则:** 每个任务都由一个失败的测试驱动（RED），然后编写最少的代码让测试通过（GREEN），最后进行重构（REFACTOR）。

---

#### **任务 1: 定义“存活”技能 (Skill Definition)**
*   **上下文:** 我们需要一个最简单的技能作为工作流的最终目标。这是我们TDD的“靶心”。
*   **任务:** 在 `src/dsgs_spec_kit_integration/skills/` 目录下创建 `liveness.py` 文件。
*   **核验标准:**
    *   [ ] 文件 `src/dsgs_spec_kit_integration/skills/liveness.py` 已创建。
    *   [ ] 文件中包含一个名为 `execute` 的函数，该函数返回字符串 `"alive"`。

#### **任务 2: 创建端到端集成测试 (E2E Integration Test - RED)**
*   **上下文:** 这是驱动所有后续开发的核心测试。它将定义我们最终要实现的目标，并首先以失败状态存在。
*   **任务:** 在 `tests/integration/` 目录下创建 `test_e2e_liveness_skill.py` 文件，并编写一个失败的测试。
*   **核验标准:**
    *   [ ] 文件 `tests/integration/test_e2e_liveness_skill.py` 已创建。
    *   [ ] 文件中包含测试用例 `test_liveness_skill_end_to_end`。
    *   [ ] 该测试尝试从核心模块（如 `SkillManager`）调用 `liveness` 技能，并断言结果为 `"alive"`。
    *   [ ] **(关键)** 运行 `pytest tests/integration/test_e2e_liveness_skill.py`，**确认测试因核心模块或方法未实现而失败**。

#### **任务 3: 实现最小化核心逻辑 (Minimal Core Logic - GREEN)**
*   **上下文:** 为了让上述的集成测试通过，我们需要用最少的代码实现一个可以找到并执行 `liveness` 技能的核心逻辑。
*   **任务:**
    1.  在 `src/dsgs_spec_kit_integration/core/` 目录下创建或修改核心文件（如 `skill_manager.py`）。
    2.  实现一个最小化的类（如 `SkillManager`），它能够根据技能名称动态加载 `skills` 目录下的模块并执行其 `execute` 函数。
*   **核验标准:**
    *   [ ] **(关键)** 再次运行 `pytest tests/integration/test_e2e_liveness_skill.py`，**确认测试现在通过**。

#### **任务 4: 添加单元测试并重构 (Unit Tests & Refactor - REFACTOR)**
*   **上下文:** 集成测试通过后，核心逻辑是可工作的，但可能很脆弱。我们需要为刚刚创建的核心逻辑添加独立的单元测试，以确保其在各种情况下的行为都符合预期，并为未来的代码重构提供安全保障。
*   **任务:**
    1.  在 `tests/unit/` 目录下为刚才实现的核心逻辑（如 `SkillManager`）编写单元测试。
    2.  测试边界情况，例如：当请求一个不存在的技能时，是否能优雅地抛出异常。
    3.  对核心逻辑代码进行必要的重构，提高其可读性和可维护性。
*   **核验标准:**
    *   [ ] **(关键)** 运行 `pytest tests/unit/`，**确认所有新的单元测试都通过**。
    *   [ ] 再次运行 `pytest tests/integration/`，**确保重构没有破坏端到端功能**。
