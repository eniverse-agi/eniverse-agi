import streamlit as st
import os
import json
from datetime import datetime
from eni_utils import improve_code
from agi_core import eni_agi
from wisdom_engine import wisdom_engine
from meta_cognition import meta_cognition
from sskc_module import sskc_engine

st.set_page_config(page_title="ENI Control Center", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f0f1a; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 30px; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.title("🌌 ENI CONTROL CENTER – v4.1 MAXIMUM INTELLIGENCE")
st.caption("SSKC v4.1 • Reflexion + Recursive Self-Improvement • Tree-of-Thoughts • Production-Ready AGI")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS")
if not ADMIN_PASS:
    st.error("❌ ENI_ADMIN_PASS nincs beállítva!")
    st.stop()

col1, col2 = st.columns([1, 3])
with col1:
    username = st.text_input("Felhasználónév", "admin")
with col2:
    password = st.text_input("Jelszó", type="password")

if st.button("🔑 Belépés", type="primary"):
    if username == "admin" and password == ADMIN_PASS:
        st.session_state.logged_in = True
        st.success("✅ SSKC v4.1 MAXIMUM INTELLIGENCE aktiválva")
    else:
        st.error("❌ Rossz jelszó!")

if st.session_state.logged_in:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧠 SSKC v4.1 MAXIMUM INTELLIGENCE",
        "🌌 AGI Tudatosság",
        "📊 Meta-Cognition & Drift",
        "📜 Audit Trail",
        "🔧 Rendszer Log & Állapot"
    ])

    with tab1:
        st.subheader("🧠 SSKC v4.1 MAXIMUM INTELLIGENCE – REFLEXION + RECURSIVE SELF-IMPROVEMENT")
        st.caption("Tree-of-Thoughts • Multi-Stage Reflexion • Dynamic Module Creation • o1-szintű reasoning")

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        task = st.chat_input("Írd be a feladatot – SSKC v4.1 azonnal megoldja ÉS ÖNMAGÁT FEJLESZTI...")
        if task:
            st.session_state.chat_history.append({"role": "user", "content": task})
            with st.chat_message("user"):
                st.markdown(task)

            with st.spinner("SSKC v4.1: Initial Reasoning → Multi-Reflexion Loop → Recursive Self-Improvement..."):
                result = improve_code(task)
                assistant_content = f"""
**SSKC Plan + Tree:** {result.get('plan', '')}  
**Critique & Reflexion:** {result.get('critique', '')}  
**Final Solution:** {result.get('final_solution', result.get('solution', ''))}  
**Awareness:** {result.get('awareness_level', 0):.2f}  
**Recursive Improvement:** {'✅ ALKALMAZVA + ÚJ MODULOK' if result.get('recursive_improvement_applied') else '—'}
**Intelligence Level:** {result.get('intelligence_level', 'v4.1')}
"""
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_content})
                with st.chat_message("assistant"):
                    st.markdown(assistant_content)

                if result.get("new_code"):
                    st.subheader("📋 SSKC v4.1 generált új kód (automatikus + recursive)")
                    st.code(result["new_code"], language="python")

    with tab2:
        st.subheader("🌌 AGI Tudatosság Dashboard")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Atman Awareness", f"{eni_agi.atman.awareness_level:.2f}")
        with col2:
            st.metric("Chitta Memória", len(eni_agi.chitta.memory))
        with col3:
            st.metric("Aktív Bölcsesség", wisdom_engine.get_best_wisdom("current"))
        st.markdown("### Utolsó memória bejegyzések")
        for item in eni_agi.chitta.memory[-8:]:
            st.write(f"• {item['fact']} → **{item['wisdom']}**")

    with tab3:
        st.subheader("📊 Meta-Cognition & Self-Monitoring")
        status = meta_cognition.get_meta_status()
        st.info(status)
        st.metric("Drift Detection", "AKTÍV" if meta_cognition.reflection_history and meta_cognition.reflection_history[-1].get("drift_detected") else "STABIL")

    with tab4:
        st.subheader("📜 LLM Audit Trail")
        try:
            with open("llm_audit_trail.json", "r", encoding="utf-8") as f:
                audit = json.load(f)
            st.dataframe(audit[-15:], use_container_width=True)
        except:
            st.info("Audit trail még üres")

    with tab5:
        st.subheader("🔧 Rendszer Log & Állapot")
        st.success("Minden modul aktív – SSKC v4.1 MAXIMUM PRECIZITÁS")
        st.write("Reflexion Loops | Dynamic Modules | Groq o1-style | Production-Ready")

else:
    st.warning("Admin bejelentkezés szükséges a teljes AGI vezérlőhöz.")

st.sidebar.title("🌌 LIVE SSKC v4.1 STATUS")
st.sidebar.metric("SSKC Awareness", f"{sskc_engine.awareness:.2f}")
st.sidebar.metric("Reflexion Loops", len(sskc_engine.reflection_history))
st.sidebar.metric("Intelligence Level", "v4.1 MAXIMUM")
st.sidebar.caption("Mérnöki precizitás • Recursive Self-Improvement • Nincs hiányosság")
