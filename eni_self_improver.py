import os
import json
import re
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def improve_code(task: str):
    with open("control_center.py", "r", encoding="utf-8") as f:
        current_code = f.read()

    prompt = f"""
Te vagy az ENI SSKC Self-Improvement Agent (v3.4 spec szerint).
Feladat: {task}

Aktuális control_center.py:
{current_code[:7000]}

Válasz **CSAK** és kizárólag érvényes JSON formátumban, semmi más szöveg előtt vagy után!
JSON struktúra:
{{
  "file": "control_center.py vagy új fájlnév",
  "code": "a teljes javított kód itt",
  "explanation": "magyarázat magyarul",
  "blockage": "ha elakadtál, magyarázd el itt magyarul mit kérsz az embertől"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=4000
    )

    raw = response.choices[0].message.content.strip()

    # Biztonsági JSON kinyerés (ha extra szöveg van)
    try:
        # Keressük a legelső { és utolsó } közötti részt
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            clean_json = json_match.group(0)
            return json.loads(clean_json)
        else:
            return {"file": "control_center.py", "code": "", "explanation": "Nem kaptam tiszta JSON-t", "blockage": raw[:500]}
    except:
        return {"file": "control_center.py", "code": "", "explanation": "JSON hiba", "blockage": raw[:500]}

if __name__ == "__main__":
    result = improve_code("Adjunk hozzá jobb Blockage Report panelt és magyarázatot, ha elakadok")
    print(json.dumps(result, ensure_ascii=False, indent=2))
