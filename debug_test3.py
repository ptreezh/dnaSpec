import tempfile
import os
from pathlib import Path
from shared_context import SharedContextManager, Task

# 创建测试
with tempfile.TemporaryDirectory() as temp_dir:
    test_path = Path(temp_dir)
    print(f"临时目录: {test_path}")
    
    # 创建测试文件，使发现工作
    (test_path / "PROJECT_SPEC.json").write_text('{"tasks": []}')
    
    # 创建上下文管理器
    context = SharedContextManager(str(test_path))
    
    # 注册一个新任务
    new_task = Task(
        task_id="test_task_12345",
        description="Test new task creation",
        status="pending"
    )
    
    print(f"注册任务前的任务数: {len(context.tasks)}")
    context.register_task(new_task)
    print(f"注册任务后的任务数: {len(context.tasks)}")
    
    # 检查文档文件是否存在
    doc_file = test_path / "doc" / "task.md"
    print(f"文档文件路径: {doc_file}")
    print(f"文档文件是否存在: {doc_file.exists()}")
    
    if doc_file.exists():
        print("文档内容:")
        print(doc_file.read_text())
    else:
        print("文档文件不存在！")
        
        # 检查doc目录是否存在
        doc_dir = test_path / "doc"
        print(f"Doc目录是否存在: {doc_dir.exists()}")
        if doc_dir.exists():
            print("Doc目录内容:", list(doc_dir.iterdir()))