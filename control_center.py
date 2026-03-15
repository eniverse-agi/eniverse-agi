import streamlit as st
import os
from eni_script import ENIScript
from eni_utils import improve_code

st.set_page_config(page_title="ENI Control Center", page_icon="🔐", layout="wide")

ADMIN_USER = "admin"
ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS")
if not ADMIN_PASS:
    st.error("❌ ENI_ADMIN_PASS nincs beállítva!")
    st.stop()

st.title("🔐 ENI Control Center")
st.caption("Executive Controller • GIL • Swarm Intelligence • Signalum • SSKC v2.0 – Plan Mode")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

username = st.text_input("Felhasználónév", "admin")
password = st.text_input("Jelszó", type="password")

if st.button("🔑 Belépés"):
    if username == ADMIN_USER and password == ADMIN_PASS:
        st.session_state.logged_in = True
        st.success("✅ Belépés sikeres!")
    else:
        st.error("❌ Rossz jelszó!")

if st.session_state.logged_in:
    script = ENIScript()

    # Chat history
    st.subheader("💬 Beszélgetés az SSKC ágenssel (Plan Mode)")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    task = st.chat_input("Mit csináljon az ágens? (Plan Mode aktiválva)")
    if task:
        st.session_state.chat_history.append({"role": "user", "content": task})
        st.chat_message("user").write(task)

        with st.spinner("Az ágens tervez, gondolkozik és végrehajt..."):
            result = improve_code(task)
            explanation = result.get("explanation", "Nincs magyarázat")
            new_code = result.get("new_code", "")

            st.session_state.chat_history.append({"role": "assistant", "content": f"**Plan:** {result.get('plan','')}\n**Thinking:** {result.get('thinking','')}\n**Result:** {explanation}"})
            st.chat_message("assistant").write(f"**Plan:** {result.get('plan','')}\n**Thinking:** {result.get('thinking','')}\n**Result:** {explanation}")

            if new_code:
                st.subheader("📋 Generált új kód (automatikusan commit-olva)")
                st.code(new_code, language="python")
                st.success("✅ Automatikus módosítás végrehajtva!")

            if result.get("blockage"):
                st.warning("⚠️ Blockage: " + result["blockage"])
else:
    st.warning("Ez a felület csak az admin számára elérhető.")
