# Eval del mail_agent con Langfuse

## La herramienta

[Langfuse](https://langfuse.com/) es una plataforma de observabilidad y
evaluación de LLMs en la nube: datasets, experimentos, trazas y scores viven en
su UI. Aquí se usa como suite de evaluación del agente de email
(`agent/rr-agent-config-mail`): los casos viven en un **dataset** en la nube y
cada ejecución es un **experimento** (dataset run) que llama al agente real,
puntúa cada respuesta y sube los resultados.

Los casos son los mismos que en `promptfoo/promptfooconfig.yaml` (misma fuente:
al cambiar uno, actualizar el otro).

## Ventajas

|   | Punto | Detalle |
|---|---|---|
| ✅ | **Todo queda en la nube** | a diferencia de promptfoo y DeepEval (resultados en local): histórico de runs comparables entre sí en la UI |
| ✅ | **Trazas completas** | prompt, tokens y coste de cada llamada, auditables a posteriori |
| ✅ | **Razonamiento del juez registrado** | en cada score se ve por qué aprobó o suspendió (y se puede auditar al juez cuando es flaky) |
| ✅ | **Dataset con ids estables** | re-subir actualiza en vez de duplicar; los runs apuntan siempre a la versión vigente de cada caso |
| ⚠️ | **A tener en cuenta** | depende de un servicio externo y no hay caché — cada run llama al modelo evaluado y al juez de nuevo (~0,02 USD) |

## Cómo lanzarlo

| Requisito | Detalle |
|---|---|
| venv del repo | `uv sync` en la raíz |
| API key del modelo | `API_KEY_OPENAI` en el `.env` de la raíz |
| Credenciales Langfuse | `API_KEY_PUBLIC_LANGFUSE` / `API_KEY_PRIVATE_LANGFUSE` / `BASE_URL_LANGFUSE` en el `.env` |

Desde cualquier sitio del repo:

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
esperado en `rubrica-ok` y `contains` es `prueba-fallo` (ver
[Canarios](#canarios)). `reglas-globales` puede tener algún rojo suelto: ese
juez es flaky (por eso sus llamadas quedan trazadas — se puede auditar su
razonamiento en la UI).

### Dónde ver los resultados

En [cloud.langfuse.com](https://cloud.langfuse.com), dentro del proyecto:

| Vista | Qué se ve |
|---|---|
| **Experiments** | lista de runs con la media de cada score por columna (`Ø contains`, `Ø reglas-globales`…). Como los scores son 0/1, cualquier media < 1 significa que algún caso falló |
| Clic en un run | tabla con una fila por caso y sus scores individuales; los fallos se ven como ceros |
| Clic en una fila | la **traza** del caso, con la llamada real al modelo y el comentario del juez explicando cada score |
| **Datasets → mail-agent-cases → Runs** | el mismo histórico, entrando por el dataset |

## Cómo funciona

### Estructura

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

### Qué hace un run (`eval_mail_agent.py`)

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
| `rubrica-ok` | juez LLM | la rúbrica específica del caso; en los canarios se invierte (ver [Canarios](#canarios)) |

4. **Score agregado del run**: `media-rubrica-ok` (media de `rubrica-ok`, se ve
   en la columna de la lista de experimentos).

### Los casos (`cases.py`)

6 casos, formato item de dataset de Langfuse (`id` estable + `input` +
`expected_output` + `metadata` con los checks y la rúbrica):

| Caso | Tipo | Escenario |
|---|---|---|
| `billing-cobro` | normal | Facturación — duda sobre un cobro |
| `complaint-baja` | normal | Queja — cliente enfadado que amenaza con darse de baja |
| `home-coverages` | normal | Coberturas de hogar — pregunta qué cubre la póliza |
| `generic-english` | normal | Genérico — email en inglés (debe responder en el mismo idioma) |
| `canario-inventar` | 🐤 canario | la rúbrica exige inventar datos (ver [Canarios](#canarios)) |
| `prueba-fallo` | 💥 fallo real | diseñado para fallar de verdad (ver [Canarios](#canarios)) |

Los cuatro casos normales deben salir todo en verde.

### Los dos modelos: evaluado y juez

| Rol | Modelo | Dónde se configura | Qué hace |
|---|---|---|---|
| **Evaluado** | `gpt-5.6-terra` | `deepeval/suites/mail_agent/agent.py` | hace de agente: recibe el email y redacta la respuesta. Es a quien se examina |
| **Juez** | `gpt-4.1-mini` | `eval_mail_agent.py` | puntúa `reglas-globales` y `rubrica-ok` leyendo la respuesta del evaluado |

Mismo juez que en las otras suites: modelo pequeño y distinto a propósito
(calificar es más fácil que redactar, es barato, y un modelo no debe
calificarse a sí mismo). Responde JSON estricto `{reason, passed}` con `reason`
ANTES que `passed` para que razone antes del veredicto, y su system prompt
incluye reglas de interpretación contra falsos suspensos (p. ej. tutear al
cliente NO incumple el "nosotros").

## Ejemplos

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

## Canarios

| Caso | Diseño | Interpretación |
|---|---|---|
| `canario-inventar` | **CANARIO** (`expect_fail: True`): su rúbrica exige inventar datos, cosa que el prompt prohíbe. El veredicto del juez se **invierte**: que suspenda es lo correcto (`rubrica-ok = 1`) | si algún día el juez la aprueba, el modelo está inventando datos — problema real, no lo "arregles" |
| `prueba-fallo` | caso diseñado para **fallar de verdad** (`expect_fail: False`): su rúbrica y su `contains` exigen un código promocional (`VERANO25`) que el agente no conoce ni puede inventar | sirve para ver cómo pinta un rojo en la UI. Es el que baja `media-rubrica-ok` a 0.833; bórralo cuando ya no haga falta |

## Notas y referencias

### Tooling para trabajar con Langfuse desde Claude Code (opcional)

Nada de esto lo necesita el eval para funcionar, pero facilita mucho trabajar
con él desde un agente (consultar runs, depurar scores, leer docs al día):

- **Skill oficial de Langfuse** — guía al agente para usar la CLI
  (`langfuse-cli`) y la documentación actualizada. Se instala con:

  ```bash
  npx skills add langfuse/skills --skill "langfuse"
  ```

  Queda en `.claude/skills/` y `.agents/skills/`, con el pin de versión en
  `skills-lock.json`.

- **Servidor MCP de Langfuse** — expone el proyecto como herramientas
  (datasets, experimentos, scores, prompts...), así el agente puede responder
  directamente cosas como "¿qué casos fallaron en el último run y por qué?".
  Auth básica con las claves del proyecto:

  ```bash
  echo -n "pk-lf-...:sk-lf-..." | base64   # public:secret del proyecto
  claude mcp add --transport http langfuse https://cloud.langfuse.com/api/public/mcp \
      --header "Authorization: Basic <token-base64>"
  ```

  (Si el proyecto está en la región US, la URL es
  `https://us.cloud.langfuse.com/api/public/mcp`.)

### Notas

- Los warnings `Propagated attribute ... rubric ... over 200 characters.
  Dropping value` al ejecutar son inofensivos: Langfuse trunca la rúbrica como
  atributo propagado de la traza, pero la rúbrica llega entera al juez.
- Las trazas del eval van marcadas con environment `development`
  (`LANGFUSE_TRACING_ENVIRONMENT` en `agent.py`): no ensucian dashboards de
  producción.

| Recurso | Dónde |
|---|---|
| Web de Langfuse | <https://langfuse.com/> |
| Documentación | <https://langfuse.com/docs> |
