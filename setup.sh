#!/bin/bash
set -e

echo "========================================"
echo "     Audio Cleaner - Setup (macOS)"
echo "========================================"
echo

# ── 1. Homebrew ───────────────────────────────────────────────────────────────
echo "[1/4] Verificando Homebrew..."
if ! command -v brew &>/dev/null; then
    echo "Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "[OK] Homebrew encontrado."
fi

# ── 2. Python ─────────────────────────────────────────────────────────────────
echo
echo "[2/4] Verificando Python..."
if ! command -v python3 &>/dev/null; then
    echo "Instalando Python..."
    brew install python
else
    echo "[OK] $(python3 --version) encontrado."
fi

# ── 3. BlackHole (substituto do VB-Audio no macOS) ───────────────────────────
echo
echo "[3/4] Verificando BlackHole (driver de audio virtual)..."
if ! brew list --cask blackhole-2ch &>/dev/null; then
    echo "Instalando BlackHole..."
    brew install --cask blackhole-2ch
    echo "[OK] BlackHole instalado."
    echo "     Reinicie o Mac para o driver ser reconhecido."
else
    echo "[OK] BlackHole ja instalado."
fi

# ── 4. Dependencias Python ────────────────────────────────────────────────────
echo
echo "[4/4] Instalando dependencias Python..."
pip3 install -r "$(dirname "$0")/requirements.txt"
echo "[OK] Dependencias instaladas."

# ── Modelo Whisper ────────────────────────────────────────────────────────────
echo
echo "Baixando modelo Whisper tiny (~75MB)..."
HF_HOME="/Library/Application Support/AudioCleaner/models" \
python3 -c "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu', compute_type='int8')"
echo "[OK] Modelo pronto."

echo
echo "========================================"
echo "          Setup concluido!"
echo "========================================"
echo
echo "Proximos passos:"
echo "  1. REINICIE o Mac (necessario para o BlackHole funcionar)"
echo "  2. Va em Preferencias do Sistema → Som → Saida"
echo "     e mude a saida do browser para 'BlackHole 2ch'"
echo "  3. Execute: bash run.sh"
echo
