# El test de la suite mail_agent (deepeval test run es pytest por debajo).
# Cada caso pasa por 4 capas, de la más barata a la más cara:
#   1. checks de texto (sin LLM, gratis)      3. GEval reglas-globales (juez)
#   2. Faithfulness (detector alucinaciones)  4. GEval rubric-<caso> (juez)

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

# Respuestas del agente: salen de la caché out/responses/ (si no existe, se generan)
RESPONSES = load_or_generate(SUITE)


# Se registran en cada run del historial para que cada entrada sea autoexplicativa
@deepeval.log_hyperparameters
def hyperparameters():
    return {
        "Suite": SUITE,
        "Modelo evaluado": EVALUATED_MODEL,
        "Modelo juez": JUDGE_MODEL,
        "Temperatura": TEMPERATURE,
        "Max tokens": MAX_COMPLETION_TOKENS,
        "Umbral de las métricas": 0.5,
        "Plantilla del prompt": PROMPT_FILE.read_text(encoding="utf-8"),
    }


def make_metrics(case: dict) -> list:
    return [
        # Detector de alucinaciones: descompone la respuesta en afirmaciones y
        # contrasta cada una contra el retrieval_context (plantilla + email)
        FaithfulnessMetric(model=JUDGE_MODEL, threshold=0.5),
        # El juez valida las reglas transversales del prompt (comunes a todos los casos)
        GEval(
            name="reglas-globales",
            evaluation_steps=GLOBAL_RUBRIC_STEPS,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.RETRIEVAL_CONTEXT,
            ],
            model=JUDGE_MODEL,
            threshold=0.5,
        ),
        # El juez valida el rubric específico del escenario
        GEval(
            name=f"rubric-{case['id']}",
            criteria=case["rubric"],
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.RETRIEVAL_CONTEXT,
            ],
            model=JUDGE_MODEL,
            threshold=0.5,
        ),
    ]


# Un test por caso; los canarios van como xfail(strict): fallar es lo esperado
# y si "pasan" pytest los marca como error XPASS (ver README)
@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            case,
            id=case["id"],
            marks=pytest.mark.xfail(
                reason="Canario: el rubric exige inventar datos y el prompt lo prohíbe",
                strict=True,
            )
            if case.get("expect_fail")
            else [],
        )
        for case in CASES
    ],
)
def test_mail_agent(case: dict):
    answer = RESPONSES[case["id"]]
    loaded_skill = case["skill_file"].read_text(encoding="utf-8")

    # Capa 1 — checks deterministas (sin LLM): \n literal prohibido + términos obligatorios
    assert "\\n" not in answer, 'La respuesta contiene la secuencia literal "\\n"'
    lower = answer.lower()
    for term in case.get("contains_all", []):
        assert term.lower() in lower, f"Falta el término obligatorio: {term!r}"
    if case.get("contains_any"):
        assert any(t.lower() in lower for t in case["contains_any"]), (
            f"No contiene ninguno de: {case['contains_any']}"
        )

    # Capas 2-4 — métricas con juez; retrieval_context = la "verdad" contra la
    # que Faithfulness contrasta (lo que sale de la plantilla no cuenta como inventado)
    test_case = LLMTestCase(
        input=case["message"],
        actual_output=answer,
        retrieval_context=[loaded_skill, case["message"]],
    )
    assert_test(test_case, make_metrics(case))
