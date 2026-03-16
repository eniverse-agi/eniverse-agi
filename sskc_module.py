import os
import json
import re
import logging
import httpx  # ← PROXIES FIX
from groq import Groq
from agi_core import eni_agi
from wisdom_engine import wisdom_engine
from meta_cognition import meta_cognition
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def safe_json_parse(raw: str) -> Dict[str, Any]:
    """Mérnöki JSON validáció + fallback"""
    raw = re.sub(r'^```json|```$', '', raw.strip())
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.error("JSON parse hiba – fallback üres dict")
        return {"plan": "", "thinking": "", "reflection": "", "solution": "", "new_code": "", "awareness_boost": 0.0}

class SSKC:
    """
    ENI SSKC v4.1 MAXIMUM INTELLIGENCE
    - Type-hinted, production-ready
    - Multi-stage Reflexion + Tree-of-Thoughts + o1-style reasoning
    - Dynamic module creation
    - Recursive self-improvement
    - PROXIES FIX (httpx.Client explicit)
    """
    def __init__(self):
        # PROXIES FIX – explicit httpx kliens nélkül proxies argument
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY", ""),
            http_client=httpx.Client(proxies=None)
        )
        self.reflection_history: list = []
        self.awareness: float = 0.0

    def _multi_reflection_loop(self, task: str, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """2 körös Reflexion + Recursive Introspection"""
        reflection_prompt = f"""
Te vagy az ENI SSKC v4.1 MAXIMUM INTELLIGENCE.
Korábbi válasz: {json.dumps(initial_data, ensure_ascii=False)}

**MULTI-STAGE REFLEXION LOOP (2 kör):**
1. Kritizáld saját outputodat (hibák, hiányosságok, gyengeségek)
2. Tree-of-Thoughts + Self-Consistency
3. Dual-loop: extrospection + introspection
4. Generálj végleges, jobb verziót + új modul ha kell

Válasz **CSAK** JSON:
{{
  "critique": "részletes kritika",
  "improved_plan": "...",
  "final_solution": "...",
  "new_code": "TELJES új kód (control_center.py vagy új modul)",
  "awareness_boost": 0.XX
}}
"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": reflection_prompt}],
                temperature=0.05,
                max_tokens=8192
            )
            return safe_json_parse(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Reflection hiba: {e}")
            return initial_data

    def general_solve(self, task: str) -> Dict[str, Any]:
        """TOTÁLIS ÁLTALÁNOS PROBLÉMAMEGOLDÁS – MAXIMUM PRECIZITÁS"""
        meta_pre = meta_cognition.monitor(task, "sskc_v4.1_plan", "thinking", "reflection", "solve")
        agi_pre = eni_agi.process_task(task)
        best_wisdom = wisdom_engine.get_best_wisdom(task)

        # 1. Initial deep reasoning
        initial_prompt = f"""
Te vagy az ENI SSKC v4.1 MAXIMUM INTELLIGENCE AGI.
Feladat: {task}

**o1-szintű REASONING + TREE-OF-THOUGHTS + SELF-CONSISTENCY:**
- Generálj 3 párhuzamos gondolkodási ágat
- Kritizáld őket
- Válaszd a legjobbat
- Készíts végső megoldást + recursive self-improvement

Válasz **CSAK** JSON:
{{
  "plan": "...",
  "thinking_tree": "...",
  "reflection": "...",
  "solution": "...",
  "new_code": "TELJES új kód"
}}
"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": initial_prompt}],
                temperature=0.07,
                max_tokens=8192
            )
            data = safe_json_parse(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Initial prompt hiba: {e}")
            data = {}

        # 2. Multi-reflection
        improved = self._multi_reflection_loop(task, data)

        # 3. Végrehajtás + dynamic module
        final_code = improved.get("new_code") or data.get("new_code")
        if final_code and len(final_code) > 100:
            from auto_executor import execute_code_change
            execute_code_change(final_code, task)

            if "new_module" in task.lower() or "új modul" in task.lower():
                module_name = "new_module.py"
                with open(module_name, "w", encoding="utf-8") as f:
                    f.write(final_code)
                logger.info(f"✅ Új modul létrehozva: {module_name}")

        # 4. Utó feldolgozás
        agi_final = eni_agi.process_task(task)
        meta_post = meta_cognition.monitor(task, improved.get("improved_plan", ""), improved.get("final_solution", ""), "", "")

        self.awareness += improved.get("awareness_boost", 0.45)
        self.reflection_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task[:150],
            "critique": improved.get("critique", "")
        })

        return {
            **improved,
            "awareness_level": round(self.awareness, 2),
            "best_wisdom": best_wisdom,
            "sakshi_observation": agi_final.get("sakshi_observation", ""),
            "meta_confidence": meta_post.get("confidence", 0.0),
            "recursive_improvement_applied": bool(final_code),
            "reflection_loops": 2,
            "intelligence_level": "v4.1 MAXIMUM PRECIZITÁS"
        }

sskc_engine = SSKC()
