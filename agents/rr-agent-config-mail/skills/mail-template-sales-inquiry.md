---
name: mail-template-sales-inquiry
description: "Plantilla para emails de INTERÉS COMERCIAL: petición de precio, información de producto, alta nueva, cliente potencial. Señales: remitente no cliente, asunto con 'precio'/'presupuesto'/'información'/'contratar'."
---
## Plantilla — Consulta comercial

Tono: cercano, útil, sin presión. Estructura:

1. Saludo + agradecer el interés.
2. Responde a lo que pregunta con la información disponible; si pide precio y no lo tienes, explica cómo obtener una cotización.
3. Un (1) beneficio diferencial relevante a lo que pide — no un folleto entero.
4. Llamada a la acción suave (un enlace, un siguiente paso, ofrecer resolver dudas).
5. Cierre cordial.

No inventes precios, coberturas ni condiciones. Máximo 2 preguntas de vuelta si necesitas datos para cotizar.

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
