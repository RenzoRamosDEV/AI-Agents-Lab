---
name: mail-template-payment-method
description: "Plantilla para emails que piden CAMBIAR/ACTUALIZAR EL MÉTODO DE PAGO de la póliza: pasar a tarjeta, volver a introducir el IBAN, o corregir los datos de cobro. Señales: 'cambiar método de pago'/'actualizar tarjeta'/'cambiar el IBAN'/'la cuenta del recibo'/'que me cobréis en otra tarjeta'. No es para dudas de importe/cobro concreto (eso es `mail-template-billing`) ni para cambiar el capital, datos de contacto u otras gestiones."
---
## Cambio de método de pago en RenzoSeguros

### Qué hace esta skill

Decide si el correo pide cambiar/actualizar el método de pago de la póliza (tarjeta o IBAN) y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente introduce el nuevo método de pago desde app o web y lo asocia a la vivienda asegurada.

### Definiciones del dominio (imprescindibles para clasificar bien)

- MÉTODO DE PAGO = la forma de cobro de la cuota: tarjeta o IBAN (domiciliación). Se cambia desde MI CUENTA, introduciendo el nuevo método y asociándolo a la vivienda asegurada.
- Detalle con tarjeta: el banco pide autorizar el cobro con una cuantía a 0 €; si hubiese algún cargo pendiente, se cargaría al asociar el método.

La clasificación solo tiene que responder: ¿el cliente quiere cambiar cómo se le cobra la póliza (tarjeta/IBAN)?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Hay intención de CAMBIAR/actualizar el método de pago (tarjeta o IBAN)?
3. Decide: quiere cambiar el método de pago → APLICA, redacta con la plantilla; pregunta por un importe/cobro concreto → NO APLICA (`mail-template-billing`); cambia capital, datos de contacto u otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → MÉTODO DE PAGO: "cambiar método de pago", "actualizar la tarjeta", "pagar con otra tarjeta", "cambiar el IBAN", "cambiar la cuenta del recibo", "domiciliar en otra cuenta", "que me cobréis en...".
- Señales que apuntan a OTRAS skills: dudas de un importe o de un cobro concreto (`billing`); cambio de teléfono/email (`contact-changes`); cambio de capital (`coverage-changes`).

### Qué SÍ dispara la plantilla

- "Quiero cambiar mi método de pago a tarjeta."
- "Necesito actualizar el IBAN de la póliza."
- "Quiero que me cobréis en otra cuenta / tarjeta."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Dudas sobre un importe o un cobro concreto (eso es `mail-template-billing`).
- Cambios de teléfono/email (`mail-template-contact-changes`), de capital (`mail-template-coverage-changes`) u otras gestiones.
- Cancelación, contratación o siniestros.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, incluida la nota del cargo de 0 € con tarjeta y los cargos pendientes.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Tendrías que seguir estos pasos e introducir nuevo método de pago:

1. Accede a la app de RenzoSeguros o vía web a www.renzoseguros.com sección MI CUENTA
2. Introduce teléfono móvil asociado a la póliza y código facilitado posteriormente por SMS
3. Dirígete a la pantalla de Bienvenida
4. Dirígete al icono del hombrecito (si es por app) en la esquina superior izquierda, o bien a tu nombre en la esquina superior derecha (si es por web)
5. Dirígete a MÉTODO DE PAGO (puedes modificar el pago a Tarjeta o volver a introducir el IBAN).
6. Introduce MÉTODO DE PAGO. Una vez introducido, accede a este y selecciona la vivienda asegurada que quieras asociar al método de pago.
6a.- En caso de hacerlo por tarjeta, tendrás que seguir los pasos que te marque cada banco para autorizar el cobro (pondrá cuantía a 0 euros). Si hubiese algún cargo pendiente, se te cargaría
7 - GUARDAR
```

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
