@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Ejecuta primero INSTALAR_WINDOWS.bat
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m pip install "pyinstaller>=6,<7"
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --windowed --onedir --name "AI-Music-Video-Studio" --add-data "index.html;." --collect-all "faster_whisper" --collect-all "ctranslate2" desktop.py
if errorlevel 1 goto :error
echo.
echo El ejecutable se encuentra en dist\AI-Music-Video-Studio\AI-Music-Video-Studio.exe
echo Mantener juntos TODOS los archivos de esta carpeta dist.
pause
exit /b 0
:error
echo Fallo en la compilacion de Windows.
pause
exit /b 1
