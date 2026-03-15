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
st.caption("Executive Controller • GIL • Swarm Intelligence • Signalum • SSKC v1.0")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

    st.subheader("📊 Aktuális állapot")
    st.info("Signalum Risk Level: **R0** | Swarm: 7 ágens aktív | LLM Audit: élő")

    command = st.text_input("ENI Script parancs", "eni.think piaci elemzés").strip()
    if st.button("🚀 Végrehajt"):
        if command:
            st.success(script.execute(command))

    st.subheader("🤖 Adj feladatot az SSKC ágensnek")
    task = st.text_input("Mit csináljon az ágens?", "Adj hozzá teljes 4-szintű XAI magyarázatot").strip()

    if st.button("Küldd az ágensnek"):
        if not task:
            st.error("❌ A feladat nem lehet üres!")
        else:
            with st.spinner("Az ágens dolgozik..."):
                result = improve_code(task)
                st.success("✅ " + result.get("explanation", "Nincs magyarázat"))

                if result.get("new_code"):
                    st.subheader("📋 Generált új kód (másold be control_center.py-ba)")
                    st.code(result["new_code"], language="python")

                if result.get("blockage"):
                    st.warning("⚠️ Blockage: " + result["blockage"])

    if st.button("🔴 Circuit Breaker ON"):
        st.error("⚠️ Minden folyamat leállítva!")
else:
    st.warning("Ez a felület csak az admin számára elérhető.")
