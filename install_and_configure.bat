@echo off
rem DSGS Context Engineering Skills - 一键安装和配置脚本
rem 自动处理环境依赖安装和CLI工具自动配置

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              DSGS Context Engineering Skills                  ║
echo ║                   一键安装配置脚本                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

rem 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python。请先安装Python 3.8或更高版本。
    pause
    exit /b 1
)

rem 检查Git是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Git。请先安装Git。
    pause
    exit /b 1
)

echo ✅ 检测到Python和Git
echo.

rem 克隆项目或更新现有项目
if exist "dnaSpec" (
    echo 🔄 更新现有项目...
    cd dnaSpec
    git pull
) else (
    echo 📦 克隆项目...
    git clone https://github.com/ptreezh/dnaSpec.git
    cd dnaSpec
)

echo.
echo 🛠️  安装依赖和DSGS包...
pip install -e .

if errorlevel 1 (
    echo ❌ 安装失败
    pause
    exit /b 1
)

echo.
echo 🚀 运行自动配置...
python run_auto_config.py

echo.
echo ✅ 安装和配置完成！
echo.
echo 现在您可以在AI CLI工具中使用以下命令：
echo   /speckit.dsgs.context-analysis [上下文] - 分析上下文质量
echo   /speckit.dsgs.context-optimization [上下文] - 优化上下文
echo   /speckit.dsgs.cognitive-template [任务] - 应用认知模板
echo   ...以及其他DSGS技能
echo.
echo 按任意键退出...
pause >nul