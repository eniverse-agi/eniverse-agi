import os
import json
import re
import logging
from groq import Groq

# Logging beállítása
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

def read_code_snippet(filepath: str, max_chars: int = 6500) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(max_chars + 50)
            return content[:max_chars]
    except FileNotFoundError:
        logger.error(f"{filepath} fájl nem található")
        return "Nincs fájl."
    except IOError as e:
        logger.error(f"I/O hiba: {str(e)}")
        return "Fájl olvasási hiba."
    except Exception as e:
        logger.error(f"Váratlan hiba: {str(e)}")
        return "Hiba a fájl olvasása során."

def improve_code(task: str) -> dict:
    try:
        current_code = read_code_snippet("control_center.py")
    except Exception as e:
        logger.error(f"Kód beolvasás hiba: {str(e)}")
        return {"explanation": "Hiba a kód beolvasása során", "blockage": str(e)}

    prompt = f"""
Te vagy az ENI SSKC Self-Improvement Agent (v3.4 spec szerint).
Feladat: {task}

Aktuális control_center.py:
{current_code}

Válasz **CSAK** érvényes JSON formátumban, semmi más szöveg előtt vagy után!
{{
  "explanation": "magyarázat magyarul, mit csináltál",
  "blockage": "ha elakadtál, magyarázd el magyarul mit kérsz az embertől (vagy üres string)"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=3000
        )
        raw = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"LLM hiba: {str(e)}")
        return {"explanation": "LLM hívási hiba", "blockage": str(e)}

    # Robusztus JSON kinyerés
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        return {"explanation": "JSON parse hiba", "blockage": raw[:500]}
