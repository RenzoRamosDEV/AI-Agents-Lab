---
name: mail-template-article-22
description: "Plantilla para emails sobre CANCELAR LA PÓLIZA DE LA ANTIGUA ASEGURADORA cuando ya se está FUERA DEL PLAZO de preaviso (mínimo 30 días naturales por ley): explica que no llega el plazo y explora si aún puede darse de baja por el artículo 22 de la Ley de Contrato de Seguro (subida de precio sin preaviso suficiente). Señales: cambio desde otra aseguradora, mención de plazo/preaviso agotado, 'no me deja cancelar la otra', renovación inminente de la póliza saliente. No es para cancelar la propia póliza de RenzoSeguros (eso es `mail-template-policy-cancellation`) ni para la saliente DENTRO de plazo (eso es `mail-template-renewal-opposition`)."
---
## Artículo 22 — Fuera de plazo con la aseguradora saliente

### Qué hace esta skill

Decide si el correo trata de cancelar la póliza de la ANTIGUA aseguradora (típicamente al cambiarse a RenzoSeguros) estando ya fuera del plazo legal de preaviso y, si es así, redacta la respuesta con la plantilla oficial: informa de que no se llega al plazo y plantea las preguntas del artículo 22 LCS para ver si aún puede darse de baja.

### Definiciones del dominio (imprescindibles para clasificar bien)

- PREAVISO LEGAL = plazo mínimo de 30 días naturales que hay que dar a la aseguradora saliente para oponerse a la prórroga/cancelar a vencimiento. Fuera de ese plazo, la gestión estándar de cancelación no se puede realizar.
- ARTÍCULO 22 LCS = vía excepcional: si la aseguradora saliente subió el precio con menos de dos meses de preaviso y no avisó, habría incumplido la ley (salvo pacto en contrario) y el cliente podría darse de baja amparándose en el art. 22 de la Ley de Contrato de Seguro.
- Se refiere a la póliza de OTRA aseguradora (la saliente), no a la de RenzoSeguros.

La clasificación solo tiene que responder: ¿el cliente quiere cancelar su aseguradora anterior pero está fuera del plazo de preaviso?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Se trata de cancelar la póliza de la aseguradora anterior estando fuera de plazo (renovación inminente, "no llego a los 30 días", "no me deja cancelar la otra")?
3. Decide: cancelación de la saliente fuera de plazo → APLICA, redacta con la plantilla (informa del plazo + preguntas del art. 22); cancelar la propia póliza de RenzoSeguros → NO APLICA (`mail-template-policy-cancellation`); no renovar a vencimiento dentro de plazo → NO APLICA (`mail-template-renewal-opposition`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → ARTÍCULO 22 / FUERA DE PLAZO: "cancelar mi seguro anterior", "darme de baja de la otra aseguradora", "estoy fuera de plazo", "no llego a los 30 días", "me renueva ya la otra", "no me dejan cancelar", "me han subido el precio y no me avisaron".
- Señales que apuntan a OTRAS skills: cancelar la póliza de RenzoSeguros en vigor (`mail-template-policy-cancellation`); no renovar a vencimiento la póliza de la saliente con plazo suficiente (`mail-template-renewal-opposition`).

### Qué SÍ dispara la plantilla

- "Quiero cambiarme a RenzoSeguros pero no llego a cancelar mi seguro anterior a tiempo."
- "Mi antigua aseguradora me renueva ya y estoy fuera de plazo, ¿puedo hacer algo?"
- "Me han subido el precio del seguro anterior y no me avisaron, ¿puedo darme de baja?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Cancelar la propia póliza de RenzoSeguros en vigor (eso es `mail-template-policy-cancellation`).
- Oponerse a la prórroga a vencimiento con plazo suficiente (eso es `mail-template-renewal-opposition`).
- Consultas de coberturas, capital, datos, pago, contratación o siniestros.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, incluidas las preguntas del art. 22.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
El plazo legal de preaviso que se tiene que dar a la antigua aseguradora por ley es de, como mínimo, de 30 días naturales, por lo que estamos fuera de plazo para realizar la gestión de cancelación de tu póliza de tu aseguradora actual.

Sin embargo, nos gustaría hacerte algunas preguntas a ver si pudieses pelearlo: ¿Han subido el precio de tu seguro? Si es así, ¿te han avisado de la subida?, ¿con qué plazo? Si te lo han subido con menos de dos meses de preaviso y no te han avisado han incumplido la ley vigente (salvo pacto personal en contrario) y con la norma en la mano podrías darte de baja, en virtud del artículo 22 de la Ley de Contrato de Seguro.
```

### Ejemplos y casos límite

- "Mi antigua aseguradora me renueva en dos semanas, ¿puedo hacer algo?" → fuera de plazo: APLICA.
- "Mi antiguo seguro vence dentro de tres meses, ¿cómo lo doy de baja?" → dentro de plazo: `mail-template-renewal-opposition`.
- "Quiero cancelar ya mi póliza de RenzoSeguros" → `mail-template-policy-cancellation`.

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
