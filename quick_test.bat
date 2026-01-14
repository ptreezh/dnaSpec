@echo off
chcp 65001 >nul
cls
echo.
echo ╔════════════════════════════════════════════╗
echo ║   DNASPEC iflow 命令快速测试工具           ║
echo ║   Quick Test for DNASPEC Commands          ║
echo ╚════════════════════════════════════════════╝
echo.
echo 当前目录: %CD%
echo.

REM 检查 iflow 是否可用
where iflow >nul 2>&1
if %errorlevel% equ 0 (
    echo [√] iflow 命令已找到
    set "IFLOW_CMD=iflow"
) else (
    echo [!] iflow 命令未找到，使用完整路径
    set "IFLOW_CMD=node "C:\Users\Zhang\AppData\Roaming\npm\node_modules\@iflow-ai\iflow-cli\bundle\iflow.js""
)

echo.
echo ══════════════════════════════════════════════
echo  可用的 DNASPEC 命令:
echo ══════════════════════════════════════════════
echo.
echo   [1] task-decomposer    - 任务分解工具
echo   [2] architect          - 系统架构设计
echo   [3] agent-creator      - 智能代理创建
echo   [4] constraint-gen     - 约束规则生成
echo   [5] modulizer          - 代码模块化
echo   [6] dapi-checker       - API接口验证
echo   [7] cache-manager      - 缓存策略优化
echo   [8] git-operations     - Git仓库管理
echo.
echo   [9]  列出所有命令 (验证安装)
echo   [0]  启动 iflow 交互模式
echo   [Q]  退出
echo.
echo ══════════════════════════════════════════════

:menu
set /p choice="请选择测试项目 (0-9, Q): "

if /i "%choice%"=="1" goto test_decomposer
if /i "%choice%"=="2" goto test_architect
if /i "%choice%"=="3" goto test_agent
if /i "%choice%"=="4" goto test_constraint
if /i "%choice%"=="5" goto test_modulizer
if /i "%choice%"=="6" goto test_dapi
if /i "%choice%"=="7" goto test_cache
if /i "%choice%"=="8" goto test_git
if /i "%choice%"=="9" goto test_list
if /i "%choice%"=="0" goto test_interactive
if /i "%choice%"=="Q" goto end
goto invalid

:test_decomposer
echo.
echo [测试] 任务分解工具
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.task-decomposer 将'开发一个简单的待办事项应用'分解为5个主要步骤"
echo.
goto menu

:test_architect
echo.
echo [测试] 系统架构设计
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.architect 为一个个人博客系统设计基础架构"
echo.
goto menu

:test_agent
echo.
echo [测试] 智能代理创建
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.agent-creator 创建一个简单的文件分类助手代理"
echo.
goto menu

:test_constraint
echo.
echo [测试] 约束规则生成
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.constraint-generator 为用户登录功能生成3条安全约束"
echo.
goto menu

:test_modulizer
echo.
echo [测试] 代码模块化
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.modulizer 说明如何将单体应用重构为模块化架构"
echo.
goto menu

:test_dapi
echo.
echo [测试] API接口验证
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.dapi-checker 列出REST API设计的基本检查项"
echo.
goto menu

:test_cache
echo.
echo [测试] 缓存策略优化
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.cache-manager 为一个Web应用建议3条缓存优化策略"
echo.
goto menu

:test_git
echo.
echo [测试] Git仓库管理
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "/dnaspec.git-operations 列出Git仓库维护的最佳实践"
echo.
goto menu

:test_list
echo.
echo [测试] 列出所有命令
echo ─────────────────────────────────────────────
%IFLOW_CMD% -p "请列出所有 /dnaspec 开头的命令，并简要说明每个命令的用途"
echo.
goto menu

:test_interactive
echo.
echo [启动] iflow 交互模式
echo ─────────────────────────────────────────────
echo 提示: 在交互模式中输入以下命令测试:
echo   /dnaspec.task-decomposer 任务描述
echo   /dnaspec.architect 架构需求
echo   /dnaspec.agent-creator 代理需求
echo.
echo 按 Ctrl+C 退出交互模式
echo ─────────────────────────────────────────────
%IFLOW_CMD%
echo.
goto menu

:invalid
echo.
echo [!] 无效选择，请重新输入
echo.
goto menu

:end
echo.
echo ══════════════════════════════════════════════
echo 感谢使用 DNASPEC iflow 测试工具！
echo ══════════════════════════════════════════════
echo.
timeout /t 2 >nul
exit /b 0
