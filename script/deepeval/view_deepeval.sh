#!/usr/bin/env bash
# Sirve el frontend de resultados del eval de DeepEval en local.
# (Hace falta un servidor: un HTML abierto a pelo no puede leer los JSON del historial.)
#
# Uso: script/deepeval/view_deepeval.sh [puerto]   (por defecto 8377)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT="${1:-8377}"

cd "$REPO_ROOT/deepeval"
echo "→ Frontend del eval en: http://localhost:$PORT/frontend/"
echo "  (Ctrl+C para parar)"
exec "$REPO_ROOT/.venv/bin/python" -m http.server "$PORT" --bind 127.0.0.1
