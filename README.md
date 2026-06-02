# 🎙️ Audio Cleaner

Remove vícios de linguagem em tempo real durante aulas ou reuniões online, interceptando o áudio do browser antes de chegar nos seus fones/speakers.

## Como funciona

```
Browser → VB-Audio Virtual Cable → Audio Cleaner → Fones/Speakers
                                        ↓
                               Whisper (STT local)
                                        ↓
                          Detecta e silencia vícios
```

O áudio é capturado com ~2 segundos de atraso, transcrito localmente com o modelo Whisper e as palavras configuradas como vícios são silenciadas antes de chegar ao ouvido.

---

## Requisitos

- Windows 10/11
- Python 3.8+
- [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) (gratuito)
- GPU NVIDIA (opcional — usa CPU automaticamente se não disponível)

---

## Instalação

**1. Clone o repositório**
```bash
git clone https://github.com/olympiorenno/audio-cleaner.git
cd audio-cleaner
```

**2. Instale as dependências**
```bash
pip install faster-whisper sounddevice numpy
```

**3. Instale o VB-Audio Virtual Cable**
- Baixe em [vb-audio.com/Cable](https://vb-audio.com/Cable/)
- Execute `VBCABLE_Setup_x64.exe` como administrador
- Reinicie o PC

---

## Como usar

**1. Configure o browser**
- Vá em `Configurações do Windows → Som → Mixer de volume`
- Mude a saída do seu browser para **"CABLE Input (VB-Audio Virtual Cable)"**

**2. Execute o script**

Dê dois cliques em `run.bat`

ou pelo terminal:
```bash
python audio_cleaner.py
```

**3. Assista a aula normalmente**
- O áudio limpo chegará nos seus fones automaticamente
- O terminal mostrará cada vício removido em tempo real

---

## Configuração

Edite as variáveis no topo do `audio_cleaner.py`:

```python
# Vícios a remover
TICS = [
    "né", "né?", "certo", "então", "tipo", ...
]

# "é" longo (hesitação): remove se durar mais que X segundos
E_LONGO_MIN_SEGUNDOS = 0.4

# Tamanho da janela de processamento (segundos de atraso)
CHUNK_SECONDS = 2.0
```

---

## GPU vs CPU

O script detecta automaticamente se há GPU NVIDIA disponível:

| Hardware | Velocidade | Modelo recomendado |
|----------|------------|-------------------|
| GPU NVIDIA (CUDA) | Rápido | `base` ou `small` |
| CPU | Moderado | `tiny` |

Para trocar o modelo, altere `WHISPER_MODEL` no script.

---

## Dependências

| Pacote | Uso |
|--------|-----|
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Transcrição de fala (STT) |
| [sounddevice](https://python-sounddevice.readthedocs.io/) | Captura e reprodução de áudio |
| [numpy](https://numpy.org/) | Processamento de áudio |

---

## Licença

MIT
