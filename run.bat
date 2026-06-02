@echo off
cd /d "%~dp0"

REM ── Verifica atualizacao automatica ──────────────────────────
echo Verificando atualizacoes...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/olympiorenno/audio-cleaner/main/audio_cleaner.py' -UseBasicParsing -TimeoutSec 5; if ($r.StatusCode -eq 200) { $r.Content | Set-Content -Path '%~dp0audio_cleaner.py' -Encoding UTF8; Write-Host '  Atualizado!' } } catch { Write-Host '  Sem internet, usando versao local.' }"

REM ── Encontra Python e roda ────────────────────────────────────
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
