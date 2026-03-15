import streamlit as st
import os
import json
import re
from groq import Groq
from eni_script import ENIScript

client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="ENI Control Center", page_icon="🔐", layout="wide")

# BIZTONSÁG
ADMIN_USER = "admin"
ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS", "default123")

st.title("🔐 ENI Control Center")
st.caption("Executive Controller • GIL • Swarm Intelligence • Signalum • SSKC v1.0")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Felhasználónév", "admin")
password = st.text_input("Jelszó", type="password")

if st.button("🔑 Belépés"):
    if username == ADMIN_USER and password == ADMIN_PASS:
        st.session_state.logged_in = True
        st.success("✅ Belépés sikeres – most már csak te irányítasz!")
    else:
        st.error("❌ Rossz jelszó!")

if st.session_state.logged_in:
    script = ENIScript()

    st.subheader("📊 Aktuális állapot")
    st.info("Signalum Risk Level: **R0** | Swarm: 7 ágens aktív | LLM Audit: élő")

    # Normál parancs
    command = st.text_input("ENI Script parancs", "eni.think piaci elemzés")
    if st.button("🚀 Végrehajt"):
        result = script.execute(command)
        st.success(result)

    # KÖZVETLEN FELADAT AZ ÁGENSNEK (real-time)
    st.subheader("🤖 Adj feladatot az SSKC ágensnek")
    task = st.text_input("Mit csináljon az ágens?", "piaci elemzés + adj hozzá új funkciót")
    if st.button("Küldd az ágensnek (real-time)"):
        with st.spinner("Az ágens dolgozik..."):
            try:
                result = improve_code(task)
                st.success("✅ " + result.get("explanation", "Nincs magyarázat"))
                if result.get("blockage"):
                    st.warning("⚠️ Blockage: " + result["blockage"])
            except Exception as e:
                st.error(f"Hiba: {str(e)}")

    if st.button("🔴 Circuit Breaker ON"):
        st.error("⚠️ Minden folyamat leállítva!")

    st.caption("Minden döntés naplózva az LLM Audit Trail-be.")
else:
    st.warning("Ez a felület csak az admin számára elérhető.")

# === AZ LLM FÜGGVÉNY (közvetlenül itt) ===
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

Válasz **CSAK** érvényes JSON formátumban:
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
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    clean = json_match.group(0) if json_match else '{"explanation": "Nem kaptam tiszta JSON-t", "blockage": "' + raw[:300] + '"}'

    try:
        return json.loads(clean)
    except:
        return {"explanation": "JSON parse hiba", "blockage": raw[:500]}
