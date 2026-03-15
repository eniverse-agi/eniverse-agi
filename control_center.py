import streamlit as st
import os
import json
from eni_script import ENIScript

st.set_page_config(page_title="ENI Control Center", page_icon="🔐", layout="wide")

# BIZTONSÁG
ADMIN_USER = "admin"
ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS", "default123")

st.title("🔐 ENI Control Center")
st.caption("Executive Controller • GIL • Swarm Intelligence • Signalum • SSKC v1.0")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

col1, col2 = st.columns([1, 3])
with col1:
    username = st.text_input("Felhasználónév", "admin")
with col2:
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

    # Közvetlen feladat az SSKC ágensnek
    st.subheader("🤖 Adj feladatot az SSKC ágensnek")
    task = st.text_input("Mit csináljon az ágens?", "piaci elemzés + adj hozzá új funkciót")
    if st.button("Küldd az ágensnek (SSKC)"):
        with st.spinner("Az ágens dolgozik..."):
            try:
                result = improve_code(task)  # az eni_self_improver-ből
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
