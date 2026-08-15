---
name: mail-template-legal-assistance
description: "Plantilla para emails que quieren SOLICITAR el servicio de ASISTENCIA / ASESORAMIENTO JURÍDICO de la póliza (se pide de forma análoga a dar un parte de siniestro). Señales: 'quiero asesoramiento jurídico'/'necesito el abogado de la póliza'/'cómo solicito la asistencia jurídica'/'defensa jurídica'. No es para preguntar QUÉ incluye la cobertura jurídica en abstracto (eso es `mail-template-home-coverages`) ni para dar parte de un siniestro material (eso es `mail-template-claim-report`)."
---
## Solicitar asistencia jurídica en RenzoSeguros

### Qué hace esta skill

Decide si el correo quiere solicitar el servicio de asistencia/asesoramiento jurídico de la póliza y, si es así, redacta la respuesta con la plantilla oficial: se solicita de forma análoga a dar un parte, desde app o web, seleccionando la incidencia OTROS y detallando el motivo.

### Definiciones del dominio (imprescindibles para clasificar bien)

- ASISTENCIA / ASESORAMIENTO JURÍDICO = servicio de defensa jurídica y reclamación de daños incluido en la póliza. Se SOLICITA de forma análoga a dar un parte de siniestro (botón DAR PARTE), no es una consulta de qué cubre.
- Se abre desde app o web con DAR PARTE → DAR PARTE CON ASISTENCIA O INDEMNIZACIÓN → tipo de incidencia OTROS, detallando la solicitud y adjuntando prueba.

La clasificación solo tiene que responder: ¿el cliente quiere solicitar/activar el servicio de asistencia jurídica?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Quiere solicitar/activar la asistencia jurídica o pregunta cómo hacerlo?
3. Decide: quiere solicitarla / cómo pedirla → APLICA, redacta con la plantilla; solo pregunta QUÉ incluye la cobertura jurídica en abstracto → NO APLICA (`mail-template-home-coverages`); es un siniestro material (agua, robo...) → NO APLICA (`mail-template-claim-report`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → ASISTENCIA JURÍDICA: "asesoramiento jurídico", "asistencia jurídica", "el abogado de la póliza", "defensa jurídica", "reclamación de daños", "quiero que me asesore un abogado", "cómo solicito la ayuda legal de mi seguro".
- Señales que apuntan a OTRAS skills: "¿qué incluye la asistencia jurídica?" en abstracto (`home-coverages`); un daño material como agua/robo/incendio (`claim-report`).

### Qué SÍ dispara la plantilla

- "Quiero solicitar el asesoramiento jurídico de mi póliza."
- "¿Cómo pido la asistencia jurídica / el abogado del seguro?"
- "Necesito activar la defensa jurídica para reclamar un daño."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Preguntar QUÉ incluye la cobertura de asistencia jurídica en abstracto (eso es `mail-template-home-coverages`).
- Dar parte de un siniestro material: daños por agua, robo, incendio... (eso es `mail-template-claim-report`).
- Gestiones administrativas: datos, pago, capital, cancelación, contratación.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Para solicitar asesoramiento jurídico debes de solicitarlo de modo análogo a dar un parte de siniestro:

Accede a www.renzoseguros.com MI CUENTA o a la app de RenzoSeguros, a tu espacio personal:

Selecciona la opción DAR PARTE

Selecciona la opción DAR PARTE CON ASISTENCIA O INDEMNIZACION

En el paso donde se debe de indicar el tipo de incidencia selecciona la opción OTROS

Detalla la solicitud de Asistencia Jurídica y el motivo de solicitarla

Adjunta video o fotografía del motivo de la solicitud
```

