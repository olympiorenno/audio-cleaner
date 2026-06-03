@echo off
set HF_HOME=C:\ProgramData\AudioCleaner\models

REM Mata instancias anteriores para nao sobrepor audio
taskkill /F /IM python.exe /FI "WINDOWTITLE eq audio_cleaner*" >nul 2>&1

REM Inicia o Audio Cleaner
python "%~dp0audio_cleaner.py"
pause
