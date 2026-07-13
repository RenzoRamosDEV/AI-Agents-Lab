---
name: mail-template-electrical-damage
description: "Plantilla INFORMATIVA para emails que preguntan por la cobertura de DAÑOS ELÉCTRICOS: aclara que RenzoSeguros NO la ofrece entre sus coberturas disponibles. Señales: 'daños eléctricos'/'sobretensión'/'se me han estropeado los electrodomésticos por la luz'/'subida de tensión'/'¿cubrís los daños eléctricos?'. No es para consultar el resto de coberturas disponibles (eso es `mail-template-home-coverages`) ni para dar parte de otro siniestro."
---
## Daños eléctricos en RenzoSeguros

### Qué hace esta skill

Decide si el correo pregunta si RenzoSeguros cubre los daños eléctricos y, si es así, redacta la respuesta con la plantilla oficial: informa de que esa cobertura NO está incluida entre las disponibles con RenzoSeguros. Es informativa: aclara la no cobertura, no ejecuta ni tramita nada.

### Definiciones del dominio (imprescindibles para clasificar bien)

- DAÑOS ELÉCTRICOS = daños en aparatos/instalaciones por causas eléctricas (sobretensión, subida de tensión, cortocircuito). Esta cobertura NO forma parte del haber de coberturas disponibles con RenzoSeguros.

La clasificación solo tiene que responder: ¿el cliente pregunta por la cobertura de daños eléctricos?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Pregunta si están cubiertos los daños eléctricos / por sobretensión?
3. Decide: pregunta por daños eléctricos → APLICA, redacta con la plantilla; pregunta por otras coberturas disponibles → NO APLICA (`mail-template-home-coverages`); quiere dar parte de otro siniestro → NO APLICA (`mail-template-claim-report`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → DAÑOS ELÉCTRICOS: "daños eléctricos", "sobretensión", "subida de tensión", "cortocircuito", "se me han estropeado los electrodomésticos por la luz", "un rayo me ha fundido aparatos".
- Señales que apuntan a OTRAS skills: preguntar por el conjunto de coberturas (`home-coverages`); un daño de otra naturaleza para dar parte (`claim-report`).

### Qué SÍ dispara la plantilla

- "¿Cubrís los daños eléctricos?"
- "Se me han estropeado los electrodomésticos por una subida de tensión, ¿está cubierto?"
- "¿Tenéis cobertura de sobretensión?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Consultar el resto de coberturas disponibles (eso es `mail-template-home-coverages`).
- Dar parte de un siniestro de otra naturaleza (eso es `mail-template-claim-report`).
- Gestiones administrativas: datos, pago, capital, cancelación, contratación.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
La cobertura de Daños eléctricos no estaría incluida en el haber de coberturas disponibles con RenzoSeguros.
```

