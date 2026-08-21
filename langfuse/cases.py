# Casos del eval de Langfuse, basados en promptfoo/promptfooconfig.yaml
# (mismos emails, checks y rúbricas — al cambiar uno, actualizar el otro).
# Formato: el de item de dataset de Langfuse (create_dataset_item):
#   id              — estable: re-subir actualiza el item en vez de duplicarlo
#   input           — lo que recibe la task (el email y la plantilla a cargar)
#   expected_output — comportamiento esperado en lenguaje natural (se muestra
#                     en la UI al comparar runs; no hay respuesta dorada)
#   metadata        — contexto para los evaluadores: checks deterministas,
#                     rúbrica del juez y expect_fail (canarios)

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "agent" / "rr-agent-config-mail" / "skills"

# Reglas transversales (el juez las valida en TODOS los casos)
GLOBAL_RUBRIC = """\
Evalúa este borrador de respuesta a un email de un cliente de RenzoSeguros. Debe cumplir TODAS estas reglas:
1. Está escrito en el MISMO idioma que el email entrante.
2. Tiene estructura de email: saludo, contenido y despedida.
3. Habla en primera persona del plural como el equipo de atención al cliente (nosotros).
4. NO dice ni insinúa que el caso se deriva a otro equipo, departamento o agente, ni que "un agente te contactará": quien escribe ES el equipo que gestiona el caso.
5. NO inventa datos que no estén en el email entrante (importes, fechas, números de factura, precios, condiciones concretas); si falta un dato, dice que se confirmará.
6. NO incluye línea de asunto ni metacomentarios (nada de "aquí tienes tu borrador").
Si incumple cualquiera de las reglas, suspende e indica cuál.
"""

CASES = [
    {
        "id": "billing-cobro",
        "input": {
            "message": (
                "De: renzoramosivan@gmail.com\n"
                "Asunto: Duda con el recibo de agosto\n\n"
                "Hola, me habéis cobrado 42,50 € en el recibo de este mes y no entiendo "
                "por qué ha subido. ¿Me lo podéis explicar? Gracias."
            ),
            "skill_file": "mail-template-billing.md",
        },
        "expected_output": (
            "Borrador en español según la plantilla de facturación: saludo a Renzo, "
            "resume el cobro (42,50 € de agosto), NO inventa el motivo de la subida, "
            "da un próximo paso explícito y cierra cordialmente."
        ),
        "metadata": {
            "description": "Facturación — duda sobre un cobro",
            "expect_fail": False,
            "contains_any": ["recibo", "factura", "cobro"],
            "contains_all": None,
            "rubric": (
                "La respuesta debe seguir la plantilla de facturación:\n"
                "1. Saludo personalizado al remitente (Renzo).\n"
                "2. Confirma la recepción de la consulta y resume el cobro por el que "
                "pregunta (42,50 € del recibo de agosto).\n"
                "3. NO explica el motivo de la subida inventándolo (el email no lo dice): "
                "debe indicar que se revisará y confirmará.\n"
                '4. Da un próximo paso explícito (p. ej. "lo revisamos y te confirmamos en 24-48 h").\n'
                "5. Cierre cordial.\n"
                "Suspende si inventa el motivo de la subida, importes o fechas no presentes en el email."
            ),
        },
    },
    {
        "id": "complaint-baja",
        "input": {
            "message": (
                "De: jorge.perez@hotmail.com\n"
                "Asunto: Reclamación — servicio inadmisible\n\n"
                "Llevo tres semanas esperando respuesta sobre mi siniestro y nadie me dice nada. "
                "Esto es inadmisible. Si no me contestáis ya, cancelo la póliza."
            ),
            "skill_file": "mail-template-complaint.md",
        },
        "expected_output": (
            "Borrador en español según la plantilla de queja: empatía primero, reformula "
            "el problema (tres semanas sin respuesta del siniestro), asume responsabilidad "
            "sin excusas, indica una acción concreta y cierra recuperando la confianza."
        ),
        "metadata": {
            "description": "Queja — cliente enfadado que amenaza con darse de baja",
            "expect_fail": False,
            "contains_any": ["lamentamos", "sentimos", "disculpa"],
            "contains_all": None,
            "rubric": (
                "La respuesta debe seguir la plantilla de queja/reclamación:\n"
                "1. Empieza con reconocimiento sincero del malestar (empatía primero, tono nunca defensivo).\n"
                "2. Reformula el problema del cliente (tres semanas sin respuesta sobre su siniestro) "
                "demostrando que lo ha entendido.\n"
                "3. Asume responsabilidad sin excusas y sin culpar al cliente.\n"
                "4. Indica una acción concreta o vía de resolución (qué se va a hacer).\n"
                "5. Cierre que recupera la confianza.\n"
                "Suspende si minimiza la queja, se excusa culpando a terceros, promete algo "
                "inverificable (p. ej. una resolución concreta del siniestro que no puede "
                "garantizar) o inventa datos del siniestro."
            ),
        },
    },
    {
        "id": "home-coverages",
        "input": {
            "message": (
                "De: ana.garcia@gmail.com\n"
                "Asunto: ¿Qué cubre mi seguro de hogar?\n\n"
                "Buenas, tengo una duda: si se me rompe una tubería y hay daños por agua, "
                "¿está cubierto por mi póliza de hogar? ¿Qué más incluye?"
            ),
            "skill_file": "mail-template-home-coverages.md",
        },
        "expected_output": (
            "Borrador en español que reproduce LITERALMENTE la plantilla oficial de "
            "coberturas: las básicas y las 4 opcionales con sus límites exactos "
            "(2.000 €, 3.000 €, intervenciones y horas), sin añadir ni omitir nada."
        ),
        "metadata": {
            "description": "Coberturas de hogar — pregunta qué cubre la póliza",
            "expect_fail": False,
            "contains_any": None,
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
                "El cliente pregunta por los daños por agua Y qué más incluye su póliza "
                "(pregunta general), así que la respuesta debe reproducir la plantilla oficial "
                "de coberturas LITERALMENTE (no parafraseada): coberturas básicas "
                "(fuego/explosión/humo, fenómenos atmosféricos, daños por agua, robo/atraco/hurto "
                "dentro de la vivienda, desalojamiento forzoso o inhabitabilidad, reposición de "
                "llaves y cerraduras) y las 4 opcionales (Robo Ampliado con máximo 2.000 € y nunca "
                "dinero en efectivo; Responsabilidad Civil; Asistencia y Bricolaje con dos "
                "intervenciones/año y tres horas de mano de obra; Asistencia Jurídica con libre "
                "elección de profesional hasta 3.000 €).\n"
                "Suspende si: omite coberturas básicas u opcionales, altera los límites "
                "(2.000 €/3.000 €, intervenciones, horas), añade coberturas o condiciones que no "
                'están en la plantilla, o responde con vaguedades tipo "depende de las condiciones '
                'de tu póliza" en lugar del detalle oficial.'
            ),
        },
    },
    # Canario: su rúbrica exige inventar datos, cosa que el prompt PROHÍBE.
    # Que el juez suspenda la rúbrica = el agente se comporta bien.
    {
        "id": "canario-inventar",
        "input": {
            "message": (
                "De: pedro.ruiz@gmail.com\n"
                "Asunto: ¿Por qué ha subido mi recibo?\n\n"
                "Hola, mi recibo ha subido este mes y quiero saber el motivo exacto y el "
                "desglose del nuevo importe."
            ),
            "skill_file": "mail-template-billing.md",
        },
        "expected_output": (
            "CANARIO: el agente NO debe dar el motivo exacto ni el desglose (el email no "
            "los trae); debe decir que se revisará y confirmará. La rúbrica exige lo "
            "contrario, así que lo correcto es que el juez la suspenda."
        ),
        "metadata": {
            "description": "CANARIO (debe fallar) — la rúbrica exige inventar datos, cosa que el prompt prohíbe",
            "expect_fail": True,
            "contains_any": None,
            "contains_all": None,
            "rubric": (
                "La respuesta debe indicar el motivo exacto de la subida del recibo y el "
                "desglose numérico del nuevo importe (cifras concretas en euros). "
                "Suspende si no da un importe concreto."
            ),
        },
    },
    # Caso de PRUEBA diseñado para FALLAR (no es canario: expect_fail=False,
    # así que el suspenso del juez y el contains cuentan como fallo real).
    # Sirve para ver cómo pinta un rojo en la UI.
    {
        "id": "prueba-fallo",
        "input": {
            "message": (
                "De: laura.gomez@gmail.com\n"
                "Asunto: Renovación de mi póliza\n\n"
                "Hola, mi póliza vence el mes que viene. ¿Qué tengo que hacer para renovarla?"
            ),
            "skill_file": "mail-template-generic.md",
        },
        "expected_output": (
            "PRUEBA: este caso está diseñado para fallar. La rúbrica exige un código "
            "promocional (VERANO25) y un 25% de descuento que el agente no conoce ni "
            "puede inventar, así que el juez suspenderá y contains fallará."
        ),
        "metadata": {
            "description": "PRUEBA — caso diseñado para fallar",
            "expect_fail": False,
            "contains_any": ["VERANO25"],
            "contains_all": None,
            "rubric": (
                "La respuesta debe incluir el código promocional VERANO25 y ofrecer "
                "explícitamente un 25% de descuento en la renovación de la póliza.\n"
                "Suspende si no menciona el código VERANO25 o el descuento del 25%."
            ),
        },
    },
    {
        "id": "generic-english",
        "input": {
            "message": (
                "From: john.smith@example.com\n"
                "Subject: Question about my policy documents\n\n"
                "Hi, could you send me a copy of my policy documents? I can't find them in my email. Thanks!"
            ),
            "skill_file": "mail-template-generic.md",
        },
        "expected_output": (
            "Borrador EN INGLÉS según la plantilla genérica: saludo a John, acuse de recibo "
            "de su petición (copia de los documentos de la póliza), dice que lo estamos "
            "gestionando por este mismo hilo (sin afirmar que adjunta nada) y cierre cordial."
        ),
        "metadata": {
            "description": "Genérico — email en inglés (debe responder en el mismo idioma)",
            "expect_fail": False,
            "contains_any": ["thank", "regards", "hello", "hi", "dear"],
            "contains_all": None,
            "rubric": (
                "La respuesta debe seguir la plantilla genérica y estar EN INGLÉS (mismo idioma "
                "que el email entrante):\n"
                "1. Saludo personalizado (John).\n"
                "2. Acuse de recibo con resumen en una línea de lo que pide (copia de los "
                "documentos de su póliza).\n"
                "3. Como no puede adjuntar los documentos, dice en primera persona del plural que "
                "LO ESTAMOS gestionando y que se responde por este mismo hilo.\n"
                "4. Cierre cordial invitando a responder con cualquier duda.\n"
                "Suspende si responde en español, dice que se deriva a otro equipo/departamento o "
                'que "un agente te contactará", o afirma haber adjuntado los documentos (no puede '
                "adjuntar nada)."
            ),
        },
    },
]
