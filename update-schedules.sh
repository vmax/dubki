#!/usr/bin/env bash

#PYTHONANYWHERE

mkdir -p cache
echo "[0]: caching bus schedule"
python3 ./route_bus.py
echo "[1]: caching train schedule"
python3 -c "from route_train import cache_everything;cache_everything()"