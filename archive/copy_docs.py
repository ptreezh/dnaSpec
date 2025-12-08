import os
import shutil

# 复制测试目录
source_tests = r"D:\DAIP\dnaSpec\tests"
dest_tests = r"D:\DAIP\dnaspec-core\tests"

if os.path.exists(source_tests):
    shutil.copytree(source_tests, dest_tests)
    print(f"成功复制测试目录 {source_tests} 到 {dest_tests}")

# 复制重要文档
important_files = [
    r"D:\DAIP\dnaSpec\P2-T4_HOOK_SYSTEM_ENHANCEMENT_REPORT.md",
    r"D:\DAIP\dnaSpec\README.md",
    r"D:\DAIP\dnaSpec\pyproject.toml"
]

dest_docs = r"D:\DAIP\dnaspec-core"
os.makedirs(dest_docs, exist_ok=True)

for file_path in important_files:
    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        dest_path = os.path.join(dest_docs, filename)
        shutil.copy2(file_path, dest_path)
        print(f"成功复制文件 {file_path} 到 {dest_path}")