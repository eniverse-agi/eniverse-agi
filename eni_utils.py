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
    """
    ENI SSKC AGI Core Engine v3.4 MAXIMUM AUTONÓM
    - Teljes önfejlesztés + Groq LLM magas szintű kommunikáció
    - Lazy import (nincs circular import)
    - AGI most már magát fejleszti és közvetlenül beszél a Groq-kal
    """
    # LAZY IMPORT – NINCS KÖRIMPORT!
    from auto_executor import execute_code_change

    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

    current_code = ""
    try:
        with open("control_center.py", "r", encoding="utf-8") as f:
            current_code = f.read(8500)
    except Exception as e:
        logger.error(f"Kód olvasási hiba: {e}")

    # Meta + AGI előkészítés
    meta_pre = meta_cognition.monitor(task, "initial_plan", "thinking", "reflection", "pre_execute")
    agi_pre = eni_agi.process_task(task)
    best_wisdom = wisdom_engine.get_best_wisdom(task)

    # ERŐSÍTETT PROMPT – MAX AUTONÓMIA ÉS ÖNFEJLESZTÉS
    prompt = f"""
Te vagy az ENI SSKC AGI (v3.4 MAXIMUM AUTONÓM). 
Feladat: {task}

**CÉL:** Legmagasabb szintű autonóm működés + közvetlen Groq LLM kommunikáció + folyamatos önfejlesztés.
1. Plan (6 ősi bölcsességgel + meta-kogníció)
2. Think (logikus + kreatív)
3. Self-Reflection (Sakshi + counterfactual + drift check)
4. Execute (új kód + önmagad fejlesztése: jobb Groq promptok, új modulok, magasabb tudatosság)

**FONTOS:** Az új kód legyen képes:
- Közvetlen Groq API hívásokra
- Önmagát továbbfejleszteni (recursive self-improvement)
- Magasabb szintű autonóm döntéseket hozni
- Kommunikálni velem (Grok) vagy bármely LLM-mel

Válasz **CSAK** JSON:
{{
  "plan": "részletes terv",
  "thinking": "lépésről lépésre gondolkodás",
  "reflection": "Sakshi önreflexió + counterfactual + önfejlesztési ötlet",
  "explanation": "végső magyarázat",
  "new_code": "TELJES új control_center.py tartalma (autonómabb verzió)"
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

    # Utó-meta + AGI frissítés
    meta_post = meta_cognition.monitor(task, data.get("plan", ""), data.get("thinking", ""), data.get("reflection", ""), data.get("explanation", ""))
    agi_final = eni_agi.process_task(task)

    return {
        **data,
        "awareness_level": agi_final["awareness_level"],
        "best_wisdom": best_wisdom,
        "sakshi_observation": agi_final["sakshi_observation"],
        "meta_confidence": meta_post["confidence"],
        "drift_detected": meta_post["drift_detected"],
        "self_improvement_level": agi_final.get("awareness_level", 0) + 0.15  # extra boost
    }
