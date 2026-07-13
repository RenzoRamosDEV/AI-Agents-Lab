---
name: mail-template-claim-report
description: "Plantilla para emails que quieren DAR PARTE DE UN SINIESTRO de hogar (abrir/comunicar una incidencia: daños por agua, robo, incendio, etc.) para pedir indemnización o reparación. Señales: 'dar parte'/'abrir siniestro'/'comunicar un daño'/'me ha pasado X en casa'/'quiero reclamar un daño'. No es para consultar QUÉ cubre la póliza (eso es `mail-template-home-coverages`) ni para gestiones administrativas de la póliza."
---
## Dar parte de siniestro — Hogar en RenzoSeguros

### Qué hace esta skill

Decide si el correo quiere dar parte de un siniestro de hogar (comunicar una incidencia para pedir indemnización o reparación) y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente abre el parte desde app o web, selecciona la incidencia, la describe y adjunta pruebas.

### Definiciones del dominio (imprescindibles para clasificar bien)

- SINIESTRO / PARTE = comunicación de un daño o incidencia ya ocurrido (daños por agua, robo, incendio, fenómenos atmosféricos...) para que RenzoSeguros lo tramite. El cliente lo abre él mismo por app o web con el botón DAR PARTE → PEDIR INDEMNIZACIÓN/REPARACIÓN.
- Adjuntos: fotografías y/o vídeos de la incidencia, hasta un máximo de 35 MB.

La clasificación solo tiene que responder: ¿el cliente quiere dar parte de un siniestro ocurrido en su hogar?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Hay un siniestro/incidencia ocurrido y quiere darlo de parte o pregunta cómo hacerlo?
3. Decide: quiere dar parte / cómo abrir el siniestro → APLICA, redacta con la plantilla; solo pregunta QUÉ cubre la póliza en abstracto → NO APLICA (`mail-template-home-coverages`); gestión administrativa (datos, pago, capital, cancelación...) → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → DAR PARTE: dar parte, abrir siniestro, comunicar un daño/incidencia, "quiero reclamar un daño", "me ha pasado X en casa", "cómo pido la reparación/indemnización".
- → TIPO DE INCIDENCIA (para seleccionar en el flujo): daños por agua ("se me ha inundado", "gotera", "tubería"), robo ("me han entrado", "atraco"), incendio/fuego, fenómenos atmosféricos (viento, pedrisco, nieve).
- Señales que NO son dar parte: "¿esto lo cubre mi póliza?" en abstracto (consulta de coberturas), sin un daño concreto que comunicar.

### Qué SÍ dispara la plantilla

- "Se me ha inundado el salón, ¿cómo doy el parte?"
- "Quiero abrir un siniestro por un robo en casa."
- "¿Cómo reclamo la reparación de un daño por agua?"
- "Me ha entrado agua por el tejado, quiero comunicarlo."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Consultar QUÉ cubre la póliza en abstracto, sin un daño concreto (eso es `mail-template-home-coverages`).
- Gestiones administrativas: cambio de datos, pago, capital, cancelación, contratación.
- Dudas de precio/presupuesto (interés comercial).

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, incluido el límite de 35 MB de adjuntos.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Tienen que abrir parte vía app o web de RenzoSeguros (www.renzoseguros.com MI CUENTA):

Seleccionar botón DAR PARTE.

Seleccionar la opción PEDIR INDEMIZACIÓN/REPARACIÓN

En el punto donde pide seleccionar incidencia, selecciona la opción que corresponda (DAÑOS POR AGUA, ROBO...) y describe la incidencia que corresponda.

Adjunta fotografías y/o videos hasta un máximo de 35MB de la incidencia.
```

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
