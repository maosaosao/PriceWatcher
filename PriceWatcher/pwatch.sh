#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

while true
do
  python PriceWatcher/main.py
  sleep 10
done
