@echo off
setlocal

set "ROOT=%~dp0"
set "PROTO_DIR=%ROOT%07_gui_prototype"
set "PORT=8000"

if not exist "%PROTO_DIR%\" (
  echo GUI prototype directory not found:
  echo   %PROTO_DIR%
  pause
  exit /b 1
)

cd /d "%PROTO_DIR%"

echo GUI HTML static prototype server
echo.
echo Server root:
echo   %PROTO_DIR%
echo.
echo Standard URLs:
echo   http://localhost:%PORT%/start_screen/index.html
echo   http://localhost:%PORT%/town_hub/index.html
echo   http://localhost:%PORT%/guild_screen/index.html
echo   http://localhost:%PORT%/world_map/index.html
echo   http://localhost:%PORT%/dungeon_exploration/index.html
echo   http://localhost:%PORT%/combat_screen/index.html
echo   http://localhost:%PORT%/synthesis_screen/index.html
echo.
echo Do not use file:// for prototype smoke testing; fixtures may fail to load.
echo Press Ctrl+C to stop the server.
echo.

set "PYTHON_CMD="

if exist "%ROOT%.venv\Scripts\python.exe" (
  "%ROOT%.venv\Scripts\python.exe" --version >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=%ROOT%.venv\Scripts\python.exe"
)

if not defined PYTHON_CMD (
  py -3 --version >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
  python --version >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  echo No usable Python command found.
  echo Install Python, fix .venv, or run the bundled Codex Python manually.
  pause
  exit /b 1
)

%PYTHON_CMD% -m http.server %PORT%

pause
