# ¿Qué es `mail_agent_prompt.json`?

Es **lo que se le manda al modelo en cada test**: un guion con huecos.

## Tiene 2 mensajes

1. **`system`** → las instrucciones del agente (copia del prompt real, el de
   `agent/rr-agent-config-mail/prompts/` que espeja el de LangSmith).
2. **`user`** → el email del cliente que hay que contestar.

Primero las normas, luego el trabajo. Así examinamos a **nuestro agente**,
no a un modelo sin instrucciones.

## Los huecos `{{...}}`

Promptfoo los rellena en cada test con las `vars` del `promptfooconfig.yaml`:

- `{{today_datetime}}` → la fecha (fija, para que el test sea siempre igual)
- `{{skill_catalog}}` → la lista de plantillas
- `{{message}}` → el email del caso
- `{{loaded_skill}}` → la plantilla ya cargada (en producción el agente la
  carga solo con `load_skill`; en el eval no hay herramientas, así que se la damos hecha)

