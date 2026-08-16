# Eval del mail_agent con promptfoo

Suite de evaluación del agente de email (`agent/rr-agent-config-mail`): lanza los
tests contra un LLM real y valida que las respuestas cumplen las reglas y
plantillas del agente.

## Cómo lanzarlo

Necesita Node ≥ 22 y las API keys del `.env` de la raíz:

```bash
nvm use 22
npx promptfoo eval --env-file ../.env   # corre los tests
npx promptfoo view                      # UI de resultados en http://localhost:15500
```

Resultado esperado: **4 en verde + 1 en rojo**. El rojo es el CANARIO (ver abajo).
Cada eval deja además sus resultados en `out/latest.json` (carpeta gitignoreada).

## Estructura de `promptfooconfig.yaml`

| Bloque | Qué es |
|---|---|
| `prompts` | lo que se envía al modelo en cada test (mensajes chat) |
| `providers` | el modelo EVALUADO, el que hace de agente de email |
| `defaultTest` | lo común a todos los tests (transform, modelo juez, vars y asserts globales) |
| `tests` | los casos concretos (email entrante + plantilla esperada + asserts propios) |

### `prompts` — lo que recibe el modelo

Apunta a `prompts/mail_agent_prompt.json`: el prompt real del agente (system) +
el email entrante (user), con huecos `{{...}}` que se rellenan con las vars de
cada test. Explicado en detalle en [`prompts/README.md`](prompts/README.md).

### `providers` — el modelo evaluado

Apunta a `providers/openai.yaml`: `gpt-5.6-terra` con el mismo `response_format`
(JSON con campo `answer`) que usa el agente real. Para evaluar otro modelo,
añade otro fichero ahí y cambia la referencia. El juez NO va aquí.

### `defaultTest` — lo común a todos los tests

Cada test hereda todo esto además de lo suyo:

- **`transform`**: el modelo devuelve `{"answer": "..."}`; extrae el texto de
  `answer` para que los asserts evalúen solo la respuesta.
- **Juez** (`options.provider`): `gpt-4.1-mini`, solo para los asserts
  `llm-rubric`. Es un modelo pequeño y distinto del evaluado a propósito:
  calificar es más fácil que redactar, es barato, y un modelo no debe
  calificarse a sí mismo. Al cambiar el evaluado, el corrector sigue siendo el
  mismo — comparable.
- **`vars` comunes**: `today_datetime` (fecha congelada → eval reproducible) y
  `skill_catalog` (el catálogo de plantillas).
- **`assert` globales**: sin `\n` literal + rubric con las reglas transversales
  (mismo idioma, estructura de email, "nosotros", no derivar, no inventar datos).

### `tests` — los casos

Cada caso tiene tres partes:

```yaml
- description: Nombre corto del caso
  vars:
    loaded_skill: file://../agent/.../mail-template-billing.md  # plantilla que debería usar
    message: |                                                  # el email entrante
      De: cliente@gmail.com
      Asunto: Duda con mi recibo

      Hola, me habéis cobrado 42,50 € y no sé por qué.
  assert:
    - type: icontains-any        # determinista: palabras que DEBEN aparecer
      value: [recibo, cobro]
    - type: llm-rubric           # el juez valida estos criterios
      value: |
        1. Saluda al remitente.
        2. NO inventa el motivo del cobro: dice que se revisará.
```

Tipos útiles: `icontains` / `icontains-any` / `icontains-all` (contiene, sin
mayúsculas), `not-contains` (prohibido), `llm-rubric` (criterios juzgados por
LLM). Lista completa: <https://promptfoo.dev/docs/configuration/expected-outputs/>

**El CANARIO**: su assert exige algo que el prompt prohíbe (inventar el desglose
de un recibo), así que rojo = el modelo se comporta bien. Si algún día sale en
verde, el modelo está inventando datos — problema real. No lo "arregles".
