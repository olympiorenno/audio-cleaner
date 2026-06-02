"""
Audio Cleaner - Servidor WebSocket
===================================
Recebe chunks de audio da extensao Chrome,
processa com Whisper e retorna posicoes dos vicios.

Instalar dependencia extra:
    pip install websockets
"""

import asyncio
import json
import base64
import numpy as np
import warnings
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

import websockets
from faster_whisper import WhisperModel

# ── Configuracoes ──────────────────────────────────────────────────────────────

TICS = [
    "né", "né?", "ne", "ne?",
    "então", "então,",
    "pessoal", "pessoal,",
    "ok", "ok?",
]
E_LONGO_MIN = 0.40
E_MUTE_EXTRA_BEFORE = 0.1
E_MUTE_EXTRA_AFTER  = 0.3
SAMPLE_RATE = 16000
HOST = "localhost"
PORT = 8765

# ── Setup Whisper ──────────────────────────────────────────────────────────────

def detect_device():
    try:
        import ctranslate2
        types = ctranslate2.get_supported_compute_types("cuda")
        if "float16" in types or "int8_float16" in types:
            print("GPU NVIDIA detectada! Usando CUDA.")
            return "cuda", "float16"
    except Exception:
        pass
    print("CUDA nao disponivel. Usando CPU.")
    return "cpu", "int8"

device, compute = detect_device()

print("Carregando modelo Whisper...")
model = WhisperModel("tiny", device=device, compute_type=compute)
print("Modelo carregado! Aquecendo...")
_warmup = np.random.randn(16000).astype(np.float32) * 0.01
list(model.transcribe(_warmup, language="pt", vad_filter=False)[0])
print(f"Servidor pronto em ws://{HOST}:{PORT}\n")

# ── Deteccao de vicios ─────────────────────────────────────────────────────────

def is_tic(word, duration=0.0):
    w = word.strip().lower().rstrip(".,!?;:-")
    if w in ("é", "e", "ee", "éé", "ée", "e...", "é..."):
        return duration >= E_LONGO_MIN
    return w in [t.lower() for t in TICS]

def processar(audio_float32):
    segments, _ = model.transcribe(
        audio_float32,
        language="pt",
        word_timestamps=True,
        vad_filter=False,
    )
    vicios = []
    for seg in segments:
        if seg.words:
            for word in seg.words:
                dur = word.end - word.start
                if is_tic(word.word, dur):
                    w = word.word.strip().lower().rstrip(".,!?;:-")
                    if w in ("é", "e", "ee", "éé", "ée", "e...", "é..."):
                        start = max(0, word.start - E_MUTE_EXTRA_BEFORE)
                        end   = word.end + E_MUTE_EXTRA_AFTER
                    else:
                        start = word.start
                        end   = word.end
                    vicios.append({
                        "word":  word.word.strip(),
                        "start": round(start, 3),
                        "end":   round(end,   3),
                    })
                    print(f"  [-] '{word.word.strip()}' {dur:.2f}s [{start:.1f}->{end:.1f}]")
    return vicios

# ── WebSocket handler ──────────────────────────────────────────────────────────

total_vicios = 0

async def handler(websocket):
    global total_vicios
    client = websocket.remote_address
    print(f"[+] Extensao conectada: {client}")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                if data.get("type") == "audio":
                    # Recebe audio como array de floats base64
                    raw = base64.b64decode(data["audio"])
                    audio = np.frombuffer(raw, dtype=np.float32)

                    if len(audio) < SAMPLE_RATE * 0.5:
                        continue  # chunk muito pequeno

                    vicios = processar(audio)
                    total_vicios += len(vicios)

                    await websocket.send(json.dumps({
                        "type":   "result",
                        "vicios": vicios,
                        "total":  total_vicios,
                    }))

                elif data.get("type") == "ping":
                    await websocket.send(json.dumps({"type": "pong"}))

            except Exception as e:
                print(f"  [Erro] {e}")

    except websockets.exceptions.ConnectionClosed:
        print(f"[-] Extensao desconectada: {client}")

async def main():
    async with websockets.serve(handler, HOST, PORT):
        print(f"Aguardando conexao da extensao Chrome...")
        print(f"Total de vicios: 0")
        await asyncio.Future()  # roda para sempre

if __name__ == "__main__":
    asyncio.run(main())
