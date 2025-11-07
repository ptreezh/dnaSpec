@echo off
REM DSGS Context Engineering Skills - 快速启动脚本 (Windows)

echo.
echo ===============================================
echo    DSGS Context Engineering Skills 快速启动
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
python simple_demo.py

echo.
echo ===============================================
echo    DSGS Context Engineering Skills 启动完成
echo ===============================================
echo.
echo 💡 使用提示:
echo    1. 保持虚拟环境激活 (venv\) 
echo    2. 使用: python simple_demo.py 重新运行演示
echo    3. 查看 LOCAL_DEPLOYMENT_GUIDE.md 获取完整文档
echo    4. 在Python代码中导入和使用: 
echo       from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
echo.
pause