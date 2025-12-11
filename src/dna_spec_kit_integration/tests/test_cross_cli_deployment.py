"""
跨CLI部署测试
验证DNASPEC技能在不同CLI工具中的部署和执行
"""
import unittest
import json
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.dna_spec_kit_integration.skills.context_analysis_independent import execute_context_analysis
from src.dna_spec_kit_integration.skills.system_architect_independent import execute_system_architect
from src.dna_spec_kit_integration.skills.simple_architect_independent import execute_simple_architect
from src.dna_spec_kit_integration.core.qwen_cli_adapter import QwenCliAdapter


class TestCrossCLIDeployment(unittest.TestCase):
    """跨CLI部署测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.test_context = "请设计一个高可用的电商系统，需要支持商品管理、订单处理、支付功能，要求能够处理高并发场景"
        self.basic_args = {
            "input": self.test_context,
            "detail_level": "standard",
            "options": {},
            "context": {}
        }
    
    def test_context_analysis_independent_execution(self):
        """测试独立上下文分析技能执行"""
        result = execute_context_analysis(self.basic_args)
        
        # 验证返回结果结构
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("metadata", result)
        
        # 验证数据内容
        data = result["data"]
        self.assertIn("overall_score", data)
        self.assertIn("metrics", data)
        self.assertIsInstance(data["overall_score"], (int, float))
        self.assertGreaterEqual(data["overall_score"], 0)
        self.assertLessEqual(data["overall_score"], 1)
        
        # 验证元数据
        metadata = result["metadata"]
        self.assertEqual(metadata["skill_name"], "context-analysis")
        self.assertEqual(metadata["detail_level"], "standard")
    
    def test_context_analysis_detail_levels(self):
        """测试上下文分析技能的不同详细级别"""
        # 测试基础级别
        basic_args = self.basic_args.copy()
        basic_args["detail_level"] = "basic"
        basic_result = execute_context_analysis(basic_args)
        self.assertEqual(basic_result["status"], "success")
        basic_data = basic_result["data"]
        self.assertIn("overall_score", basic_data)
        self.assertIn("main_issues", basic_data)
        
        # 测试标准级别
        standard_args = self.basic_args.copy()
        standard_args["detail_level"] = "standard"
        standard_result = execute_context_analysis(standard_args)
        self.assertEqual(standard_result["status"], "success")
        standard_data = standard_result["data"]
        self.assertIn("overall_score", standard_data)
        self.assertIn("metrics", standard_data)
        self.assertIn("issues", standard_data)
        self.assertIn("suggestions", standard_data)
        
        # 测试详细级别
        detailed_args = self.basic_args.copy()
        detailed_args["detail_level"] = "detailed"
        detailed_result = execute_context_analysis(detailed_args)
        self.assertEqual(detailed_result["status"], "success")
        detailed_data = detailed_result["data"]
        self.assertIn("overall_score", detailed_data)
        self.assertIn("metrics", detailed_data)
        self.assertIn("issues", detailed_data)
        self.assertIn("suggestions", detailed_data)
        self.assertIn("detailed_analysis", detailed_data)
    
    def test_system_architect_independent_execution(self):
        """测试独立系统架构师技能执行"""
        result = execute_system_architect(self.basic_args)
        
        # 验证返回结果结构
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("metadata", result)
        
        # 验证数据内容
        data = result["data"]
        self.assertIn("architecture_type", data)
        self.assertIn("recommended_tech_stack", data)
        self.assertIn("identified_modules", data)
        
        # 验证元数据
        metadata = result["metadata"]
        self.assertEqual(metadata["skill_name"], "system-architect")
        self.assertEqual(metadata["detail_level"], "standard")
    
    def test_simple_architect_independent_execution(self):
        """测试独立简易架构师技能执行"""
        result = execute_simple_architect(self.basic_args)
        
        # 验证返回结果结构
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("metadata", result)
        
        # 验证数据内容
        data = result["data"]
        self.assertIn("recommended_architecture", data)
        self.assertIn("technology_stack", data)
        self.assertIn("deployment_strategy", data)
        
        # 验证元数据
        metadata = result["metadata"]
        self.assertEqual(metadata["skill_name"], "simple-architect")
        self.assertEqual(metadata["detail_level"], "standard")
    
    def test_qwen_cli_adapter_initialization(self):
        """测试Qwen CLI适配器初始化"""
        adapter = QwenCliAdapter()
        self.assertIsNotNone(adapter)
        self.assertIsInstance(adapter.supported_skills, list)
        self.assertGreater(len(adapter.supported_skills), 0)
    
    def test_qwen_cli_adapter_plugin_generation(self):
        """测试Qwen CLI适配器插件生成"""
        adapter = QwenCliAdapter()
        plugin_manifest = adapter.generate_qwen_plugin_manifest(
            "context-analysis", 
            "Analyze context quality"
        )
        
        # 验证插件清单结构
        self.assertIn("type", plugin_manifest)
        self.assertIn("function", plugin_manifest)
        self.assertIn("metadata", plugin_manifest)
        self.assertEqual(plugin_manifest["type"], "function")
        
        # 验证函数定义
        func = plugin_manifest["function"]
        self.assertIn("name", func)
        self.assertIn("description", func)
        self.assertIn("parameters", func)
        self.assertEqual(func["name"], "dnaspec-context-analysis")
        self.assertEqual(func["description"], "Analyze context quality")
        
        # 验证元数据
        metadata = plugin_manifest["metadata"]
        self.assertIn("author", metadata)
        self.assertIn("version", metadata)
        self.assertIn("tags", metadata)
        self.assertEqual(metadata["skill_name"], "context-analysis")
    
    def test_qwen_cli_adapter_deployment(self):
        """测试Qwen CLI适配器部署功能"""
        # 使用临时目录进行测试
        temp_dir = Path(__file__).parent / "temp_qwen_plugins"
        adapter = QwenCliAdapter(str(temp_dir))
        
        try:
            # 部署单个技能
            result = adapter.deploy_skill_to_qwen(
                "context-analysis",
                "Analyze context quality"
            )
            
            # 验证部署结果
            self.assertIn("success", result)
            self.assertTrue(result["success"])
            self.assertIn("plugin_file", result)
            self.assertIn("config_file", result)
            
            # 验证文件创建
            plugin_file = Path(result["plugin_file"])
            config_file = Path(result["config_file"])
            self.assertTrue(plugin_file.exists())
            self.assertTrue(config_file.exists())
            
            # 验证插件文件内容
            with open(plugin_file, 'r', encoding='utf-8') as f:
                plugin_content = json.load(f)
            self.assertEqual(plugin_content["function"]["name"], "dnaspec-context-analysis")
            
        finally:
            # 清理临时文件
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
    
    def test_invalid_input_handling(self):
        """测试无效输入处理"""
        # 测试空输入
        invalid_args = {
            "input": "",
            "detail_level": "standard",
            "options": {},
            "context": {}
        }
        
        result = execute_context_analysis(invalid_args)
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertEqual(result["error"]["type"], "VALIDATION_ERROR")
        
        # 测试非字符串输入
        invalid_args["input"] = 123
        result = execute_context_analysis(invalid_args)
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertEqual(result["error"]["type"], "VALIDATION_ERROR")
    
    def test_command_line_interface(self):
        """测试命令行接口"""
        import subprocess
        import tempfile
        
        # 测试上下文分析技能命令行接口
        cmd = [
            sys.executable, 
            "src/dna_spec_kit_integration/skills/context_analysis_independent.py",
            "测试命令行接口"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root, encoding='utf-8')
            self.assertEqual(result.returncode, 0)
            
            # 验证输出是有效的JSON
            self.assertIsNotNone(result.stdout, "命令行输出为空")
            output = json.loads(result.stdout)
            self.assertEqual(output["status"], "success")
            self.assertIn("data", output)
            
        except FileNotFoundError:
            self.skipTest("无法找到技能脚本文件")
        except json.JSONDecodeError as e:
            self.fail(f"命令行输出不是有效的JSON格式: {e}")
        except Exception as e:
            self.fail(f"命令行测试失败: {e}")


if __name__ == "__main__":
    unittest.main()