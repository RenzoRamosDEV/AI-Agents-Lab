---
name: mail-template-policy-cancellation
description: "Plantilla para emails que piden CANCELAR/DAR DE BAJA la póliza DE RenzoSeguros. Señales: verbos 'cancelar'/'dar de baja'/'anular' sobre la póliza/el seguro de RenzoSeguros; preguntas de cómo cancelar. No es para dar de baja a vencimiento la póliza de OTRA compañía al cambiarse a RenzoSeguros (eso es `mail-template-renewal-opposition`, o `mail-template-article-22` si quedan menos de 30 días), ni para quejas con amenaza de baja como forma de presión (eso es queja/insatisfacción), ni para pedir que RenzoSeguros ejecute la cancelación directamente sin pasar por el autoservicio."
---
## Cancelación de póliza RenzoSeguros

### Qué hace esta skill

Decide si un email pide cancelar/dar de baja una póliza de RenzoSeguros y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente cancela desde app o web, con confirmación por SMS.

### Definiciones del dominio (imprescindibles para clasificar bien)

- CANCELACIÓN / BAJA = dejar sin efecto la póliza DE RenzoSeguros a petición del cliente. El proceso lo completa el propio cliente por app o web y se confirma con un SMS al teléfono vinculado a la póliza.
- Esta skill aplica SOLO a la póliza de RenzoSeguros. Dar de baja a vencimiento la póliza de OTRA compañía (la aseguradora anterior/saliente, típico al cambiarse a RenzoSeguros) es OPOSICIÓN A PRÓRROGA (`mail-template-renewal-opposition`; si quedan menos de 30 días para su renovación, `mail-template-article-22`).

La clasificación solo tiene que responder: ¿el cliente quiere cancelar su póliza DE RenzoSeguros y pide (o necesita) el procedimiento?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿De qué póliza habla? Si es la de OTRA compañía (la anterior/saliente, típico al cambiarse a RenzoSeguros) → NO APLICA (`mail-template-renewal-opposition`, o `mail-template-article-22` si está fuera de plazo).
3. ¿Pide la baja INMEDIATA o la baja A VENCIMIENTO (no renovar, "cuando venza", "oposición a prórroga a RenzoSeguros")? La plantilla cubre SOLO la baja inmediata: si pide no renovar a vencimiento, NO reproduzcas la plantilla — acusa recibo en primera persona del plural, en nombre del equipo (estamos revisándolo y te respondemos por este mismo hilo) y marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.
4. ¿Hay intención real de CANCELAR la póliza de RenzoSeguros y necesidad del procedimiento? Distínguelo de una queja que menciona la baja solo como amenaza/presión.
5. Decide: quiere cancelar y necesita saber cómo → APLICA, redacta con la plantilla; queja con amenaza de baja sin pedir el procedimiento → NO APLICA (`mail-template-complaint`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
6. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → CANCELACIÓN: cancelar, dar de baja, anular, "ya no la necesito", "quiero rescindir", "dejar el seguro" — referidos a la póliza DE RenzoSeguros.
- Señales que apuntan a OPOSICIÓN A PRÓRROGA (no aquí): "mi antiguo seguro", "mi otra aseguradora", "me acabo de pasar a RenzoSeguros y quiero cancelar el anterior", menciones a otra compañía (Mapfre, Mutua, AXA...), "oposición a prórroga" (→ `mail-template-renewal-opposition`; fuera de plazo → `mail-template-article-22`).
- Señales que NO son cancelación real: "como no me lo arregléis me doy de baja" (amenaza dentro de una queja), "¿qué pasa si cancelo?" sin decidirlo (consulta informativa a valorar como caso límite).

### Qué SÍ dispara la plantilla

- "Quiero cancelar mi póliza."
- "¿Cómo doy de baja el seguro?"
- "Ya no la necesito, quiero anularla."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Dar de baja a vencimiento la póliza de OTRA compañía al cambiarse a RenzoSeguros (eso es `mail-template-renewal-opposition`; con menos de 30 días de plazo, `mail-template-article-22`).
- Una queja o insatisfacción que menciona la baja solo como amenaza/presión, sin pedir el procedimiento en sí (eso es `mail-template-complaint`).
- Consultas sobre coberturas, capital, pagos o cualquier otra gestión que no sea cancelar.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE (ambas vías, app y web).
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Puedes cancelar la póliza vía app o web de RenzoSeguros:

A través de la aplicación

1. Accede a tu cuenta a través del número de teléfono vinculado a tu póliza
2. Accede al icono de la CASA en la parte inferior de tu pantalla de Bienvenida.
3. Haces click en tu póliza
4. "Deslizas" hacia abajo
5. Leerás ¿Ya no nos necesitas?
6. Seleccionas CANCELAR LA PÓLIZA
7. Recibirás un SMS para poder confirmar la cancelación de la misma en el teléfono vinculado a la póliza

A través de la WEB

1. Accede a tu cuenta a través del número de teléfono vinculado a tu póliza
2. Haces click en tu póliza
3. "Deslizas" hacia abajo
4. Leerás ¿Ya no nos necesitas?
5. Seleccionas CANCELAR LA PÓLIZA
6. Recibirás un SMS para poder confirmar la cancelación de la misma en el teléfono vinculado a la póliza
```

### Ejemplos y casos límite

- "No quiero renovar mi póliza de RenzoSeguros el año que viene" → habla de la póliza de RenzoSeguros, así que llega aquí, pero la plantilla describe la baja inmediata, no la baja a vencimiento: marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.
- "Quiero cancelar mi seguro de Mapfre ahora que estoy con vosotros" → `mail-template-renewal-opposition` (o `mail-template-article-22` si quedan menos de 30 días).
- "Como no me lo arregléis me doy de baja" → amenaza dentro de una queja: `mail-template-complaint`.

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
