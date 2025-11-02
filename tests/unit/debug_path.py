# 调试路径计算
import os

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
print("Current file:", current_file)

# 计算项目根目录 (向上三级: tests/unit/test_hook_system.py -> tests -> . -> project_root)
parent_dir = os.path.dirname(current_file)  # tests/unit/
grandparent_dir = os.path.dirname(parent_dir)  # tests/
project_root = os.path.dirname(grandparent_dir)  # project root
print("Project root:", project_root)

# 检查项目根目录下是否存在src目录
src_dir = os.path.join(project_root, 'src')
print("Src dir exists:", os.path.exists(src_dir))

# 检查是否存在hook.py
hook_file = os.path.join(project_root, 'src', 'dsgs_spec_kit_integration', 'core', 'hook.py')
print("Hook file exists:", os.path.exists(hook_file))

# 打印Python路径
import sys
print("Python path first 3 entries:", sys.path[:3])