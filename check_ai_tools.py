import subprocess
import os

print('直接测试系统中是否能找到AI工具:')

# 测试claude
try:
    # 使用shell=True来运行Windows命令
    result = subprocess.run('where claude', shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Claude: ✅ 找到了 - {result.stdout.strip()}')
    else:
        print('Claude: ❌ 未找到')
except Exception as e:
    print(f'Claude: 错误 - {e}')

# 测试qwen  
try:
    result = subprocess.run('where qwen', shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Qwen: ✅ 找到了 - {result.stdout.strip()}')
    else:
        print('Qwen: ❌ 未找到')
except Exception as e:
    print(f'Qwen: 错误 - {e}')

# 测试cursor
try:
    result = subprocess.run('where cursor', shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Cursor: ✅ 找到了 - {result.stdout.strip()}')
    else:
        print('Cursor: ❌ 未找到')
except Exception as e:
    print(f'Cursor: 错误 - {e}')

# 检查当前dnaspec安装版本
print('\n检查dnaspec安装情况:')
try:
    import subprocess
    result = subprocess.run(['npm', 'list', '-g', 'dnaspec'], shell=True, capture_output=True, text=True)
    print(f'dnaspec安装情况: {result.stdout if result.stdout.strip() else "未安装或错误"}')
except Exception as e:
    print(f'检查dnaspec安装情况失败: {e}')