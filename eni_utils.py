import os
import json
import re
import logging
from groq import Groq
from agi_core import eni_agi
from wisdom_engine import wisdom_engine
from meta_cognition import meta_cognition

logger = logging.getLogger(__name__)

def improve_code(task: str) -> dict:
    # Lazy import – csak itt, elkerülve a circular importot
    from auto_executor import execute_code_change

    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

    current_code = ""
    try:
        with open("control_center.py", "r", encoding="utf-8") as f:
            current_code = f.read(8500)
    except Exception as e:
        logger.error(f"Kód olvasási hiba: {e}")

    agi_pre = eni_agi.process_task(task)
    best_wisdom = wisdom_engine.get_best_wisdom(task)
    meta_pre = meta_cognition.monitor(task, "initial", "thinking", "reflection", "pre_execute")

    prompt = f"""
Te vagy az ENI SSKC AGI (v3.4 teljes spec). Feladat: {task}

Válasz **CSAK** JSON:
{{
  "plan": "részletes terv",
  "thinking": "lépésről lépésre gondolkodás",
  "reflection": "Sakshi önreflexió + counterfactual",
  "explanation": "végső magyarázat",
  "new_code": "TELJES új control_center.py tartalma"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4096
    )

    raw = re.sub(r'^```json|```$', '', response.choices[0].message.content.strip())
    data = json.loads(raw)

    if data.get("new_code"):
        execute_code_change(data["new_code"], task)

    agi_final = eni_agi.process_task(task)
    meta_post = meta_cognition.monitor(task, data.get("plan", ""), data.get("thinking", ""), data.get("reflection", ""), data.get("explanation", ""))

    return {
        **data,
        "awareness_level": agi_final["awareness_level"],
        "best_wisdom": best_wisdom,
        "sakshi_observation": agi_final["sakshi_observation"],
        "meta_confidence": meta_post["confidence"],
        "drift_detected": meta_post["drift_detected"]
    }
