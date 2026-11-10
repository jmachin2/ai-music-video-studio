@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" server.py
) else (
  echo Primero ejecuta INSTALAR_WINDOWS.bat
  pause
)
