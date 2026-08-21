#!/usr/bin/env bash
# Ejecuta el eval del mail_agent con Langfuse (carpeta langfuse/).
#
# Qué hace: sincroniza el dataset "mail-agent-cases" y lanza un experimento
# (dataset run) llamando al agente REAL, con scores deterministas + jueces LLM.
# No hay caché: cada run llama al modelo evaluado y al juez de nuevo.
#
# Uso: script/langfuse/run_langfuse.sh
#
# Resultados: en la UI de Langfuse (Datasets → mail-agent-cases → Runs,
# o la pestaña Experiments). El propio run imprime el resumen al terminar.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVAL_DIR="$REPO_ROOT/langfuse"
VENV_BIN="$REPO_ROOT/.venv/bin"

if [[ ! -x "$VENV_BIN/python" ]]; then
    echo "✗ No existe el venv del repo ($VENV_BIN/python). Créalo con: uv sync" >&2
    exit 1
fi

if [[ ! -f "$REPO_ROOT/.env" ]]; then
    echo "✗ Falta el .env en la raíz del repo (API_KEY_OPENAI y credenciales LANGFUSE_*)." >&2
    exit 1
fi

# IMPORTANTE: se ejecuta desde dentro de langfuse/ — la carpeta se llama igual
# que el paquete Python y desde la raíz haría sombra al import del SDK.
cd "$EVAL_DIR"

echo "→ Lanzando experimento en Langfuse (dataset mail-agent-cases)..."
"$VENV_BIN/python" eval_mail_agent.py

echo "✓ Experimento terminado. Revisa los scores en la UI:"
echo "  https://cloud.langfuse.com → tu proyecto → Experiments (o Datasets → mail-agent-cases → Runs)"
