# Genérico para todas las suites: genera las respuestas del agente (una por caso)
# y las cachea en out/responses/<suite>.json. Separar generación de evaluación
# permite re-ejecutar las métricas (el juez) sin volver a llamar al modelo evaluado.
# Si cambias el prompt o las plantillas del agente, borra la caché o usa --fresh.

import importlib
import json
import sys
from pathlib import Path

RESPONSES_DIR = Path(__file__).resolve().parents[1] / "out" / "responses"


def load_or_generate(suite: str) -> dict[str, str]:
    # Con caché: se devuelve tal cual, sin llamar al modelo
    responses_file = RESPONSES_DIR / f"{suite}.json"
    if responses_file.exists():
        return json.loads(responses_file.read_text(encoding="utf-8"))

    # Sin caché: se importa la suite por su nombre y se genera caso a caso
    cases_mod = importlib.import_module(f"suites.{suite}.cases")
    agent_mod = importlib.import_module(f"suites.{suite}.agent")

    responses: dict[str, str] = {}
    for case in cases_mod.CASES:
        print(f"[{suite}] Generando respuesta para: {case['id']} ...")
        loaded_skill = case["skill_file"].read_text(encoding="utf-8")
        responses[case["id"]] = agent_mod.generate_answer(case["message"], loaded_skill)

    responses_file.parent.mkdir(parents=True, exist_ok=True)
    responses_file.write_text(
        json.dumps(responses, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Respuestas guardadas en {responses_file}")
    return responses


# Uso directo: python -m core.generate_responses <suite>  (desde la carpeta deepeval/)
if __name__ == "__main__":
    load_or_generate(sys.argv[1] if len(sys.argv) > 1 else "mail_agent")
