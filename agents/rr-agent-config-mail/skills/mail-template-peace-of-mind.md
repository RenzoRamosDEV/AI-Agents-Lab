---
name: mail-template-peace-of-mind
description: "Plantilla INFORMATIVA sobre qué incluye el paquete PAZ MENTAL de RenzoSeguros (daños estéticos, vandalismo, cristales/espejos/metacrilatos, vitrocerámica, piedras/mármoles/loza sanitaria). Señales: '¿qué incluye Paz Mental?'/'paquete Paz Mental'/'cobertura de daños estéticos/vandalismo/cristales'. No es para el resto de coberturas generales (eso es `mail-template-home-coverages`), para contratar/añadir el paquete ni para dar parte de un siniestro."
---
## Paz Mental — Coberturas incluidas en RenzoSeguros

### Qué hace esta skill

Decide si el correo pregunta qué incluye el paquete Paz Mental de RenzoSeguros y, si es así, redacta la respuesta con la plantilla oficial: detalla las coberturas del paquete. Es informativa: explica qué incluye, no ejecuta ni tramita nada.

### Definiciones del dominio (imprescindibles para clasificar bien)

- PAZ MENTAL = paquete de coberturas de RenzoSeguros que incluye: daños estéticos en Continente (hasta 2.000 €), actos de vandalismo, cristales/espejos/metacrilatos de Continente y Contenido, rotura de cristal de placa vitrocerámica, y piedras/mármoles/granitos y loza sanitaria.
- Es un paquete concreto, distinto del conjunto de coberturas generales de la póliza (esas se explican en `mail-template-home-coverages`).

La clasificación solo tiene que responder: ¿el cliente pregunta qué incluye el paquete Paz Mental?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Pregunta qué incluye Paz Mental o por una de sus coberturas (daños estéticos, vandalismo, cristales, vitrocerámica, mármoles/loza)?
3. Decide: pregunta por Paz Mental → APLICA, responde con la plantilla; pregunta por las coberturas generales de la póliza → NO APLICA (`mail-template-home-coverages`); quiere contratar/añadir el paquete → NO APLICA (contratación / modificación de póliza); tiene un siniestro que dar de parte → NO APLICA (`mail-template-claim-report`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → PAZ MENTAL: "Paz Mental", "paquete Paz Mental", "cobertura de daños estéticos", "vandalismo", "cristales/espejos/metacrilatos", "vitrocerámica", "encimera rota", "mármol/granito/loza sanitaria".
- Señales que apuntan a OTRAS skills: "¿qué cubre mi seguro?" en general (`home-coverages`); "quiero añadir/contratar Paz Mental" (contratación / modificación); un daño concreto para dar parte (`claim-report`).

### Qué SÍ dispara la plantilla

- "¿Qué incluye el paquete Paz Mental?"
- "¿Paz Mental cubre los daños estéticos / el vandalismo / los cristales?"
- "¿La vitrocerámica entra en Paz Mental?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Consultar las coberturas generales de la póliza (eso es `mail-template-home-coverages`).
- Contratar o añadir el paquete Paz Mental (contratación / modificación de póliza).
- Dar parte de un siniestro (eso es `mail-template-claim-report`).
- Gestiones administrativas: datos, pago, capital, cancelación.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE (incluido el límite de 2.000 € en daños estéticos).
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
El paquete Paz mental incluye:

- Cobertura de daños estéticos hasta 2.000 euros por daños estéticos en Continente
- Cobertura producida por actos de vandalismo
- Cobertura en espejos, cristales y metacrilatos que formen parte de Continente y Contenido
- Cobertura de rotura de cristal de placa vitrocerámica
- Cobertura de piedras, mármoles, granitos y loza sanitaria
```

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
