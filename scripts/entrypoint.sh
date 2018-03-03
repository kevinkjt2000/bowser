#!/bin/sh
set -e

env | sort

pip install -e .

exec "$@"
