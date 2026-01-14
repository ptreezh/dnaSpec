@echo off
echo ========================================
echo DNASPEC iflow 命令测试脚本
echo ========================================
echo.
echo 项目目录: %CD%
echo.
echo 可用的 DNASPEC 命令:
echo   1. /dnaspec.task-decomposer    - 任务分解
echo   2. /dnaspec.architect          - 系统架构设计
echo   3. /dnaspec.agent-creator      - 创建智能代理
echo   4. /dnaspec.constraint-generator - 生成约束规则
echo   5. /dnaspec.modulizer          - 代码模块化
echo   6. /dnaspec.dapi-checker       - API验证
echo   7. /dnaspec.cache-manager      - 缓存管理
echo   8. /dnaspec.git-operations     - Git操作
echo.
echo ========================================
echo.
echo 选择测试模式:
echo   1. 快速测试 - 列出所有 dnaspec 命令
echo   2. 任务分解测试
echo   3. 架构设计测试
echo   4. 代理创建测试
echo   5. 进入交互模式
echo   6. 退出
echo.
set /p choice="请选择 (1-6): "

if "%choice%"=="1" (
    echo.
    echo 测试: 列出所有 dnaspec 命令
    echo.
    node "C:\Users\Zhang\AppData\Roaming\npm\node_modules\@iflow-ai\iflow-cli\bundle\iflow.js" -p "列出所有 /dnaspec 开头的命令及其用途，请简洁说明"
) else if "%choice%"=="2" (
    echo.
    echo 测试: 任务分解
    echo.
    node "C:\Users\Zhang\AppData\Roaming\npm\node_modules\@iflow-ai\iflow-cli\bundle\iflow.js" -p "/dnaspec.task-decomposer 将'开发一个待办事项应用'分解为具体的开发任务步骤"
) else if "%choice%"=="3" (
    echo.
    echo 测试: 系统架构设计
    echo.
    node "C:\Users\Zhang\AppData\Roaming\npm\node_modules\@iflow-ai\iflow-cli\bundle\iflow.js" -p "/dnaspec.architect 为一个博客系统设计系统架构"
) else if "%choice%"=="4" (
    echo.
    echo 测试: 创建智能代理
    echo.
    node "C:\Users\Zhang\AppData\Roaming\npm\node_modules\@iflow-ai\iflow-cli\bundle\iflow.js" -p "/dnaspec.agent-creator 创建一个自动化代码审查代理"
) else if "%choice%"=="5" (
    echo.
    echo 启动 iflow 交互模式...
    echo 提示: 输入 /dnaspec.task-decomposer 或其他命令来测试
    echo.
    node "C:\Users\Zhang\AppData\Roaming\npm\node_modules\@iflow-ai\iflow-cli\bundle\iflow.js"
) else if "%choice%"=="6" (
    echo.
    echo 退出测试
    exit /b 0
) else (
    echo.
    echo 无效选择，退出
    exit /b 1
)

echo.
echo ========================================
echo 测试完成
echo ========================================
pause
