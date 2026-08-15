---
name: mail-template-formal-complaint
description: "Plantilla que explica el PROCEDIMIENTO FORMAL DE RECLAMACIÓN de RenzoSeguros en 3 etapas (equipo responsable por email → formulario de reclamación → Defensor del Asegurado). Úsala cuando el cliente quiere PONER una reclamación formal o pregunta CÓMO reclamar/escalar su caso. Señales: 'quiero poner una reclamación'/'cómo reclamo'/'quiero escalar esto'/'no me han resuelto y quiero reclamar formalmente'/'Defensor del Asegurado'. Distinta de `mail-template-complaint`, que es la respuesta empática a una queja/insatisfacción sin petición de proceso formal."
---
## Procedimiento de reclamación en RenzoSeguros

### Qué hace esta skill

Decide si el cliente quiere poner una reclamación formal o pregunta cómo reclamar/escalar su caso y, si es así, redacta la respuesta con la plantilla oficial: explica el procedimiento en 3 etapas (equipo responsable por email, formulario de reclamación y, finalmente, Defensor del Asegurado).

### Definiciones del dominio (imprescindibles para clasificar bien)

- RECLAMACIÓN FORMAL = el cliente quiere activar/entender el proceso reglado para que su caso se revise, no solo desahogarse. Tiene 3 etapas escalables:
  - Etapa 1: informar al equipo responsable — siniestros a tramitacion@renzoseguros.com; póliza/contrato a contacto@renzoseguros.com.
  - Etapa 2: rellenar el formulario https://reclamacion.renzoseguros.com/ (respuesta en 15 días laborables; el plazo legal es de 2 meses).
  - Etapa 3: escalar al Defensor del Asegurado (entidad legal independiente), solo tras no quedar satisfecho en la etapa anterior.
- Difiere de una queja emocional sin petición de proceso: eso se atiende con empatía (`mail-template-complaint`).

La clasificación solo tiene que responder: ¿el cliente quiere poner una reclamación formal o saber cómo reclamar/escalar?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Pide poner una reclamación formal, cómo reclamar o cómo escalar su caso (menciona reclamación/formulario/Defensor del Asegurado)?
3. Decide: quiere el proceso de reclamación → APLICA, redacta con la plantilla; solo expresa malestar/insatisfacción sin pedir proceso formal → NO APLICA (`mail-template-complaint`); es otra gestión concreta (siniestro, capital, pago...) → NO APLICA, deja que lo gestione su flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → RECLAMACIÓN FORMAL: "quiero poner una reclamación", "cómo reclamo", "reclamación formal", "quiero escalar esto", "hoja de reclamaciones", "Defensor del Asegurado", "no me han resuelto y quiero reclamar".
- Señales que apuntan a `mail-template-complaint`: malestar, enfado o insatisfacción sin pedir proceso ("estoy muy descontento", "esto es un desastre") sin mención de reclamar formalmente.

### Qué SÍ dispara la plantilla

- "Quiero poner una reclamación formal."
- "¿Cómo reclamo si no estoy conforme con la respuesta?"
- "Quiero escalar mi caso, ¿cuáles son los pasos?"
- "Quiero acudir al Defensor del Asegurado."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Malestar/insatisfacción sin petición de proceso formal (eso es `mail-template-complaint`).
- Gestiones concretas: dar parte de siniestro, cambios de póliza, dudas de facturación, etc.
- Consultas informativas generales.

### Redacción de la respuesta

1. Saludo personalizado al remitente, con un reconocimiento breve y empático de la situación.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, con sus 3 etapas, emails, formulario y plazos.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
RenzoSeguros tiene la misión de proteger tu hogar y hacerte la vida más fácil. Sin embargo, a veces las cosas no salen tan bien como habíamos planeado. ¡No te preocupes! Podemos trabajar juntos para encontrar una solución:


Etapa 1

Si tu queja es relativa al departamento de siniestros. Informa al equipo encargado sobre dicha a través de tramitacion@renzoseguros.com

Si tu queja es relativa a tu póliza o la gestión de tu contrato. Informa al equipo encargado a través de contacto@renzoseguros.com

Si estás satisfecho con la respuesta daremos por finalizado aquí el proceso. Si no, pasaríamos al siguiente paso.

Etapa 2

Infórmanos sobre el problema rellenando este formulario: https://reclamacion.renzoseguros.com/

La Ley General de Seguros establece el plazo de respuesta para las reclamaciones en 2 meses, sin embargo, con el fin de poder resolverlo cuanto antes, en RenzoSeguros revisaremos tu caso y te responderemos en un plazo de 15 días laborables.

Recuerda que, si estás en espera de la resolución, por parte de la compañía dentro de los 15 días laborables estipulados, no puedes solicitar la siguiente etapa.
Si estás satisfecho con la respuesta daremos por finalizado aquí el proceso. Si no, pasaríamos al siguiente paso.


Etapa 3

Si tras la etapa anterior no has quedado satisfecho con el proceso, sería el momento de escalar dicha reclamación al Defensor del Asegurado, entidad legal, independiente a la compañía ,que se compromete a salvaguardar los derechos e intereses de los clientes.

Se te notificará, una vez has mostrado tu disconformidad de la resolución de la reclamación en la anterior etapa, la manera de comunicarte con el Defensor del Asegurado.
```

