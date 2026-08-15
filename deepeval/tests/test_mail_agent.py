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
JUDGE_MODEL = "gpt-4.1-mini"

RESPONSES = load_or_generate(SUITE)


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
        FaithfulnessMetric(model=JUDGE_MODEL, threshold=0.5),
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

    assert "\\n" not in answer, 'La respuesta contiene la secuencia literal "\\n"'
    lower = answer.lower()
    for term in case.get("contains_all", []):
        assert term.lower() in lower, f"Falta el término obligatorio: {term!r}"
    if case.get("contains_any"):
        assert any(t.lower() in lower for t in case["contains_any"]), (
            f"No contiene ninguno de: {case['contains_any']}"
        )

    test_case = LLMTestCase(
        input=case["message"],
        actual_output=answer,
        retrieval_context=[loaded_skill, case["message"]],
    )
    assert_test(test_case, make_metrics(case))
