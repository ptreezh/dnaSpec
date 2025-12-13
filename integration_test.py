# integration_test.py
import unittest
import tempfile
import os
from pathlib import Path
import json
from task_discovery import TaskDiscovery
from task_storage import TaskStorage
from shared_context import SharedContextManager, Task
from agent_base import Agent

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # 创建测试项目结构
        (self.test_dir / "PROJECT_SPEC.json").write_text(
            json.dumps({
                "tasks": [
                    {"description": "Develop API endpoints", "status": "pending"},
                    {"description": "Write tests", "status": "pending"}
                ]
            })
        )
    
    def tearDown(self):
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_full_system_workflow(self):
        """测试完整的系统工作流程"""
        # 1. 初始化共享上下文管理器
        context = SharedContextManager(str(self.test_dir))
        
        # 2. 验证任务已从项目文档加载
        self.assertGreaterEqual(len(context.tasks), 2)
        
        # 3. 创建智能体
        agent = Agent("api_dev_agent", "developer", ["API", "develop"])
        agent.connect_to_context(context)
        
        # 4. 验证智能体已连接到上下文
        self.assertEqual(agent.context_manager, context)
        
        # 5. 智能体尝试认领匹配的任务
        claimed_task_id = agent.claim_matchable_task()
        
        # 6. 验证任务分配
        if claimed_task_id:
            self.assertIn(claimed_task_id, agent.assigned_tasks)
            # 验证任务状态已更新
            task = context.tasks[claimed_task_id]
            self.assertEqual(task.status, "in_progress")
            self.assertEqual(task.assigned_to, "api_dev_agent")
        
        # 7. 验证任务状态已同步到文档
        doc_file = self.test_dir / "doc" / "task.md"
        self.assertTrue(doc_file.exists())
        
        # 8. 检查文档内容是否包含相关任务
        content = doc_file.read_text()
        if claimed_task_id:
            # 获取认领的任务描述，验证它在文档中
            claimed_task = context.tasks[claimed_task_id]
            self.assertIn(claimed_task.description, content)

if __name__ == '__main__':
    unittest.main()