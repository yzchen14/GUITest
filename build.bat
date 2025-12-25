@echo off
REM Windows build script for GUITest with PyInstaller

echo ======================================
echo Building GUITest Windows Executable
echo ======================================

REM Check if Node.js is installed
where node >nul 2>nul
if errorlevel 1 (
    echo ERROR: Node.js is not installed. Please install Node.js first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Install Python dependencies
echo.
echo [1/4] Installing Python dependencies...
pip install pyinstaller fastapi uvicorn pywebview
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

REM Build React frontend
echo.
echo [2/4] Building React frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install npm dependencies
    cd ..
    pause
    exit /b 1
)
call npm run build
if errorlevel 1 (
    echo ERROR: Failed to build React frontend
    cd ..
    pause
    exit /b 1
)
cd ..

REM Create PyInstaller executable
echo.
echo [3/4] Building executable with PyInstaller...
pyinstaller build_exe.spec --clean
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo ======================================
echo Build Complete!
echo ======================================
echo.
echo The executable is located at:
echo   dist\GUITest\GUITest.exe
echo.
pause
