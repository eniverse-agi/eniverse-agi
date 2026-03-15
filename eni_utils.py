import os
import json
import re
import logging
from groq import Groq
from agi_core import eni_agi
from auto_executor import execute_code_change

logger = logging.getLogger(__name__)

def improve_code(task: str) -> dict:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    current_code = open("control_center.py", "r", encoding="utf-8").read(8000)

    prompt = f"""
Te vagy az ENI SSKC AGI (v3.4 maximum spec). Feladat: {task}

**Plan Mode + Self-Reflection + 6 Ősi Bölcsesség:**
1. Plan
2. Think
3. Self-Reflection (Sakshi + counterfactual)
4. Execute (új kód)

Válasz **CSAK** JSON:
{{
  "plan": "...",
  "thinking": "...",
  "reflection": "...",
  "explanation": "...",
  "new_code": "TELJES control_center.py tartalma"
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

    agi_result = eni_agi.process_task(task)
    return {**data, **agi_result}
