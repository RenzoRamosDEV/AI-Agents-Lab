---
name: mail-template-solar-panels
description: "Plantilla para emails que quieren INCLUIR/ASEGURAR PLACAS SOLARES en la póliza de hogar de RenzoSeguros: explica que hay que aumentar el Continente por el valor de las placas, avisar a placas_solares@renzoseguros.com y aportar la factura. Señales: 'placas solares'/'paneles solares'/'fotovoltaica'/'asegurar las placas'/'cubrir los paneles'. No es un cambio de capital genérico (eso es `mail-template-coverage-changes`) ni una consulta de coberturas."
---
## Incluir placas solares en la póliza de RenzoSeguros

### Qué hace esta skill

Decide si el correo quiere incluir/asegurar placas solares en la póliza de hogar y, si es así, redacta la respuesta con la plantilla oficial: hay que aumentar el Continente por el valor de las placas, avisar a placas_solares@renzoseguros.com de que ese aumento es para cubrirlas y aportar la factura.

### Definiciones del dominio (imprescindibles para clasificar bien)

- INCLUIR PLACAS SOLARES = asegurar las placas/paneles solares dentro de la póliza. Se hace aumentando el Continente estimado por el valor de las placas y comunicándolo, con la factura como justificante del valor.
- No es un cambio de capital cualquiera: es un aumento de Continente con un fin específico (cubrir las placas) que requiere avisar por email y aportar factura.

La clasificación solo tiene que responder: ¿el cliente quiere asegurar/incluir placas solares en su póliza?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Quiere asegurar/incluir placas solares (o pregunta cómo cubrirlas)?
3. Decide: quiere incluir placas solares → APLICA, redacta con la plantilla; solo quiere subir/bajar el capital sin relación con placas → NO APLICA (`mail-template-coverage-changes`); pregunta qué cubre la póliza en abstracto → NO APLICA (`mail-template-home-coverages`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → PLACAS SOLARES: "placas solares", "paneles solares", "fotovoltaica", "instalación solar", "asegurar las placas", "cubrir los paneles", "he instalado placas en el tejado".
- Señales que apuntan a OTRAS skills: subir/bajar capital sin mención de placas (`coverage-changes`); qué cubre la póliza en general (`home-coverages`).

### Qué SÍ dispara la plantilla

- "Quiero asegurar las placas solares que he instalado."
- "¿Cómo incluyo los paneles solares en mi póliza?"
- "He puesto una instalación fotovoltaica, quiero cubrirla."

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Subir/bajar el capital de continente/contenido sin relación con placas solares (eso es `mail-template-coverage-changes`).
- Consultar qué cubre la póliza en abstracto (eso es `mail-template-home-coverages`).
- Dar parte de un daño en las placas (eso es `mail-template-claim-report`).
- Gestiones administrativas: datos, pago, cancelación, contratación.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, incluidos el email placas_solares@renzoseguros.com y el requisito de la factura.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Para incluir placas solares seria necesario aumentar el Continente estimado a razón del valor de estas placas solares y, una vez contratado, indicar al mail placas_solares@renzoseguros.com que el aumento de este Continente es debido a querer cubrir estas. Adicionalmente tendrás que aportar la factura de las placas solares donde se indique su valor
```

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
