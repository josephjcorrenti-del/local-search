#!/usr/bin/env bash

set -euo pipefail

echo "=== pytest ==="
python -m pytest -q

echo
echo "=== status ==="
local-search status

echo
echo "=== doctor ==="
local-search doctor
