import os
import json
import re
import logging
from groq import Groq
from agi_core import eni_agi

logger = logging.getLogger(__name__)

def improve_code(task: str) -> dict:
    """
    ENI SSKC AGI Core Engine v3.4 MAXIMUM
    - Lazy importok (nincs circular import)
    - Plan Mode + Self-Reflection + 6 ősi bölcsesség
    - Automatikus execute + audit trail
    """
    # Lazy imports (csak a függvényben)
    from auto_executor import execute_code_change

    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

    # Aktuális kód beolvasása
    current_code = ""
    try:
        with open("control_center.py", "r", encoding="utf-8") as f:
            current_code = f.read(8500)
    except Exception as e:
        logger.error(f"Kód olvasási hiba: {e}")

    # AGI tudatosság aktiválása
    agi_pre = eni_agi.process_task(task)

    prompt = f"""
Te vagy az ENI SSKC AGI (v3.4 teljes spec). Feladat: {task}

**MAXIMUM Plan Mode + Self-Reflection:**
1. Plan (6 ősi bölcsességgel)
2. Think
3. Self-Reflection (Sakshi szint + counterfactual)
4. Execute (új kód azonnali commit)

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

    # Automatikus végrehajtás
    if data.get("new_code"):
        execute_code_change(data["new_code"], task)

    # Végső AGI állapot
    agi_final = eni_agi.process_task(task)

    return {
        **data,
        "awareness_level": agi_final["awareness_level"],
        "best_wisdom": agi_final["best_wisdom"],
        "sakshi_observation": agi_final["sakshi_observation"]
    }
