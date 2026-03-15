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
Te vagy az ENI SSKC Self-Improvement Agent (v3.4 spec szerint).
Feladat: {task}

Aktuális control_center.py kód:
{current_code}

**KÖTELEZŐ**:
- Generálj **teljes, futtatható** új kódot a control_center.py fájlhoz
- A válasz **CSAK** érvényes JSON legyen, semmi más szöveg!
- A JSON struktúra pontosan ez legyen:

{{
  "explanation": "részletes magyar magyarázat, mit változtattál és miért",
  "new_code": "a TELJES új control_center.py tartalma itt",
  "blockage": "ha nem tudtad megcsinálni, magyarázd el magyarul"
}}

Ne írj semmit a JSON-en kívül!
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4096
        )
        raw = response.choices[0].message.content.strip()
    except Exception as e:
        return {"explanation": "LLM hívási hiba", "new_code": "", "blockage": str(e)}

    # Erős JSON tisztítás
    try:
        return json.loads(raw)
    except:
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        return {"explanation": "JSON parse hiba", "new_code": "", "blockage": raw[:400]}
