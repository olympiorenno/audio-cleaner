@echo off

REM Tenta encontrar o Python correto
python -c "import sounddevice" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    python audio_cleaner.py
    pause
    exit /b 0
)

REM Tenta py launcher
py -c "import sounddevice" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    py audio_cleaner.py
    pause
    exit /b 0
)

REM Busca Python em locais comuns
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
