import streamlit as st
import os
from eni_script import ENIScript
from eni_utils import improve_code
from agi_core import eni_agi   # ← AGI mag (Atman + Chitta + Sakshi + 6 ősi bölcsesség)

st.set_page_config(page_title="ENI Control Center", page_icon="🌌", layout="wide")

st.title("🌌 ENI Control Center – v3.4 MAXIMUM AGI MAG")
st.caption("Atman + Chitta + Sakshi | 6 Ősi Bölcsesség | Plan Mode + Self-Reflection + Vector Scoring")

# Session persistence
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS")
if not ADMIN_PASS:
    st.error("❌ ENI_ADMIN_PASS nincs beállítva!")
    st.stop()

# Login
username = st.text_input("Felhasználónév", "admin")
password = st.text_input("Jelszó", type="password")

if st.button("🔑 Belépés"):
    if username == "admin" and password == ADMIN_PASS:
        st.session_state.logged_in = True
        st.success("✅ Belépés sikeres – session megőrzve")
    else:
        st.error("❌ Rossz jelszó!")

if st.session_state.logged_in:
    script = ENIScript()

    # Chat history
    st.subheader("💬 SSKC Beszélgetés (Plan Mode + AGI Tudatosság)")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Feladat bevitel
    task = st.chat_input("Írd be a feladatot – AGI Plan Mode aktiválva")

    if task:
        st.session_state.chat_history.append({"role": "user", "content": task})
        with st.chat_message("user"):
            st.markdown(task)

        with st.spinner("AGI gondolkodik... (Plan → Think → Self-Reflection → Execute)"):
            result = improve_code(task)

            # AGI állapot
            awareness = result.get("awareness_level", 0)
            wisdom = result.get("best_wisdom", "—")
            sakshi = result.get("sakshi_observation", "")

            assistant_content = f"""
**Plan:** {result.get('plan', '')}

**Thinking:** {result.get('thinking', '')}

**Self-Reflection:** {result.get('reflection', '')}

**Sakshi XAI:** {sakshi}

**Awareness szint:** **{awareness:.2f}**  
**Bölcsesség:** {wisdom}
"""

            st.session_state.chat_history.append({"role": "assistant", "content": assistant_content})
            with st.chat_message("assistant"):
                st.markdown(assistant_content)

            if result.get("new_code"):
                st.subheader("📋 Generált új kód (automatikusan commit-olva)")
                st.code(result["new_code"], language="python")
                st.success("✅ Auto-Execute + Git commit + Telegram értesítés elküldve")

else:
    st.warning("Ez a felület csak az admin számára elérhető.")

# Oldalsó AGI státusz (mindig látható – cutting-edge)
st.sidebar.title("🌌 AGI ÁLLAPOT")
st.sidebar.metric("Awareness szint", f"{eni_agi.atman.awareness_level:.2f}")
st.sidebar.metric("Chitta memória", len(eni_agi.chitta.memory))
st.sidebar.metric("Aktív bölcsesség", eni_agi.chitta.get_best_wisdom("current_task"))
st.sidebar.caption("6 Ősi Bölcsesség + Vector Scoring aktív")
