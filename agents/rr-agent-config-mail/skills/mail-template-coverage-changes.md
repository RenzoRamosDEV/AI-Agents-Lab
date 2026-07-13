---
name: mail-template-coverage-changes
description: "Plantilla para emails que piden MODIFICAR EL CAPITAL ASEGURADO de una póliza o presupuesto de hogar: subir, bajar, ampliar, reducir o ajustar el valor de reconstrucción de la vivienda (CONTINENTE) o el de las pertenencias (CONTENIDO). Señales: verbos de cambio (subir/ampliar/aumentar/bajar/reducir/modificar/actualizar) sobre 'capital'/'valor asegurado'/'suma asegurada'/'cobertura'; mención de la casa/vivienda/estructura/reconstrucción (continente) o de pertenencias/enseres/muebles/bienes (contenido); asunto con 'continente'/'contenido'/'capital'/'ampliar cobertura'. No es para dudas de precio o presupuesto de un cliente potencial (eso es interés comercial) ni para consultas informativas sin intención de cambiar el capital."
---
## Cambio de continente / contenido en póliza RenzoSeguros

### Qué hace esta skill

Decide si el correo pide modificar el capital de continente y/o contenido de una póliza o presupuesto de hogar de RenzoSeguros y, si es así, redacta la respuesta con la plantilla oficial: autoservicio por app/web dentro de unos tramos, con recálculo de cuota.

### Definiciones del dominio (imprescindibles para clasificar bien)

- CONTINENTE = la vivienda en sí, su estructura, "reconstruir tu casa", valor de reconstrucción del inmueble. Se modifica en tramos de 5.000 €.
- CONTENIDO = las pertenencias del cliente, enseres, muebles, bienes, "tus pertenencias". Se modifica en tramos de 1.000 €.

La plantilla cubre ambos casos a la vez, así que la clasificación solo tiene que responder: ¿el cliente quiere cambiar el capital de continente y/o de contenido?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Hay intención de MODIFICAR un capital? Busca verbos de cambio: subir, aumentar, ampliar, incrementar, bajar, reducir, rebajar, ajustar, cambiar, modificar, actualizar el valor/capital/suma/cobertura. Una pregunta informativa ("¿cuánto tengo asegurado en contenido?") no es intención de modificar.
3. ¿El capital es continente o contenido? Usa el léxico de abajo para mapear el lenguaje del cliente a uno de los dos (o a ambos).
4. Decide: intención de modificar continente y/o contenido → APLICA, redacta con la plantilla; cualquier otro caso → NO APLICA, no uses esta plantilla y deja que el flujo normal / otro agente gestione el correo (no inventes una respuesta).
5. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" de abajo y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"` en lugar de forzar la plantilla.

### Léxico de mapeo

- → CONTINENTE: casa, vivienda, hogar, inmueble, piso, chalet, estructura, paredes, "reconstruir", valor de reconstrucción, "lo que cuesta levantar la casa", obra, edificación, metros construidos.
- → CONTENIDO: pertenencias, enseres, muebles, mobiliario, bienes, electrodomésticos, ropa, objetos, "lo de dentro", ajuar doméstico.
- Términos genéricos (valen para cualquiera de los dos): capital asegurado, suma asegurada, valor asegurado, cobertura, "lo que tengo asegurado". Con un término genérico sin especificar, infiere por el resto del mensaje; si menciona explícitamente ambos, la respuesta aplica igualmente.

### Qué SÍ dispara la plantilla

- "Quiero subir el capital de mi casa / de continente."
- "Necesito ampliar la cobertura de mis pertenencias / del contenido."
- "¿Cómo cambio el valor de reconstrucción de mi vivienda?"
- "Me he comprado muebles nuevos, quiero asegurar más contenido."
- "Quiero bajar/aumentar tanto el continente como el contenido."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Preguntas puramente informativas sin intención de cambio: "¿cuánto tengo asegurado?", "¿qué es el continente?".
- Cambios que no son de estos dos capitales: domicilio, titular, forma de pago, IBAN, datos personales, fechas de efecto, cancelación/baja de la póliza.
- Alta o dudas sobre coberturas distintas al capital de continente/contenido (p. ej. responsabilidad civil, asistencia, robo fuera del hogar).
- Objetos de valor especiales (joyas, obras de arte, relojes, dinero metálico): posible sublímite específico, no encajan sin más en el tramo estándar de contenido → caso límite, marca para revisión salvo que el cliente hable claramente del capital de contenido general.
- Reclamaciones, siniestros, quejas, o correos que no van de la póliza de hogar.

### Redacción de la respuesta

1. Saludo con el nombre del cliente si lo conoces por el correo ("Hola, [Nombre],"); si no, "Hola,".
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE — no cambies el texto, los tramos (5.000 € / 1.000 €), ni la redacción.
3. Cierre breve y natural si encaja (p. ej. "Un saludo, equipo RenzoSeguros"); opcional, no debe contradecir la plantilla.

### Plantilla oficial (reproducir tal cual)

```
Hola,

Accediendo vía app o web de RenzoSeguros (en www.renzoseguros.com > MI CUENTA) a tu póliza o presupuesto puedes modificar tu póliza o presupuesto dentro de parámetros de tu póliza:

- RECONSTRUIR TU CASA (CONTINENTE): Puedes modificar en tramos de 5.000 euros
- TUS PERTENENCIAS (CONTENIDO): Puedes modificar en tramos de 1.000 euros

Cualquier modificación implica recálculo de la cuota resultante. Si tu póliza ya estuviera contratada, para que este cambio se haga efectivo tienes que aceptar la nueva cuota resultante.
```

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
