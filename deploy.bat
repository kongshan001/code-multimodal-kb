@echo off
REM ============================================================
REM  一键部署（Windows）：装全部环境 + 接入项目（代码+文档+本地记忆+注册）
REM  用法: deploy.bat <代码目录> [文档目录] [项目名]
REM  前置：仅 Python 3.12+。其余（cmm/graphify/ollama/mem0ai）本脚本自动装。
REM ============================================================
chcp 65001 >nul
cd /d "%~dp0"
if "%~1"=="" (echo 用法: %0 ^<代码目录^> [文档目录] [项目名] & pause & exit /b 1)
set "CODE=%~1"
set "DOCS="
if not "%~2"=="" set "DOCS=--docs %~2"
if "%~3"=="" (set "NAME=%~n1") else (set "NAME=%~3")
echo === 一键部署: %NAME% (code=%CODE%) ===
where python >nul 2>&1 || (echo [错误] 未找到 python，先装 Python 3.12+ 并加入 PATH & pause & exit /b 1)
python "%~dp0setup-kb.py" --full --code "%CODE%" %DOCS% --name "%NAME%" --memory-mode local
echo === 完成：重启 Claude Code 后 mcp__* 工具可用 ===
echo. & pause
