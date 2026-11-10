@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo ERROR: instala Python 3.12 para Windows desde https://www.python.org/downloads/
  echo Durante la instalacion activa "Add Python to PATH".
  pause
  exit /b 1
)
py -3.12 -V >nul 2>nul
if errorlevel 1 (
  echo ERROR: esta version necesita Python 3.12 de 64 bits.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" py -3.12 -m venv .venv
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error
echo.
echo INSTALACION COMPLETADA.
echo Para storyboard automatico instala Ollama: https://ollama.com/download
echo Despues ejecuta en CMD: ollama pull llama3.2:3b
echo Finalmente abre ABRIR_APLICACION_WINDOWS.bat
pause
exit /b 0
:error
echo ERROR: revisa los mensajes anteriores.
pause
exit /b 1
