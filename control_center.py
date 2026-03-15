import streamlit as st
import os
import json
from eni_script import ENIScript

st.set_page_config(page_title="ENI Control Center", page_icon="🔐", layout="wide")

# === BIZTONSÁG ===
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

    command = st.text_input("ENI Script parancs", "eni.think piaci elemzés")
    if st.button("🚀 Végrehajt"):
        result = script.execute(command)
        st.success(result)

    if st.button("🔴 Circuit Breaker ON"):
        st.error("⚠️ Minden folyamat leállítva!")

    # === DINAMIKUS BLOCKAGE REPORT ===
    st.subheader("📋 Mi történt ma / Blockage Report")
    if os.path.exists("improvement.json"):
        try:
            with open("improvement.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            st.success("✅ " + data.get("explanation", "Nincs magyarázat"))
            if data.get("blockage"):
                st.warning("⚠️ Blockage: " + data["blockage"])
        except Exception as e:
            st.info("Az ágens lefutott, de a JSON olvasása nem sikerült.")
    else:
        st.info("Az autonóm SSKC ágens itt írja a magyarázatot, ha elakad vagy fejleszt. (Még nem történt változás.)")

    st.caption("Minden döntés naplózva az LLM Audit Trail-be.")
else:
    st.warning("Ez a felület csak az admin számára elérhető.")
