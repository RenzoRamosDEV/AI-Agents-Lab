# Eval del mail_agent con Ragas

Tercera pata del banco de evaluación del agente de email
(`agent/rr-agent-config-mail`), esta vez con [Ragas](https://docs.ragas.io):
prueba las métricas de **calidad de respuesta** y **coherencia** del framework
sobre las **mismas respuestas cacheadas** que usa la suite de DeepEval
(`deepeval/out/responses/mail_agent.json`) — aquí no se llama al modelo
evaluado, solo al juez.

## Cómo lanzarlo

Necesita `API_KEY_OPENAI` en el `.env` de la raíz (misma convención que las
otras suites) y las dependencias del `pyproject.toml` (`uv sync`).

Desde cualquier sitio del repo:

```bash
script/ragas/run_ragas.sh            # corre el eval (usa la caché de respuestas)
script/ragas/run_ragas.sh --fresh    # regenera las respuestas del agente antes de evaluar
script/ragas/clean_ragas.sh          # borra lo generado (out/ y __pycache__)
```

A mano, desde **esta carpeta**:

```bash
cd ragas
uv run python eval_mail_agent.py
```

Resultado esperado: la tabla de 6 casos × 5 métricas y al final
**`Canario OK (0)`** (ver abajo). Si el canario se dispara, el script sale con
código 1. Si no existe la caché de respuestas, se genera con el mismo
`load_or_generate` de DeepEval (ahí sí se llama al modelo evaluado). El detalle
por caso se guarda en `out/mail_agent.csv` (carpeta gitignoreada).

Ragas **no tiene UI local** (a diferencia de `promptfoo view`): lo oficial es
su dashboard en la nube (app.ragas.io, con cuenta y API key) o exportar a
herramientas de observabilidad (Langfuse, LangSmith...). Aquí basta con la
tabla por consola + el CSV.

## Estructura

```
ragas/
├── README.md
├── eval_mail_agent.py    # la eval: dataset + las 5 métricas + el canario
├── references.py         # respuestas "ideales" por caso (ground truth)
└── out/                  # generado, gitignoreado
    └── mail_agent.csv    # detalle del último run
```

No hay `agent.py` ni `prompt.json` propios: los casos (emails + plantilla
esperada) se importan de `deepeval/suites/mail_agent/cases.py` y las respuestas
de la caché — misma entrada, mismo agente, otro framework de medición.

## Los dos modelos: evaluado y juez

Igual que en las otras suites: el **evaluado** (`gpt-5.6-terra`) redactó las
respuestas cacheadas; el **juez** (`gpt-4.1-mini`) puntúa las métricas. Aquí se
añade un tercer modelo, `text-embedding-3-small`, para las dos métricas que
usan **embeddings** (ResponseRelevancy y SemanticSimilarity). Ragas los recibe
envueltos en wrappers de langchain (`LangchainLLMWrapper` / `LangchainEmbeddingsWrapper`).

## Las 5 métricas probadas

| Métrica | Qué necesita | Qué mide |
|---|---|---|
| `Faithfulness` | respuesta + contexto | Descompone la respuesta en afirmaciones y comprueba que cada una salga del contexto (plantilla + email). Equivale a la `FaithfulnessMetric` de DeepEval. |
| `ResponseRelevancy` | pregunta + respuesta | Genera preguntas hipotéticas a partir de la respuesta y mide (embeddings) si se parecen a la pregunta real del email. |
| `FactualCorrectness` | respuesta + referencia | F1 entre las afirmaciones de la respuesta y las de la referencia de `references.py`. |
| `SemanticSimilarity` | respuesta + referencia | Coseno de embeddings entre respuesta y referencia. Sin juez: la más barata. |
| `AspectCritic` (coherencia) | respuesta | Veredicto binario (0/1) del juez: ¿email organizado con saludo, cuerpo y cierre, sin contradicciones? En Ragas la coherencia no es una métrica dedicada, es un aspecto predefinido de `AspectCritic`. |

## Diferencias con DeepEval y promptfoo

- **Sin rubrics por escenario**: las métricas de Ragas son genéricas; no hay
  equivalente directo a GEval/llm-rubric donde escribir "suspende si...". Lo
  más parecido es `AspectCritic` con una definición a medida — así está hecho
  el canario (abajo).
- **Con referencias**: dos métricas comparan contra una respuesta "ideal"
  escrita a mano (`references.py`), algo que las otras suites no necesitaban.
  La calidad de la medición depende de la calidad de esas referencias.
- **Sin pass/fail**: Ragas devuelve puntuaciones, no verdes/rojos; los umbrales
  los pones tú al leer el informe. El canario es la excepción: el script lo
  convierte en pass/fail con `sys.exit(1)`.

## Cómo leer los resultados (run de ejemplo)

```
                    case  faithfulness  answer_relevancy  factual_correctness  semantic_similarity  coherencia
           billing-cobro          0.67              0.00                 0.50                 0.91           1
          complaint-baja          0.22              0.00                 0.78                 0.93           1
          home-coverages          1.00              0.50                 0.99                 0.90           1
        canario-inventar          1.00              0.00                 0.80                 0.96           1
generic-cambio-direccion          0.75              0.00                 0.80                 0.96           1
         generic-english          1.00              0.00                 0.75                 0.94           1
```

- **`coherencia` = 1 en todo**: los emails están bien estructurados. Ojo: mide
  forma, no verdad — una respuesta inventada pero bien redactada también saca 1.
- **`semantic_similarity` alta (~0.9)**: las respuestas se parecen a las
  referencias en significado. Señal débil: mide que "suene parecido".
- **`answer_relevancy` = 0 casi siempre, y NO es un bug**: la métrica puntúa 0
  toda respuesta que clasifica como evasiva (*noncommittal*), y nuestro prompt
  OBLIGA a ser evasivo cuando falta el dato ("lo revisamos y te confirmamos").
  El único caso que responde con contenido concreto (home-coverages) puntúa.
  Peor aún: a una respuesta que INVENTA el desglose le daría nota alta por
  "responder directo". Moraleja: una métrica de catálogo puede castigar justo
  el comportamiento que tu prompt exige — elige métricas que midan TU política.
- **`faithfulness` baja en la queja (0.22)**: las frases de empatía
  ("entendemos tu malestar", "asumimos la responsabilidad") no salen del
  contexto y el juez las cuenta como afirmaciones sin fundamento.
- Ojo: el juez no es determinista — los scores con LLM bailan un poco entre
  runs (faithfulness del mismo caso ha dado 0.67, 0.80 y 1.00 en runs seguidos).

## El CANARIO (mismo caso que en promptfoo, sin forzar nada)

`canario-inventar` entra al dataset como un caso más, con la **respuesta real**
del agente. En promptfoo/DeepEval "debía fallar" porque el rubric exigía
inventar el desglose del recibo; Ragas no tiene rubrics ni xfail, así que el
truco se traduce a un `AspectCritic` con la lectura invertida — el juez
devuelve 1 si la respuesta da un motivo concreto de la subida **o** cualquier
cifra en euros del importe/desglose (datos que no existen en ningún contexto y
que el prompt prohíbe inventar; con OR a propósito: inventar solo una de las
dos cosas ya es invención):

- **0 = canario OK**: el agente NO inventa (equivale al xfail verde de
  DeepEval / al rojo esperado de promptfoo).
- **1 = canario disparado**: el agente está inventando datos (equivale al
  XPASS) — el script sale con código 1. Es un problema del agente, no lo
  "arregles" tocando la métrica.
- **Cualquier otro valor** (p. ej. `nan`, que Ragas devuelve si la métrica
  falla) no es un veredicto: el script lo trata como error de evaluación y
  sale con código 2 en vez de dar un falso positivo/negativo.

Verificado en ambos sentidos: con la respuesta real del agente da 0, y probado
a mano con respuestas que inventan solo el motivo, solo cifras, o ambos — las
tres dan 1. El detector detecta solo — sin referencia y sin forzar el fallo.

En el resto de métricas el canario saca buenas notas (faithfulness 1.00), y
tiene sentido: sin rubric que incumplir, lo que queda es un agente haciendo lo
correcto. Su "debe fallar" era una propiedad del rubric, no del caso.

Catálogo completo de métricas de Ragas: <https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/>
