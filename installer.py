"""
Audio Cleaner - Instalador
Empacotado com PyInstaller em um .exe standalone
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import tempfile
import ctypes
import winreg
import shutil

REPO_URL   = "https://github.com/olympiorenno/audio-cleaner/archive/refs/heads/main.zip"
VBCABLE_URL = "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip"
PYTHON_URL  = "https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe"
INSTALL_DIR = os.path.join(os.environ.get("LOCALAPPDATA", "C:\\"), "AudioCleaner")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    input("Uma nova janela foi aberta com permissao de administrador.\nPressione Enter para fechar esta...")
    sys.exit()


def log(msg):
    print(msg, flush=True)


def vbcable_installed():
    try:
        import subprocess
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-WmiObject Win32_SoundDevice | Where-Object { $_.Name -like '*VB-Audio*' } | Measure-Object | Select-Object -ExpandProperty Count"],
            capture_output=True, text=True
        )
        return int(result.stdout.strip()) > 0
    except:
        return False


def python_installed():
    return shutil.which("python") is not None


def download_with_progress(url, dest, label):
    def progress(count, block, total):
        pct = min(int(count * block * 100 / total), 100)
        print(f"\r  {label}: {pct}%", end="", flush=True)
    urllib.request.urlretrieve(url, dest, reporthook=progress)
    print()  # nova linha após 100%


def install_python():
    log("  Baixando Python 3.13...")
    installer = os.path.join(tempfile.gettempdir(), "python_installer.exe")
    download_with_progress(PYTHON_URL, installer, "Baixando Python")
    log("  Instalando Python (pode demorar 1-2 min)...")
    subprocess.run([installer, "/quiet", "InstallAllUsers=0", "PrependPath=1"], check=True)
    log("  Python instalado!")


def install_vbcable():
    zip_path = os.path.join(tempfile.gettempdir(), "vbcable.zip")
    download_with_progress(VBCABLE_URL, zip_path, "Baixando VB-Cable")
    extract_path = os.path.join(tempfile.gettempdir(), "vbcable")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_path)
    log("  Instalando VB-Audio Virtual Cable...")
    setup_exe = os.path.join(extract_path, "VBCABLE_Setup_x64.exe")
    subprocess.run([setup_exe, "-i", "-h"], check=True)
    log("  VB-Audio Virtual Cable instalado!")


def download_app():
    zip_path = os.path.join(tempfile.gettempdir(), "audiocleaner.zip")
    download_with_progress(REPO_URL, zip_path, "Baixando Audio Cleaner")

    extract_path = os.path.join(tempfile.gettempdir(), "audiocleaner_src")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_path)

    src = os.path.join(extract_path, "audio-cleaner-main")
    if os.path.exists(INSTALL_DIR):
        shutil.rmtree(INSTALL_DIR)
    shutil.copytree(src, INSTALL_DIR)
    log(f"  Arquivos instalados em: {INSTALL_DIR}")


def install_dependencies():
    log("  Instalando dependências Python (pode demorar 2-3 min)...")
    req = os.path.join(INSTALL_DIR, "requirements.txt")
    subprocess.run(["python", "-m", "pip", "install", "-r", req, "--progress-bar", "on"], check=True)
    log("  Dependências instaladas!")


def download_whisper_model():
    log("  Baixando modelo Whisper tiny (~75MB)...")
    log("  (isso evita espera na primeira vez que usar)")
    # Salva em pasta compartilhada para todos os usuarios
    env = os.environ.copy()
    models_dir = os.path.join(os.environ.get("PROGRAMDATA", r"C:\ProgramData"), "AudioCleaner", "models")
    env["HF_HOME"] = models_dir
    os.makedirs(models_dir, exist_ok=True)
    subprocess.run([
        "python", "-c",
        "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu', compute_type='int8')"
    ], check=True, env=env)
    log("  Modelo Whisper baixado!")


def create_shortcut():
    # Pega o caminho real do Desktop (funciona mesmo com OneDrive)
    result = subprocess.run(
        ["powershell", "-Command", "[Environment]::GetFolderPath('Desktop')"],
        capture_output=True, text=True
    )
    desktop  = result.stdout.strip()
    shortcut = os.path.join(desktop, "Audio Cleaner.lnk")
    target   = os.path.join(INSTALL_DIR, "run.bat")

    ps_script = os.path.join(tempfile.gettempdir(), "create_shortcut.ps1")
    with open(ps_script, "w", encoding="utf-8") as f:
        f.write(f'$ws = New-Object -ComObject WScript.Shell\n')
        f.write(f'$s = $ws.CreateShortcut("{shortcut}")\n')
        f.write(f'$s.TargetPath = "{target}"\n')
        f.write(f'$s.WorkingDirectory = "{INSTALL_DIR}"\n')
        f.write(f'$s.IconLocation = "shell32.dll,168"\n')
        f.write(f'$s.Save()\n')

    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_script], check=True)
    log(f"  Atalho criado em: {shortcut}")


def main():
    if not is_admin():
        log("Solicitando permissão de administrador...")
        run_as_admin()
        return

    print("=" * 50)
    print("     Audio Cleaner - Instalador")
    print("=" * 50)
    print()

    # 1. Python
    log("[1/5] Verificando Python...")
    if python_installed():
        log("  [OK] Python já instalado.")
    else:
        install_python()

    # 2. VB-Cable
    log("\n[2/5] Verificando VB-Audio Virtual Cable...")
    if vbcable_installed():
        log("  [OK] VB-Audio Virtual Cable já instalado.")
    else:
        install_vbcable()

    # 3. Baixa app
    log("\n[3/5] Baixando Audio Cleaner...")
    download_app()

    # 4. Dependências
    log("\n[4/5] Instalando dependências...")
    install_dependencies()

    # 5. Baixa modelo Whisper
    log("\n[5/6] Baixando modelo de IA (Whisper)...")
    download_whisper_model()

    # 6. Atalho
    log("\n[6/6] Criando atalho no Desktop...")
    create_shortcut()

    print()
    print("=" * 50)
    print("  Instalação concluída com sucesso!")
    print("=" * 50)
    print()
    print("Próximos passos:")
    print("  1. REINICIE o PC")
    print("  2. Durante a aula, vá em:")
    print("     Configurações > Som > Mixer de volume")
    print("     e mude o browser para 'CABLE Input'")
    print("  3. Clique no atalho 'Audio Cleaner' no Desktop")
    print()
    input("Pressione Enter para fechar...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print()
        print("=" * 50)
        print("  ERRO durante a instalacao:")
        print(f"  {e}")
        print("=" * 50)
        input("Pressione Enter para fechar...")
