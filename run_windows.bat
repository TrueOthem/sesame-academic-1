@echo off
REM This script runs the SESAME Academic application with X11 forwarding on Windows

REM Check if VcXsrv is running
tasklist /FI "IMAGENAME eq vcxsrv.exe" 2>NUL | find /I /N "vcxsrv.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo VcXsrv is already running.
) else (
    echo VcXsrv is not running. Please start VcXsrv with "Multiple windows" and "No Access Control" options.
    echo You can download VcXsrv from https://sourceforge.net/projects/vcxsrv/
    pause
    exit /b 1
)

REM Set the DISPLAY environment variable
set DISPLAY=127.0.0.1:0.0

REM Run the CLI application
echo Running SESAME Academic CLI with interactive plotting...
call venv\Scripts\activate.bat
python cli.py --analysis lca --defaults

pause
