#!/usr/bin/env bash
# Limpia todo lo generado por el eval de Ragas:
#   - ragas/out/       (el CSV con el detalle del último run)
#   - __pycache__/     (bytecode de Python dentro de ragas/)
#
# OJO: la caché de respuestas del agente vive en deepeval/out/responses/ y es
# compartida — se limpia con script/deepeval/clean_deepeval.sh (o con --fresh).
#
# Uso: script/ragas/clean_ragas.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/ragas"

echo "→ Limpiando artefactos generados por el eval de Ragas..."
rm -rfv "$EVAL_DIR/out" | sed 's/^/  /'
find "$EVAL_DIR" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
echo "✓ Limpio. El próximo run regenerará el informe."
