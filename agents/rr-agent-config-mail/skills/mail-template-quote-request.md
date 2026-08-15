---
name: mail-template-quote-request
description: "Plantilla para CALCULAR UN PRESUPUESTO NUEVO desde cero, cuando el cliente AÚN NO TIENE presupuesto: cómo calcular el precio en app/web con 'Calcula tu precio en 1 min'. Señales: 'quiero un presupuesto'/'cuánto me costaría'/'calcular precio'/'cotización', sin tener aún ninguno. NO uses esta si el cliente YA TIENE un presupuesto y quiere verlo/ajustarlo → `mail-template-quote-access`; ni si ya revisó el borrador y quiere CONTRATAR → `mail-template-policy-purchase`."
---
## Obtener un presupuesto en RenzoSeguros

### Qué hace esta skill

Decide si el correo quiere obtener/calcular un presupuesto nuevo de RenzoSeguros (cotizar desde cero) y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente calcula su precio desde app o web siguiendo unos pasos, sin introducir datos bancarios si solo quiere el presupuesto.

### Definiciones del dominio (imprescindibles para clasificar bien)

- PRESUPUESTO / COTIZACIÓN NUEVA = calcular el precio desde cero con "Calcula tu precio en 1 min", rellenando los datos requeridos hasta obtener el presupuesto final ("LO QUIERO").
- Difiere de acceder a un presupuesto ya generado (`mail-template-quote-access`) y de finalizar la contratación de un borrador existente (`mail-template-policy-purchase`).

La clasificación solo tiene que responder: ¿el cliente quiere calcular/obtener un presupuesto que aún no tiene?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Quiere obtener/calcular un presupuesto nuevo (aún no tiene uno)?
3. Decide: quiere un presupuesto nuevo → APLICA, redacta con la plantilla; ya tiene un presupuesto y quiere acceder/ajustarlo → NO APLICA (`mail-template-quote-access`); ya tiene el borrador y quiere contratar → NO APLICA (`mail-template-policy-purchase`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → PRESUPUESTO NUEVO: "quiero un presupuesto", "cuánto me costaría", "calcular el precio", "una cotización", "precio de un seguro de hogar", "me interesa contratar, ¿cuánto es?".
- Señales que apuntan a OTRAS skills: ya tiene presupuesto y quiere verlo/ajustarlo (`quote-access`); quiere finalizar la contratación de un borrador (`policy-purchase`).

### Qué SÍ dispara la plantilla

- "Quiero un presupuesto para un seguro de hogar."
- "¿Cuánto me costaría aseguraros la casa?"
- "¿Cómo calculo el precio de una póliza?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Acceder a un presupuesto ya generado (eso es `mail-template-quote-access`).
- Finalizar la contratación con un borrador ya revisado (eso es `mail-template-policy-purchase`).
- Gestiones de una póliza ya contratada (capital, datos, pago, cancelación...).

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, incluida la nota de no introducir datos bancarios si solo quiere el presupuesto.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Debes proceder a gestionar la cotización desde la aplicación o la web de RenzoSeguros, solo tienes que seguir unos sencillos pasos:

Accede a la página de www.renzoseguros.com o la aplicación de la misma

Ve a "Calcula tu precio en 1 min"

Rellena todos los campos requeridos
Una vez hayas rellenado todos los datos te saltara un resumen de la póliza, tienes que clickar en "LO QUIERO" y se procederá a darte la cotización/presupuesto final.


 Si únicamente desea obtener el presupuesto, no introduzca datos bancarios ni de tarjeta.
```

