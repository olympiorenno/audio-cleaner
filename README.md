# 🎙️ Audio Cleaner

Remove vícios de linguagem em tempo real durante aulas ou reuniões online — intercepta o áudio do browser, detecta as palavras configuradas e as silencia antes de chegar nos seus fones.

> Desenvolvido com Python + [faster-whisper](https://github.com/SYSTRAN/faster-whisper) + VB-Audio Virtual Cable.

---

## ✨ Como funciona

```
Browser → VB-Audio Virtual Cable → Audio Cleaner → Fones/Speakers
                                         ↓
                                Whisper (100% local)
                                         ↓
                           Detecta e silencia os vícios
```

- Processamento **100% local** — sem nuvem, sem custo, sem internet
- Detecta automaticamente GPU NVIDIA (CUDA) — usa CPU como fallback
- Atraso de ~2 segundos (necessário para transcrever antes de tocar)

---

## 🖥️ Requisitos

- Windows 10/11
- Python 3.8+ → [python.org/downloads](https://python.org/downloads)
- [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) (gratuito)
- GPU NVIDIA opcional (mais rápido, mas não obrigatório)

---

## 🚀 Instalação

**Baixe e execute o instalador:**

👉 [AudioCleaner-Setup.exe](https://github.com/olympiorenno/audio-cleaner/raw/main/AudioCleaner-Setup.exe)

O instalador faz **tudo automaticamente**:
- ✅ Instala o Python
- ✅ Baixa e instala o VB-Audio Virtual Cable
- ✅ Instala todas as dependências
- ✅ Cria atalho **Audio Cleaner** no Desktop

Após instalar: **reinicie o PC** e clique no atalho.

---

## ▶️ Como usar

**1. Configure o browser**
- `Configurações do Windows → Som → Mixer de volume`
- Mude a saída do seu browser para **"CABLE Input (VB-Audio Virtual Cable)"**

**2. Inicie o Audio Cleaner**

Dê dois cliques em **`run.bat`**

**3. Assista normalmente**
- O áudio limpo chegará nos seus fones com ~2s de atraso
- O terminal mostrará cada vício removido em tempo real:
```
  [-] 'né' 0.22s  [0.9→1.1]
  [-] 'é' 0.64s  [0.0→0.6]
[Status] Vícios removidos: 12
```

---

## ⚙️ Configuração

Edite o topo do `audio_cleaner.py`:

```python
# Palavras a remover
TICS = [
    "né", "né?", "certo", "então", "tipo", ...
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
