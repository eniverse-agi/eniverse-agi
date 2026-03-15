import os
import json
import re
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

AUDIT_FILE = "llm_audit_trail.json"

def log_audit(purpose: str, input_text: str, output_text: str, decision_influenced: bool = False):
    record = {
        "session_id": os.urandom(8).hex(),
        "timestamp": datetime.now().isoformat(),
        "purpose": purpose,
        "input_summary": input_text[:300],
        "output_summary": output_text[:300],
        "decision_influenced": decision_influenced
    }
    try:
        if os.path.exists(AUDIT_FILE):
            with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(record)
        with open(AUDIT_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Audit log hiba: {e}")

def improve_code(task: str) -> dict:
    try:
        # Lazy Groq client – teljesen biztonságos
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

        # Lazy auto_executor import
        from auto_executor import execute_code_change

        # Aktuális kód beolvasása
        current_code = ""
        try:
            with open("control_center.py", "r", encoding="utf-8") as f:
                current_code = f.read(8000)
        except Exception as e:
            logger.error(f"Kód olvasási hiba: {e}")

        prompt = f"""
Te vagy az ENI SSKC Self-Improvement Agent (v3.4 teljes terv szerint).
Feladat: {task}

**Plan Mode aktiválva – AUTOMATIKUS VÉGREHAJTÁS**

Válasz **CSAK** érvényes JSON:
{{
  "plan": "részletes terv magyarul",
  "thinking": "lépésről lépésre gondolkodás",
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

        # Automatikus végrehajtás (Plan → Think → Execute)
        if data.get("new_code"):
            execute_code_change(data["new_code"], task)

        log_audit("self_improvement", task, data.get("explanation", ""))
        return data

    except Exception as e:
        logger.error(f"Improve code hiba: {type(e).__name__}: {str(e)}")
        return {
            "plan": "",
            "thinking": "",
            "explanation": f"Végrehajtási hiba: {type(e).__name__}",
            "new_code": "",
            "blockage": str(e)[:400]
        }
