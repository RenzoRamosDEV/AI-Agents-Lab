#!/usr/bin/env bash
# Ejecuta el eval de una suite con DeepEval (carpeta deepeval/).
#
# Uso:
#   script/deepeval/run_deepeval.sh                      # suite por defecto: mail_agent
#   script/deepeval/run_deepeval.sh <suite>              # p. ej. auto_agent (necesita suites/<suite>/ y tests/test_<suite>.py)
#   script/deepeval/run_deepeval.sh [<suite>] --fresh    # borra la caché y regenera las respuestas del agente
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/deepeval"
VENV_BIN="$REPO_ROOT/.venv/bin"

SUITE="mail_agent"
FRESH=0
for arg in "$@"; do
    case "$arg" in
        --fresh) FRESH=1 ;;
        *) SUITE="$arg" ;;
    esac
done

if [[ ! -f "$EVAL_DIR/tests/test_${SUITE}.py" ]]; then
    echo "✗ No existe la suite '$SUITE' (falta deepeval/tests/test_${SUITE}.py)" >&2
    echo "  Suites disponibles:" >&2
    ls "$EVAL_DIR/tests"/test_*.py 2>/dev/null | sed -E 's/.*test_(.+)\.py/    - \1/' >&2
    exit 1
fi

if [[ "$FRESH" == 1 ]]; then
    echo "→ Borrando caché de respuestas (out/responses/$SUITE.json)..."
    rm -f "$EVAL_DIR/out/responses/$SUITE.json"
fi

# IMPORTANTE: hay que ejecutar desde dentro de deepeval/ — la carpeta se llama
# igual que el paquete Python y desde la raíz haría sombra al import.
cd "$EVAL_DIR"

export DEEPEVAL_TELEMETRY_OPT_OUT=1

status=0
"$VENV_BIN/deepeval" test run "tests/test_${SUITE}.py" || status=$?

# Archiva el resultado en out/history/<suite>/ (para el frontend) y reconstruye el índice
LATEST="$EVAL_DIR/.deepeval/.latest_test_run.json"
if [[ -f "$LATEST" ]]; then
    mkdir -p "$EVAL_DIR/out/history/$SUITE"
    cp "$LATEST" "$EVAL_DIR/out/history/$SUITE/run-$(date +%Y%m%d-%H%M%S).json"
    "$VENV_BIN/python" -c "
import glob, json, os
d = '$EVAL_DIR/out/history'
idx = {}
for p in sorted(glob.glob(d + '/*/run-*.json')):
    idx.setdefault(os.path.basename(os.path.dirname(p)), []).append(os.path.basename(p))
with open(d + '/index.json', 'w') as f:
    json.dump(idx, f)
total = sum(len(v) for v in idx.values())
print(f'→ Run archivado en out/history/$SUITE/ ({total} runs en el historial, {len(idx)} suites)')
"
fi

exit $status
