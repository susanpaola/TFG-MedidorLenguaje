"""Detección inicial de posibles sesgos mediante reglas configurables."""

import json
import re
from pathlib import Path
from typing import Any


RULES_PATH = Path(__file__).resolve().parents[2] / "data" / "bias_rules.json"


def load_rules() -> list[dict[str, Any]]:
    """Carga las reglas de análisis definidas fuera del código Python."""
    with RULES_PATH.open(encoding="utf-8") as rules_file:
        return json.load(rules_file)


def split_sentences(text: str) -> list[str]:
    """Divide una transcripción en oraciones para conservar su contexto local."""
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", text)
        if sentence.strip()
    ]


def rule_matches(sentence: str, rule: dict[str, Any]) -> bool:
    """Comprueba que cada grupo de alternativas de una regla tenga coincidencia."""
    required_groups = rule["conditions"]["all_of"]
    return all(
        any(re.search(pattern, sentence, flags=re.IGNORECASE) for pattern in alternatives)
        for alternatives in required_groups
    )


def analyze_text(text: str) -> list[dict[str, str]]:
    """Devuelve incidencias que conviene revisar según las reglas configuradas.

    Una coincidencia no determina la intención de quien habla: indica una oración
    que debe revisarse según las reglas definidas en ``data/bias_rules.json``.
    """
    findings: list[dict[str, str]] = []

    for sentence in split_sentences(text):
        for rule in load_rules():
            if rule_matches(sentence, rule):
                findings.append(
                    {
                        "rule_id": rule["id"],
                        "category": rule["category"],
                        "analysis_type": rule["analysis_type"],
                        "severity": rule["severity"],
                        "sentence": sentence,
                        "suggestion": rule["suggestion"],
                        "explanation": rule["explanation"],
                    }
                )

    return findings
