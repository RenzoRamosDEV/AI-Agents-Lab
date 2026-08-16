"""Config de pytest/deepeval: expone la clave del .env raíz como OPENAI_API_KEY,
que es la variable que DeepEval usa por defecto para el modelo juez."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

os.environ.setdefault("OPENAI_API_KEY", os.environ.get("API_KEY_OPENAI", ""))
