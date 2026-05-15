#!/usr/bin/env bash

set -euo pipefail

echo "=== status ==="
local-search status

echo
echo "=== doctor ==="
local-search doctor

echo
echo "=== pytest ==="
python -m pytest -q
