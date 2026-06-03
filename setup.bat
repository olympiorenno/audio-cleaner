@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================
echo      Audio Cleaner - Setup
echo ========================================
echo.

REM ── Permissao de Administrador ───────────────────────────────────────────────
net session >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Solicitando permissao de Administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM ── 1. Python ─────────────────────────────────────────────────────────────────
echo [1/5] Verificando Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado. Baixando instalador...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe' -OutFile '%TEMP%\python_installer.exe' -UseBasicParsing"
    IF NOT EXIST "%TEMP%\python_installer.exe" (
        echo [ERRO] Falha ao baixar Python. Verifique sua conexao.
        pause & exit /b 1
    )
    echo Instalando Python...
    "%TEMP%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1
    FOR /F "tokens=*" %%P IN ('powershell -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\", \"User\")"') DO SET "PATH=%%P;%PATH%"
    python --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERRO] Instalacao do Python falhou.
        echo Instale manualmente em: https://python.org/downloads
        pause & exit /b 1
    )
    echo [OK] Python instalado.
) ELSE (
    FOR /F "tokens=*" %%V IN ('python --version 2^>^&1') DO echo [OK] %%V encontrado.
)

REM ── 2. Alias Python da Microsoft Store ───────────────────────────────────────
echo.
echo [2/5] Desativando alias Python da Microsoft Store...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\python.exe" /ve /d "" /f >nul 2>&1
echo [OK] Pronto.

REM ── 3. VB-Audio Virtual Cable ─────────────────────────────────────────────────
echo.
echo [3/5] Verificando VB-Audio Virtual Cable...
powershell -Command "Get-WmiObject Win32_SoundDevice | Where-Object { $_.Name -like '*VB-Audio*' }" | findstr /i "VB-Audio" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo [OK] VB-Audio Virtual Cable ja instalado.
) ELSE (
    echo Baixando VB-Audio Virtual Cable...
    powershell -Command "Invoke-WebRequest -Uri 'https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip' -OutFile '%TEMP%\vbcable.zip' -UseBasicParsing"
    IF NOT EXIST "%TEMP%\vbcable.zip" (
        echo [ERRO] Falha ao baixar. Instale manualmente em: https://vb-audio.com/Cable/
        pause & exit /b 1
    )
    powershell -Command "Expand-Archive -Path '%TEMP%\vbcable.zip' -DestinationPath '%TEMP%\vbcable' -Force"
    echo Instalando VB-Audio Virtual Cable...
    "%TEMP%\vbcable\VBCABLE_Setup_x64.exe" -i -h
    echo [OK] VB-Audio Virtual Cable instalado.
)

REM ── 4. Dependencias Python ────────────────────────────────────────────────────
echo.
echo [4/5] Instalando dependencias Python...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r "%~dp0requirements.txt"
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao instalar dependencias.
    pause & exit /b 1
)
echo [OK] Dependencias instaladas.

REM ── 5. Modelo Whisper ─────────────────────────────────────────────────────────
echo.
echo [5/5] Baixando modelo de IA Whisper (~75MB)...
echo       (evita espera na primeira vez que usar)
set HF_HOME=%PROGRAMDATA%\AudioCleaner\models
mkdir "%PROGRAMDATA%\AudioCleaner\models" >nul 2>&1
python -c "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu', compute_type='int8')"
IF %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Nao foi possivel baixar o modelo agora.
    echo         Ele sera baixado automaticamente no primeiro uso (~12s).
) ELSE (
    echo [OK] Modelo Whisper pronto.
)

REM ── Concluido ─────────────────────────────────────────────────────────────────
echo.
echo ========================================
echo          Setup concluido!
echo ========================================
echo.
echo Proximos passos:
echo.
echo  1. REINICIE o PC
echo     (necessario para o VB-Cable funcionar)
echo.
echo  2. Durante a aula/reuniao:
echo     Configuracoes do Windows ^> Som ^> Mixer de volume
echo     Mude a saida do browser para "CABLE Input (VB-Audio)"
echo.
echo  3. Clique duas vezes em run.bat para iniciar
echo.
pause
