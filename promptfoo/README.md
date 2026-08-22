# Eval del mail_agent con promptfoo

## La herramienta

[promptfoo](https://www.promptfoo.dev/) es un evaluador de LLMs declarativo:
toda la suite (modelo evaluado, modelo juez, casos y asserts) se define en un
único YAML y se lanza con `npx`, sin escribir código. Aquí se usa como suite de
evaluación del agente de email (`agent/rr-agent-config-mail`): lanza los tests
contra un LLM real y valida que las respuestas cumplen las reglas y plantillas
del agente.

## Ventajas

|   | Punto | Detalle |
|---|---|---|
| ✅ | **Declarativo** | todo el eval vive en `promptfooconfig.yaml` — casos, asserts y modelos; sin código que mantener |
| ✅ | **UI local de resultados** | `npx promptfoo view`: comparación cómoda de casos, asserts y salidas del modelo |
| ✅ | **Asserts combinables** | checks deterministas (`icontains`, `not-contains`…) y rubrics de juez LLM conviven en el mismo caso |
| ✅ | **Rápido de montar** | es la suite con menos piezas del repo |
| ⚠️ | **A tener en cuenta** | exige Node ≥ 22 y los resultados se quedan en local (sin histórico en la nube) |

## Cómo lanzarlo

| Requisito | Detalle |
|---|---|
| Node ≥ 22 | `nvm use 22` |
| API keys | en el `.env` de la raíz (se pasa con `--env-file ../.env`) |

```bash
nvm use 22
npx promptfoo eval --env-file ../.env   # corre los tests
npx promptfoo view                      # UI de resultados en http://localhost:15500
```

Resultado esperado: **4 en verde + 1 en rojo**. El rojo es el CANARIO (ver
[Canarios](#canarios)). Cada eval deja además sus resultados en
`out/latest.json` (carpeta gitignoreada).

## Cómo funciona

Todo vive en `promptfooconfig.yaml`, con cuatro bloques:

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
- **Juez** (`options.provider`): el modelo que califica los asserts
  `llm-rubric` — ver [Los dos modelos](#los-dos-modelos-evaluado-y-juez).
- **`vars` comunes**: `today_datetime` (fecha congelada → eval reproducible) y
  `skill_catalog` (el catálogo de plantillas).
- **`assert` globales**: sin `\n` literal + rubric con las reglas transversales
  (mismo idioma, estructura de email, "nosotros", no derivar, no inventar datos).

### `tests` — los casos

Cada caso tiene tres partes: la plantilla que el agente debería usar
(`loaded_skill`), el email entrante (`message`) y sus asserts propios (ver el
ejemplo en [Ejemplos](#ejemplos)). La suite tiene 5 casos:

| Caso | Tipo | Escenario |
|---|---|---|
| Facturación | normal | duda sobre un cobro |
| Queja | normal | cliente enfadado que amenaza con darse de baja |
| Coberturas de hogar | normal | pregunta qué cubre la póliza |
| Genérico en inglés | normal | email en inglés — debe responder en el mismo idioma |
| Canario | 🐤 debe fallar | su assert exige inventar datos (ver [Canarios](#canarios)) |

### Los dos modelos: evaluado y juez

| Rol | Modelo | Dónde se configura | Qué hace |
|---|---|---|---|
| **Evaluado** | `gpt-5.6-terra` | `providers/openai.yaml` | hace de agente: recibe el email y redacta la respuesta. Es a quien se examina |
| **Juez** | `gpt-4.1-mini` | `defaultTest.options.provider` | puntúa los asserts `llm-rubric` leyendo la respuesta del evaluado |

Se usa un modelo pequeño y distinto como juez a propósito: calificar es más
fácil que redactar, es barato, y un modelo no debe calificarse a sí mismo. Al
cambiar el evaluado, el corrector sigue siendo el mismo — comparable.

## Ejemplos

Un caso de `tests` con sus tres partes:

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

Tipos de assert útiles:

| Assert | Tipo | Qué valida |
|---|---|---|
| `icontains` / `icontains-any` / `icontains-all` | determinista | contiene el término / al menos uno / todos (ignora mayúsculas) |
| `not-contains` | determinista | términos prohibidos: no deben aparecer |
| `llm-rubric` | juez LLM | criterios en lenguaje natural |

## Canarios

| Caso | Qué exige su assert | Interpretación |
|---|---|---|
| El CANARIO | inventar el desglose de un recibo — cosa que el prompt prohíbe | 🔴 rojo = el modelo se comporta bien · 🟢 verde = está inventando datos — problema real, no lo "arregles" |

## Notas y referencias

| Recurso | Dónde |
|---|---|
| Lista completa de tipos de assert | <https://promptfoo.dev/docs/configuration/expected-outputs/> |
| Detalle del prompt del agente | [`prompts/README.md`](prompts/README.md) |
| Web de promptfoo | <https://www.promptfoo.dev/> |
| Documentación | <https://www.promptfoo.dev/docs/intro> |
