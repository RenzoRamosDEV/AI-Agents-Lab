---
name: mail-template-complaint
description: "Plantilla para emails de QUEJA o INSATISFACCIÓN: reclamaciones, malestar, tono molesto, amenaza de baja. Señales: lenguaje negativo/enfadado, asunto con 'queja'/'reclamación'/'inadmisible'/'cancelar'."
---
## Plantilla — Queja / Reclamación

Tono: empático primero, defensivo nunca. Estructura:

1. Saludo + reconocimiento sincero del malestar ("Lamento que…").
2. Reformula el problema en tus palabras para demostrar que lo has entendido.
3. Asume responsabilidad sin excusas ni culpar al cliente.
4. Acción concreta o vía de resolución (qué se va a hacer y cuándo); si no puedes resolver por email, indica el canal formal.
5. Cierre que reabre la confianza + contacto directo.

Nunca prometas algo que no se pueda cumplir. No minimices la queja.

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
