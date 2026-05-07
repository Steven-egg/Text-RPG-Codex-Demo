@echo off
setlocal
set "BUNDLED_PY=C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%BUNDLED_PY%" (
  "%BUNDLED_PY%" "%~dp0element_maze.py"
) else (
  py "%~dp0element_maze.py"
  if errorlevel 1 python "%~dp0element_maze.py"
)

pause
