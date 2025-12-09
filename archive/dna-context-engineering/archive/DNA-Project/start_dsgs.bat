@echo off
REM DSGS Gemini CLI Extensions 启动脚本

echo ========================================
echo    DSGS Gemini CLI Extensions
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 进入项目目录
cd /d "%~dp0"

REM 启动交互式界面
echo 启动DSGS交互式界面...
echo.
python gemini_interactive_ui.py

echo.
echo 程序已退出。
pause