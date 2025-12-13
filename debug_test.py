import tempfile
import os
from pathlib import Path
import json

# 临时调试
test_content = "# Todo List\n\n- [ ] Write documentation\n- [x] Code review\n"
print("测试内容:")
print(repr(test_content))

lines = test_content.split('\n')
print("\n分行内容:")
for i, line in enumerate(lines):
    print(f"{i}: {repr(line)}")
    
print("\n检查每行是否以任务标记开头:")
for i, line in enumerate(lines):
    line = line.strip()
    print(f"{i}: {repr(line)} - startswith('- [ ]'): {line.startswith('- [ ]')}, startswith('- [x]'): {line.startswith('- [x]')}, startswith('TODO:'): {line.startswith('TODO:')}")

# 导入并测试
from task_discovery import TaskDiscovery

# 创建临时文件并测试
with tempfile.TemporaryDirectory() as temp_dir:
    todo_file = Path(temp_dir) / "todo.md"
    with open(todo_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    discovery = TaskDiscovery(temp_dir)
    tasks = discovery._parse_task_file(todo_file)
    
    print(f"\n解析结果:")
    for i, task in enumerate(tasks):
        print(f"{i}: {task}")