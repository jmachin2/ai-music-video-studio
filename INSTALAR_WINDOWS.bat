@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt
echo.
echo Instala Ollama desde https://ollama.com/download y ejecuta: ollama pull llama3.2:3b
pause
