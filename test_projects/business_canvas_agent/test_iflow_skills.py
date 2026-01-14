#!/usr/bin/env python3
"""
DNASPEC 技能 iflow 测试脚本

自动化测试 DNASPEC 技能在 iflow 中的可用性
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

class IFlowSkillTester:
    """iflow 技能测试器"""

    def __init__(self):
        self.iflow_path = r"C:\Users\Zhang\AppData\Roaming\npm\node_modules\@iflow-ai\iflow-cli\bundle\iflow.js"
        self.test_results = []
        self.start_time = datetime.now()

    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def check_iflow_availability(self):
        """检查 iflow 可用性"""
        self.log("检查 iflow 可用性...")

        try:
            result = subprocess.run(
                ['node', self.iflow_path, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"✅ iflow 可用: {version}")
                return True
            else:
                self.log(f"❌ iflow 不可用: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ 检查失败: {e}", "ERROR")
            return False

    def check_deployment_status(self):
        """检查 DNASPEC 部署状态"""
        self.log("检查 DNASPEC 部署状态...")

        hook_file = Path.home() / '.stigmergy' / 'hooks' / 'iflow' / 'dnaspec_iflow_hook.js'

        if hook_file.exists():
            self.log(f"✅ iflow 钩子已部署: {hook_file}")
            return True
        else:
            self.log(f"❌ iflow 钩子未部署", "ERROR")
            return False

    def test_skill_command(self, skill_name, prompt):
        """测试技能命令"""
        self.log(f"测试技能: {skill_name}")

        # 构建 iflow 命令
        command = f"/speckit.dnaspec.{skill_name}\n\n{prompt}"

        self.log(f"输入提示: {prompt[:50]}...")

        # 由于 iflow 是交互式的，我们创建一个测试文件
        test_file = Path("test_input.txt")
        test_file.write_text(command, encoding='utf-8')

        self.log(f"⚠️  需要: 在 iflow 中手动执行命令")
        self.log(f"命令: /speckit.dnaspec.{skill_name}")
        self.log(f"提示: {prompt}")

        return {
            'name': f"测试 {skill_name}",
            'skill': skill_name,
            'prompt': prompt,
            'status': 'manual_test_required',
            'command': f"/speckit.dnaspec.{skill_name}"
        }

    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 70)
        print("🚀 DNASPEC 技能 iflow 测试套件")
        print("=" * 70)
        print()

        # 检查 1: iflow 可用性
        iflow_ok = self.check_iflow_availability()
        print()

        # 检查 2: 部署状态
        deployment_ok = self.check_deployment_status()
        print()

        if not (iflow_ok and deployment_ok):
            self.log("⚠️  环境检查失败，请先解决上述问题", "WARNING")
            return

        # 测试用例
        test_cases = [
            {
                'name': '架构设计技能',
                'skill': 'architect',
                'command': '/speckit.dnaspec.architect',
                'prompt': '''请为商业画布分析智能体设计系统架构。

需求：
1. 数据输入模块（9个商业画布模块）
2. AI 分析引擎（评估完整性和一致性）
3. 建议生成模块（战略优化建议）
4. 技术栈使用 Python

请提供：
- 系统架构图
- 模块划分
- 数据流设计'''
            },
            {
                'name': '上下文分析技能',
                'skill': 'context-analysis',
                'command': '/speckit.dnaspec.context-analysis',
                'prompt': '''请分析商业画布分析智能体的项目上下文：

项目目标：创建AI智能体分析商业模式画布
核心功能：完整性检查、一致性验证、AI分析、建议生成
技术栈：Python, FastAPI, OpenAI API
目标用户：创业者、产品经理、投资人'''
            },
            {
                'name': '认知模板技能',
                'skill': 'cognitive-template',
                'command': '/speckit.dnaspec.cognitive-template',
                'prompt': '''请为商业画布分析创建认知模板：

分析维度：
1. 商业模式完整性
2. 逻辑一致性
3. 可行性评估
4. 优化建议生成'''
            },
            {
                'name': '上下文优化技能',
                'skill': 'context-optimization',
                'command': '/speckit.dnaspec.context-optimization',
                'prompt': '''请优化商业画布分析智能体的项目上下文：

当前问题：
- 分析深度不足
- 建议缺乏针对性
- 输出格式不够专业

优化目标：
- 提高分析质量
- 增强建议实用性
- 改进输出格式'''
            }
        ]

        # 生成测试指南
        self.log("生成测试指南...")

        guide_file = Path("IFLOW_MANUAL_TEST_GUIDE.md")
        guide_content = self._generate_test_guide(test_cases)
        guide_file.write_text(guide_content, encoding='utf-8')

        self.log(f"✅ 测试指南已生成: {guide_file}")

        # 显示测试摘要
        self._print_test_summary(test_cases)

        # 保存测试结果
        self._save_test_results(test_cases)

    def _generate_test_guide(self, test_cases):
        """生成测试指南"""
        guide = f"""# iflow 手动测试指南

生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🚀 测试步骤

### 1. 启动 iflow

```bash
cd D:/DAIP/dnaSpec/test_projects/business_canvas_agent
iflow
```

### 2. 执行测试命令

"""

        for i, test in enumerate(test_cases, 1):
            guide += f"""#### 测试 {i}: {test['name']}

**命令**:
```
{test['command']}
```

**完整提示**:
```
{test['prompt']}
```

**期望输出**:
- [ ] 命令被识别
- [ ] 技能成功执行
- [ ] 输出格式正确
- [ ] 结果质量高

**评分**: ⭐⭐⭐⭐⭐

**备注**: [记录测试结果]

---

"""

        guide += """## 📊 测试结果记录表

| 测试项 | 命令识别 | 执行成功 | 输出质量 | 实用性 | 总评 |
|--------|---------|---------|---------|--------|------|
| 架构设计 |   ✅/❌  |   ✅/❌  |  ⭐⭐⭐⭐⭐ | ✅/❌ |    |
| 上下文分析 |   ✅/❌  |   ✅/❌  |  ⭐⭐⭐⭐⭐ | ✅/❌ |    |
| 认知模板 |   ✅/❌  |   ✅/❌  |  ⭐⭐⭐⭐⭐ | ✅/❌ |    |
| 上下文优化 |   ✅/❌  |   ✅/❌  |  ⭐⭐⭐⭐⭐ | ✅/❌ |    |

## 💡 使用技巧

1. **分步执行**: 一次执行一个技能，观察输出
2. **详细输入**: 提供完整的上下文信息
3. **迭代优化**: 基于输出调整输入，逐步完善
4. **记录结果**: 及时记录测试结果和问题

## 🔧 遇到问题？

### iflow 并发限制
```
您当前的账号已达到平台并发限制
```

**解决**:
1. 关闭所有其他 iflow 实例
2. 等待 1-2 分钟
3. 重启 iflow

### 命令不识别
```
未知命令：/speckit.dnaspec.architect
```

**解决**:
1. 检查 Stigmergy 钩子是否存在
2. 重新部署: `dnaspec deploy --force-stigmergy`
3. 重启 iflow

### 输出质量问题

**解决**:
1. 提供更详细的输入
2. 明确需求和期望
3. 使用结构化提示

---

**准备好开始测试了！** 🚀
"""
        return guide

    def _print_test_summary(self, test_cases):
        """打印测试摘要"""
        print("=" * 70)
        print("📋 测试摘要")
        print("=" * 70)
        print()

        print(f"总测试数: {len(test_cases)}")
        print()

        for i, test in enumerate(test_cases, 1):
            print(f"{i}. {test['name']}")
            print(f"   命令: {test['command']}")
            print(f"   状态: 需要手动测试")
            print()

        print("=" * 70)
        print("✅ 测试指南已生成，请按照指南在 iflow 中手动测试")
        print("=" * 70)

    def _save_test_results(self, test_cases):
        """保存测试结果"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'environment': {
                'iflow_path': self.iflow_path,
                'deployment_mode': 'stigmergy',
                'hook_location': str(Path.home() / '.stigmergy' / 'hooks' / 'iflow')
            },
            'test_cases': test_cases,
            'status': 'manual_test_required',
            'next_steps': [
                '1. 启动 iflow',
                '2. 按照 IFLOW_MANUAL_TEST_GUIDE.md 执行测试',
                '3. 记录测试结果',
                '4. 反馈问题和建议'
            ]
        }

        results_file = Path("test_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        self.log(f"✅ 测试结果已保存: {results_file}")


def main():
    """主函数"""
    tester = IFlowSkillTester()

    try:
        tester.run_all_tests()

        print()
        print("🎯 下一步操作:")
        print()
        print("1. 查看测试指南:")
        print("   cat IFLOW_MANUAL_TEST_GUIDE.md")
        print()
        print("2. 启动 iflow:")
        print("   iflow")
        print()
        print("3. 按照指南执行测试")
        print()

    except KeyboardInterrupt:
        print("\n⚠️  测试被中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
