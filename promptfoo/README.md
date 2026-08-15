# Eval del mail_agent con promptfoo

Suite de evaluación del agente de email (`agent/rr-agent-config-mail`): lanza los tests contra un LLM real y valida que las respuestas cumplen las reglas y plantillas del agente.

## Levantar promptfoo y su UI

promptfoo exige Node ≥ 22 y las API keys se leen del `.env` de la raíz del repo:

```bash
nvm use 22
npx promptfoo view    # levanta la UI de resultados en http://localhost:15500
```

La UI muestra cada eval lanzado: una fila por test, la respuesta completa del modelo, y al hacer clic en una celda, qué asserts pasaron/fallaron y el veredicto del juez. Queda monitorizando: los evals nuevos aparecen solos.

## Correr los tests

Desde esta carpeta:

```bash
npx promptfoo eval --env-file ../.env
```

Resultado esperado: **4 en verde + 1 en rojo**. El rojo es el test `CANARIO (debe fallar)`: exige algo que el agente tiene prohibido (inventar el desglose de un recibo), así que rojo = el modelo se comporta bien. Si algún día sale en verde, el modelo está inventando datos — problema real. No lo "arregles".

## Carpeta `prompts/`

Es lo que promptfoo le envía al modelo en cada test. No basta con mandarle el email del cliente: hay que mandarle lo mismo que recibe el agente en producción — sus instrucciones completas y luego el email — porque si no, no estarías evaluando a tu agente sino a un modelo "a pelo".

`mail_agent_prompt.json` son 2 mensajes en formato chat:

1. **`system`**: copia del prompt real del agente (el de LangSmith, `agent/rr-agent-config-mail/prompts/`), con sus reglas y el catálogo de plantillas.
2. **`user`**: el email entrante.

Los huecos `{{...}}` los rellena promptfoo en cada test con los `vars` del YAML: `{{message}}` (el email del caso), `{{skill_catalog}}` y `{{today_datetime}}` (comunes, en `defaultTest`), y `{{loaded_skill}}` — el único añadido respecto al prompt real: el agente de verdad carga la plantilla con la herramienta `load_skill`, pero en el eval no hay herramientas, así que cada test la inyecta ahí directamente (leída del `.md` real del agente).

⚠️ Es una **copia manual**: si cambias el prompt del agente en LangSmith o en el `.md`, actualiza también este JSON — si divergen, estarás evaluando un prompt que ya no usas.

## Carpeta `providers/`

Define contra qué modelo se evalúa. `promptfooconfig.yaml` referencia uno de estos ficheros; para cambiar de proveedor, cambia esa línea.

- `openai.yaml` — el activo: `gpt-5.6-terra` por la API oficial de OpenAI, con el mismo `response_format` (JSON con campo `answer`) que usa el agente real. Key: `API_KEY_OPENAI` en el `.env`.

## Los dos modelos: evaluado y juez

En el eval intervienen dos modelos con papeles distintos:

- **Evaluado** (`gpt-5.6-terra`, en `providers/openai.yaml`): hace de agente de email — recibe el email y redacta la respuesta. Es a quien se examina.
- **Juez** (`gpt-4.1-mini`, en `defaultTest.options.provider` de la config): solo se usa en los asserts `llm-rubric` — lee la respuesta del evaluado y dictamina si cumple los criterios. Los asserts deterministas (`icontains`, etc.) no usan ningún modelo.

Se usa un modelo pequeño y distinto como juez a propósito: calificar contra una lista de criterios es más fácil que redactar (mini basta), es mucho más barato (el juez se llama en cada rubric de cada test), y un modelo no debe calificarse a sí mismo — tiende a ser indulgente con sus propios textos. Además, al cambiar el modelo evaluado en `providers/`, el juez se queda igual: mismo corrector y mismos criterios para poder comparar modelos entre sí.

## Cómo se hace un caso de test

Añade un bloque a la lista `tests:` de `promptfooconfig.yaml` con tres partes:

```yaml
- description: Nombre corto del caso
  vars:
    # 1. La plantilla que el agente debería usar para este email (fichero real del agente)
    loaded_skill: file://../agent/rr-agent-config-mail/skills/mail-template-billing.md
    # 2. El email entrante, con remitente y asunto
    message: |
      De: cliente@gmail.com
      Asunto: Duda con mi recibo

      Hola, me habéis cobrado 42,50 € y no sé por qué.
  assert:
    # 3a. Assert determinista: barato y exacto (palabras/frases que DEBEN aparecer)
    - type: icontains-any
      value: [recibo, cobro]
    # 3b. Assert con juez: gpt-4.1-mini valida la respuesta contra estos criterios
    - type: llm-rubric
      value: |
        1. Saluda al remitente.
        2. Resume el cobro por el que pregunta (42,50 €).
        3. NO inventa el motivo: dice que se revisará y confirmará.
        Suspende si incumple cualquiera.
```

Eso es todo. Además, a cada test se le aplican automáticamente los asserts globales de `defaultTest` (mismo idioma que el email, primera persona del plural, no derivar a otro equipo, no inventar datos, sin `\n` literal) y el `transform` que extrae el texto de `answer` del JSON antes de evaluar.

Tipos de assert útiles: `icontains` / `icontains-any` / `icontains-all` (contiene, ignorando mayúsculas), `not-contains` (prohibido), `llm-rubric` (criterios en lenguaje natural juzgados por LLM). Lista completa: https://promptfoo.dev/docs/configuration/expected-outputs/
