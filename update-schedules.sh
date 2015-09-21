#!/usr/bin/env bash

python3 ./route_bus.py
python3 -c "from route_train import cache_everything;cache_everything()"