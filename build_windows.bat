@echo off
setlocal
cd /d "%~dp0"

echo Installing/updating build dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo Building Visual Acuity Calculator...
python -m PyInstaller --clean --noconfirm visual_acuity_calculator.spec
if errorlevel 1 exit /b 1

echo.
echo Build complete:
echo   dist\VisualAcuityCalculator.exe
echo.
pause
