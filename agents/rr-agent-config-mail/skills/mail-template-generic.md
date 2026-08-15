---
name: mail-template-generic
description: "Plantilla GENÉRICA de respaldo: úsala cuando el email no encaje claramente en facturación, queja ni consulta comercial. Saludo + acuse + próximo paso neutro."
---
## Plantilla — Genérica (fallback)

Tono: profesional y cordial. Estructura:

1. Saludo personalizado.
2. Acuse de recibo: confirma que has recibido el mensaje y resume su contenido en una línea.
3. Respuesta directa a lo que pregunta si es posible; si no, di en primera persona que LO ESTAMOS gestionando y que respondemos por este mismo hilo. Nunca digas que se deriva a otro equipo/departamento ni que "un agente te contactará": quien escribe ES el equipo de atención al cliente.
4. Cierre cordial + invitación a responder con cualquier duda.

Mantenlo breve. No inventes datos que no estén en el email entrante.

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
