@echo off
setlocal

set "ROOT=%~dp0"
set "BRIDGE_SCRIPT=%ROOT%06_tools\gui_runtime_bridge.py"
if not defined HOST set "HOST=127.0.0.1"
if not defined PORT set "PORT=8010"

if not exist "%BRIDGE_SCRIPT%" (
  echo GUI runtime bridge script not found:
  echo   %BRIDGE_SCRIPT%
  pause
  exit /b 1
)

cd /d "%ROOT%"

echo GUI runtime bridge server
echo.
echo Repository root:
echo   %ROOT%
echo.
echo Live test URLs:
echo   http://%HOST%:%PORT%/start_screen/index.html?mode=live
echo   http://%HOST%:%PORT%/town_hub/index.html?mode=live
echo   http://%HOST%:%PORT%/world_map/index.html?mode=live
echo   http://%HOST%:%PORT%/inn_screen/index.html?mode=live
echo.
echo API smoke URL:
echo   http://%HOST%:%PORT%/api/session
echo.
echo Python runtime remains gameplay authority.
echo Do not edit save.json manually; use bridge actions such as Save Game.
echo Press Ctrl+C to stop the server.
echo.

set "PYTHON_EXE="
set "PYTHON_ARGS="

if exist "%ROOT%.venv\Scripts\python.exe" (
  "%ROOT%.venv\Scripts\python.exe" --version >nul 2>nul
  if not errorlevel 1 set "PYTHON_EXE=%ROOT%.venv\Scripts\python.exe"
)

if not defined PYTHON_EXE (
  py -3 --version >nul 2>nul
  if not errorlevel 1 (
    set "PYTHON_EXE=py"
    set "PYTHON_ARGS=-3"
  )
)

if not defined PYTHON_EXE (
  python --version >nul 2>nul
  if not errorlevel 1 set "PYTHON_EXE=python"
)

if not defined PYTHON_EXE (
  if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" --version >nul 2>nul
    if not errorlevel 1 set "PYTHON_EXE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
  )
)

if not defined PYTHON_EXE (
  echo No usable Python command found.
  echo Install Python, fix .venv, or run the bundled Codex Python manually:
  echo   C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe "%BRIDGE_SCRIPT%" --host %HOST% --port %PORT%
  pause
  exit /b 1
)

"%PYTHON_EXE%" %PYTHON_ARGS% "%BRIDGE_SCRIPT%" --host "%HOST%" --port "%PORT%"

pause
