"""
Audio Cleaner - Remove vícios de linguagem em tempo real
=========================================================
Requisitos:
    pip install faster-whisper sounddevice numpy

Como usar:
    1. Instale o VB-Audio Virtual Cable
    2. No browser, defina a saída de áudio como "CABLE Input"
    3. Execute este script: python audio_cleaner.py
    4. O áudio limpo tocará nos seus speakers normais
"""

VERSION = "1.1.6"

import os
import warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

import sounddevice as sd
import numpy as np
import threading
import queue
import time
from concurrent.futures import ThreadPoolExecutor
from faster_whisper import WhisperModel

# ─── CONFIGURAÇÕES ────────────────────────────────────────────────────────────

TICS = [
    "né", "né?", "certo", "certo?", "então", "tipo", "assim",
    "tá", "tá?", "ok", "hmm", "ahm", "ahn", "eh", "é isso",
    "entendeu", "entendeu?", "compreenderam", "pessoal"
]

E_LONGO_MIN_SEGUNDOS = 0.05   # threshold baixo para pegar todos os "é"
E_MUTE_EXTRA        = 0.4    # estende o mute alem do timestamp (cobre o "éééé" completo)

SAMPLE_RATE     = 16000
CHUNK_SECONDS   = 3.0
DEBUG_WORDS     = False  # True = mostra todas as palavras (para diagnostico)
WHISPER_MODEL    = "tiny"
WHISPER_LANGUAGE = "pt"

# ─── SETUP ────────────────────────────────────────────────────────────────────

# Detecta automaticamente se CUDA está disponível e funcional
def detect_device():
    try:
        import ctranslate2
        # Tenta criar um modelo mínimo na GPU para confirmar que funciona
        types = ctranslate2.get_supported_compute_types("cuda")
        if "float16" in types or "int8_float16" in types:
            print("GPU NVIDIA detectada! Usando CUDA.")
            return "cuda", "float16"
    except Exception:
        pass
    print("CUDA não disponível. Usando CPU.")
    return "cpu", "int8"

WHISPER_DEVICE, COMPUTE_TYPE = detect_device()

print(f"Audio Cleaner v{VERSION}")
print("=" * 40)
print("Carregando modelo Whisper...")
model = WhisperModel(WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=COMPUTE_TYPE)
print(f"Modelo '{WHISPER_MODEL}' carregado em {WHISPER_DEVICE.upper()}!")
print("Aquecendo modelo (~12s, so na primeira vez do dia)...")

import numpy as _np
import threading as _threading

_warmup_done = False
def _spinner():
    chars = ["|", "/", "-", "\\"]
    i = 0
    while not _warmup_done:
        print(f"\r  {chars[i % len(chars)]} aguarde...", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r  Pronto!          ")

_t = _threading.Thread(target=_spinner, daemon=True)
_t.start()
list(model.transcribe(_np.random.randn(16000).astype(_np.float32) * 0.01, language=WHISPER_LANGUAGE, vad_filter=False)[0])
_warmup_done = True
_t.join()
print()


def select_devices():
    devices = sd.query_devices()
    input_dev, output_dev = None, None

    for i, dev in enumerate(devices):
        if input_dev is None and "CABLE Output (VB-Audio Virtual Cable)" in dev["name"] and dev["max_input_channels"] > 0:
            input_dev = i
        if output_dev is None and "Fones de ouvido" in dev["name"] and dev["max_output_channels"] > 0:
            output_dev = i

    if output_dev is None:
        for i, dev in enumerate(devices):
            if "Realtek" in dev["name"] and dev["max_output_channels"] > 0:
                output_dev = i
                break
    if output_dev is None:
        output_dev = sd.default.device[1]
    if input_dev is None:
        input_dev = sd.default.device[0]

    print(f"Entrada : {devices[input_dev]['name']}")
    print(f"Saída   : {devices[output_dev]['name']}\n")
    return input_dev, output_dev


def is_tic(word: str, duration: float = 0.0) -> bool:
    w = word.strip().lower().rstrip(".,!?;:-")
    if w in ("é", "e", "ee", "éé", "ée", "e...", "é...", "eee", "ééé", "eh"):
        return duration >= E_LONGO_MIN_SEGUNDOS
    return w in [t.lower() for t in TICS]


def mute_segment(audio: np.ndarray, start_s: float, end_s: float, fade_ms: int = 20) -> np.ndarray:
    s    = max(0, int(start_s * SAMPLE_RATE))
    e    = min(len(audio), int(end_s * SAMPLE_RATE))
    fade = int(fade_ms * SAMPLE_RATE / 1000)
    if s > fade:
        audio[s - fade:s] *= np.linspace(1, 0, fade)
    audio[s:e] = 0
    if e + fade < len(audio):
        audio[e:e + fade] *= np.linspace(0, 1, fade)
    return audio



def transcreve_e_muta(chunk, tics_counter):
    """Processa um chunk: transcreve e muta vícios. Roda em thread separada."""
    segments, _ = model.transcribe(
        chunk,
        language=WHISPER_LANGUAGE,
        word_timestamps=True,
        vad_filter=False,
    )
    for seg in segments:
        if seg.words:
            for word in seg.words:
                dur = word.end - word.start
                if DEBUG_WORDS:
                    print(f"  [w] '{word.word.strip()}' {dur:.2f}s")
                if is_tic(word.word, dur):
                    w = word.word.strip().lower().rstrip(".,!?;:-")
                    # Para "é" estende o mute para cobrir o som completo
                    extra = E_MUTE_EXTRA if w in ("é","e","ee","éé","ée","e...","é...","eee","ééé","eh") else 0
                    chunk = mute_segment(chunk, word.start, word.end + extra)
                    tics_counter[0] += 1
                    print(f"  [-] '{word.word.strip()}' {dur:.2f}s  <<< REMOVIDO")
    return chunk


class AudioCleaner:
    def __init__(self):
        self.raw_queue    = queue.Queue()
        self.future_queue = queue.Queue()   # fila de futures (processamento paralelo)
        self.running      = False
        self.tics_removed = 0

    def capture_callback(self, indata, frames, time_info, status):
        if status:
            print(f"  [captura] {status}")
        self.raw_queue.put(indata[:, 0].copy())

    def process_loop(self):
        """Acumula audio e submete chunks para processamento paralelo."""
        chunk_size = int(CHUNK_SECONDS * SAMPLE_RATE)
        buf = np.array([], dtype=np.float32)
        audio_recebido = False
        t_inicio = time.time()
        executor = ThreadPoolExecutor(max_workers=2)
        counter = [0]
        self._counter = counter  # referencia para status

        while self.running:
            while len(buf) < chunk_size and self.running:
                try:
                    chunk = self.raw_queue.get(timeout=0.1)
                    if not audio_recebido:
                        audio_recebido = True
                        print("Audio recebido! Processando...\n")
                    buf = np.concatenate([buf, chunk])
                except queue.Empty:
                    if not audio_recebido and (time.time() - t_inicio) > 10:
                        print("[AVISO] Nenhum audio recebido apos 10s.")
                        print("  Verifique se o browser esta usando 'CABLE Input' como saida.")
                        t_inicio = time.time()
                    continue

            if not self.running:
                break

            chunk = buf[:chunk_size].copy()
            buf   = buf[chunk_size:]

            # Submete para processamento em paralelo (nao bloqueia)
            future = executor.submit(transcreve_e_muta, chunk, counter)
            self.future_queue.put(future)

        self.tics_removed = counter[0]
        executor.shutdown(wait=False)

    def playback_loop(self, output_device):
        silence = np.zeros(int(0.05 * SAMPLE_RATE), dtype=np.float32)
        stream  = sd.OutputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=output_device,
            latency="low",
        )
        stream.start()

        # Pre-carrega 2 futures antes de comecar a tocar
        print("Aguardando buffer inicial...", flush=True)
        futures = []
        while len(futures) < 2:
            try:
                futures.append(self.future_queue.get(timeout=1.0))
            except queue.Empty:
                continue
        print("Buffer pronto! Tocando...\n", flush=True)
        for f in futures:
            stream.write(f.result())

        while self.running:
            try:
                future = self.future_queue.get(timeout=0.05)
                stream.write(future.result())
            except queue.Empty:
                stream.write(silence)

        stream.stop()
        stream.close()

    def run(self):
        input_dev, output_dev = select_devices()
        print(f"Vícios : {', '.join(TICS)}")
        print(f"'é' longo: > {E_LONGO_MIN_SEGUNDOS}s")
        print(f"Atraso : ~{CHUNK_SECONDS:.0f}s\n")
        print("Iniciando... Pressione Ctrl+C para parar.\n")

        self.running = True

        threading.Thread(target=self.process_loop,  daemon=True).start()
        threading.Thread(target=self.playback_loop, args=(output_dev,), daemon=True).start()

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=input_dev,
            blocksize=int(SAMPLE_RATE * 0.05),
            callback=self.capture_callback,
        ):
            try:
                while True:
                    time.sleep(5)
                    n = self._counter[0] if hasattr(self, '_counter') else self.tics_removed
                    print(f"[Status] Vícios removidos: {n}")
            except KeyboardInterrupt:
                print(f"\nEncerrando... Total: {self.tics_removed} vícios removidos.")
                self.running = False


if __name__ == "__main__":
    AudioCleaner().run()

