import json
import os
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
AUDIT_FILE = "llm_audit_trail.json"

def log_llm_interaction(purpose: str, input_text: str, output_text: str, decision_influenced: bool = False):
    record = {
        "session_id": hashlib.sha256(f"{datetime.now().isoformat()}{input_text}".encode()).hexdigest()[:24],
        "timestamp": datetime.now().isoformat(),
        "purpose": purpose,
        "input_hash": hashlib.sha3_512(input_text.encode()).hexdigest(),
        "output_hash": hashlib.sha3_512(output_text.encode()).hexdigest(),
        "input_summary": input_text[:300],
        "output_summary": output_text[:300],
        "decision_influenced": decision_influenced,
        "model": "llama-3.3-70b-versatile"
    }
    try:
        if os.path.exists(AUDIT_FILE):
            with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(record)
        with open(AUDIT_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        logger.info(f"Audit Trail: {record['session_id']}")
    except Exception as e:
        logger.error(f"Audit hiba: {e}")
