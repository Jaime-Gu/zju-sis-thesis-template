@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo 没有找到 Python。请先按照 使用说明.md 安装 Python，并勾选 Add python.exe to PATH。
  pause
  exit /b 1
)

python scripts\build.py
if errorlevel 1 (
  echo.
  echo 生成失败。请把上面的错误信息完整复制下来，再对照 使用说明.md 的“遇到问题怎么办”处理。
  pause
  exit /b 1
)

start "" "output\开题和文献综述.pdf"
pause
