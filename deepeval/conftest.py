# Config de pytest/deepeval: carga el .env de la raíz y expone API_KEY_OPENAI
# como OPENAI_API_KEY, la variable que DeepEval espera para el modelo juez.
# Al estar en la raíz de la carpeta, pytest lo carga siempre y de paso hace
# importables core/ y suites/ desde los tests.

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

os.environ.setdefault("OPENAI_API_KEY", os.environ.get("API_KEY_OPENAI", ""))
