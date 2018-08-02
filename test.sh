#!/usr/bin/env bash

python -m pytest --cov=scorevideo_lib tests/src/
find scorevideo_lib -name *.py | xargs pylint
find tests/src -name *.py | xargs pylint