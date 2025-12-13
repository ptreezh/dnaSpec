# test_agent_base.py
import unittest
from shared_context import SharedContextManager
from agent_base import Agent

class TestAgentBase(unittest.TestCase):
    def setUp(self):
        self.context_manager = SharedContextManager()
        # 添加一些测试任务
        from shared_context import Task
        task1 = Task("task_1", "Develop API endpoints", status="pending")
        task2 = Task("task_2", "Write tests", status="pending")
        self.context_manager.tasks = {
            "task_1": task1,
            "task_2": task2
        }
    
    def test_connect_to_context(self):
        """测试连接到共享上下文"""
        agent = Agent("test_agent", "developer", ["develop", "code"])
        agent.connect_to_context(self.context_manager)
        
        self.assertEqual(agent.context_manager, self.context_manager)
    
    def test_claim_assigned_task(self):
        """测试认领分配给自己的任务"""
        agent = Agent("test_agent", "developer", ["develop", "code"])
        agent.connect_to_context(self.context_manager)
        
        # 先分配任务给智能体
        task = self.context_manager.tasks["task_1"]
        task.assigned_to = "test_agent"
        
        result = agent.claim_assigned_task("task_1")
        
        self.assertTrue(result)
        self.assertIn("task_1", agent.assigned_tasks)
        
        # 验证状态已更新
        self.assertEqual(self.context_manager.tasks["task_1"].status, "in_progress")
    
    def test_claim_matchable_task(self):
        """测试认领匹配能力的任务"""
        agent = Agent("test_agent", "developer", ["API", "develop"])
        agent.connect_to_context(self.context_manager)
        
        # 修改任务描述以匹配智能体能力
        self.context_manager.tasks["task_1"].description = "Develop API endpoints"
        
        claimed_task_id = agent.claim_matchable_task()
        
        self.assertIsNotNone(claimed_task_id)
        self.assertIn(claimed_task_id, agent.assigned_tasks)
        
        # 验证任务状态已更新
        self.assertEqual(self.context_manager.tasks[claimed_task_id].status, "in_progress")
        self.assertEqual(self.context_manager.tasks[claimed_task_id].assigned_to, "test_agent")
    
    def test_make_autonomous_decision(self):
        """测试自主决策"""
        agent = Agent("test_agent", "planner", ["plan", "evaluate"])
        
        # 验证基类方法会抛出异常，需要子类实现
        with self.assertRaises(NotImplementedError):
            agent.make_autonomous_decision({})

if __name__ == '__main__':
    unittest.main()