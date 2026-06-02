@echo off
setlocal enabledelayedexpansion

echo ========================================
echo      Audio Cleaner - Setup Automatico
echo ========================================
echo.

REM ── Verifica se esta rodando como Administrador ──────────────────────────────
net session >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Solicitando permissao de Administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM ── 1. Verifica e instala Python ─────────────────────────────────────────────
echo [1/4] Verificando Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado. Baixando instalador...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe' -OutFile '%TEMP%\python_installer.exe' -UseBasicParsing"

    IF NOT EXIST "%TEMP%\python_installer.exe" (
        echo [ERRO] Falha ao baixar Python. Verifique sua conexao.
        pause
        exit /b 1
    )

    echo Instalando Python...
    "%TEMP%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1

    REM Atualiza PATH da sessao atual
    FOR /F "tokens=*" %%P IN ('powershell -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\", \"User\")"') DO SET "PATH=%%P;%PATH%"

    python --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERRO] Instalacao do Python falhou.
        echo Instale manualmente em: https://python.org/downloads
        pause
        exit /b 1
    )
    echo [OK] Python instalado com sucesso.
) ELSE (
    FOR /F "tokens=*" %%V IN ('python --version 2^>^&1') DO echo [OK] %%V encontrado.
)

REM ── 2. Desativa alias Python da Microsoft Store ───────────────────────────────
echo.
echo [2/4] Desativando alias Python da Microsoft Store...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\python.exe" /ve /d "" /f >nul 2>&1
powershell -Command "$path = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.py\OpenWithProgids'; if (Test-Path $path) { Remove-ItemProperty -Path $path -Name 'Applications\python.exe' -ErrorAction SilentlyContinue }" >nul 2>&1
echo [OK] Alias desativado.

REM ── 3. Instala VB-Audio Virtual Cable ─────────────────────────────────────────
echo.
echo [3/4] Verificando VB-Audio Virtual Cable...

powershell -Command "Get-WmiObject Win32_SoundDevice | Where-Object { $_.Name -like '*VB-Audio*' }" | findstr /i "VB-Audio" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo [OK] VB-Audio Virtual Cable ja esta instalado.
) ELSE (
    echo Baixando VB-Audio Virtual Cable...
    powershell -Command "Invoke-WebRequest -Uri 'https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip' -OutFile '%TEMP%\vbcable.zip' -UseBasicParsing"

    IF NOT EXIST "%TEMP%\vbcable.zip" (
        echo [ERRO] Falha ao baixar VB-Cable. Verifique sua conexao com a internet.
        echo Baixe manualmente em: https://vb-audio.com/Cable/
        pause
        exit /b 1
    )

    echo Extraindo...
    powershell -Command "Expand-Archive -Path '%TEMP%\vbcable.zip' -DestinationPath '%TEMP%\vbcable' -Force"

    echo Instalando VB-Audio Virtual Cable...
    "%TEMP%\vbcable\VBCABLE_Setup_x64.exe" -i -h

    echo [OK] VB-Audio Virtual Cable instalado.
    echo.
    echo ATENCAO: Sera necessario reiniciar o PC apos a instalacao.
)

REM ── 4. Instala dependencias Python ────────────────────────────────────────────
echo.
echo [4/4] Instalando dependencias Python...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas.

REM ── Concluido ─────────────────────────────────────────────────────────────────
echo.
echo ========================================
echo         Setup concluido!
echo ========================================
echo.
echo Proximos passos:
echo  1. Reinicie o PC (necessario para o VB-Cable funcionar)
echo  2. Durante a aula, va em:
echo     Configuracoes do Windows - Som - Mixer de volume
echo     e mude a saida do browser para "CABLE Input"
echo  3. Clique duas vezes em run.bat para iniciar
echo.
pause
