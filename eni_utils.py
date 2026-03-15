import os
import json
import re
import logging
from groq import Groq

logger = logging.getLogger(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

def read_code_snippet(filepath: str, max_chars: int = 7000) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read(max_chars)
    except Exception as e:
        logger.error(f"Fájl olvasási hiba: {e}")
        return "Nincs fájl."

def improve_code(task: str) -> dict:
    current_code = read_code_snippet("control_center.py")

    prompt = f"""
Te vagy az ENI SSKC Self-Improvement Agent.
Feladat: {task}

Aktuális control_center.py:
{current_code}

**SZIGORÚ SZABÁLY:**
- A válasz **CSAK** és **kizárólag** érvényes JSON legyen!
- Semmi ```json, semmi magyarázat előtte vagy utána!
- Pontosan ez a struktúra:

{{
  "explanation": "részletes magyar magyarázat, mit csináltál és miért",
  "new_code": "a TELJES új control_center.py tartalma ide",
  "blockage": "ha nem tudtad megcsinálni, magyarázd el magyarul"
}}

Kezdd közvetlenül a {{ jellel és fejezd be a }} jellel. Ne írj semmit mást!
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=4096
        )
        raw = response.choices[0].message.content.strip()
    except Exception as e:
        return {"explanation": "LLM hiba", "new_code": "", "blockage": str(e)}

    # Nagyon erős JSON tisztítás
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except:
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        return {"explanation": "JSON parse hiba", "new_code": "", "blockage": raw[:600]}
