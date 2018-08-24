#!/usr/bin/env bash

python -m pytest

find scorevideo_lib -name *.py | xargs pylint
find tests/src -name *.py | xargs pylint

python -m mypy scorevideo_lib
