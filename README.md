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

## 🚀 Instalação

Escolha a opção que se encaixa melhor:

---

### Opção 1 — Instalador automático (recomendado)

> Ideal para quem só quer usar, sem configurar nada.

**Requisitos:** Windows 10/11 com acesso à internet.

1. Baixe o instalador:

   👉 **[AudioCleaner-Setup.exe](https://github.com/olympiorenno/audio-cleaner/raw/main/dist/AudioCleaner-Setup.exe)**

2. Clique duas vezes e aguarde — ele instala tudo automaticamente:
   - Python
   - VB-Audio Virtual Cable (driver de áudio virtual)
   - Dependências Python
   - Modelo de IA Whisper (~75 MB)
   - Atalho **Audio Cleaner** no Desktop

3. **Reinicie o PC** ao final.

---

### Opção 2 — Setup manual (para quem prefere controle)

> Ideal para desenvolvedores ou quem já tem Python instalado.

**Requisitos:** Windows 10/11, acesso à internet.

1. Clone o repositório:
   ```bash
   git clone https://github.com/olympiorenno/audio-cleaner.git
   cd audio-cleaner
   ```

2. Execute o setup (como Administrador):
   ```
   setup.bat
   ```
   Ele instala o VB-Audio Virtual Cable, as dependências Python e baixa o modelo Whisper.

3. **Reinicie o PC** ao final.

---

## ▶️ Como usar

**1. Configure o browser**

Abra o Mixer de Volume do Windows:
`Configurações → Som → Mixer de volume`

Mude a saída do seu browser para **"CABLE Input (VB-Audio Virtual Cable)"**.

> 💡 No Windows 11, você também encontra isso clicando com o botão direito no ícone de som na barra de tarefas.

**2. Inicie o Audio Cleaner**

Clique duas vezes no atalho **Audio Cleaner** no Desktop — ou execute diretamente:
```
run.bat
```

**3. Assista normalmente**

O áudio chegará nos seus fones com ~2s de atraso e os vícios serão silenciados:

```
  [-] 'né' 0.22s  <<< REMOVIDO
  [-] 'é' 0.64s   <<< REMOVIDO
[Status] Vícios removidos: 12
```

Pressione **Ctrl+C** para encerrar.

> ⚠️ Sempre use Ctrl+C para fechar — fechar a janela sem parar o script pode deixar o áudio travado.

---

## ⚙️ Configuração

Edite o topo do `audio_cleaner.py` para personalizar:

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

## 🔗 Projetos relacionados

| Projeto | Descrição |
|---------|-----------|
| [audio-cleaner](https://github.com/olympiorenno/audio-cleaner) | **Este repositório** — usa VB-Audio Virtual Cable + Whisper |
| [audio_cleaner_extension](https://github.com/olympiorenno/audio_cleaner_extension) | Versão com extensão Chrome — sem VB-Cable, funciona direto no browser via WebSocket |
| [audio-cleaner-keyword](https://github.com/olympiorenno/audio-cleaner-keyword) | Versão leve — detecta vícios por palavras-chave sem Whisper, menor consumo de CPU |

---

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para ideias de melhorias e como enviar um Pull Request.

---

## 📄 Licença

MIT — use, modifique e distribua à vontade.
