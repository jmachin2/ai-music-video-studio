@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
  echo Primero ejecuta INSTALAR_WINDOWS.bat
  pause
  exit /b 1
)
start "AI Music Video Studio" ".venv\Scripts\pythonw.exe" desktop.py
