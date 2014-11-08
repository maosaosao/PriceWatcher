#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

while true
do
  python PriceWatcher/main.py
  sleep 60*3
done
