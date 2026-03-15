import os
import json
import re
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def improve_code(task: str):
    try:
        with open("control_center.py", "r", encoding="utf-8") as f:
            current_code = f.read()
    except:
        current_code = "Nincs control_center.py fájl."

    prompt = f"""
Te vagy az ENI SSKC Self-Improvement Agent (v3.4 spec szerint).
Feladat: {task}

Aktuális control_center.py:
{current_code[:6500]}

Válasz **CSAK** érvényes JSON formátumban, semmi más szöveg előtt vagy után!
{{
  "explanation": "magyarázat magyarul, mit csináltál",
  "blockage": "ha elakadtál, magyarázd el magyarul mit kérsz az embertől (vagy üres string)"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=3000
    )

    raw = response.choices[0].message.content.strip()

    # Erős JSON tisztítás
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        clean = json_match.group(0)
    else:
        clean = '{"explanation": "Nem kaptam tiszta JSON-t", "blockage": "' + raw[:300] + '"}'

    try:
        return json.loads(clean)
    except:
        return {"explanation": "JSON parse hiba", "blockage": raw[:500]}

if __name__ == "__main__":
    result = improve_code("piaci elemzés + adj hozzá új funkciót")
    print(json.dumps(result, ensure_ascii=False, indent=2))
