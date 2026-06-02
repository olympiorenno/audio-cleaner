@echo off
echo ========================================
echo     Audio Cleaner - Instalacao
echo ========================================
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale o Python em: https://python.org/downloads
    echo IMPORTANTE: marque "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado.
echo.
echo Instalando dependencias...
echo.
python -m pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao instalar dependencias.
    echo Tente rodar como Administrador.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Instalacao concluida com sucesso!
echo ========================================
echo.
echo Proximos passos:
echo  1. Instale o VB-Audio Virtual Cable:
echo     https://vb-audio.com/Cable/
echo.
echo  2. Configure o seu browser para usar
echo     "CABLE Input" como saida de audio.
echo.
echo  3. Clique duas vezes em run.bat para iniciar.
echo.
pause
