# test_shared_context.py
import unittest
import tempfile
import os
from pathlib import Path
import json
from shared_context import SharedContextManager, Task

class TestSharedContext(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # 创建测试用的项目结构和任务文件
        (self.test_dir / "PROJECT_SPEC.json").write_text(
            json.dumps({
                "tasks": [
                    {"description": "Design system architecture", "status": "pending"},
                    {"description": "Implement authentication", "status": "pending"},
                    {"description": "Write documentation", "status": "completed"}
                ]
            })
        )
    
    def tearDown(self):
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_load_tasks_from_project_docs(self):
        """测试从项目文档加载任务"""
        context = SharedContextManager(str(self.test_dir))
        
        # 应该加载3个任务
        self.assertEqual(len(context.tasks), 3)
        
        descriptions = [t.description for t in context.tasks.values()]
        self.assertIn("Design system architecture", descriptions)
        self.assertIn("Implement authentication", descriptions)
        self.assertIn("Write documentation", descriptions)
    
    def test_register_new_task(self):
        """测试注册新任务"""
        context = SharedContextManager(str(self.test_dir))
        original_count = len(context.tasks)
        
        new_task = Task(
            task_id="test_task_12345",
            description="Test new task creation",
            status="pending"
        )
        context.register_task(new_task)
        
        self.assertEqual(len(context.tasks), original_count + 1)
        self.assertIn("test_task_12345", context.tasks)
        
        # 验证任务已保存到文档
        doc_file = self.test_dir / "doc" / "task.md"
        self.assertTrue(doc_file.exists())
        self.assertIn("Test new task creation", doc_file.read_text())
    
    def test_update_task_status(self):
        """测试更新任务状态"""
        context = SharedContextManager(str(self.test_dir))
        
        # 找到一个pending状态的任务
        pending_task = next((t for t in context.tasks.values() if t.status == "pending"), None)
        self.assertIsNotNone(pending_task)
        
        # 更新状态
        context.update_task_status(pending_task.id, "in_progress", "agent_123")
        
        # 验证状态已更新
        self.assertEqual(context.tasks[pending_task.id].status, "in_progress")
        self.assertEqual(context.tasks[pending_task.id].assigned_to, "agent_123")

if __name__ == '__main__':
    unittest.main()