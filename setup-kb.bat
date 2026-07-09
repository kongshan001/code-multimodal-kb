@echo off
REM ============================================================
REM  KB+Memory 交互式接入（Windows）—— 双击或命令行运行均可
REM  逐项提示录入代码/文档目录、项目名、是否启用记忆等，回车用默认。
REM  前置：先装 Python 3.12+（加入 PATH）+ codebase-memory-mcp + graphify + claude
REM  详见 docs/deployment-runbook.md
REM ============================================================
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>&1 || (echo [错误] 未找到 python —— 请先装 Python 3.12+ 并加入 PATH & pause & exit /b 1)
python "%~dp0setup-kb.py" --interactive %*
echo.
pause
