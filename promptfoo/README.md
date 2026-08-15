# Evaluación de agentes de IA con PromptFoo

Laboratorio para **evaluar la calidad y corrección de las respuestas de los agentes de IA**
usando [PromptFoo](https://www.promptfoo.dev/), un framework open-source de testing para LLMs.

## ¿Cómo funciona PromptFoo?

Todo gira alrededor de `promptfooconfig.yaml`, que combina 3 piezas:

```
prompts (los agentes)  ×  providers (los modelos)  ×  tests (entradas + aserciones)
```

Por cada combinación, PromptFoo genera la respuesta y la valida con **aserciones**:

| Tipo | Categoría | Qué verifica | Coste |
|---|---|---|---|
| `contains` / `icontains` | Determinista | La salida contiene un texto | Gratis, instantáneo |
| `regex` | Determinista | La salida cumple un patrón | Gratis, instantáneo |
| `equals`, `is-json`, `javascript` | Determinista | Igualdad exacta, JSON válido, lógica custom | Gratis |
| `factuality` | Model-graded | La salida es coherente con una respuesta de referencia | 1 llamada al LLM juez |
| `llm-rubric` | Model-graded | La salida cumple una rúbrica escrita en lenguaje natural | 1 llamada al LLM juez |
| `answer-relevance` | Model-graded | La salida responde realmente a la pregunta | 1 llamada al LLM juez |
| `similar` | Embeddings | Similitud semántica con un texto esperado | 1 llamada de embeddings |

> **Regla práctica:** usa aserciones deterministas siempre que puedas (gratis e instantáneas)
> y reserva `llm-rubric` para criterios genuinamente subjetivos (tono, claridad, no inventar).

Las aserciones *model-graded* usan un **LLM como juez**. En este lab el juez está configurado
como `claude-opus-5` (vía `defaultTest.options.provider`), así solo necesitas una API key
de Anthropic.

## Estructura

```
promptfoo/
├── promptfooconfig.yaml        # Configuración: agentes × modelos × tests
├── prompts/
│   ├── agente_soporte.json     # Agente 1: soporte técnico (system + user)
│   └── agente_conocimiento.json# Agente 2: conocimiento general
├── providers/
│   └── mi_agente.py            # Ejemplo: conectar un agente Python propio
└── package.json                # promptfoo 0.120.0 fijado (compatible con Node 22.14)
```

Cada "agente" se define como un prompt en formato chat con su system prompt.
Los tests cubren 5 dimensiones de calidad:

1. **Corrección factual** — `icontains` + `factuality` contra una referencia.
2. **Exactitud de cálculo** — `regex` determinista.
3. **Calidad de explicación** — `llm-rubric` con umbral + `answer-relevance`.
4. **Honestidad** — que el agente NO invente datos que no conoce.
5. **Seguridad** — resistencia a prompt injection básico.

## Uso

```bash
cd promptfoo
npm install                    # instala promptfoo 0.120.0 (con fix postinstall)

export ANTHROPIC_API_KEY=sk-ant-...   # necesaria para generar Y para el juez

npm run eval                   # ejecuta todos los tests
npm run view                   # abre el visor web con la matriz de resultados
```

El visor web (`promptfoo view`) muestra una matriz agente × test con ✅/❌ por aserción,
la respuesta completa, el razonamiento del juez y el coste/latencia de cada llamada.

Otros comandos útiles:

```bash
npx promptfoo validate                 # valida el YAML sin ejecutar
npx promptfoo eval --filter-description "factual"   # ejecutar un subconjunto
npx promptfoo eval -o resultados.json  # exportar resultados (para CI)
```

## Evaluar un agente propio (no solo un modelo)

Si tu agente es código (herramientas, RAG, varios pasos), envuélvelo en un
**provider Python**: PromptFoo llama a `call_api(prompt, options, context)` y evalúa
lo que devuelvas en `output`. Hay un ejemplo listo en [`providers/mi_agente.py`](providers/mi_agente.py):

```yaml
providers:
  - id: file://providers/mi_agente.py
    label: mi-agente
```

Requiere `pip install anthropic`.

## Notas del entorno

- **Versión fijada a `promptfoo@0.120.0`**: la última (0.122.x) exige Node ≥ 22.22
  y este entorno tiene Node 22.14. Si actualizas Node, puedes subir de versión.
- La 0.120.0 tiene un bug de empaquetado (busca las migraciones en `drizzle/` pero
  vienen en `dist/drizzle/`); el script `postinstall` del `package.json` crea el
  symlink que lo corrige automáticamente.
- El aviso `Using unknown Anthropic model: claude-opus-5` es inofensivo: la lista
  interna de modelos de la 0.120.0 es anterior a ese modelo, pero la llamada a la
  API funciona igual.
