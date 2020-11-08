#!/bin/bash


git submodule update --init || exit 1

source "private/source.sh" || exit 1

python3 src/bot.py

