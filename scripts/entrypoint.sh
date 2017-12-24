#!/bin/sh
set -e

pip install -e .

exec "$@"
