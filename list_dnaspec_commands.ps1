# DNASPEC 命令快速查看脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DNASPEC iflow 命令列表" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$commandsPath = ".iflow\commands"
if (Test-Path $commandsPath) {
    $files = Get-ChildItem -Path $commandsPath -Filter "dnaspec-*.md"

    Write-Host "找到 $($files.Count) 个 DNASPEC 命令:" -ForegroundColor Green
    Write-Host ""

    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        $name = $file.Name -replace '\.md$', ''

        # 提取描述和命令
        if ($content -match '## Command\r?\n`([^`]+)`') {
            $command = $matches[1]
        } else {
            $command = "/$name"
        }

        if ($content -match '## Description\r?\n(.+?)(?:\r?\n|\r?\r\n)') {
            $description = $matches[1].Trim()
        } else {
            $description = "无描述"
        }

        Write-Host "命令: $command" -ForegroundColor Yellow
        Write-Host "文件: $($file.Name)" -ForegroundColor Gray
        Write-Host "描述: $description" -ForegroundColor White
        Write-Host ""
    }
} else {
    Write-Host "未找到命令目录: $commandsPath" -ForegroundColor Red
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Green
Write-Host "  1. 运行: .\test_iflow_commands.bat" -ForegroundColor White
Write-Host "  2. 或手动运行: iflow -p `"/dnaspec.task-decomposer 你的任务`"" -ForegroundColor White
Write-Host "  3. 或进入交互模式: iflow" -ForegroundColor White
Write-Host ""
