# 测试脚本
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from dsgs_architect import DSGSArchitect
    skill = DSGSArchitect()
    print('Skill loaded successfully')
    print(f'Name: {skill.name}')
    print(f'Description: {skill.description}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()