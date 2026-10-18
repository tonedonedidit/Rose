#!/usr/bin/env python3
"""One-time setup for render.py: installs the free voice engine and downloads assets (~355 MB).

Kokoro-82M voice model: Apache-2.0 (commercial use OK).
US state shapes: Natural Earth, public domain.
"""
import os
import subprocess
import sys
import urllib.request

DEST = os.environ.get("STUDIO_ASSETS", os.path.expanduser("~/.cache/studio-tts"))
FILES = {
    "kokoro-v1.0.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
    "states.geojson": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_1_states_provinces.geojson",
}

subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kokoro-onnx", "soundfile", "numpy", "pillow"], check=True)
os.makedirs(DEST, exist_ok=True)
for name, url in FILES.items():
    path = os.path.join(DEST, name)
    if not os.path.exists(path):
        print(f"downloading {name}")
        urllib.request.urlretrieve(url, path)
print(f"assets ready in {DEST}; ffmpeg required on PATH")
