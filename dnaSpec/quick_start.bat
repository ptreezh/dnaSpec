@echo off
REM DSGS与spec.kit整合项目 - 快速启动脚本 (Windows)

echo.
echo ===============================================
echo    DSGS与spec.kit整合项目 快速启动
echo ===============================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未找到，请安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 安装依赖...
pip install -e . >nul 2>&1
if errorlevel 1 (
    echo ❌ 安装依赖失败
    pause
    exit /b 1
)

echo ✅ 依赖安装完成

REM 运行快速演示
echo.
echo 🚀 运行系统演示...
python -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'dist'))

print('=== DSGS与spec.kit整合项目 演示 ===')
print()

# 演示上下文分析技能
from clean_skills.context_analysis import execute as context_analysis_execute
result = context_analysis_execute({'context': '设计一个用户登录系统', 'mode': 'enhanced'})
print('✓ 上下文分析技能（增强模式）演示:')
print(result[:200] + '...' if len(result) > 200 else result)
print()

# 演示Git技能
from clean_skills.git_skill import execute as git_execute
result = git_execute({'operation': 'status'})
print('✓ Git技能演示 (仓库状态):')
print(result[:100] + '...' if len(result) > 100 else result)
print()

# 演示临时工作区技能
from clean_skills.temp_workspace_skill import execute as temp_workspace_execute
result = temp_workspace_execute({'operation': 'create-workspace'})
print('✓ 临时工作区管理演示: 工作区创建成功')
ws_path = result

# 添加一个文件
temp_workspace_execute({
    'operation': 'add-file',
    'file_path': 'demo_file.py',
    'file_content': '# 这是一个演示文件\nprint(\"Hello DSGS!\")'
})
print('✓ 文件添加到临时工作区')

# 确认文件
temp_workspace_execute({'operation': 'confirm-file', 'confirm_file': 'demo_file.py'})
print('✓ 文件确认演示')

# 清理工作区
temp_workspace_execute({'operation': 'clean-workspace'})
print('✓ 临时工作区清理演示')

print()
print('=== 演示完成 ===')
print('项目包含完整的AI安全工作流，防止AI生成文件污染项目！')
"

echo.
echo ===============================================
echo    DSGS与spec.kit整合项目 启动完成
echo ===============================================
echo.
echo 💡 使用提示:
echo    1. 保持虚拟环境激活 (venv\) 
echo    2. 使用: python -c \"...\" 运行自定义命令
echo    3. 查看 INSTALL_GUIDE.md 获取完整安装文档
echo    4. 查看 README.md 了解所有技能和功能
echo    5. 查看 AI_SAFETY_GUIDELINES.md 了解AI安全工作流
echo    6. 在Python代码中导入和使用:
echo       from clean_skills import context_analysis_execute, git_execute, temp_workspace_execute
echo.
pause