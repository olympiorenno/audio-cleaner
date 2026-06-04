#!/bin/bash
export HF_HOME="/Library/Application Support/AudioCleaner/models"

# Mata instancia anterior especifica do audio_cleaner
pkill -f "audio_cleaner.py" 2>/dev/null
sleep 1

# Inicia o Audio Cleaner
python3 "$(dirname "$0")/audio_cleaner.py"
