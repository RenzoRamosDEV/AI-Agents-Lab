#!/usr/bin/env bash
# Ejecuta el eval de Ragas (carpeta ragas/) sobre el mail_agent.
#
# Uso:
#   script/ragas/run_ragas.sh            # usa la caché de respuestas compartida con DeepEval
#   script/ragas/run_ragas.sh --fresh    # borra esa caché y regenera las respuestas del agente
#
# Sale con código 1 si falla algo o si el CANARIO se dispara (el agente inventa datos).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/ragas"
VENV_BIN="$REPO_ROOT/.venv/bin"

SUITE="mail_agent"

for arg in "$@"; do
    case "$arg" in
        --fresh)
            # La caché es la MISMA que usa DeepEval: borrar aquí afecta a ambas suites
            echo "→ Borrando caché de respuestas (deepeval/out/responses/$SUITE.json)..."
            rm -f "$REPO_ROOT/deepeval/out/responses/$SUITE.json"
            ;;
        *)
            echo "✗ Argumento no reconocido: $arg (solo se admite --fresh)" >&2
            exit 1
            ;;
    esac
done

# Se ejecuta desde dentro de ragas/ para que resuelvan los imports locales
# (references) y los relativos a deepeval/ que hace el propio script
cd "$EVAL_DIR"

export RAGAS_DO_NOT_TRACK=true

exec "$VENV_BIN/python" eval_mail_agent.py
