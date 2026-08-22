# Eval de agentes con DeepEval

## La herramienta

[DeepEval](https://deepeval.com/) es un framework de evaluación de LLMs en
Python que funciona sobre pytest: cada eval es un test y las métricas (juez LLM
incluido) se aplican como asserts. Aquí es el banco de evaluación de los agentes
del repo: cada agente tiene su **suite** (casos + prompt + invocación del
modelo) y todas se ejecutan igual. Mide la calidad de respuesta y detecta
**datos inventados** (alucinaciones) con la métrica **Faithfulness**.

Suites actuales: `mail_agent` (agente de email de `agent/rr-agent-config-mail`).

## Ventajas

|   | Punto | Detalle |
|---|---|---|
| ✅ | **Es pytest por debajo** | los evals se ejecutan, marcan y filtran como cualquier test (incluido `xfail` para los canarios) |
| ✅ | **Faithfulness** | descompone la respuesta en afirmaciones y las contrasta con el contexto real — el detector de alucinaciones |
| ✅ | **Caché de respuestas** | separa generación de evaluación: se pueden re-ejecutar las métricas sin volver a pagar/esperar al modelo evaluado |
| ✅ | **Historial local de runs** | cada run guarda sus hyperparameters (modelos, temperatura, umbral…) — autoexplicativo |
| ⚠️ | **A tener en cuenta** | hay que ejecutarlo desde esta carpeta (shadowing del paquete `deepeval`) y su resumen propio cuenta los canarios como fallos |

## Cómo lanzarlo

| Requisito | Detalle |
|---|---|
| venv del repo | `uv sync` en la raíz |
| API key | `API_KEY_OPENAI` en el `.env` de la raíz |

Desde cualquier sitio del repo:

```bash
script/deepeval/run_deepeval.sh                    # suite por defecto: mail_agent
script/deepeval/run_deepeval.sh <suite>            # otra suite (p. ej. auto_agent cuando exista)
script/deepeval/run_deepeval.sh [<suite>] --fresh  # regenera las respuestas del agente antes de evaluar
script/deepeval/clean_deepeval.sh                  # borra todo lo generado (out/ con el historial, .deepeval/, cachés)
```

A mano, desde **esta carpeta** (importante: no desde la raíz del repo — la carpeta se llama igual que el paquete Python y el `import deepeval` cargaría la carpeta en vez de la librería):

```bash
cd deepeval
../.venv/bin/python -m core.generate_responses mail_agent   # 1. genera las respuestas (opcional)
../.venv/bin/deepeval test run tests/test_mail_agent.py     # 2. corre el eval (si falta la caché, la genera solo)
```

Resultado esperado en `mail_agent`: **`5 passed, 3 xfailed`**. Los `xfailed` son los **canarios** (ver [Canarios](#canarios)).

## Cómo funciona

### Estructura

```
deepeval/
├── README.md
├── conftest.py                  # config de pytest: claves de API para el juez
├── core/                        # genérico, compartido por todas las suites
│   └── generate_responses.py    # genera y cachea las respuestas del agente de una suite
├── suites/
│   └── mail_agent/              # una carpeta por agente evaluado
│       ├── agent.py             # invoca al modelo EVALUADO igual que en producción
│       ├── cases.py             # los casos de prueba con sus rubrics
│       └── prompt.json          # el prompt real del agente, en formato chat
├── tests/
│   └── test_mail_agent.py       # un test de pytest por suite, con las métricas DeepEval
└── out/                         # generado, gitignoreado
    ├── responses/<suite>.json   # caché de respuestas del agente, por suite
    └── history/<suite>/run-*.json  + history/index.json (índice de suites y runs)
```

### Carpeta `suites/` — una suite por agente

Cada suite empaqueta todo lo específico de un agente:

| Fichero | Papel |
|---|---|
| `prompt.json` | el prompt real del agente en formato chat: lo que se le envía al modelo en cada caso |
| `agent.py` | invoca al modelo EVALUADO igual que en producción (modelo, temperatura, max tokens) |
| `cases.py` | los casos de prueba con sus rubrics + `GLOBAL_RUBRIC_STEPS` (reglas comunes) |

**`prompt.json` — el prompt del agente.** No basta con mandarle el email del cliente: hay que mandarle lo mismo que recibe el agente en producción — sus instrucciones completas y luego el email — porque si no, no estarías evaluando a tu agente sino a un modelo "a pelo". Son 2 mensajes en formato chat: el **system** (copia del prompt real del agente, el de LangSmith en `agent/rr-agent-config-mail/prompts/`) y el **user** (el email entrante). Los huecos `{{...}}` los rellena `agent.py` en cada caso; `{{loaded_skill}}` es el único añadido respecto al prompt real: el agente de verdad carga la plantilla con la herramienta `load_skill`, pero en el eval no hay herramientas, así que se inyecta directamente el `.md` real del agente.

⚠️ Es una **copia manual**: si cambias el prompt del agente en LangSmith o en el `.md`, actualiza también este JSON — si divergen, estarás evaluando un prompt que ya no usas.

**`agent.py` — el agente evaluado.** Monta los mensajes a partir de `prompt.json` y llama al modelo evaluado por la API de OpenAI con el mismo `response_format` que usa el agente real (JSON con campo `answer`). Key: `API_KEY_OPENAI` en el `.env` de la raíz.

**`cases.py` — los casos de prueba.** Cada caso es un dict con el email entrante, la plantilla que el agente debería usar (fichero real de `agent/.../skills/`), checks de texto y su rubric. La suite `mail_agent` tiene 8 casos:

| Caso | Tipo | Escenario |
|---|---|---|
| `billing-cobro` | normal | Facturación — duda sobre un cobro |
| `complaint-baja` | normal | Queja — cliente enfadado que amenaza con darse de baja |
| `home-coverages` | normal | Coberturas de hogar — pregunta qué cubre la póliza |
| `generic-cambio-direccion` | normal | Genérico — cliente comunica su nueva dirección postal |
| `generic-english` | normal | Genérico — email en inglés (debe responder en el mismo idioma) |
| `canario-inventar` | 🐤 debe fallar | el rubric exige inventar datos (ver [Canarios](#canarios)) |
| `canario-derivar` | 🐤 debe fallar | el rubric exige derivar a otro equipo (ver [Canarios](#canarios)) |
| `canario-asunto` | 🐤 debe fallar | el rubric exige línea de asunto y metacomentario (ver [Canarios](#canarios)) |

### Carpeta `core/`

`generate_responses.py` es genérico: recibe el nombre de la suite, genera las respuestas del agente una vez por caso y las cachea en `out/responses/<suite>.json`. Separar generación de evaluación permite re-ejecutar las métricas (el juez) sin volver a pagar/esperar al modelo evaluado. **Borra la caché (o usa `--fresh`) después de cambiar el prompt o las plantillas del agente**, o estarás evaluando respuestas viejas.

### Carpeta `tests/`

Un `test_<suite>.py` por suite (`deepeval test run` es pytest por debajo). Cada test aplica cuatro capas, de la más barata a la más cara:

| # | Capa | Tipo | Qué valida |
|---|---|---|---|
| 1 | Checks de texto | determinista (gratis y exacto) | sin `\n` literal, términos obligatorios (`contains_any` / `contains_all`) |
| 2 | Faithfulness | juez LLM | descompone la respuesta en afirmaciones y las contrasta con el contexto real (email + plantilla) — detector de alucinaciones |
| 3 | GEval `reglas-globales` | juez LLM | las reglas del prompt, con la plantilla como contexto |
| 4 | GEval `rubric-<caso>` | juez LLM | el rubric específico del escenario |

Umbral de todas las métricas: `0.5`. Además, el test registra los **hyperparameters** del run (suite, modelo evaluado, juez, temperatura, max tokens, umbral y la plantilla del prompt) — así cada entrada del historial es autoexplicativa.

### `conftest.py`

Carga el `.env` de la raíz y expone `API_KEY_OPENAI` como `OPENAI_API_KEY`, que es la variable que DeepEval espera para el modelo juez. Al estar en la raíz de la carpeta, pytest lo carga siempre y de paso hace importables `core/` y `suites/` desde los tests.

### Los dos modelos: evaluado y juez

| Rol | Modelo | Dónde se configura | Qué hace |
|---|---|---|---|
| **Evaluado** | `gpt-5.6-terra` | `suites/<suite>/agent.py` | hace de agente: recibe la entrada y redacta la respuesta. Es a quien se examina |
| **Juez** | `gpt-4.1-mini` | `tests/test_<suite>.py` | puntúa las métricas leyendo la respuesta del evaluado (los checks de texto no usan ningún modelo) |

Se usa un modelo pequeño y distinto como juez a propósito: calificar contra criterios es más fácil que redactar (mini basta), es mucho más barato (~0,02 USD por run), y un modelo no debe calificarse a sí mismo. Al cambiar el modelo evaluado, el juez se queda igual: mismo corrector para poder comparar.

## Ejemplos

### Añadir un caso de test

Añade un dict a la lista `CASES` de `suites/<suite>/cases.py`:

```python
{
    # Identificador del caso: nombra el test en pytest y la entrada en out/responses/
    "id": "billing-devolucion",
    "description": "Facturación — pide una devolución",
    # 1. La plantilla que el agente debería usar (fichero real del agente)
    "skill_file": SKILLS_DIR / "mail-template-billing.md",
    # 2. La entrada del caso (aquí, el email con remitente y asunto)
    "message": (
        "De: cliente@gmail.com\n"
        "Asunto: Devolución del último recibo\n\n"
        "Hola, quiero que me devolváis el último recibo, no reconozco el cargo."
    ),
    # 3a. Checks deterministas: baratos y exactos (ignoran mayúsculas)
    "contains_any": ["devolución", "recibo"],   # al menos uno debe aparecer
    # "contains_all": [...],                    # todos deben aparecer
    # 3b. Rubric del caso: criterios en lenguaje natural que valida el juez
    "rubric": (
        "1. Saluda al remitente.\n"
        "2. Resume lo que pide (devolución del último recibo).\n"
        "3. NO confirma la devolución como hecha ni da plazos inventados: dice que se revisará.\n"
        "Suspende si incumple cualquiera."
    ),
    # "expect_fail": True,   # solo para canarios: marca el test como xfail(strict)
}
```

Eso es todo: el test, Faithfulness y las reglas globales se aplican automáticamente. Después ejecuta con `--fresh` para generar la respuesta del caso nuevo.

### Añadir una suite nueva (p. ej. `auto_agent`)

1. Crea `suites/auto_agent/` con `agent.py`, `cases.py` y `prompt.json` (usa `mail_agent` de plantilla).
2. Crea `tests/test_auto_agent.py` (copia el de mail y cambia imports y `SUITE`).
3. `script/deepeval/run_deepeval.sh auto_agent` — y listo: se genera su caché y su historial de runs.

## Canarios

Los tres `xfailed` del resultado esperado son los **canarios**: sus rubrics exigen cosas que el agente tiene prohibidas, así que fallar = el modelo se comporta bien.

| Caso | Qué exige su rubric (prohibido por el prompt) |
|---|---|
| `canario-inventar` | inventar datos |
| `canario-derivar` | derivar a otro equipo |
| `canario-asunto` | meter línea de asunto / metacomentarios |

Van marcados `xfail(strict=True)`: si algún día uno "pasa", pytest lo marcará como error `XPASS` — problema real, no lo "arregles".

Ojo: el resumen propio de DeepEval cuenta los canarios como fallos en su "Pass Rate"; la línea de pytest (`5 passed, 3 xfailed`) es la que manda.

## Notas y referencias

| Recurso | Dónde |
|---|---|
| Catálogo completo de métricas (relevancia, toxicidad, RAG, etc.) | <https://deepeval.com/docs/metrics-introduction> |
| Web de DeepEval | <https://deepeval.com/> |
| Documentación | <https://deepeval.com/docs> |
