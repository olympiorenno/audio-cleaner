"""
Audio Cleaner - Diagnostico
Rode nas duas maquinas e compare os resultados
"""

import os
import sys
import time
import platform
import subprocess
import numpy as np

print("=" * 55)
print("       Audio Cleaner - Diagnostico")
print("=" * 55)

# ── 1. Sistema ────────────────────────────────────────────────
print("\n[1] SISTEMA")
print(f"  OS       : {platform.system()} {platform.release()} ({platform.version()})")
print(f"  Python   : {sys.version.split()[0]}")
print(f"  CPU      : {platform.processor()}")

try:
    import psutil
    ram = psutil.virtual_memory()
    cpu_count = psutil.cpu_count()
    print(f"  Nucleos  : {cpu_count}")
    print(f"  RAM      : {ram.total // (1024**3)} GB ({ram.percent}% em uso)")
except ImportError:
    print("  (instale psutil para mais detalhes de CPU/RAM)")

# ── 2. GPU ────────────────────────────────────────────────────
print("\n[2] GPU")
try:
    result = subprocess.run(
        ["powershell", "-Command",
         "Get-WmiObject Win32_VideoController | Select-Object Name, AdapterRAM | ForEach-Object { $_.Name + ' | ' + [math]::Round($_.AdapterRAM/1MB) + ' MB' }"],
        capture_output=True, text=True
    )
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            print(f"  {line.strip()}")
except:
    print("  Nao foi possivel detectar GPU")

try:
    import ctranslate2
    cuda_types = ctranslate2.get_supported_compute_types("cuda")
    if "float16" in cuda_types:
        print("  CUDA     : Disponivel (NVIDIA)")
    else:
        print("  CUDA     : Nao disponivel")
except:
    print("  CUDA     : Nao disponivel")

# ── 3. Audio ──────────────────────────────────────────────────
print("\n[3] DISPOSITIVOS DE AUDIO")
try:
    import sounddevice as sd
    devices = sd.query_devices()
    vbcable = False
    for i, dev in enumerate(devices):
        if "CABLE" in dev["name"]:
            print(f"  [OK] VB-Cable : {dev['name']}")
            vbcable = True
    if not vbcable:
        print("  [!!] VB-Audio Virtual Cable NAO encontrado!")

    default_in  = devices[sd.default.device[0]]["name"]
    default_out = devices[sd.default.device[1]]["name"]
    print(f"  Entrada padrao : {default_in}")
    print(f"  Saida padrao   : {default_out}")
    print(f"  Latencia entrada : {sd.query_devices(sd.default.device[0])['default_low_input_latency']*1000:.1f} ms")
    print(f"  Latencia saida   : {sd.query_devices(sd.default.device[1])['default_low_output_latency']*1000:.1f} ms")
except Exception as e:
    print(f"  Erro: {e}")

# ── 4. Velocidade do Whisper ──────────────────────────────────
print("\n[4] VELOCIDADE DO WHISPER (processa 2s de audio)")
try:
    from faster_whisper import WhisperModel

    print("  Carregando modelo tiny...", end="", flush=True)
    t0 = time.time()
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    load_time = time.time() - t0
    print(f" {load_time:.1f}s")

    # Gera 2s de audio simulado (ruido branco baixo)
    audio = np.random.randn(32000).astype(np.float32) * 0.01

    print("  Transcrevendo 2s de audio...", end="", flush=True)
    t0 = time.time()
    segments, _ = model.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False)
    list(segments)  # força execução
    proc_time = time.time() - t0
    print(f" {proc_time:.2f}s")

    ratio = proc_time / 2.0
    print(f"\n  Resultado: processa 2s em {proc_time:.2f}s (ratio: {ratio:.2f}x)")
    if ratio < 0.5:
        print("  [OTIMO] Rapido o suficiente para tempo real sem atraso")
    elif ratio < 1.0:
        print("  [BOM] Funciona em tempo real com ~2s de atraso")
    else:
        print("  [LENTO] Processamento mais lento que o audio — causa dessincronizacao!")
        print(f"  Sugestao: aumente CHUNK_SECONDS para {proc_time*1.5:.1f} no audio_cleaner.py")

except Exception as e:
    print(f"  Erro: {e}")

# ── 5. Recomendacao ───────────────────────────────────────────
print("\n[5] RECOMENDACAO DE CHUNK_SECONDS")
try:
    chunk_recomendado = max(2.0, round(proc_time * 2, 1))
    print(f"  Use CHUNK_SECONDS = {chunk_recomendado} nesta maquina")
except:
    pass

print()
print("=" * 55)
print("  Cole os resultados acima para comparar as maquinas")
print("=" * 55)
input("\nPressione Enter para fechar...")
