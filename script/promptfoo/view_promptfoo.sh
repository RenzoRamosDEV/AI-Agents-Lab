#!/usr/bin/env bash
# Levanta la UI de resultados de promptfoo en local.
# Muestra cada eval lanzado y queda monitorizando: los evals nuevos aparecen solos.
#
# Uso: script/promptfoo/view_promptfoo.sh [puerto]   (por defecto 15500)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/promptfoo"
PORT="${1:-15500}"

# promptfoo exige Node >= 22; si el node activo es más viejo, usa el de nvm.
NODE_MAJOR="$(node --version 2>/dev/null | sed 's/^v//' | cut -d. -f1 || echo 0)"
if (( NODE_MAJOR < 22 )); then
    NVM_NODE="$(ls -d "${NVM_DIR:-$HOME/.nvm}"/versions/node/v* 2>/dev/null | sort -V | tail -1 || true)"
    if [[ -z "$NVM_NODE" || "$(basename "$NVM_NODE" | sed 's/^v//' | cut -d. -f1)" -lt 22 ]]; then
        echo "✗ promptfoo necesita Node >= 22 y no se encontró (ni activo ni en nvm)." >&2
        echo "  Instálalo con: nvm install 22" >&2
        exit 1
    fi
    export PATH="$NVM_NODE/bin:$PATH"
fi

cd "$EVAL_DIR"
export PROMPTFOO_DISABLE_TELEMETRY=1

echo "→ UI de promptfoo en: http://localhost:$PORT"
echo "  (Ctrl+C para parar)"
exec npx promptfoo view --port "$PORT" --yes
