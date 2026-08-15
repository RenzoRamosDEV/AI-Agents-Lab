---
name: mail-template-policy-purchase
description: "Plantilla para CONTRATAR/FINALIZAR el alta a partir de un borrador/presupuesto YA EXISTENTE que el cliente quiere formalizar: cómo revisar el borrador y completar el pago. Señales: 'contratar'/'finalizar'/'activar'/'formalizar' la póliza, dudas de cómo pagar o del cargo de 0 €. NO uses esta si el cliente AÚN NO TIENE presupuesto y quiere calcularlo → `mail-template-quote-request`; ni si solo quiere ver/ajustar el presupuesto sin decidir contratar → `mail-template-quote-access`; ni para modificar una póliza YA contratada."
---
## Contratación de póliza en RenzoSeguros

### Qué hace esta skill

Decide si el correo pide contratar/finalizar la contratación de una póliza de RenzoSeguros (a partir de un borrador o presupuesto ya existente) y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente completa la contratación desde la web, verificando el borrador y los datos de pago.

### Definiciones del dominio (imprescindibles para clasificar bien)

- CONTRATAR = formalizar/activar una póliza a partir de un borrador o presupuesto ya generado, completando la verificación y los datos de pago. El proceso lo completa el propio cliente por web (MI CUENTA).
- Detalle de pago con tarjeta: hay un paso de autorización de un cargo de 0 € — es correcto y esperado; solo asocia la tarjeta a la póliza; la cuota se abona a la fecha de inicio de la póliza.

La clasificación solo tiene que responder: ¿el cliente quiere contratar/finalizar una póliza a partir de un borrador que ya tiene?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Hay intención de CONTRATAR/finalizar el alta de una póliza a partir de un borrador/presupuesto existente? Una petición de precio de quien aún no tiene presupuesto no es esto.
3. Decide: quiere contratar y necesita el procedimiento → APLICA, redacta con la plantilla; pide precio/presupuesto sin tenerlo → NO APLICA (interés comercial); quiere modificar una póliza ya contratada u otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → CONTRATAR: contratar, finalizar la contratación, formalizar, activar la póliza, "quiero dar de alta el seguro", "cómo termino de contratar", "completar el alta".
- Señales de contexto que refuerzan: ya tiene borrador/presupuesto, duda sobre el pago o el cargo de 0 €, duda de dónde pulsar CONTRATAR.
- Señales que NO son contratación: "¿cuánto me costaría?", "quiero un presupuesto" sin tenerlo (interés comercial).

### Qué SÍ dispara la plantilla

- "Quiero contratar la póliza, ¿cómo lo hago?"
- "Tengo el presupuesto/borrador y quiero finalizar la contratación."
- "¿Cómo termino de dar de alta el seguro y pago?"
- "Me pide autorizar un pago de 0 €, ¿es correcto?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Petición de precio/presupuesto de un cliente potencial que aún no lo tiene (interés comercial).
- Modificar una póliza ya contratada (capital, datos de contacto, forma de pago...) → sus flujos correspondientes.
- Cancelación, siniestros, quejas u otras gestiones distintas al alta.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, incluida la explicación del cargo de 0 € con tarjeta.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Para Contratar Poliza sigue estos pasos:

Accede directamente a www.renzoseguros.com MI CUENTA

Introducir teléfono y código SMS que recibirás.

En la pantalla de Bienvenida verás recuadro con tu póliza. Haz click en este.

Verifica los parámetros del borrador (Coberturas, fecha de inicio...)

Selecciona el botón CONTRATAR y finaliza el proceso de introducción de datos de pago (en caso de ser por tarjeta hay un paso que será el de autorizar pago de 0 euros, sería correcto esto, pues se asociaría la tarjeta a la póliza y se abonaría la cuota a fecha de inicio de la póliza)

A modo de verificación de la contratación, recibirás mail con póliza y Condiciones Generales y Especiales de esta.
```

