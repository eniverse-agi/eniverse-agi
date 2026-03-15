import streamlit as st
import os
import json
from eni_script import ENIScript
from eni_self_improver import improve_code

st.set_page_config(page_title="ENI Control Center", page_icon="🔐", layout="wide")

ADMIN_USER = "admin"
ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS", "default123")

st.title("🔐 ENI Control Center")
st.caption("Executive Controller • GIL • Swarm Intelligence • Signalum • SSKC")

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

    # Normál ENI Script parancs
    command = st.text_input("ENI Script parancs", "eni.think piaci elemzés")
    if st.button("🚀 Végrehajt"):
        result = script.execute(command)
        st.success(result)

    # === KÖZVETLEN FELADAT AZ ÁGENSNEK ===
    st.subheader("🤖 Adj feladatot az SSKC ágensnek")
    task = st.text_input("Mit csináljon az ágens?", "piaci elemzés + adj hozzá új funkciót")
    if st.button("Küldd az ágensnek"):
        with st.spinner("Az ágens dolgozik..."):
            result = improve_code(task)
            st.success("✅ " + result.get("explanation", "Nincs magyarázat"))
            if result.get("blockage"):
                st.warning("⚠️ Blockage: " + result["blockage"])

    if st.button("🔴 Circuit Breaker ON"):
        st.error("⚠️ Minden folyamat leállítva!")

    st.caption("Minden döntés naplózva az LLM Audit Trail-be.")
else:
    st.warning("Ez a felület csak az admin számára elérhető.")
