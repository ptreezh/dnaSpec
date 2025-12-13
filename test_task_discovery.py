# test_task_discovery.py
import unittest
import tempfile
import os
from pathlib import Path
import json
from task_discovery import TaskDiscovery

class TestTaskDiscovery(unittest.TestCase):
    def setUp(self):
        """设置测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """清理测试环境"""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_discover_tasks_from_json_file(self):
        """测试从JSON文件发现任务"""
        # 创建测试项目结构
        (self.test_dir / "PROJECT_SPEC.json").write_text(
            json.dumps({
                "tasks": [
                    {"description": "Create API endpoints", "status": "pending"},
                    {"description": "Implement authentication", "status": "completed"}
                ]
            })
        )
        
        discovery = TaskDiscovery(str(self.test_dir))
        tasks = discovery.discover_tasks()
        
        self.assertEqual(len(tasks), 2)
        self.assertIn("Create API endpoints", [t['description'] for t in tasks])
    
    def test_discover_tasks_from_markdown_file(self):
        """测试从Markdown文件发现任务"""
        (self.test_dir / "todo.md").write_text(
            "# Todo List\n\n- [ ] Write documentation\n- [x] Code review\n"
        )
        
        discovery = TaskDiscovery(str(self.test_dir))
        tasks = discovery.discover_tasks()
        
        pending_tasks = [t for t in tasks if t['status'] == 'pending']
        completed_tasks = [t for t in tasks if t['status'] == 'completed']
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(pending_tasks[0]['description'], "Write documentation")
    
    def test_discover_tasks_upward_traversal(self):
        """测试向上遍历发现任务"""
        # 创建目录结构
        sub_dir = self.test_dir / "subfolder"
        sub_dir.mkdir()
        
        # 在根目录创建项目标识和任务文件
        (self.test_dir / ".git").mkdir()
        (self.test_dir / "tasks.json").write_text(
            json.dumps([{"description": "Root task", "status": "pending"}])
        )
        
        # 在子目录进行发现
        os.chdir(sub_dir)
        discovery = TaskDiscovery()
        tasks = discovery.discover_tasks()
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['description'], "Root task")
    
    def test_multiple_task_file_formats(self):
        """测试多种任务文件格式"""
        # 创建多种格式的任务文件
        (self.test_dir / "PROJECT_SPEC.json").write_text(
            json.dumps({"tasks": [{"description": "JSON task", "status": "pending"}]})
        )
        (self.test_dir / "todo.md").write_text("- [ ] Markdown task\n")
        
        discovery = TaskDiscovery(str(self.test_dir))
        tasks = discovery.discover_tasks()
        
        descriptions = [t['description'] for t in tasks]
        self.assertIn("JSON task", descriptions)
        self.assertIn("Markdown task", descriptions)

if __name__ == '__main__':
    unittest.main()