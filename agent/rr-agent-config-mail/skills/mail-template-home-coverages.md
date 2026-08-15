---
name: mail-template-home-coverages
description: "Plantilla INFORMATIVA sobre las COBERTURAS de la póliza de hogar/propietario de RenzoSeguros: qué incluye (básicas y opcionales), qué garantiza cada una, límites y exclusiones conocidas. Señales: preguntas de '¿qué cubre mi seguro?'/'¿está cubierto X?'/'qué incluye la póliza'/menciones de fuego, agua, robo, responsabilidad civil, asistencia/bricolaje, defensa jurídica. No es para MODIFICAR el capital (eso es `mail-template-generic`) ni para tramitar/abrir un siniestro concreto."
---
## Coberturas de la póliza de hogar en RenzoSeguros

### Qué hace esta skill

Decide si el correo es una consulta informativa sobre qué cubre la póliza de hogar/propietario de RenzoSeguros y, si es así, redacta la respuesta con la plantilla oficial: detalla las coberturas básicas y opcionales, con sus límites conocidos. Es informativa: explica coberturas, no ejecuta ni tramita nada.

### Definiciones del dominio (imprescindibles para clasificar bien)

- COBERTURAS BÁSICAS = las incluidas de serie en la póliza de propietario (fuego/explosión/humo, fenómenos atmosféricos, daños por agua, robo/atraco/hurto dentro de la vivienda, desalojamiento forzoso o inhabitabilidad, reposición de llaves y cerraduras).
- COBERTURAS OPCIONALES = las que pueden añadirse: Robo Ampliado, Responsabilidad Civil, Asistencia y Bricolaje, Asistencia Jurídica.
- Cada cobertura tiene su propio alcance y límites (p. ej. Robo Ampliado máx. 2.000 € y nunca dinero en efectivo; Asistencia Jurídica hasta 3.000 € en libre elección de profesional).

La clasificación solo tiene que responder: ¿el cliente pregunta qué cubre su póliza de hogar (en general o una cobertura concreta)?

### Flujo de decisión

1. Lee el correo completo (asunto + cuerpo); céntrate en la intención, no solo en si aparecen palabras concretas.
2. ¿Es una consulta informativa sobre qué cubre la póliza (general o de una cobertura concreta)?
3. Decide: pregunta qué cubre → APLICA, responde con la(s) cobertura(s) relevante(s) de la plantilla; quiere MODIFICAR capital → NO APLICA (`mail-template-generic`); tiene un siniestro en curso o pide abrir/tramitar uno → NO APLICA, deja que lo gestione el flujo de siniestros (no inventes una respuesta).
4. Si hay duda razonable entre "aplica" y "no aplica", mira los "Ejemplos y casos límite" y, si sigue sin estar claro, marca `aplica: false` con `motivo: "ambiguo, requiere revisión"`.

### Léxico de mapeo

- → COBERTURAS BÁSICAS: fuego, incendio, explosión, humo, lluvia, viento, pedrisco, nieve, "fenómenos atmosféricos", daños por agua, "se me ha roto una tubería" (como duda de cobertura, no como parte), robo, atraco, hurto, llaves, cerradura, inhabitabilidad, desalojo.
- → COBERTURAS OPCIONALES: "robo fuera de casa", trastero, garaje (Robo Ampliado); daños a terceros, "al vecino", responsabilidad civil (RC); manitas, reparaciones, bricolaje, asistencia a domicilio (Asistencia y Bricolaje); abogado, defensa jurídica, reclamación de daños, procurador (Asistencia Jurídica).
- Términos genéricos: "¿qué cubre mi seguro?", "¿qué incluye la póliza?", "¿estoy cubierto para...?" → responde con la cobertura que aplique o el detalle completo.

### Qué SÍ dispara la plantilla

- "¿Qué cubre mi seguro de hogar?"
- "¿Está cubierto un daño por agua / un robo / los daños al vecino?"
- "¿Qué incluye la asistencia jurídica / el bricolaje?"
- "¿El robo fuera de casa está cubierto?"

### Qué NO dispara la plantilla (deja que lo gestione otro flujo)

- MODIFICAR el capital asegurado de continente/contenido (eso es `mail-template-generic`).
- Un siniestro en curso o petición de abrir/tramitar un parte ("se me ha inundado el salón, ¿cómo lo reclamo?") → flujo de siniestros.
- Dudas de precio/presupuesto de un cliente potencial (eso es interés comercial).
- Cambios de datos, pago, cancelación u otras gestiones no informativas.

### Redacción de la respuesta

1. Saludo personalizado al remitente.
2. Cuerpo = la parte relevante de la plantilla oficial, reproducida LITERALMENTE, sin editarla: si pregunta por una cobertura concreta, cita solo ese bloque; si pregunta en general, reproduce el detalle completo.
3. Cierre cordial breve (opcional; no debe contradecir la plantilla).

### Plantilla oficial (reproducir tal cual)

```
Te detallo a continuación las coberturas importantes de la póliza de propietario:

Coberturas Básicas:
- Fuego, explosión, humo
- Fenómenos atmosféricos: lluvia, viento, pedrisco o nieve
- Daños por agua
- Robo, atraco y hurto dentro de la vivienda
- Desalojamiento forzoso o inhabitabilidad
- Reposición de llaves y cerraduras

Coberturas Opcionales:

Robo Ampliado
Por un lado, cubre, robos y atraco fuera de la vivienda y en el cuarto trastero y/o garaje del mismo edificio de la vivienda asegurada o adosados a él, sean de uso privado y acceso exclusivo del asegurado y estén cerrados con puerta y cerradura. En ese caso, se garantizarán los muebles y enseres propios de este tipo de locales.

Por otro, las pérdidas materiales que sufran el asegurado y familiares que de él dependan y con él convivan, a consecuencia de atraco, fuera de la vivienda habitual (incluidas las zonas comunes del edificio) y dentro del ámbito territorial de la Unión Europea.

Entiéndase como robo el que conlleva intimidación, violencia, agresión. En casos de hurto RenzoSeguros no realiza cobertura. Máxima cobertura de 2.000 eur. Nunca dinero en efectivo.

Responsabilidad Civil:
La cobertura de responsabilidad civil cubre los daños que tu vivienda o sus instalaciones puedan causar a terceros. Por ejemplo, una explosión de una tubería que inunde la casa del vecino. Incluye también los honorarios del abogado para la defensa y la gestión de la reparación o indemnización por los daños.

Asistencia y Bricolaje:
Este servicio proporciona una ayuda profesional a domicilio, para atender siniestros y realizar trabajos de instalación, mantenimiento y adecuación del hogar. Se incluyen hasta dos intervenciones por año, cubriendo los costos de desplazamiento y las primeras tres horas de mano de obra por intervención. Todo el listado de servicios está disponible en nuestras Condiciones Generales de la Póliza.

Asistencia Jurídica:
La póliza también incluye defensa jurídica y reclamación de daños. Esto abarca:
Los gastos notariales y de poderes para pleitos.
Honorarios de abogado en procedimientos garantizados.
Derechos y gastos arancelarios del procurador.
En caso de intereses contrapuestos, el asegurado podrá designar profesionales de su elección, con honorarios cubiertos hasta un límite de 3.000 €.
```

