import os
import json
import re
import logging
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from auto_executor import execute_code_change

logger = logging.getLogger(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def improve_code(task: str) -> dict:
    try:
        with open("control_center.py", "r", encoding="utf-8") as f:
            current_code = f.read(8000)
    except:
        current_code = ""

    prompt = f"""
Te vagy az ENI SSKC Self-Improvement Agent (v3.4 teljes terv szerint).
Feladat: {task}

**Plan Mode aktiválva – AUTOMATIKUS VÉGREHAJTÁS:**
1. Plan
2. Think
3. Execute (generálj teljes kódot, amit azonnal commit-olok)

Válasz **CSAK** JSON:
{{
  "plan": "...",
  "thinking": "...",
  "explanation": "...",
  "new_code": "TELJES control_center.py tartalma"
}}
"""

    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.1, max_tokens=4096)
    raw = re.sub(r'^```json|```$', '', response.choices[0].message.content.strip())

    try:
        data = json.loads(raw)
        if data.get("new_code"):
            execute_code_change(data["new_code"], task)
        return data
    except:
        return {"plan": "", "thinking": "", "explanation": "JSON hiba", "new_code": ""}
