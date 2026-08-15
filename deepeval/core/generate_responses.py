import importlib
import json
import sys
from pathlib import Path

RESPONSES_DIR = Path(__file__).resolve().parents[1] / "out" / "responses"


def load_or_generate(suite: str) -> dict[str, str]:
    responses_file = RESPONSES_DIR / f"{suite}.json"
    if responses_file.exists():
        return json.loads(responses_file.read_text(encoding="utf-8"))

    cases_mod = importlib.import_module(f"suites.{suite}.cases")
    agent_mod = importlib.import_module(f"suites.{suite}.agent")

    responses: dict[str, str] = {}
    for case in cases_mod.CASES:
        print(f"[{suite}] Generando respuesta para: {case['id']} ...")
        loaded_skill = case["skill_file"].read_text(encoding="utf-8")
        responses[case["id"]] = agent_mod.generate_answer(case["message"], loaded_skill)

    responses_file.parent.mkdir(parents=True, exist_ok=True)
    responses_file.write_text(
        json.dumps(responses, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Respuestas guardadas en {responses_file}")
    return responses


if __name__ == "__main__":
    load_or_generate(sys.argv[1] if len(sys.argv) > 1 else "mail_agent")
