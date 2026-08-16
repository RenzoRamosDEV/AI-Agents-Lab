# El test de la suite mail_agent (deepeval test run es pytest por debajo).
#
# Flujo: carga las respuestas del agente → crea un test por caso → cada test
# aplica 4 capas de validación, de la más barata a la más cara:
#   Capa 1. Checks de texto — sin LLM, gratis y exactos
#   Capa 2. Faithfulness — detector de alucinaciones (datos inventados)
#   Capa 3. GEval reglas-globales — el juez valida las reglas del prompt
#   Capa 4. GEval rubric-<caso> — el juez valida los criterios del escenario

import deepeval
import pytest
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from core.generate_responses import load_or_generate
from suites.mail_agent.agent import (
    EVALUATED_MODEL,
    MAX_COMPLETION_TOKENS,
    PROMPT_FILE,
    TEMPERATURE,
)
from suites.mail_agent.cases import CASES, GLOBAL_RUBRIC_STEPS

SUITE = "mail_agent"

# Modelo JUEZ: pequeño y distinto del evaluado a propósito — calificar es más
# fácil que redactar, es barato, y un modelo no debe calificarse a sí mismo
JUDGE_MODEL = "gpt-4.1-mini"

# Nota mínima (de 0 a 1) para aprobar cada métrica con juez
THRESHOLD = 0.5

# Respuestas del agente: salen de la caché out/responses/ (si no existe, se generan)
RESPONSES = load_or_generate(SUITE)


# Ficha del run: se guarda en el historial para que cada entrada sea autoexplicativa
@deepeval.log_hyperparameters
def hyperparameters():
    return {
        "Suite": SUITE,
        "Modelo evaluado": EVALUATED_MODEL,
        "Modelo juez": JUDGE_MODEL,
        "Temperatura": TEMPERATURE,
        "Max tokens": MAX_COMPLETION_TOKENS,
        "Umbral de las métricas": THRESHOLD,
        "Plantilla del prompt": PROMPT_FILE.read_text(encoding="utf-8"),
    }


# Capa 1 — checks deterministas: si algo falla aquí, ni se llama al juez
def run_text_checks(case: dict, answer: str):
    # Prohibida la secuencia literal \n (dos caracteres); los saltos reales sí
    assert "\\n" not in answer, 'La respuesta contiene la secuencia literal "\\n"'
    lower = answer.lower()
    # contains_all: TODOS los términos deben aparecer (ignorando mayúsculas)
    for term in case.get("contains_all", []):
        assert term.lower() in lower, f"Falta el término obligatorio: {term!r}"
    # contains_any: al menos UNO debe aparecer
    if case.get("contains_any"):
        assert any(t.lower() in lower for t in case["contains_any"]), (
            f"No contiene ninguno de: {case['contains_any']}"
        )


# Capas 2-4 — las tres métricas que puntúa el juez para un caso
def make_metrics(case: dict) -> list:
    return [
        # Capa 2: descompone la respuesta en afirmaciones y contrasta cada una
        # contra el retrieval_context (plantilla + email); lo que no salga de ahí
        # cuenta como inventado
        FaithfulnessMetric(model=JUDGE_MODEL, threshold=THRESHOLD),
        # Capa 3: las reglas transversales del prompt, comunes a todos los casos
        GEval(
            name="reglas-globales",
            evaluation_steps=GLOBAL_RUBRIC_STEPS,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.RETRIEVAL_CONTEXT,
            ],
            model=JUDGE_MODEL,
            threshold=THRESHOLD,
        ),
        # Capa 4: el rubric específico de este escenario
        GEval(
            name=f"rubric-{case['id']}",
            criteria=case["rubric"],
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.RETRIEVAL_CONTEXT,
            ],
            model=JUDGE_MODEL,
            threshold=THRESHOLD,
        ),
    ]


# Convierte cada caso de cases.py en un parámetro de pytest con su id.
# Los canarios llevan la marca xfail(strict): fallar es lo esperado, y si algún
# día uno "pasa", pytest lo convierte en error XPASS (ver README)
def build_params() -> list:
    params = []
    for case in CASES:
        marks = []
        if case.get("expect_fail"):
            marks.append(
                pytest.mark.xfail(
                    reason="Canario: el rubric exige algo que el prompt prohíbe",
                    strict=True,
                )
            )
        params.append(pytest.param(case, id=case["id"], marks=marks))
    return params


@pytest.mark.parametrize("case", build_params())
def test_mail_agent(case: dict):
    # Lo que respondió el agente a este caso y la plantilla que debía usar
    answer = RESPONSES[case["id"]]
    loaded_skill = case["skill_file"].read_text(encoding="utf-8")

    # Capa 1 — sin LLM
    run_text_checks(case, answer)

    # Capas 2-4 — con juez; retrieval_context es la "verdad" contra la que
    # Faithfulness contrasta (lo que sale de la plantilla no cuenta como inventado)
    test_case = LLMTestCase(
        input=case["message"],
        actual_output=answer,
        retrieval_context=[loaded_skill, case["message"]],
    )
    assert_test(test_case, make_metrics(case))
