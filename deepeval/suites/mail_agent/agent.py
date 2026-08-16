import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_FILE = Path(__file__).resolve().parent / "prompt.json"

load_dotenv(REPO_ROOT / ".env")

EVALUATED_MODEL = "gpt-5.6-terra"
TEMPERATURE = 1
MAX_COMPLETION_TOKENS = 4096

TODAY_DATETIME = "2026-08-15 12:00"

SKILL_CATALOG = """\
- mail-template-billing (v1): Plantilla para emails sobre FACTURACIÓN: dudas de cobros, importes, recibos, métodos de pago, devoluciones. Señales: remitente de finanzas/administración, asunto con 'factura'/'recibo'/'cobro'/'pago'.
- mail-template-complaint (v1): Plantilla para emails de QUEJA o INSATISFACCIÓN: reclamaciones, malestar, tono molesto, amenaza de baja. Señales: lenguaje negativo/enfadado, asunto con 'queja'/'reclamación'/'inadmisible'/'cancelar'.
- mail-template-generic (v1): Plantilla GENÉRICA de respaldo: úsala cuando el email no encaje claramente en facturación, queja ni consulta comercial. Saludo + acuse + próximo paso neutro.
- mail-template-home-coverages (v1): Plantilla INFORMATIVA sobre las COBERTURAS de la póliza de hogar/propietario de RenzoSeguros: qué incluye (básicas y opcionales), qué garantiza cada una, límites y exclusiones conocidas. Señales: preguntas de '¿qué cubre mi seguro?'/'¿está cubierto X?'/'qué incluye la póliza'/menciones de fuego, agua, robo, responsabilidad civil, asistencia/bricolaje, defensa jurídica. No es para MODIFICAR el capital (eso es `mail-template-generic`) ni para tramitar/abrir un siniestro concreto.
"""

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "response_schema",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
            "additionalProperties": False,
        },
    },
}


def build_messages(message: str, loaded_skill: str) -> list[dict]:
    template = json.loads(PROMPT_FILE.read_text(encoding="utf-8"))
    replacements = {
        "{{today_datetime}}": TODAY_DATETIME,
        "{{skill_catalog}}": SKILL_CATALOG,
        "{{loaded_skill}}": loaded_skill,
        "{{message}}": message,
    }
    messages = []
    for msg in template:
        content = msg["content"]
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        messages.append({"role": msg["role"], "content": content})
    return messages


def generate_answer(message: str, loaded_skill: str) -> str:
    client = OpenAI(api_key=os.environ["API_KEY_OPENAI"])
    completion = client.chat.completions.create(
        model=EVALUATED_MODEL,
        messages=build_messages(message, loaded_skill),
        temperature=TEMPERATURE,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
        response_format=RESPONSE_FORMAT,
    )
    return json.loads(completion.choices[0].message.content)["answer"]
