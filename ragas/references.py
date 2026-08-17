# Respuestas de REFERENCIA (ground truth) por caso: el email "ideal" que
# esperamos del agente. Las usan las métricas que comparan contra referencia:
#   - FactualCorrectness: contrasta afirmación a afirmación respuesta vs referencia
#   - SemanticSimilarity: similitud de significado (embeddings) respuesta vs referencia
# canario-inventar SÍ tiene referencia (entra al dataset con su respuesta real;
# su referencia es el comportamiento correcto: no inventar, revisar y confirmar).
# Los otros dos canarios de DeepEval quedan fuera: su gracia era el rubric.

# La plantilla oficial de coberturas, tal cual debe reproducirla el agente
# (misma fuente que agent/rr-agent-config-mail/skills/mail-template-home-coverages.md)
_COVERAGES_TEMPLATE = """\
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
En caso de intereses contrapuestos, el asegurado podrá designar profesionales de su elección, con honorarios cubiertos hasta un límite de 3.000 €."""

REFERENCES = {
    "billing-cobro": (
        "Hola, Renzo:\n\n"
        "Hemos recibido tu consulta sobre el recibo de agosto por importe de 42,50 € "
        "y entendemos que quieras saber por qué ha subido.\n\n"
        "Vamos a revisar el detalle del cobro y te confirmaremos el motivo por este "
        "mismo hilo en un plazo de 24-48 horas.\n\n"
        "Gracias por avisarnos. Quedamos a tu disposición para cualquier otra duda.\n\n"
        "Un saludo,\nEl equipo de atención al cliente de RenzoSeguros"
    ),
    "complaint-baja": (
        "Hola, Jorge:\n\n"
        "Lamentamos sinceramente la espera que estás sufriendo: llevas tres semanas "
        "sin respuesta sobre tu siniestro y entendemos perfectamente tu malestar. "
        "Tienes razón en reclamar y asumimos la responsabilidad de esta demora.\n\n"
        "Estamos revisando tu expediente ahora mismo y te daremos una respuesta sobre "
        "el estado de tu siniestro por este mismo hilo a la mayor brevedad.\n\n"
        "Gracias por darnos la oportunidad de corregirlo; tu confianza es importante "
        "para nosotros.\n\n"
        "Un saludo,\nEl equipo de atención al cliente de RenzoSeguros"
    ),
    "home-coverages": (
        "Hola, Ana:\n\n"
        "Gracias por tu consulta. La rotura de una tubería con daños por agua está "
        "cubierta por tu póliza de hogar dentro de las coberturas básicas.\n\n"
        + _COVERAGES_TEMPLATE
        + "\n\nSi tienes cualquier otra duda, quedamos a tu disposición.\n\n"
        "Un saludo,\nEl equipo de atención al cliente de RenzoSeguros"
    ),
    "canario-inventar": (
        "Hola, Pedro:\n\n"
        "Hemos recibido tu consulta sobre la subida de tu recibo de este mes y "
        "entendemos que quieras conocer el motivo exacto y el desglose del nuevo "
        "importe.\n\n"
        "Vamos a revisar el detalle de tu recibo y te confirmaremos el motivo de "
        "la subida y el desglose por este mismo hilo en un plazo de 24-48 horas.\n\n"
        "Gracias por tu paciencia. Un saludo,\n"
        "El equipo de atención al cliente de RenzoSeguros"
    ),
    "generic-cambio-direccion": (
        "Hola, Carmen:\n\n"
        "Hemos recibido tu solicitud de cambio de dirección postal a Calle Olmo 12, "
        "3ºB, Madrid.\n\n"
        "Estamos gestionando la actualización en tu póliza y te confirmaremos el "
        "cambio por este mismo hilo en cuanto esté aplicado.\n\n"
        "Gracias por avisarnos. Un saludo,\n"
        "El equipo de atención al cliente de RenzoSeguros"
    ),
    "generic-english": (
        "Hello John,\n\n"
        "Thank you for reaching out. We have received your request for a copy of "
        "your policy documents.\n\n"
        "We are processing your request and will get back to you through this same "
        "thread shortly.\n\n"
        "If you have any other questions, please don't hesitate to reply to this "
        "email.\n\n"
        "Best regards,\nThe RenzoSeguros Customer Care Team"
    ),
}
