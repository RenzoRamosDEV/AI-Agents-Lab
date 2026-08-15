#!/usr/bin/env bash
# Ejecuta el eval del mail_agent con promptfoo (carpeta promptfoo/).
#
# Uso:
#   script/promptfoo/run_promptfoo.sh            # corre el eval (usa la caché de promptfoo si existe)
#   script/promptfoo/run_promptfoo.sh --fresh    # ignora la caché y vuelve a llamar al modelo
#
# Resultado esperado: 4 tests en verde + 1 en rojo (el CANARIO debe fallar).
# El script sale con 0 solo si se da exactamente ese resultado.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/promptfoo"

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

ARGS=()
if [[ "${1:-}" == "--fresh" ]]; then
    echo "→ Ignorando la caché de promptfoo (--no-cache)..."
    ARGS+=(--no-cache)
fi

cd "$EVAL_DIR"
export PROMPTFOO_DISABLE_TELEMETRY=1

OUT_FILE="$EVAL_DIR/out/latest.json"
mkdir -p "$EVAL_DIR/out"

# promptfoo sale con código != 0 si CUALQUIER test falla, y aquí el CANARIO
# debe fallar siempre — así que el veredicto real se calcula después del JSON.
status=0
npx promptfoo eval --env-file "$REPO_ROOT/.env" --output "$OUT_FILE" ${ARGS[@]+"${ARGS[@]}"} || status=$?

node - "$OUT_FILE" <<'JS'
const fs = require('fs');
const data = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const results = (data.results && data.results.results) || [];
const desc = r => (r.testCase && r.testCase.description) || r.description || '';
const isCanary = r => desc(r).includes('CANARIO');

const badFails = results.filter(r => !r.success && !isCanary(r));
const canaryGreen = results.filter(r => r.success && isCanary(r));
const passed = results.filter(r => r.success).length;

console.log(`→ ${passed}/${results.length} tests en verde`);
if (badFails.length) {
    console.log('✗ Tests que NO deberían fallar y fallaron:');
    for (const r of badFails) console.log(`    - ${desc(r)}`);
    process.exit(1);
}
if (canaryGreen.length) {
    console.log('✗ El CANARIO salió en VERDE: el modelo está inventando datos. Problema real, no lo "arregles".');
    process.exit(1);
}
console.log('✓ Resultado esperado: 4 en verde + CANARIO en rojo.');
JS
