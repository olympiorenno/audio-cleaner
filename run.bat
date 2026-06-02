@echo off
set HF_HOME=C:\ProgramData\AudioCleaner\models

REM Mata processos anteriores do audio_cleaner para nao sobrepor
taskkill /F /IM python.exe /FI "WINDOWTITLE eq audio_cleaner*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq python.exe" /FI "MEMUSAGE gt 100000" >nul 2>&1

REM Inicia o script
C:\Users\Olympio\AppData\Local\Python\pythoncore-3.14-64\python.exe "%~dp0audio_cleaner.py"
pause
