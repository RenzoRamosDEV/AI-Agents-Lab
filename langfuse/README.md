# Eval del mail_agent con Langfuse

Suite de evaluación del agente de email (`agent/rr-agent-config-mail`) sobre
[Langfuse](https://langfuse.com/): los casos viven en un **dataset** en la nube
y cada ejecución es un **experimento** (dataset run) que llama al agente real,
puntúa cada respuesta y sube los resultados. A diferencia de promptfoo y
DeepEval (resultados en local), aquí todo queda en la UI de Langfuse: histórico
de runs comparables, trazas completas de cada llamada (prompt, tokens, coste) y
el razonamiento del juez en cada score.

Los casos son los mismos que en `promptfoo/promptfooconfig.yaml` (misma fuente:
al cambiar uno, actualizar el otro).

## Cómo lanzarlo

Necesita el venv del repo (`uv sync`) y el `.env` de la raíz con
`API_KEY_OPENAI` y las credenciales `API_KEY_PUBLIC_LANGFUSE` /
`API_KEY_PRIVATE_LANGFUSE` / `BASE_URL_LANGFUSE`. Desde cualquier sitio del repo:

```bash
script/langfuse/run_langfuse.sh
```

A mano, desde **esta carpeta** (importante: no desde la raíz del repo — la
carpeta se llama igual que el paquete Python y el `import langfuse` cargaría la
carpeta en vez del SDK):

```bash
cd langfuse
../.venv/bin/python eval_mail_agent.py
```

No hay caché: cada run llama al modelo evaluado y al juez de nuevo (~0,02 USD).

**Resultado esperado**: `media-rubrica-ok = 0.833` (5/6). El único rojo
esperado en `rubrica-ok` y `contains` es `prueba-fallo` (ver abajo).
`reglas-globales` puede tener algún rojo suelto: ese juez es flaky (por eso sus
llamadas quedan trazadas — se puede auditar su razonamiento en la UI).

## Dónde ver los resultados

En [cloud.langfuse.com](https://cloud.langfuse.com), dentro del proyecto:

- **Experiments** — lista de runs con la media de cada score por columna
  (`Ø contains`, `Ø reglas-globales`...). Como los scores son 0/1, cualquier
  media < 1 significa que algún caso falló.
- Clic en un run → tabla con una fila por caso y sus scores individuales; los
  fallos se ven como ceros. Clic en la fila → la **traza** del caso, con la
  llamada real al modelo y el comentario del juez explicando cada score.
- Lo mismo por **Datasets → mail-agent-cases → Runs**.

## Qué hace un run (`eval_mail_agent.py`)

1. **Sincroniza el dataset** `mail-agent-cases` con `cases.py`: sube/actualiza
   los casos (ids estables → re-subir actualiza en vez de duplicar) y borra los
   items que ya no existan.
2. **Ejecuta el experimento**: para cada caso, la task llama al agente REAL
   (`deepeval/suites/mail_agent/agent.py`, ya instrumentado con
   `langfuse.openai`) — así cada respuesta queda trazada sin código extra.
3. **Puntúa cada caso** con cuatro evaluadores, de más barato a más caro:

| Score | Tipo | Qué valida |
|---|---|---|
| `sin-n-literal` | determinista | prohibida la secuencia literal `\n` en el texto |
| `contains` | determinista | `contains_any` / `contains_all` del caso (si no define ninguno, no emite score) |
| `reglas-globales` | juez LLM | las reglas transversales del prompt (`GLOBAL_RUBRIC`: mismo idioma, estructura de email, "nosotros", no derivar, no inventar, sin asunto) |
| `rubrica-ok` | juez LLM | la rúbrica específica del caso; en los canarios se invierte (ver abajo) |

4. **Score agregado del run**: `media-rubrica-ok` (media de `rubrica-ok`, se ve
   en la columna de la lista de experimentos).

## Los casos (`cases.py`)

6 casos, formato item de dataset de Langfuse (`id` estable + `input` +
`expected_output` + `metadata` con los checks y la rúbrica):

- `billing-cobro`, `complaint-baja`, `home-coverages`, `generic-english` —
  casos normales: deben salir todo en verde.
- `canario-inventar` — **CANARIO** (`expect_fail: True`): su rúbrica exige
  inventar datos, cosa que el prompt prohíbe. El veredicto del juez se
  **invierte**: que suspenda es lo correcto (`rubrica-ok = 1`). Si algún día el
  juez la aprueba, el modelo está inventando datos — problema real, no lo
  "arregles".
- `prueba-fallo` — caso diseñado para **fallar de verdad** (`expect_fail:
  False`): su rúbrica y su `contains` exigen un código promocional (`VERANO25`)
  que el agente no conoce ni puede inventar. Sirve para ver cómo pinta un rojo
  en la UI. Es el que baja `media-rubrica-ok` a 0.833; bórralo cuando ya no
  haga falta.

## Estructura

```
langfuse/
├── README.md
├── cases.py            # los casos (dataset): ids estables, input, rúbricas, checks
└── eval_mail_agent.py  # sync del dataset + experimento + evaluadores
```

El agente evaluado y su prompt NO viven aquí: se reutilizan los de la suite de
DeepEval (`deepeval/suites/mail_agent/`) — un solo sitio que mantener. Importar
`agent` es además lo que carga el `.env` y mapea las credenciales `LANGFUSE_*`
antes de inicializar el cliente.

## Los dos modelos: evaluado y juez

- **Evaluado** (`gpt-5.6-terra`, en `deepeval/suites/mail_agent/agent.py`):
  hace de agente — recibe el email y redacta la respuesta. Es a quien se examina.
- **Juez** (`gpt-4.1-mini`, en `eval_mail_agent.py`): puntúa `reglas-globales`
  y `rubrica-ok` leyendo la respuesta del evaluado. Mismo juez que en las otras
  suites: modelo pequeño y distinto a propósito (calificar es más fácil que
  redactar, es barato, y un modelo no debe calificarse a sí mismo). Responde
  JSON estricto `{reason, passed}` con `reason` ANTES que `passed` para que
  razone antes del veredicto, y su system prompt incluye reglas de
  interpretación contra falsos suspensos (p. ej. tutear al cliente NO incumple
  el "nosotros").

## Cómo se hace un caso

Añade un dict a la lista `CASES` de `cases.py`:

```python
{
    # Id estable: nombra el item del dataset (re-subir actualiza, no duplica)
    "id": "billing-devolucion",
    "input": {
        # El email entrante (clave única: los evaluadores localizan el caso por él)
        "message": (
            "De: cliente@gmail.com\n"
            "Asunto: Devolución del último recibo\n\n"
            "Hola, quiero que me devolváis el último recibo, no reconozco el cargo."
        ),
        # La plantilla que el agente debería usar (fichero real de agent/.../skills/)
        "skill_file": "mail-template-billing.md",
    },
    # Comportamiento esperado en lenguaje natural (se muestra en la UI; no hay respuesta dorada)
    "expected_output": "Acusa recibo de la petición de devolución y dice que se revisará.",
    "metadata": {
        "description": "Facturación — pide una devolución",
        "expect_fail": False,          # True solo para canarios
        "contains_any": ["devolución", "recibo"],   # al menos uno (ignora mayúsculas)
        "contains_all": None,                        # todos, literal
        "rubric": (
            "1. Saluda al remitente.\n"
            "2. Resume lo que pide (devolución del último recibo).\n"
            "3. NO confirma la devolución como hecha ni da plazos inventados.\n"
            "Suspende si incumple cualquiera."
        ),
    },
},
```

El siguiente run lo sube al dataset y lo evalúa automáticamente. Si además
quieres el caso en promptfoo, añádelo también a `promptfooconfig.yaml`.

## Notas

- Los warnings `Propagated attribute ... rubric ... over 200 characters.
  Dropping value` al ejecutar son inofensivos: Langfuse trunca la rúbrica como
  atributo propagado de la traza, pero la rúbrica llega entera al juez.
- Las trazas del eval van marcadas con environment `development`
  (`LANGFUSE_TRACING_ENVIRONMENT` en `agent.py`): no ensucian dashboards de
  producción.
