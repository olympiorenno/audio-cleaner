@echo off
cd /d "%~dp0"

set HF_HOME=C:\ProgramData\AudioCleaner\models

REM Atualiza audio_cleaner.py em segundo plano (sem BOM)
start /b powershell -WindowStyle Hidden -Command "try { $r = Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/olympiorenno/audio-cleaner/main/audio_cleaner.py' -UseBasicParsing -TimeoutSec 5; [System.IO.File]::WriteAllText('%~dp0audio_cleaner.py', $r.Content, [System.Text.UTF8Encoding]::new($false)) } catch {}"

REM Procura Python com sounddevice instalado
FOR %%P IN (
    "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
) DO (
    IF EXIST %%P (
        %%P -c "import sounddevice" >nul 2>&1
        IF %ERRORLEVEL% EQU 0 (
            %%P audio_cleaner.py
            pause
            exit /b 0
        )
    )
)

python -c "import sounddevice" >nul 2>&1
IF %ERRORLEVEL% EQU 0 ( python audio_cleaner.py & pause & exit /b 0 )

echo [ERRO] Python com dependencias nao encontrado.
echo Execute primeiro o install.bat
pause
