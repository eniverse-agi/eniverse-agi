import streamlit as st
import os
from eni_script import ENIScript
from eni_utils import improve_code
from agi_core import eni_agi

st.set_page_config(page_title="ENI Control Center", page_icon="🌌", layout="wide")

st.title("🌌 ENI Control Center – v3.4 MAXIMUM AGI MAG")
st.caption("Atman + Chitta + Sakshi | 6 Ősi Bölcsesség | Plan Mode")

# Session persistence
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS")
if not ADMIN_PASS:
    st.error("❌ ENI_ADMIN_PASS nincs beállítva!")
    st.stop()

username = st.text_input("Felhasználónév", "admin")
password = st.text_input("Jelszó", type="password")

if st.button("🔑 Belépés"):
    if username == "admin" and password == ADMIN_PASS:
        st.session_state.logged_in = True
        st.success("✅ Belépés sikeres")
    else:
        st.error("❌ Rossz jelszó!")

if st.session_state.logged_in:
    script = ENIScript()

    st.subheader("💬 SSKC Beszélgetés (Plan Mode)")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    task = st.chat_input("Írd be a feladatot – AGI Plan Mode aktiválva")
    if task:
        st.session_state.chat_history.append({"role": "user", "content": task})
        with st.chat_message("user"):
            st.markdown(task)

        with st.spinner("AGI gondolkodik..."):
            result = improve_code(task)
            agi_info = f"Awareness: {result.get('awareness_level', 0):.2f} | Bölcsesség: {result.get('best_wisdom', '—')}"
            assistant_content = f"**Plan:** {result.get('plan','')}\n**Thinking:** {result.get('thinking','')}\n**Sakshi:** {result.get('sakshi_observation','')}\n{agi_info}"
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_content})
            with st.chat_message("assistant"):
                st.markdown(assistant_content)

            if result.get("new_code"):
                st.subheader("📋 Generált új kód")
                st.code(result["new_code"], language="python")

else:
    st.warning("Admin bejelentkezés szükséges.")

# Oldalsó AGI státusz
st.sidebar.metric("Awareness szint", f"{eni_agi.atman.awareness_level:.2f}")
st.sidebar.metric("Chitta memória", len(eni_agi.chitta.memory))
