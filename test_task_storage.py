# test_task_storage.py
import unittest
import tempfile
import os
from pathlib import Path
import json
from task_storage import TaskStorage

class TestTaskStorage(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_store_tasks_as_markdown(self):
        """测试将任务存储为Markdown格式"""
        storage = TaskStorage(str(self.test_dir))
        tasks = [
            {"description": "Complete API design", "status": "pending"},
            {"description": "Review code", "status": "completed"}
        ]
        
        result_path = storage.store_tasks(tasks, "task.md")
        
        self.assertTrue(Path(result_path).exists())
        
        # 验证内容
        content = Path(result_path).read_text()
        self.assertIn("- [ ] Complete API design", content)
        self.assertIn("- [x] Review code", content)
    
    def test_store_tasks_as_json(self):
        """测试将任务存储为JSON格式"""
        storage = TaskStorage(str(self.test_dir))
        tasks = [{"description": "Write tests", "status": "pending"}]
        
        result_path = storage.store_tasks(tasks, "tasks.json")
        
        self.assertTrue(Path(result_path).exists())
        
        # 验证JSON内容
        with open(result_path, 'r') as f:
            data = json.load(f)
        
        self.assertIn('tasks', data)
        self.assertEqual(len(data['tasks']), 1)
        self.assertEqual(data['tasks'][0]['description'], "Write tests")
    
    def test_update_task_status_in_markdown(self):
        """测试更新Markdown文件中的任务状态"""
        # 准备初始任务文件
        doc_dir = self.test_dir / "doc"
        doc_dir.mkdir()
        (doc_dir / "todo.md").write_text("- [ ] Fix bug #123\n- [ ] Add feature\n")
        
        storage = TaskStorage(str(self.test_dir))
        success = storage.update_task_status("Fix bug #123", "completed")
        
        self.assertTrue(success)
        
        # 验证状态已更新
        content = (doc_dir / "todo.md").read_text()
        self.assertIn("- [x] Fix bug #123", content)
        self.assertIn("- [ ] Add feature", content)
    
    def test_update_task_status_in_json(self):
        """测试更新JSON文件中的任务状态"""
        # 准备初始任务文件
        doc_dir = self.test_dir / "doc"
        doc_dir.mkdir()
        with open(doc_dir / "tasks.json", 'w') as f:
            json.dump({
                "tasks": [
                    {"description": "Implement login", "status": "pending"},
                    {"description": "Setup database", "status": "pending"}
                ]
            }, f)
        
        storage = TaskStorage(str(self.test_dir))
        success = storage.update_task_status("Implement login", "completed")
        
        self.assertTrue(success)
        
        # 验证状态已更新
        with open(doc_dir / "tasks.json", 'r') as f:
            data = json.load(f)
        
        login_task = next((t for t in data['tasks'] if t['description'] == 'Implement login'), None)
        self.assertIsNotNone(login_task)
        self.assertEqual(login_task['status'], 'completed')

if __name__ == '__main__':
    unittest.main()