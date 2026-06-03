# 🎙️ Audio Cleaner

Remove vícios de linguagem em tempo real durante aulas ou reuniões online — intercepta o áudio do browser via VB-Audio Virtual Cable, detecta as palavras configuradas e as silencia antes de chegar nos seus fones.

> Desenvolvido com Python + [faster-whisper](https://github.com/SYSTRAN/faster-whisper) + VB-Audio Virtual Cable.
> Processamento **100% local** — sem nuvem, sem custo, sem internet.

---

## ✨ Como funciona

```
Browser → VB-Audio Virtual Cable → Audio Cleaner → Fones/Speakers
                                         ↓
                                Whisper (100% local)
                                         ↓
                           Detecta e silencia os vícios
```

- Detecta automaticamente GPU NVIDIA (CUDA) — usa CPU como fallback
- Atraso de ~2 segundos (necessário para transcrever antes de tocar)

---

## 🖥️ Requisitos

- Windows 10/11
- Python 3.8+ → [python.org/downloads](https://python.org/downloads)
- [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) (gratuito)
- GPU NVIDIA opcional (mais rápido, mas não obrigatório)

---

## 🚀 Instalação rápida (recomendado)

Baixe e execute o instalador — ele faz **tudo automaticamente**:

👉 [AudioCleaner-Setup.exe](https://github.com/olympiorenno/audio-cleaner/raw/main/dist/AudioCleaner-Setup.exe)

O que o instalador faz:
- ✅ Verifica/instala Python
- ✅ Baixa e instala o VB-Audio Virtual Cable
- ✅ Instala todas as dependências Python
- ✅ Baixa o modelo Whisper (~75 MB)
- ✅ Cria atalho **Audio Cleaner** no Desktop

Após instalar: **reinicie o PC** e clique no atalho.

---

## 🛠️ Instalação manual (para desenvolvedores)

```bash
git clone https://github.com/olympiorenno/audio-cleaner.git
cd audio-cleaner
pip install -r requirements.txt
```

Instale o [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) manualmente e reinicie o PC.

---

## ▶️ Como usar

**1. Configure o browser**
- `Configurações do Windows → Som → Mixer de volume`
- Mude a saída do seu browser para **"CABLE Input (VB-Audio Virtual Cable)"**

**2. Inicie o Audio Cleaner**

Dê dois cliques em **`run.bat`** (ou no atalho do Desktop)

**3. Assista normalmente**
- O áudio limpo chegará nos seus fones com ~2s de atraso
- O terminal mostrará cada vício removido em tempo real:

```
  [-] 'né' 0.22s  <<< REMOVIDO
  [-] 'é' 0.64s   <<< REMOVIDO
[Status] Vícios removidos: 12
```

Pressione **Ctrl+C** para encerrar.

---

## ⚙️ Configuração

Edite o topo do `audio_cleaner.py`:

```python
# Palavras a remover
TICS = [
    "né", "né?",
    "então", "então,",
    "pessoal", "pessoal,",
    "ok", "ok?",
]

# "é" longo (hesitação): remove se durar mais que X segundos
E_LONGO_MIN_SEGUNDOS = 0.4

# Modelo Whisper: "tiny" (leve) | "base" | "small" (preciso)
WHISPER_MODEL = "tiny"
```

### Modelos disponíveis

| Modelo | Velocidade | Precisão | Recomendado para |
|--------|------------|----------|-----------------|
| `tiny` | ⚡⚡⚡ | ⭐⭐ | CPU |
| `base` | ⚡⚡ | ⭐⭐⭐ | GPU |
| `small`| ⚡ | ⭐⭐⭐⭐ | GPU potente |

---

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para ideias de melhorias e como enviar um Pull Request.

---

## 📄 Licença

MIT — use, modifique e distribua à vontade.
