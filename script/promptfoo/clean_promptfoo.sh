#!/usr/bin/env bash
# Limpia todo lo generado por el eval de promptfoo:
#   - promptfoo/out/              (export JSON del último run)
#   - ~/.promptfoo/promptfoo.db   (historial de evals que muestra la UI)
#   - ~/.promptfoo/cache/         (caché de llamadas al modelo)
#   - ~/.promptfoo/logs/ y evalLastWritten
#
# Conserva ~/.promptfoo/promptfoo.yaml (config global de promptfoo).
# Si la UI (view_promptfoo.sh) está abierta, reiníciala después de limpiar.
#
# Uso: script/promptfoo/clean_promptfoo.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/promptfoo"
PF_HOME="$HOME/.promptfoo"

echo "→ Limpiando artefactos generados por el eval..."
rm -rfv "$EVAL_DIR/out" \
        "$PF_HOME/promptfoo.db" \
        "$PF_HOME/cache" \
        "$PF_HOME/logs" \
        "$PF_HOME/evalLastWritten" | sed 's/^/  /'
echo "✓ Limpio. El próximo run llamará al modelo de nuevo (sin caché ni historial)."
