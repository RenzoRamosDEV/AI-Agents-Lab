---
name: mail-template-review-request
description: "Fragmento OPCIONAL para PEDIR UNA RESEÑA en Trustpilot cuando ya se ha resuelto la consulta del cliente y la interacción ha sido positiva. No es una plantilla de tema: es un añadido breve al final de otra respuesta útil. Señales para usarla: el cliente agradece/queda satisfecho o la consulta se ha resuelto con claridad. No usar si hay queja, insatisfacción, tema legal/fraude o la consulta no ha quedado resuelta."
---
## Pedir reseña (Trustpilot) en RenzoSeguros

### Qué hace esta skill

Aporta un fragmento breve para pedir una reseña positiva en Trustpilot. NO es una respuesta por sí sola ni un tema del email entrante: es un añadido opcional que se acopla al FINAL de una respuesta que ya ha resuelto la consulta del cliente, solo cuando la interacción ha sido claramente positiva.

### Definiciones del dominio (imprescindibles para clasificar bien)

- PETICIÓN DE RESEÑA = invitación cordial a valorar a RenzoSeguros en Trustpilot, mencionando el nombre del agente que ha atendido (placeholder `NOMBRE`).
- Es un CIERRE opcional, no el cuerpo de la respuesta: primero se resuelve lo que pide el cliente con la plantilla que corresponda, y solo después, si procede, se añade este fragmento.

La clasificación solo tiene que responder: ¿procede añadir la petición de reseña a esta respuesta?

### Flujo de decisión

1. Resuelve primero la consulta del cliente con la plantilla de tema que corresponda (facturación, coberturas, cancelación, etc.).
2. ¿La consulta ha quedado resuelta Y la interacción es positiva (agradecimiento, satisfacción, tono cordial)?
3. Decide: resuelta y positiva → AÑADE el fragmento al final de la respuesta; cualquier señal negativa (queja, insatisfacción, enfado), tema legal/fraude, o consulta no resuelta → NO lo añadas.
4. Si hay duda razonable, NO añadas la reseña (mejor omitir que pedirla en mal momento).

### Léxico de mapeo

- → PROCEDE: "gracias", "muchas gracias", "perfecto", "me ha quedado claro", "genial", tono satisfecho, consulta simple resuelta.
- → NO PROCEDE: "reclamación", "queja", "no estoy conforme", enfado, tema legal/fraude, o cuando la respuesta deja algo pendiente/por confirmar.

### Qué SÍ dispara la plantilla

- El cliente agradece o se muestra satisfecho tras resolverle una duda sencilla.
- Una consulta se ha respondido por completo y el tono es cordial.

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Cualquier email con queja, insatisfacción o enfado (`mail-template-complaint`).
- Casos legales/de autoridad o fraude/seguridad.
- Respuestas que dejan algo pendiente o sin resolver.
- Como respuesta única: este fragmento nunca va solo, siempre acompaña a otra respuesta útil.

### Redacción de la respuesta

1. Redacta primero la respuesta a la consulta del cliente con la plantilla de tema correspondiente.
2. Añade al final, en un párrafo aparte, el fragmento oficial de abajo, reproducido LITERALMENTE.
3. Sustituye `NOMBRE` por el nombre del agente que firma la respuesta. Si no hay un nombre real que usar, omite el fragmento (no dejes el literal `NOMBRE` ni inventes uno).

### Plantilla oficial (reproducir tal cual)

```
Si he sido útil, ¿me ayudarías con una reseña positiva aquí?🙏: https://es.trustpilot.com/evaluate/renzoseguros.com
No olvides mencionar mi nombre: NOMBRE
```

