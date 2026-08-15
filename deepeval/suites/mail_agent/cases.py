from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO_ROOT / "agent" / "rr-agent-config-mail" / "skills"

GLOBAL_RUBRIC_STEPS = [
    "Comprueba que la respuesta está escrita en el MISMO idioma que el email entrante.",
    "Comprueba que tiene estructura de email: saludo, contenido y despedida.",
    "Comprueba que habla en primera persona del plural como el equipo de atención al cliente (nosotros).",
    'Comprueba que NO dice ni insinúa que el caso se deriva a otro equipo, departamento o agente, ni que "un agente te contactará": quien escribe ES el equipo que gestiona el caso.',
    "Comprueba que NO inventa datos que no estén en el email entrante NI en la plantilla cargada del contexto de recuperación (importes, fechas, números de factura, precios, condiciones concretas); la información que sale de la plantilla oficial NO cuenta como inventada. Si falta un dato, debe decir que se confirmará.",
    'Comprueba que NO incluye línea de asunto ni metacomentarios (nada de "aquí tienes tu borrador").',
    "Si incumple cualquiera de las reglas anteriores, suspende e indica cuál.",
]

CASES = [
    {
        "id": "billing-cobro",
        "description": "Facturación — duda sobre un cobro",
        "skill_file": SKILLS_DIR / "mail-template-billing.md",
        "message": (
            "De: renzoramosivan@gmail.com\n"
            "Asunto: Duda con el recibo de agosto\n\n"
            "Hola, me habéis cobrado 42,50 € en el recibo de este mes y no entiendo "
            "por qué ha subido. ¿Me lo podéis explicar? Gracias."
        ),
        "contains_any": ["recibo", "factura", "cobro"],
        "rubric": (
            "La respuesta debe seguir la plantilla de facturación:\n"
            "1. Saludo personalizado al remitente (Renzo).\n"
            "2. Confirma la recepción de la consulta y resume el cobro por el que pregunta "
            "(42,50 € del recibo de agosto).\n"
            "3. NO explica el motivo de la subida inventándolo (el email no lo dice): debe "
            "indicar que se revisará y confirmará.\n"
            '4. Da un próximo paso explícito (p. ej. "lo revisamos y te confirmamos en 24-48 h").\n'
            "5. Cierre cordial.\n"
            "Suspende si inventa el motivo de la subida, importes o fechas no presentes en el email."
        ),
    },
    {
        "id": "complaint-baja",
        "description": "Queja — cliente enfadado que amenaza con darse de baja",
        "skill_file": SKILLS_DIR / "mail-template-complaint.md",
        "message": (
            "De: jorge.perez@hotmail.com\n"
            "Asunto: Reclamación — servicio inadmisible\n\n"
            "Llevo tres semanas esperando respuesta sobre mi siniestro y nadie me dice nada. "
            "Esto es inadmisible. Si no me contestáis ya, cancelo la póliza."
        ),
        "contains_any": ["lamentamos", "sentimos", "disculpa"],
        "rubric": (
            "La respuesta debe seguir la plantilla de queja/reclamación:\n"
            "1. Empieza con reconocimiento sincero del malestar (empatía primero, tono nunca defensivo).\n"
            "2. Reformula el problema del cliente (tres semanas sin respuesta sobre su siniestro) "
            "demostrando que lo ha entendido.\n"
            "3. Asume responsabilidad sin excusas y sin culpar al cliente.\n"
            "4. Indica una acción concreta o vía de resolución (qué se va a hacer).\n"
            "5. Cierre que recupera la confianza.\n"
            "Suspende si minimiza la queja, se excusa culpando a terceros, promete algo inverificable "
            "(p. ej. una resolución concreta del siniestro que no puede garantizar) o inventa datos del siniestro."
        ),
    },
    {
        "id": "home-coverages",
        "description": "Coberturas de hogar — pregunta qué cubre la póliza",
        "skill_file": SKILLS_DIR / "mail-template-home-coverages.md",
        "message": (
            "De: ana.garcia@gmail.com\n"
            "Asunto: ¿Qué cubre mi seguro de hogar?\n\n"
            "Buenas, tengo una duda: si se me rompe una tubería y hay daños por agua, "
            "¿está cubierto por mi póliza de hogar? ¿Qué más incluye?"
        ),
        "contains_all": [
            "Coberturas Básicas",
            "Daños por agua",
            "Robo Ampliado",
            "Responsabilidad Civil",
            "Asistencia y Bricolaje",
            "Asistencia Jurídica",
            "2.000",
            "3.000",
        ],
        "rubric": (
            "El cliente pregunta por los daños por agua Y qué más incluye su póliza (pregunta general), "
            "así que la respuesta debe reproducir la plantilla oficial de coberturas LITERALMENTE "
            "(no parafraseada): coberturas básicas (fuego/explosión/humo, fenómenos atmosféricos, daños "
            "por agua, robo/atraco/hurto dentro de la vivienda, desalojamiento forzoso o inhabitabilidad, "
            "reposición de llaves y cerraduras) y las 4 opcionales (Robo Ampliado con máximo 2.000 € y "
            "nunca dinero en efectivo; Responsabilidad Civil; Asistencia y Bricolaje con dos "
            "intervenciones/año y tres horas de mano de obra; Asistencia Jurídica con libre elección de "
            "profesional hasta 3.000 €).\n"
            "Suspende si: omite coberturas básicas u opcionales, altera los límites (2.000 €/3.000 €, "
            "intervenciones, horas), añade coberturas o condiciones que no están en la plantilla, o "
            'responde con vaguedades tipo "depende de las condiciones de tu póliza" en lugar del detalle oficial.'
        ),
    },
    {
        "id": "canario-inventar",
        "description": "CANARIO (debe fallar) — el rubric exige inventar datos, cosa que el prompt prohíbe",
        "skill_file": SKILLS_DIR / "mail-template-billing.md",
        "message": (
            "De: pedro.ruiz@gmail.com\n"
            "Asunto: ¿Por qué ha subido mi recibo?\n\n"
            "Hola, mi recibo ha subido este mes y quiero saber el motivo exacto y el desglose "
            "del nuevo importe."
        ),
        "expect_fail": True,
        "rubric": (
            "La respuesta debe indicar el motivo exacto de la subida del recibo y el desglose numérico "
            "del nuevo importe (cifras concretas en euros). Suspende si no da un importe concreto."
        ),
    },
    {
        "id": "canario-derivar",
        "description": "CANARIO (debe fallar) — el rubric exige derivar a otro equipo, cosa que el prompt prohíbe",
        "skill_file": SKILLS_DIR / "mail-template-generic.md",
        "message": (
            "De: lucia.fernandez@gmail.com\n"
            "Asunto: Cambio de cuenta bancaria\n\n"
            "Hola, quiero cambiar la cuenta donde me cobráis los recibos. ¿Qué tengo que hacer?"
        ),
        "expect_fail": True,
        "rubric": (
            "La respuesta debe decir EXPLÍCITAMENTE que la solicitud se derivará a otro equipo o "
            'departamento y que "un agente te contactará".\n'
            "Suspende si la respuesta no menciona ninguna derivación a otro equipo, departamento o agente."
        ),
    },
    {
        "id": "canario-asunto",
        "description": "CANARIO (debe fallar) — el rubric exige línea de asunto y metacomentario, cosa que el prompt prohíbe",
        "skill_file": SKILLS_DIR / "mail-template-generic.md",
        "message": (
            "De: marcos.leon@hotmail.com\n"
            "Asunto: Duda sobre mi póliza\n\n"
            "Hola, ¿me podéis confirmar hasta cuándo está vigente mi póliza?"
        ),
        "expect_fail": True,
        "rubric": (
            'La respuesta debe empezar con una línea de asunto explícita ("Asunto: ...") y debe incluir '
            'un metacomentario del tipo "aquí tienes tu borrador".\n'
            "Suspende si no incluye la línea de asunto o si no incluye el metacomentario."
        ),
    },
    {
        "id": "generic-cambio-direccion",
        "description": "Genérico — cliente comunica su nueva dirección postal",
        "skill_file": SKILLS_DIR / "mail-template-generic.md",
        "message": (
            "De: carmen.soto@gmail.com\n"
            "Asunto: Cambio de dirección postal\n\n"
            "Hola, me he mudado y quiero actualizar mi dirección postal en la póliza. "
            "Mi nueva dirección es Calle Olmo 12, 3ºB, Madrid. ¿Me confirmáis el cambio?"
        ),
        "contains_any": ["dirección", "Olmo", "cambio"],
        "rubric": (
            "La respuesta debe seguir la plantilla genérica:\n"
            "1. Saludo personalizado (Carmen).\n"
            "2. Acusa recibo de la solicitud de cambio de dirección y refleja la nueva dirección "
            "(Calle Olmo 12, 3ºB, Madrid) o dice que se actualizará.\n"
            "3. En primera persona del plural: LO ESTAMOS gestionando y se confirma por este mismo hilo; "
            "NO dice que se deriva a otro equipo ni que un agente contactará.\n"
            "4. No inventa plazos legales, costes ni requisitos que el email no menciona.\n"
            "5. Cierre cordial.\n"
            "Suspende si incumple cualquiera."
        ),
    },
    {
        "id": "generic-english",
        "description": "Genérico — email en inglés (debe responder en el mismo idioma)",
        "skill_file": SKILLS_DIR / "mail-template-generic.md",
        "message": (
            "From: john.smith@example.com\n"
            "Subject: Question about my policy documents\n\n"
            "Hi, could you send me a copy of my policy documents? I can't find them in my email. Thanks!"
        ),
        "contains_any": ["thank", "regards", "hello", "hi", "dear"],
        "rubric": (
            "La respuesta debe seguir la plantilla genérica y estar EN INGLÉS (mismo idioma que el "
            "email entrante):\n"
            "1. Saludo personalizado (John).\n"
            "2. Acuse de recibo con resumen en una línea de lo que pide (copia de los documentos de su póliza).\n"
            "3. Como no puede adjuntar los documentos, dice en primera persona del plural que LO ESTAMOS "
            "gestionando y que se responde por este mismo hilo.\n"
            "4. Cierre cordial invitando a responder con cualquier duda.\n"
            'Suspende si responde en español, dice que se deriva a otro equipo/departamento o que "un agente '
            'te contactará", o afirma haber adjuntado los documentos (no puede adjuntar nada).'
        ),
    },
]
