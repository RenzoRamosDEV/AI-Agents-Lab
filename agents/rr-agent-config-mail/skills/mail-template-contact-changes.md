---
name: mail-template-contact-changes
description: "Plantilla para emails que piden MODIFICAR TELÉFONO Y/O EMAIL de contacto de una póliza. Señales: verbos de cambio (actualizar/cambiar/modificar) sobre 'teléfono'/'móvil'/'número de contacto'/'email'/'correo'/'datos de contacto'. No es para cambios de domicilio, IBAN/forma de pago, capital asegurado (continente/contenido) u otras gestiones sobre la póliza."
---
## Cambio de datos de contacto (teléfono / email) en póliza RenzoSeguros

### Qué hace esta skill

Decide si un email pide actualizar el teléfono y/o el email de contacto de una póliza de RenzoSeguros y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente lo hace desde su perfil o desde la póliza, sin intervención de un agente.

### Definiciones del dominio (imprescindibles para clasificar bien)

- TELÉFONO = el número de contacto vinculado a la póliza (móvil o fijo).
- EMAIL = el correo electrónico de contacto de la póliza.

La plantilla cubre ambos a la vez, así que la clasificación solo tiene que responder: ¿el cliente quiere cambiar su teléfono y/o su email de contacto?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Hay intención de MODIFICAR el teléfono y/o el email de contacto? Una pregunta informativa ("¿qué teléfono tenéis registrado?") no es intención de modificar.
3. Decide: intención de cambiar teléfono y/o email → APLICA, redacta con la plantilla; cualquier otro dato o gestión (domicilio, IBAN, capital...) → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → TELÉFONO: teléfono, móvil, número, número de contacto, celular.
- → EMAIL: email, correo, correo electrónico, e-mail, dirección de correo.
- Términos genéricos: "datos de contacto", "mis datos" → si no especifica, la plantilla cubre ambos igualmente.

### Qué SÍ dispara la plantilla

- "Quiero cambiar mi número de teléfono."
- "Necesito actualizar el email de contacto de mi póliza."
- "¿Cómo modifico mi teléfono y correo?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Cambios de domicilio, IBAN/forma de pago, capital asegurado (continente/contenido) u otras gestiones de la póliza.
- Preguntas puramente informativas sin intención de cambio.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Si deseas modificar teléfono y/o mail, puedes acceder a tu perfil y ahí en "Configuración" puedes proceder a modificar el teléfono e email o bien puedes realizarlo accediendo a la póliza en "Editar póliza".
```

