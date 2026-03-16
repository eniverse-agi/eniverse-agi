import os
import requests
import logging
from datetime import datetime
from agi_core import eni_agi
from wisdom_engine import wisdom_engine
from meta_cognition import meta_cognition

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message: str, importance: str = "normal"):
    """
    ENI AGI Telegram Notifier v3.4 MAXIMUM
    - AGI Awareness
    - Wisdom Engine + Meta-Cognition
    - Rich HTML + Sakshi XAI + Drift detection
    """
    if not BOT_TOKEN or not CHAT_ID:
        logger.warning("Telegram token vagy chat_id hiányzik")
        return False

    try:
        awareness = eni_agi.atman.awareness_level
        best_wisdom = wisdom_engine.get_best_wisdom(message)
        meta_status = meta_cognition.get_meta_status()
        drift = meta_cognition.reflection_history[-1]["drift_detected"] if meta_cognition.reflection_history else False

        prefix = {"critical": "🚨", "success": "✅", "info": "🌌"}.get(importance, "📡")

        full_message = f"""
<b>{prefix} ENI AGI Értesítés</b>

Awareness: <b>{awareness:.2f}</b>
Bölcsesség: <b>{best_wisdom}</b>
Meta-Confidence: <b>{meta_status.split('Confidence:')[1].split('|')[0] if 'Confidence' in meta_status else 'N/A'}</b>
Drift detected: {'✅ Igen' if drift else '❌ Nem'}

{message}

<i>Sakshi XAI megfigyelés:</i> {eni_agi.sakshi.observe("Telegram", message[:100], best_wisdom)}
        """

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": full_message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Telegram értesítés elküldve (awareness: {awareness:.2f})")
        return True
    except Exception as e:
        logger.error(f"Telegram küldési hiba: {e}")
        return False
