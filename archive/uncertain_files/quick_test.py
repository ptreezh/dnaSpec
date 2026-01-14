# quick_test.py
# 快速测试所有模块是否都能导入并正常工作
print('Testing module import and basic functionality...')

from task_discovery import TaskDiscovery
from task_storage import TaskStorage
from shared_context import SharedContextManager, Task
from agent_base import Agent

print('✓ All modules imported successfully')

# 测试基本功能
import tempfile
import os
import json
from pathlib import Path

with tempfile.TemporaryDirectory() as temp_dir:
    test_path = Path(temp_dir)
    
    # 创建测试项目文件
    (test_path / 'PROJECT_SPEC.json').write_text(json.dumps({'tasks': [{'description': 'Test task', 'status': 'pending'}]}))
    
    # 测试任务发现
    discovery = TaskDiscovery(str(test_path))
    discovered_tasks = discovery.discover_tasks()
    print(f'✓ Task discovery works: found {len(discovered_tasks)} tasks')
    
    # 测试任务存储
    storage = TaskStorage(str(test_path))
    storage.store_tasks([{'description': 'New task', 'status': 'pending'}])
    print('✓ Task storage works')
    
    # 测试共享上下文
    context = SharedContextManager(str(test_path))
    print(f'✓ Shared context works: loaded {len(context.tasks)} tasks')
    
    # 测试智能体
    agent = Agent('test_agent', 'tester', ['test', 'verify'])
    agent.connect_to_context(context)
    print('✓ Agent base class works')
    
    print('\n✅ All components working together successfully!')