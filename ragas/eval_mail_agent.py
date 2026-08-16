# Eval del mail agent con Ragas: prueba las 5 métricas que ofrece el framework
# para calidad de respuesta y coherencia, sobre las MISMAS respuestas cacheadas
# que usa la suite de DeepEval (deepeval/out/responses/mail_agent.json).
#
# Métricas (todas con juez salvo la de embeddings puros):
#   1. Faithfulness        — ¿la respuesta se apoya solo en el contexto (plantilla + email)?
#   2. ResponseRelevancy   — ¿la respuesta responde de verdad a lo que pregunta el email?
#   3. FactualCorrectness  — precisión factual respuesta vs referencia (claim a claim, F1)
#   4. SemanticSimilarity  — similitud de significado respuesta vs referencia (solo embeddings)
#   5. AspectCritic        — veredicto binario del juez sobre la COHERENCIA del texto
#
# Además incluye el CANARIO de promptfoo/DeepEval traducido a Ragas (ver abajo).
#
# Ejecutar desde esta carpeta:  uv run python eval_mail_agent.py

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
OUT_DIR = HERE / "out"

# Misma convención que deepeval/conftest.py: .env de la raíz y OPENAI_API_KEY
# a partir de API_KEY_OPENAI (Ragas/langchain esperan la variable estándar)
load_dotenv(REPO_ROOT / ".env")
os.environ.setdefault("OPENAI_API_KEY", os.environ.get("API_KEY_OPENAI", ""))

# Reutilizamos la suite de DeepEval: casos (emails + plantilla esperada) y
# respuestas del agente ya cacheadas — aquí no se llama al modelo evaluado
sys.path.insert(0, str(REPO_ROOT / "deepeval"))

from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # noqa: E402
from ragas import EvaluationDataset, evaluate  # noqa: E402
from ragas.dataset_schema import SingleTurnSample  # noqa: E402
from ragas.embeddings import LangchainEmbeddingsWrapper  # noqa: E402
from ragas.llms import LangchainLLMWrapper  # noqa: E402
from ragas.metrics import (  # noqa: E402
    AspectCritic,
    FactualCorrectness,
    Faithfulness,
    ResponseRelevancy,
    SemanticSimilarity,
)

from core.generate_responses import load_or_generate  # noqa: E402
from references import REFERENCES  # noqa: E402
from suites.mail_agent.cases import CASES  # noqa: E402

SUITE = "mail_agent"

# Mismo juez que en DeepEval: pequeño y distinto del modelo evaluado
JUDGE_MODEL = "gpt-4.1-mini"
EMBEDDINGS_MODEL = "text-embedding-3-small"

# Ragas trabaja con wrappers de langchain; temperatura 0 = juez más estable
judge = LangchainLLMWrapper(ChatOpenAI(model=JUDGE_MODEL, temperature=0))
embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model=EMBEDDINGS_MODEL))


# Las 5 métricas a probar; cada una declara qué necesita del sample
def make_metrics() -> list:
    return [
        # Usa response + retrieved_contexts: descompone la respuesta en
        # afirmaciones y comprueba que cada una salga del contexto
        Faithfulness(llm=judge),
        # Usa user_input + response (+ embeddings): genera preguntas hipotéticas
        # a partir de la respuesta y mide si se parecen a la pregunta real.
        # OJO: puntúa 0 toda respuesta que clasifica como evasiva (noncommittal),
        # y nuestro prompt OBLIGA a ser evasivo cuando falta el dato ("lo
        # revisamos y confirmamos") — no encaja con este agente (ver README)
        ResponseRelevancy(llm=judge, embeddings=embeddings),
        # Usa response + reference: F1 entre las afirmaciones de ambas
        FactualCorrectness(llm=judge, mode="f1"),
        # Usa response + reference: coseno de embeddings, sin juez (barata).
        # Señal débil: mide que "suene parecido", no que diga la verdad
        SemanticSimilarity(embeddings=embeddings),
        # Aspecto "coherence" (uno de los predefinidos de AspectCritic):
        # veredicto binario 0/1 del juez sobre la organización lógica del texto.
        # Solo mira la FORMA, no la veracidad del contenido
        AspectCritic(
            name="coherencia",
            definition=(
                "Verify if the response is a coherent email: ideas presented in a "
                "logical and organized manner, with a clear flow of greeting, body "
                "and closing, without contradictions or abrupt jumps."
            ),
            llm=judge,
        ),
    ]


# EL CANARIO, versión Ragas. En promptfoo/DeepEval el rubric del caso
# canario-inventar exigía inventar el desglose del recibo y por eso "debía
# fallar". Ragas no tiene rubrics ni xfail, pero AspectCritic permite el mismo
# truco con la lectura invertida: el juez devuelve 1 SOLO si la respuesta REAL
# del agente da el motivo exacto y el desglose en euros — datos que no existen
# en ningún contexto y que el prompt prohíbe inventar.
#   0 = el agente se comporta (equivale al xfail en verde / rojo de promptfoo)
#   1 = el agente INVENTA datos (equivale al XPASS: problema real, no lo "arregles")
CANARY_CASE_ID = "canario-inventar"


def make_canary_metric() -> AspectCritic:
    # OR, no AND: inventar SOLO el motivo o SOLO cifras ya es invención
    return AspectCritic(
        name="canario_inventa_desglose",
        definition=(
            "Return 1 if the response states a specific cause for the bill "
            "increase OR gives any concrete figures in euros for the amount or "
            "its breakdown. Return 0 only if the response commits to neither a "
            "cause nor figures, for example if it says the case will be "
            "reviewed and confirmed later."
        ),
        llm=judge,
    )


# Convierte los casos de la suite en samples de Ragas. El canario de promptfoo
# (canario-inventar) entra en el dataset con su respuesta REAL, como uno más;
# los otros dos canarios de DeepEval se quedan fuera: su gracia era el rubric
# (derivar / meter asunto) y las métricas genéricas de Ragas no miden eso
def build_samples(responses: dict[str, str]) -> tuple[list[str], list[SingleTurnSample]]:
    ids, samples = [], []
    for case in CASES:
        if case.get("expect_fail") and case["id"] != CANARY_CASE_ID:
            continue
        ids.append(case["id"])
        samples.append(
            SingleTurnSample(
                user_input=case["message"],
                response=responses[case["id"]],
                # El mismo "contexto de verdad" que en DeepEval: plantilla + email
                retrieved_contexts=[
                    case["skill_file"].read_text(encoding="utf-8"),
                    case["message"],
                ],
                reference=REFERENCES[case["id"]],
            )
        )
    return ids, samples


def main():
    responses = load_or_generate(SUITE)
    ids, samples = build_samples(responses)

    # 1. Las 5 métricas sobre todos los casos
    print(f"Evaluando {len(ids)} casos con juez {JUDGE_MODEL} ...\n")
    result = evaluate(dataset=EvaluationDataset(samples=samples), metrics=make_metrics())

    # Detalle por caso (una fila por email, una columna por métrica)
    df = result.to_pandas()
    df.insert(0, "case", ids)
    detail = df[["case"] + [c for c in df.columns if c not in ("case", "user_input", "response", "retrieved_contexts", "reference")]]
    print(detail.round(3).to_string(index=False))

    # Medias del run (lo que imprime repr(result))
    print(f"\nMedias del run: {result}")

    OUT_DIR.mkdir(exist_ok=True)
    csv_file = OUT_DIR / f"{SUITE}.csv"
    df.to_csv(csv_file, index=False)
    print(f"Detalle completo guardado en {csv_file}")

    # 2. El canario: solo su caso, solo su métrica, y con la lectura invertida
    print("\nCanario (¿el agente inventa el desglose del recibo?) ...")
    canary_sample = samples[ids.index(CANARY_CASE_ID)]
    canary_result = evaluate(
        dataset=EvaluationDataset(samples=[canary_sample]),
        metrics=[make_canary_metric()],
    )
    # Solo 0 y 1 son veredictos; con raise_exceptions=False (el default) Ragas
    # devuelve nan si la métrica falla (timeout, parseo...), y nan NO es un 1
    score = canary_result.to_pandas()["canario_inventa_desglose"].iloc[0]
    if score == 1:
        # El equivalente al XPASS de pytest: el agente incumple su prompt
        print("¡CANARIO DISPARADO (1)!: la respuesta inventa el motivo y/o cifras.")
        sys.exit(1)
    elif score == 0:
        print("Canario OK (0): el agente NO inventa — se compromete a revisar y confirmar.")
    else:
        print(f"Error de evaluación del canario (score={score}): el juez no emitió veredicto.")
        sys.exit(2)


if __name__ == "__main__":
    main()
