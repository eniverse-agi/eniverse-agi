import os
import json
import re
import logging
from groq import Groq
from agi_core import eni_agi
from wisdom_engine import wisdom_engine
from meta_cognition import meta_cognition   # ← Meta-kogníció réteg

logger = logging.getLogger(__name__)

def improve_code(task: str) -> dict:
    """
    ENI SSKC AGI Core Engine v3.4 MAXIMUM
    - Meta-kogníció monitoring + self-correction
    - Wisdom Engine vector scoring
    - AGIEngine tudatosság
    - Lazy importok (nincs circular import)
    """
    # Lazy importok
    from auto_executor import execute_code_change

    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

    current_code = ""
    try:
        with open("control_center.py", "r", encoding="utf-8") as f:
            current_code = f.read(8500)
    except Exception as e:
        logger.error(f"Kód olvasási hiba: {e}")

    # 1. Meta-kogníció aktiválása (előzetes monitoring)
    meta_pre = meta_cognition.monitor(task, "initial_plan", "thinking", "reflection", "pre_execute")

    # 2. AGI + Wisdom Engine
    agi_pre = eni_agi.process_task(task)
    best_wisdom = wisdom_engine.get_best_wisdom(task)

    prompt = f"""
Te vagy az ENI SSKC AGI (v3.4 teljes spec). Feladat: {task}

**MAXIMUM Plan Mode + Meta-kogníció:**
1. Plan (6 ősi bölcsességgel)
2. Think
3. Self-Reflection (Sakshi + MetaCognition)
4. Execute (új kód + self-correction ha drift van)

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

    # 3. Automatikus végrehajtás
    if data.get("new_code"):
        execute_code_change(data["new_code"], task)

    # 4. Utó-meta-kogníció (drift check + self-correction)
    meta_post = meta_cognition.monitor(task, data.get("plan", ""), data.get("thinking", ""), data.get("reflection", ""), data.get("explanation", ""))

    agi_final = eni_agi.process_task(task)

    return {
        **data,
        "awareness_level": agi_final["awareness_level"],
        "best_wisdom": best_wisdom,
        "sakshi_observation": agi_final["sakshi_observation"],
        "meta_confidence": meta_post["confidence"],
        "drift_detected": meta_post["drift_detected"]
    }
