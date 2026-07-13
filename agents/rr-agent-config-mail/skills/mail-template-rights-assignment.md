---
name: mail-template-rights-assignment
description: "Plantilla para emails que piden la CARTA DE CESIÓN DE DERECHOS que exige un banco/entidad de crédito sobre la póliza de hogar (habitual cuando hay hipoteca o préstamo asociado a la vivienda). Señales: mención de 'cesión de derechos'/'carta de cesión'/'el banco me pide'/'hipoteca'/'préstamo' junto a la póliza de hogar. No es para dudas generales de capital asegurado sin mención del banco/hipoteca (eso es `mail-template-coverage-changes`)."
---
## Carta de cesión de derechos en póliza RenzoSeguros

### Qué hace esta skill

Decide si un email pide la Carta de Cesión de Derechos que exige un banco sobre la póliza de hogar y, si es así, redacta la respuesta con la plantilla oficial: el propio cliente la genera desde su espacio personal, ajustando antes el Continente a la deuda pendiente.

### Definiciones del dominio (imprescindibles para clasificar bien)

- CARTA DE CESIÓN DE DERECHOS = documento que el banco/entidad de crédito exige para asociar la póliza de hogar a una hipoteca o préstamo sobre la vivienda. El cliente la genera él mismo desde su espacio personal.
- CONTINENTE = capital de reconstrucción de la vivienda; suele ajustarse a la deuda pendiente con el banco antes de generar la carta (paso 2 de la plantilla).

La clasificación solo tiene que responder: ¿el cliente pide la carta de cesión de derechos que le exige un banco?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Pide la carta de cesión de derechos o el documento que le exige el banco por una hipoteca/préstamo sobre la vivienda?
3. Decide: sí lo pide → APLICA, redacta con la plantilla; solo quiere cambiar el capital sin relación con el banco → NO APLICA (`mail-template-coverage-changes`); otra gestión → NO APLICA, deja que lo gestione otro flujo (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → CESIÓN DE DERECHOS: "cesión de derechos", "carta de cesión", "el banco me pide", "documento para la hipoteca", "beneficiario acreedor", "cláusula a favor del banco".
- Señales de contexto que refuerzan: hipoteca, préstamo, entidad/banco, deuda pendiente sobre la vivienda.

### Qué SÍ dispara la plantilla

- "El banco me pide la cesión de derechos de la póliza."
- "Necesito la carta de cesión de derechos para la hipoteca."
- "¿Cómo genero el documento que me exige el banco por el préstamo?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- Dudas generales de capital asegurado (continente/contenido) sin mención de banco/hipoteca/préstamo (eso es `mail-template-coverage-changes`).
- Consultas sobre otros documentos o gestiones de la póliza no relacionadas con el banco.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la plantilla oficial, reproducida LITERALMENTE, con el énfasis en el paso 2.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Lo que te demanda el banco es la Carta de Cesión de Derechos, un documento que, una vez contratada la póliza, puedes generar desde tu espacio personal. Te indico los pasos a seguir (énfasis en paso 2):

1. Acceder a la app de RenzoSeguros o a la sección MI CUENTA a través de la web www.renzoseguros.com
2. Modificar el Continente (si es necesario) y aumentar la cifra a la deuda pendiente con el banco
3. En la pantalla principal (Hola <Nombre y apellidos>...).
4. Acceder a la póliza activa (recuadro con dirección de la vivienda)
5. En los parámetros de tu póliza, bajar hasta localizar la opción CARTA DE CESIÓN DE DERECHOS y seleccionar.
6. Introducir datos requeridos:

- Razón Social del Banco
- Importe de Continente Asegurado
- Número de Préstamo

7. Una vez introducido, hacer click en CREAR MI CARTA DE CESIÓN DE DERECHOS
8. Se guardará en el teléfono u ordenador en función de cómo estés accediendo.
```

## Handoff a un agente humano

Este canal opera SIEMPRE en modo handoff: TODO email entrante se deriva a un agente humano, sin excepción. Marca `handoff` como true y no redactes ninguna respuesta para el cliente — deja `answer` vacío. Redacta igualmente el borrador de apoyo interno con la estructura normal de arriba y ponlo en `suggested_answer` (mismo idioma del email), según el formato de salida del prompt, para que el agente humano lo use como base.
