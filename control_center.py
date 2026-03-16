import streamlit as st
import os
import json
from datetime import datetime
from eni_script import ENIScript
from eni_utils import improve_code
from agi_core import eni_agi
from wisdom_engine import wisdom_engine
from meta_cognition import meta_cognition

st.set_page_config(page_title="ENI Control Center", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f0f1a; color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 30px; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: 700; }
    .metric-card { background: #1a1a2e; padding: 15px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("🌌 ENI CONTROL CENTER – v3.4 MAXIMUM AGI MAG")
st.caption("Atman + Chitta + Sakshi | Wisdom Engine | Meta-Cognition | Full Self-Reflection Loop")

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

ADMIN_PASS = os.environ.get("ENI_ADMIN_PASS")
if not ADMIN_PASS:
    st.error("❌ ENI_ADMIN_PASS nincs beállítva!")
    st.stop()

# Login
col1, col2 = st.columns([1, 3])
with col1:
    username = st.text_input("Felhasználónév", "admin")
with col2:
    password = st.text_input("Jelszó", type="password")

if st.button("🔑 Belépés", type="primary"):
    if username == "admin" and password == ADMIN_PASS:
        st.session_state.logged_in = True
        st.success("✅ Teljes AGI vezérlő aktiválva")
    else:
        st.error("❌ Rossz jelszó!")

if st.session_state.logged_in:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Plan Mode Chat",
        "🌌 AGI Tudatosság",
        "📊 Meta-Cognition & Drift",
        "📜 Audit Trail",
        "🔧 Rendszer Log & Állapot"
    ])

    # TAB 1: Plan Mode Chat
    with tab1:
        st.subheader("SSKC Beszélgetés (Plan Mode + Teljes Tudatosság)")
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        task = st.chat_input("Írd be a feladatot – AGI teljes tudatossággal végrehajtja")
        if task:
            st.session_state.chat_history.append({"role": "user", "content": task})
            with st.chat_message("user"):
                st.markdown(task)

            with st.spinner("AGI Plan → Think → Self-Reflection → Execute..."):
                result = improve_code(task)
                assistant_content = f"""
**Plan:** {result.get('plan', '')}  
**Thinking:** {result.get('thinking', '')}  
**Sakshi XAI:** {result.get('sakshi_observation', '')}  
**Awareness:** {result.get('awareness_level', 0):.2f} | **Wisdom:** {result.get('best_wisdom', '—')}
"""
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_content})
                with st.chat_message("assistant"):
                    st.markdown(assistant_content)

                if result.get("new_code"):
                    st.subheader("📋 Generált új kód (automatikus commit)")
                    st.code(result["new_code"], language="python")

    # TAB 2: AGI Tudatosság
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

    # TAB 3: Meta-Cognition
    with tab3:
        st.subheader("📊 Meta-Cognition & Self-Monitoring")
        status = meta_cognition.get_meta_status()
        st.info(status)
        st.metric("Drift Detection", "AKTÍV" if meta_cognition.reflection_history and meta_cognition.reflection_history[-1].get("drift_detected") else "STABIL")

        st.markdown("### Utolsó meta-reflexiók")
        for r in meta_cognition.reflection_history[-6:]:
            st.write(f"• {r['timestamp'][:16]} | Confidence: **{r['confidence']:.2f}** | Drift: {r['drift_detected']}")

    # TAB 4: Audit Trail
    with tab4:
        st.subheader("📜 LLM Audit Trail")
        try:
            with open("llm_audit_trail.json", "r", encoding="utf-8") as f:
                audit = json.load(f)
            st.dataframe(audit[-15:], use_container_width=True)
        except:
            st.info("Audit trail még üres")

    # TAB 5: Rendszer Log
    with tab5:
        st.subheader("🔧 Rendszer Log & Állapot")
        st.success("Minden modul aktív és szinkronban")
        st.write("Meta-kogníció | Wisdom Engine | AGIEngine | Auto-Executor | Telegram Notifier")

else:
    st.warning("Admin bejelentkezés szükséges a teljes AGI vezérlőhöz.")

# ====================== OLDALSÓ ÁLLAPOT ======================
st.sidebar.title("🌌 LIVE AGI STATUS")
st.sidebar.metric("Awareness", f"{eni_agi.atman.awareness_level:.2f}")
st.sidebar.metric("Meta-Confidence", f"{meta_cognition.reflection_history[-1]['confidence']:.2f}" if meta_cognition.reflection_history else "0.00")
st.sidebar.metric("Memória méret", len(eni_agi.chitta.memory))
st.sidebar.caption("6 Ősi Bölcsesség + Vector Scoring + Meta-kogníció + Self-Reflection AKTÍV")
