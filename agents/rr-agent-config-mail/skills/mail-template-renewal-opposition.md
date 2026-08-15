---
name: mail-template-renewal-opposition
description: "Plantilla para emails que quieren OPONERSE A LA PRÓRROGA de la póliza de OTRA compañía (la aseguradora anterior/saliente), típicamente al cambiarse a RenzoSeguros: evitar que ese seguro se renueve a su vencimiento mediante el Formulario de Oposición a Prórroga de la app/web de RenzoSeguros, con al menos 30 días de antelación. Señales: 'oposición a prórroga', 'no renovar mi antiguo seguro', 'dar de baja mi otra aseguradora a vencimiento', 'me cambio a RenzoSeguros y quiero cancelar el anterior'. No es para cancelar ni dejar de renovar la póliza DE RenzoSeguros (eso es `mail-template-policy-cancellation`) ni para la saliente ya FUERA de plazo, a menos de 30 días (eso es `mail-template-article-22`)."
---
## Oposición a prórroga de la aseguradora saliente

### Qué hace esta skill

Decide si el correo quiere oponerse a la prórroga de la póliza de OTRA compañía (la aseguradora anterior/saliente, típicamente al cambiarse a RenzoSeguros) y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente cumplimenta el Formulario de Oposición a Prórroga desde la app o web de RenzoSeguros, con al menos 30 días de antelación al vencimiento de esa póliza saliente.

### Definiciones del dominio (imprescindibles para clasificar bien)

- OPOSICIÓN A PRÓRROGA = comunicar a la aseguradora SALIENTE (otra compañía, no RenzoSeguros) que NO se quiere renovar esa póliza a su vencimiento, para evitar la prórroga automática. Surte efecto en la próxima renovación de la póliza saliente, no de inmediato.
- Se tramita con el FORMULARIO DE OPOSICIÓN A PRÓRROGA de la app/web de RenzoSeguros (sección CONTRATOS), con al menos 30 días de antelación a la fecha de renovación de la póliza saliente. El formulario está en RenzoSeguros, pero la póliza que se da de baja es la de la otra compañía.
- Difiere de la cancelación de RenzoSeguros: cancelar (`mail-template-policy-cancellation`) da de baja YA la póliza DE RenzoSeguros en vigor; la oposición a prórroga afecta a la póliza de la OTRA aseguradora y solo evita su siguiente renovación.
- Si ya quedan MENOS de 30 días para la renovación de la saliente, la gestión estándar no llega a plazo: eso es `mail-template-article-22`.

La clasificación solo tiene que responder: ¿el cliente quiere que la póliza de su OTRA aseguradora NO se renueve al vencimiento?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿De qué póliza habla? Si es la póliza DE RenzoSeguros (cancelarla, darla de baja, no renovarla) → NO APLICA (`mail-template-policy-cancellation`). Esta skill es SOLO para la póliza de otra compañía.
3. ¿Quiere evitar la renovación de su aseguradora anterior/saliente (no una baja inmediata de RenzoSeguros)? → APLICA, redacta con la plantilla.
4. ¿Está ya fuera de plazo con la saliente (menos de 30 días para su renovación, "no llego", "no me dejan cancelar")? → NO APLICA (`mail-template-article-22`).
5. Otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
6. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → OPOSICIÓN A PRÓRROGA (saliente): "oposición a prórroga", "no renovar mi antiguo seguro", "que no se me renueve el seguro que tenía", "dar de baja mi otra aseguradora a vencimiento", "me acabo de pasar a RenzoSeguros y quiero cancelar el anterior", menciones a otra compañía (Mapfre, Mutua, AXA, Línea Directa, "mi aseguradora de antes"...).
- Señales que apuntan a CANCELACIÓN DE RenzoSeguros (no aquí): "cancelar mi póliza de RenzoSeguros", "darme de baja de RenzoSeguros", "anular la póliza" refiriéndose a la de RenzoSeguros, "no quiero renovar con vosotros".
- Señales que apuntan a ARTÍCULO 22 (no aquí): "estoy fuera de plazo", "no llego a los 30 días", "me renueva ya la otra", "no me dejan cancelar la anterior".

### Qué SÍ dispara la plantilla

- "Me he cambiado a RenzoSeguros, ¿cómo doy de baja mi seguro anterior?"
- "¿Cómo hago la oposición a prórroga de mi antigua aseguradora?"
- "No quiero que se me renueve la póliza que tenía con la otra compañía."
- "Quiero evitar la renovación automática de mi seguro de Mapfre ahora que estoy con vosotros."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Cancelar, dar de baja o no renovar la póliza DE RenzoSeguros (eso es `mail-template-policy-cancellation`).
- Cancelar la saliente estando ya fuera de plazo, a menos de 30 días de su renovación (eso es `mail-template-article-22`).
- Consultas de coberturas, capital, datos, pago, contratación o siniestros.
- Dudas de precio/presupuesto (interés comercial).

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, incluidos los plazos (30 días de antelación; los 7 días para contactar con la aseguradora saliente).
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Tendrías que seguir estos pasos:
1. Accede a la app de RenzoSeguros o vía web a www.renzoseguros.com sección MI CUENTA
2. Introduce teléfono móvil asociado a la póliza y código facilitado posteriormente por SMS
3. Dirígete a la pantalla de Bienvenida
4. Accede a la póliza ya contratada
5. Dentro de los parámetros de póliza, en la sección de CONTRATOS, accede a FORMULARIO DE OPOSICIÓN A PRÓRROGA.
6. Tendrás que cumplimentar todos los datos requeridos en el formulario, con al menos 30 días de antelación respecto a la fecha de renovación de la póliza a cancelar.
7. Una vez cumplimentado correctamente, recibirás mail con copia de la Oposición a Prorroga enviada.
8. Si tras 7 días desde que se envió no recibes notificación de la aseguradora saliente confirmando la baja a vencimiento, recomendamos contactes con ellos para que te confirmen la baja.
```

### Ejemplos y casos límite

- "Quiero daros la oposición a prórroga porque no quiero seguir con RenzoSeguros el año que viene" → NO APLICA aquí: habla de la póliza DE RenzoSeguros, no de la saliente. Ruta a `mail-template-policy-cancellation`; si el procedimiento exacto de no-renovación de RenzoSeguros no encaja allí, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.
- "Acabo de contratar con vosotros y mi seguro antiguo se renueva en 3 semanas" → fuera de plazo (menos de 30 días): `mail-template-article-22`.
- "Quiero cancelar mi seguro" o "no quiero prorrogar mi póliza" sin decir de qué compañía → no asumas que es la saliente: mira el contexto (¿es cliente de RenzoSeguros?, ¿menciona cambio de compañía?); si sigue ambiguo, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

