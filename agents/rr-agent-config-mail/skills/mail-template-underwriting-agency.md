---
name: mail-template-underwriting-agency
description: "Plantilla INFORMATIVA que explica que RenzoSeguros actúa como agencia de suscripción y qué aseguradora respalda sus pólizas (IptiQ EMEA P&C S.A, Sucursal en España). Señales: '¿quién está detrás de RenzoSeguros?'/'¿qué aseguradora es?'/'¿quién respalda la póliza?'/'¿sois una aseguradora?'/dudas sobre solvencia o quién asume el riesgo. No es para gestiones sobre la póliza ni para dudas comerciales de precio."
---
## Agencia de suscripción de RenzoSeguros

### Qué hace esta skill

Decide si el correo pregunta quién respalda las pólizas de RenzoSeguros / qué papel juega RenzoSeguros (agencia de suscripción vs aseguradora) y, si es así, redacta la respuesta con la plantilla oficial. Es informativa: aclara el rol de RenzoSeguros y la aseguradora detrás; no ejecuta ni tramita nada.

### Definiciones del dominio (imprescindibles para clasificar bien)

- AGENCIA DE SUSCRIPCIÓN = RenzoSeguros suscribe riesgos por cuenta y en nombre de una aseguradora; no es la aseguradora final.
- ASEGURADORA QUE RESPALDA = IptiQ EMEA P&C S.A, Sucursal en España (registrada en el Gran Ducado de Luxemburgo y autorizada para operar en España).

La clasificación solo tiene que responder: ¿el cliente pregunta quién respalda/asume el riesgo de su póliza o qué es RenzoSeguros?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Pregunta quién está detrás de RenzoSeguros, qué aseguradora respalda la póliza, si RenzoSeguros es una aseguradora, o por la solvencia/quién asume el riesgo?
3. Decide: sí lo pregunta → APLICA, redacta con la plantilla; es una gestión sobre la póliza (datos, capital, siniestro...) o una duda comercial de precio → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → AGENCIA DE SUSCRIPCIÓN / ASEGURADORA: "¿quién está detrás de RenzoSeguros?", "¿sois una aseguradora?", "¿qué compañía respalda mi póliza?", "¿quién asume el riesgo?", "¿quién paga si hay un siniestro?", "solvencia", "IptiQ", "¿con qué aseguradora estoy?".
- Señales que NO son esto: dudas de precio (interés comercial), gestiones de la póliza o siniestros concretos.

### Qué SÍ dispara la plantilla

- "¿Quién está detrás de RenzoSeguros, sois una aseguradora?"
- "¿Qué compañía respalda mi póliza?"
- "¿Quién asume el riesgo de mi seguro?"
- "Me preocupa la solvencia, ¿quién responde si hay un siniestro?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Gestiones sobre la póliza: capital, datos, pago, cancelación, contratación, siniestros.
- Dudas de precio/presupuesto (interés comercial).
- Consultas de qué cubre la póliza (`mail-template-home-coverages`).

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE (incluido el nombre y datos de la aseguradora).
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Respecto a tus dudas, te puedo confirmar que RenzoSeguros actúa como agencia de suscripción y, como tal, suscribe riesgos por cuenta y en nombre de una aseguradora. La entidad aseguradora que respalda las pólizas de RenzoSeguros es IptiQ EMEA P&C S.A, Sucursal en España, que está registrada en el Gran Ducado de Luxemburgo y autorizada para operar en España. Puedes confiar en que una compañía reconocida y de amplia solvencia está detrás de tus seguros.
```

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
