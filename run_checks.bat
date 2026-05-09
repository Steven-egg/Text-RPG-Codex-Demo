@echo off
python 06_tools\validate_data.py
if errorlevel 1 exit /b %errorlevel%

python element_maze.py --smoke-test
if errorlevel 1 exit /b %errorlevel%

echo all checks ok