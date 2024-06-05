#!/bin/bash

# Xvfb'yi başlat
Xvfb :99 -screen 0 1024x768x24 &

# DISPLAY ortam değişkenini ayarla
export DISPLAY=:99

python -m unittest discover -s tests

# Uygulamayı çalıştır
exec "$@"