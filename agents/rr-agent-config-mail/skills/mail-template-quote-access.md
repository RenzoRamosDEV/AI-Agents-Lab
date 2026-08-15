---
name: mail-template-quote-access
description: "Plantilla para ACCEDER A UN PRESUPUESTO QUE YA EXISTE: consultarlo, modificar sus parámetros, descargar el borrador de póliza/condiciones. Señales: 'acceder al presupuesto'/'ver mi presupuesto'/'dónde está mi presupuesto'/'modificar el presupuesto'/'descargar el borrador' (el cliente YA TIENE uno). NO uses esta si el cliente AÚN NO TIENE presupuesto y quiere calcularlo → `mail-template-quote-request`; ni si ya lo revisó y quiere CONTRATAR → `mail-template-policy-purchase`."
---
## Acceder al presupuesto en RenzoSeguros

### Qué hace esta skill

Decide si el correo quiere acceder a un presupuesto ya generado (consultarlo, ajustar parámetros, descargar el borrador o contratarlo) y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente accede al presupuesto desde app o web.

### Definiciones del dominio (imprescindibles para clasificar bien)

- PRESUPUESTO = una cotización ya generada, accesible desde app o web (MI CUENTA). Desde ahí el cliente puede modificar parámetros predefinidos, descargar el borrador de póliza y condiciones, y contratar directamente si lo desea.
- Difiere de pedir un presupuesto nuevo: esta plantilla es para acceder a uno que YA existe, no para cotizar desde cero (eso es interés comercial).

La clasificación solo tiene que responder: ¿el cliente quiere acceder a un presupuesto que ya tiene?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Quiere acceder/consultar/modificar/descargar un presupuesto que YA existe?
3. Decide: quiere acceder a su presupuesto → APLICA, redacta con la plantilla; pide un presupuesto nuevo que no tiene → NO APLICA (interés comercial); ya decidió contratar y solo quiere el paso a paso de contratación → considera `mail-template-policy-purchase`; otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → ACCEDER AL PRESUPUESTO: "acceder al presupuesto", "ver mi presupuesto", "dónde está mi presupuesto", "modificar el presupuesto", "ajustar los parámetros del presupuesto", "descargar el borrador de póliza".
- Señales que NO son esto: "quiero un presupuesto" sin tenerlo (interés comercial); "cómo contrato" cuando ya tiene claro el borrador (`mail-template-policy-purchase`).

### Qué SÍ dispara la plantilla

- "¿Dónde puedo ver mi presupuesto?"
- "Quiero modificar los parámetros de mi presupuesto."
- "¿Cómo descargo el borrador de póliza del presupuesto?"
- "Quiero acceder a mi presupuesto para ajustarlo."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Pedir un presupuesto nuevo que aún no existe (interés comercial).
- Finalizar la contratación con el borrador ya revisado (`mail-template-policy-purchase`).
- Gestiones de una póliza ya contratada (capital, datos, pago, cancelación...).

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Accediendo a dicho presupuesto vía app o web de RenzoSeguros (www.renzoseguros.com MI CUENTA) podrás acceder al presupuesto, modificar parámetros predefinidos para ajustarlos a tus necesidades, descargar borrador de póliza y condiciones y directamente contratar póliza si lo deseas.
```

