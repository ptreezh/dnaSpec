# 调试路径计算
import os

# 测试文件路径
test_file = os.path.abspath(__file__)
print('Test file:', test_file)

# 计算项目根目录
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print('Project root:', project_root)

# 检查是否存在核心文件
hook_file = os.path.join(project_root, 'src', 'dsgs_spec_kit_integration', 'core', 'hook.py')
print('Hook file exists:', os.path.exists(hook_file))