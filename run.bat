@echo off
cd /d "%~dp0"

REM ── Usa pasta compartilhada para o modelo Whisper ─────────────
set HF_HOME=C:\ProgramData\AudioCleaner\models

REM ── Atualiza audio_cleaner.py e run.bat em segundo plano ──────
start /b powershell -WindowStyle Hidden -Command "try { $base = 'https://raw.githubusercontent.com/olympiorenno/audio-cleaner/main'; $py = Invoke-WebRequest -Uri \"$base/audio_cleaner.py\" -UseBasicParsing -TimeoutSec 5; $py.Content | Set-Content -Path '%~dp0audio_cleaner.py' -Encoding UTF8; $bat = Invoke-WebRequest -Uri \"$base/run.bat\" -UseBasicParsing -TimeoutSec 5; $bat.Content | Set-Content -Path '%~dp0run.bat' -Encoding UTF8 } catch {}"

REM ── Encontra Python e roda imediatamente ──────────────────────
python -c "import sounddevice" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    python audio_cleaner.py
    pause
    exit /b 0
)

py -c "import sounddevice" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    py audio_cleaner.py
    pause
    exit /b 0
)

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

echo [ERRO] Python com dependencias nao encontrado.
echo Execute primeiro o install.bat
pause
