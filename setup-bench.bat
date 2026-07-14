@echo off
chcp 65001 >nul
REM ============================================================
REM  benchmark 一键安装（Windows）
REM  装 Python 依赖（pytest + anthropic + pyyaml）→ 可跑 bench
REM  用法: 双击 setup-bench.bat 或命令行运行
REM  前置: Python 3.12+（加入 PATH）
REM ============================================================
cd /d "%~dp0"
echo === benchmark 一键安装 ===
where python >nul 2>&1 || (
    echo [错误] 未找到 python —— 请先装 Python 3.12+ 并加入 PATH
    pause
    exit /b 1
)
python --version
echo.
echo --- 装 Python 依赖（eval/requirements.txt）---
python -m pip install -r eval\requirements.txt
if errorlevel 1 (
    echo [错误] pip install 失败 —— 检查网络 / 镜像源
    pause
    exit /b 1
)
echo.
echo === 安装完成 ===
echo.
echo 接下来：
echo   跑评测:    python -m eval.cli run code --target godot-core --method bm25
echo   对比 skills: python -m eval.cli run agent-compare --target godot-core --subset 4
echo   起前端:    python -m eval.cli web
echo   查状态:    python -m eval.cli status
echo.
echo 改配置:    编辑 bench.yaml（模型/价格/上限/端口）
echo.
pause
