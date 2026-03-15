import os
import json
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def improve_code(task: str):
    with open("control_center.py", "r") as f:
        current_code = f.read()

    prompt = f"""
    Te vagy az ENI SSKC Self-Improvement Agent (v3.4 spec szerint).
    Feladat: {task}
    Aktuális control_center.py kód:
    {current_code[:6000]}

    Dönts:
    1. Melyik fájlba írd a javítást (vagy hozz létre újat)
    2. Írd meg a teljes javított kódot
    3. Ha elakadsz: magyarázd el magyarul miért, és mit kérek az embertől
    Válasz JSON formátumban: {{"file": "control_center.py", "code": "...", "explanation": "...", "blockage": "..." }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=4000
    )
    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    result = improve_code("Adjunk hozzá Blockage Report panelt és magyarázatot ha elakadok")
    print(json.dumps(result, ensure_ascii=False, indent=2))
