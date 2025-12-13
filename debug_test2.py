import tempfile
import os
from pathlib import Path
import json

# 模拟测试场景
with tempfile.TemporaryDirectory() as temp_dir:
    # 创建todo.md
    todo_file = Path(temp_dir) / "todo.md"
    with open(todo_file, 'w', encoding='utf-8') as f:
        f.write("# Todo List\n\n- [ ] Write documentation\n- [x] Code review\n")
    
    # 设置当前工作目录并创建.git文件（模拟项目根）
    os.chdir(temp_dir)
    git_dir = Path(temp_dir) / ".git"
    git_dir.mkdir()
    
    from task_discovery import TaskDiscovery
    
    # 使用默认构造函数（从当前目录开始）
    discovery = TaskDiscovery()
    tasks = discovery.discover_tasks()
    
    print(f"发现的任务总数: {len(tasks)}")
    for i, task in enumerate(tasks):
        print(f"{i}: {task}")
    
    pending_tasks = [t for t in tasks if t['status'] == 'pending']
    completed_tasks = [t for t in tasks if t['status'] == 'completed']

    print(f"\npending_tasks数量: {len(pending_tasks)}")
    print(f"completed_tasks数量: {len(completed_tasks)}")
    
    if pending_tasks:
        print(f"pending task 0: {pending_tasks[0]}")