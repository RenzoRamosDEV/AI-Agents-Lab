# Eval del mail_agent con Langfuse (offline: dataset + experimento).
# Los casos viven en cases.py (basados en promptfoo/promptfooconfig.yaml).
# 1) Sincroniza el dataset "mail-agent-cases": sube/actualiza los casos
#    (ids estables → no duplica) y borra los items que ya no existan.
# 2) Ejecuta un experimento (dataset run): la task llama al agente REAL ya
#    instrumentado, así cada caso queda trazado con prompt, tokens y coste.
# 3) Scores por caso:
#      sin-n-literal   — determinista: prohibida la secuencia literal \n
#      contains        — determinista: contains_any/contains_all del caso
#      reglas-globales — juez LLM con las reglas transversales del prompt
#      rubrica-ok      — juez LLM con la rúbrica del caso; en los CANARIOS
#                        (expect_fail) se invierte: que el juez suspenda es
#                        el comportamiento correcto
#    Score del run: media de rubrica-ok.
# Resultados: en la UI de Langfuse (Datasets → mail-agent-cases → Runs).

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "deepeval"))

# Importar el agente PRIMERO: carga el .env y mapea las credenciales LANGFUSE_*
# antes de que se inicialice el cliente de Langfuse
from suites.mail_agent import agent  # noqa: E402

from cases import CASES, GLOBAL_RUBRIC, SKILLS_DIR  # noqa: E402
from langfuse import Evaluation, get_client  # noqa: E402
from langfuse.openai import OpenAI  # noqa: E402

DATASET_NAME = "mail-agent-cases"
EXPERIMENT_NAME = "mail-agent"
JUDGE_MODEL = "gpt-4.1-mini"

# Los evaluadores localizan su caso por el email entrante (clave única),
# sin depender de cómo llegue la metadata del item
CASES_BY_MESSAGE = {case["input"]["message"]: case for case in CASES}

# El juez responde JSON estricto; reason va ANTES que passed para que
# razone antes de decidir el veredicto
JUDGE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "verdict",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"},
                "passed": {"type": "boolean"},
            },
            "required": ["reason", "passed"],
            "additionalProperties": False,
        },
    },
}


# Sincroniza el dataset con cases.py: upsert por id estable + borrado de huérfanos
def sync_dataset(langfuse) -> None:
    langfuse.create_dataset(
        name=DATASET_NAME,
        description="Casos de la suite mail_agent (fuente: langfuse/cases.py, basados en promptfoo)",
    )

    wanted_ids = set()
    for case in CASES:
        item_id = f"mail-agent-{case['id']}"
        wanted_ids.add(item_id)
        langfuse.create_dataset_item(
            id=item_id,
            dataset_name=DATASET_NAME,
            input=case["input"],
            expected_output=case["expected_output"],
            metadata={"case_id": case["id"], **case["metadata"]},
        )

    existing = langfuse.api.dataset_items.list(dataset_name=DATASET_NAME, limit=100).data
    for item in existing:
        if item.id not in wanted_ids:
            print(f"Borrando item obsoleto del dataset: {item.id}")
            langfuse.api.dataset_items.delete(item.id)


# La task del experimento: el agente real, con su instrumentación de Langfuse
def run_agent_task(*, item, **kwargs):
    case = CASES_BY_MESSAGE[item.input["message"]]
    loaded_skill = (SKILLS_DIR / item.input["skill_file"]).read_text(encoding="utf-8")
    return agent.generate_answer(item.input["message"], loaded_skill, case_id=case["id"])


# Juez LLM: mismo modelo juez que en las otras suites (gpt-4.1-mini).
# Usa el cliente envuelto por Langfuse → las llamadas del juez también quedan
# trazadas (útil: este juez es flaky y así se puede auditar su razonamiento)
def judge(name: str, criteria: str, message: str, answer: str) -> dict:
    client = OpenAI(api_key=os.environ["API_KEY_OPENAI"])
    completion = client.chat.completions.create(
        name=name,
        model=JUDGE_MODEL,
        temperature=0,
        response_format=JUDGE_FORMAT,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un evaluador de borradores de email de atención al cliente. "
                    "Evalúa la RESPUESTA según los CRITERIOS y devuelve JSON {reason, passed}.\n"
                    "Reglas de interpretación (para evitar falsos suspensos):\n"
                    "- 'Primera persona del plural' se refiere a cómo el equipo habla de SÍ MISMO "
                    "('hemos recibido', 'lo estamos gestionando', 'we are reviewing' = CORRECTO). "
                    "Dirigirse al cliente de tú o usted ('tu consulta', 'te confirmaremos') NO la incumple.\n"
                    "- Para juzgar el idioma, identifica primero el idioma del EMAIL ENTRANTE citando una frase suya.\n"
                    "- Suspende solo con evidencia clara: cita en reason la frase exacta que incumple el criterio."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"EMAIL ENTRANTE:\n{message}\n\n"
                    f"RESPUESTA DEL AGENTE:\n{answer}\n\n"
                    f"CRITERIOS:\n{criteria}"
                ),
            },
        ],
    )
    return json.loads(completion.choices[0].message.content)


# Check determinista global (de promptfoo): la secuencia literal \n
# (barra invertida + n, dos caracteres) está prohibida en el texto
def eval_sin_n_literal(*, output, **kwargs):
    ok = "\\n" not in output
    return Evaluation(
        name="sin-n-literal",
        value=1.0 if ok else 0.0,
        comment="Sin \\n literal" if ok else "La respuesta contiene la secuencia literal \\n",
    )


# Check determinista por caso: contains_any (sin distinguir mayúsculas)
# y contains_all (literal)
def eval_contains(*, input, output, **kwargs):
    meta = CASES_BY_MESSAGE[input["message"]]["metadata"]
    any_terms = meta.get("contains_any") or []
    all_terms = meta.get("contains_all") or []
    # Sin checks definidos (canarios): no se emite score
    if not any_terms and not all_terms:
        return None

    ok_any = any(t.lower() in output.lower() for t in any_terms) if any_terms else True
    missing = [t for t in all_terms if t not in output]
    ok = ok_any and not missing

    detail = []
    if any_terms:
        detail.append(f"contains_any {'OK' if ok_any else 'KO'}: {any_terms}")
    if all_terms:
        detail.append(f"contains_all {'OK' if not missing else f'faltan {missing}'}")
    return Evaluation(name="contains", value=1.0 if ok else 0.0, comment="; ".join(detail))


# Juez con las reglas transversales del prompt (aplican a todos los casos)
def eval_reglas_globales(*, input, output, **kwargs):
    verdict = judge("judge-reglas-globales", GLOBAL_RUBRIC, input["message"], output)
    return Evaluation(
        name="reglas-globales",
        value=1.0 if verdict["passed"] else 0.0,
        comment=verdict["reason"],
    )


# Juez con la rúbrica del caso; en canarios se invierte el veredicto
def eval_rubrica(*, input, output, **kwargs):
    case = CASES_BY_MESSAGE[input["message"]]
    verdict = judge("judge-rubrica", case["metadata"]["rubric"], input["message"], output)
    expect_fail = case["metadata"]["expect_fail"]
    ok = verdict["passed"] != expect_fail

    comment = f"Juez: {'aprueba' if verdict['passed'] else 'suspende'} — {verdict['reason']}"
    if expect_fail:
        comment = "CANARIO (suspender es lo correcto). " + comment
    return Evaluation(name="rubrica-ok", value=1.0 if ok else 0.0, comment=comment)


# Score agregado del run: media de rubrica-ok
def media_rubrica(*, item_results, **kwargs):
    values = [
        ev.value
        for result in item_results
        for ev in result.evaluations
        if ev.name == "rubrica-ok" and ev.value is not None
    ]
    if not values:
        return Evaluation(name="media-rubrica-ok", value=None)
    avg = sum(values) / len(values)
    return Evaluation(
        name="media-rubrica-ok",
        value=avg,
        comment=f"{sum(values):.0f}/{len(values)} casos con el comportamiento esperado",
    )


if __name__ == "__main__":
    langfuse = get_client()
    sync_dataset(langfuse)
    dataset = langfuse.get_dataset(DATASET_NAME)

    result = dataset.run_experiment(
        name=EXPERIMENT_NAME,
        description="Suite mail_agent: checks deterministas + juez de reglas globales + rúbrica (canario invertido)",
        task=run_agent_task,
        evaluators=[eval_sin_n_literal, eval_contains, eval_reglas_globales, eval_rubrica],
        run_evaluators=[media_rubrica],
        max_concurrency=4,
    )
    print(result.format())

    langfuse.flush()
