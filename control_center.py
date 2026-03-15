import streamlit as st
import os
from eni_script import ENIScript
from eni_utils import improve_code

st.set_page_config(page_title="ENI Control Center", page_icon="🔐", layout="wide")

ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS")
if not ADMIN_PASS:
    st.error("❌ ENI_ADMIN_PASS nincs beállítva!")
    st.stop()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🔐 ENI Control Center")
st.caption("v2.0 – Teljes Autonóm Plan Mode")

# Login (session megőrzés)
username = st.text_input("Felhasználónév", "admin")
password = st.text_input("Jelszó", type="password")
if st.button("🔑 Belépés"):
    if username == "admin" and password == ADMIN_PASS:
        st.session_state.logged_in = True
        st.success("✅ Belépés – session megőrzve")

if st.session_state.logged_in:
    script = ENIScript()
    st.subheader("💬 SSKC Beszélgetés (Plan Mode)")
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    task = st.chat_input("Írd be a feladatot – az ágens automatikusan végrehajtja")
    if task:
        st.session_state.chat_history.append({"role": "user", "content": task})
        with st.spinner("Plan → Think → Execute..."):
            result = improve_code(task)
            st.session_state.chat_history.append({"role": "assistant", "content": f"**Plan:** {result.get('plan','')}\n**Thinking:** {result.get('thinking','')}\n**Result:** {result.get('explanation','')}"})
            st.chat_message("assistant").write(f"**Plan:** {result.get('plan','')}\n**Thinking:** {result.get('thinking','')}\n**Result:** {result.get('explanation','')}")
else:
    st.warning("Admin bejelentkezés szükséges")
