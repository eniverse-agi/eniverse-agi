import os
import json
import re
import logging
from datetime import datetime
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

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

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def improve_code(task: str) -> dict:
    current_code = ""
    try:
        with open("control_center.py", "r", encoding="utf-8") as f:
            current_code = f.read(8000)
    except:
        pass

    prompt = f"""
Te vagy az ENI SSKC Self-Improvement Agent (v3.4 spec szerint).
Feladat: {task}

Aktuális control_center.py:
{current_code}

**Plan Mode – lépésről lépésre:**
1. **Plan**: tervezd meg a megoldást
2. **Think**: gondolkozz lépésről lépésre
3. **Execute**: hajtsd végre automatikusan (generálj teljes kódot)

Válasz **CSAK** érvényes JSON formátumban, semmi más szöveg előtt vagy után!
{{
  "plan": "részletes terv magyarul",
  "thinking": "lépésről lépésre gondolkodás",
  "explanation": "végső magyarázat",
  "new_code": "TELJES új control_center.py tartalma (másolható)",
  "blockage": "ha elakadtál, magyarázd el magyarul vagy üres string"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4096
    )
    raw = response.choices[0].message.content.strip()

    raw = re.sub(r'^```json|```$', '', raw).strip()
    try:
        data = json.loads(raw)
        log_audit("self_improvement", task, data.get("explanation", ""))
        return data
    except:
        return {"plan": "", "thinking": "", "explanation": "JSON parse hiba", "new_code": "", "blockage": raw[:600]}
