# Como Contribuir

Obrigado pelo interesse! Toda contribuição é bem-vinda — desde correções de bug até novas funcionalidades.

---

## 💡 Ideias de melhoria

- [ ] Interface gráfica (GUI) simples — ligar/desligar sem terminal
- [ ] Detecção automática de vícios (sem precisar configurar manualmente)
- [ ] Perfis por professor/palestrante
- [ ] Suporte a macOS e Linux
- [ ] Suporte a GPU AMD (ROCm)
- [ ] Configuração via arquivo `.json` ou `.toml` (sem editar o `.py`)
- [ ] Estatísticas ao encerrar (quais vícios foram mais removidos)
- [ ] Integração com Zoom/Teams/Meet sem precisar do VB-Cable

---

## 🛠️ Como rodar localmente

```bash
git clone https://github.com/olympiorenno/audio-cleaner.git
cd audio-cleaner
```

Execute o setup (instala VB-Cable, dependências e modelo Whisper):
```
setup.bat
```

Ou instale só as dependências manualmente:
```bash
pip install -r requirements.txt
python audio_cleaner.py
```

> Você também precisará do [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) instalado.

---

## 📦 Como gerar o instalador `.exe`

O instalador é gerado com PyInstaller a partir do `installer.py`:

```bash
pip install pyinstaller
pyinstaller AudioCleaner-Setup.spec
```

O `.exe` gerado estará em `dist/AudioCleaner-Setup.exe`.

---

## 📤 Enviando contribuições

1. Faça um fork do repositório
2. Crie uma branch: `git checkout -b minha-melhoria`
3. Faça suas alterações e commit com mensagem clara:
   `git commit -m "feat: adiciona suporte a perfis por palestrante"`
4. Envie: `git push origin minha-melhoria`
5. Abra um **Pull Request** descrevendo o que mudou e por quê

---

## 🐛 Reportando bugs

Abra uma [Issue](https://github.com/olympiorenno/audio-cleaner/issues) com:
- O que aconteceu vs. o que era esperado
- Mensagem de erro completa (se houver)
- Sistema operacional, versão do Python e se tem GPU NVIDIA

---

## 🗂️ Estrutura do projeto

```
audio_cleaner.py         — lógica principal (captura, Whisper, mute, playback)
installer.py             — instalador empacotado como .exe via PyInstaller
AudioCleaner-Setup.spec  — spec do PyInstaller para rebuildar o .exe
requirements.txt         — dependências Python
run.bat                  — inicia o Audio Cleaner
setup.bat                — setup completo (Python + VB-Cable + dependências + Whisper)
```
