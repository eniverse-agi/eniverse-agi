import streamlit as st
import os
from eni_utils import improve_code
from agi_core import eni_agi

st.set_page_config(page_title="ENI Control Center", layout="wide")
st.title("🌌 ENI Control Center – v3.4 AGI MAG")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.text_input("Jelszó", type="password") == os.environ.get("ENI_ADMIN_PASS"):
    st.session_state.logged_in = True

if st.session_state.logged_in:
    task = st.chat_input("Írd be a feladatot")
    if task:
        result = improve_code(task)
        st.write("**Plan:**", result.get("plan"))
        st.write("**Awareness:**", eni_agi.atman.awareness_level)
        st.code(result.get("new_code", "Nincs új kód"), language="python")
else:
    st.warning("Add meg a jelszót")
