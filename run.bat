@echo off
set HF_HOME=%PROGRAMDATA%\AudioCleaner\models

REM Mata instancia anterior especifica do audio_cleaner
wmic process where "CommandLine like '%%audio_cleaner.py%%'" delete >nul 2>&1
timeout /t 1 /nobreak >nul

REM Inicia o Audio Cleaner
python "%~dp0audio_cleaner.py"
pause
