#!/usr/bin/env bash
# Limpia todo lo generado por el eval de DeepEval:
#   - deepeval/out/             (respuestas cacheadas del agente evaluado)
#   - deepeval/.deepeval/       (caché interna y resultados de DeepEval)
#   - __pycache__/              (bytecode de Python, en cualquier subcarpeta)
#   - .pytest_cache/            (caché de pytest, en la raíz)
#
# Uso: script/deepeval/clean_deepeval.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/deepeval"

echo "→ Limpiando artefactos generados por el eval..."
rm -rfv "$EVAL_DIR/out" "$EVAL_DIR/.deepeval" "$REPO_ROOT/.pytest_cache" | sed 's/^/  /'
find "$EVAL_DIR" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
echo "✓ Limpio. El próximo run regenerará las respuestas del agente."
