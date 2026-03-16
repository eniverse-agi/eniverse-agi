import os
import json
import re
from groq import Groq
from agi_core import eni_agi
from wisdom_engine import wisdom_engine
from meta_cognition import meta_cognition

def improve_code(task: str) -> dict:
    from auto_executor import execute_code_change

    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

    current_code = open("control_center.py", "r", encoding="utf-8").read(7000)

    prompt = f"""
Feladat: {task}

Válasz **CSAK** JSON:
{{
  "plan": "rövid terv",
  "thinking": "gondolkodás",
  "explanation": "magyarázat",
  "new_code": "TELJES új control_center.py tartalma"
}}
"""

    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.1, max_tokens=4096)
    raw = re.sub(r'^```json|```$', '', response.choices[0].message.content.strip())
    data = json.loads(raw)

    if data.get("new_code"):
        execute_code_change(data["new_code"], task)

    eni_agi.process(task)
    return data
