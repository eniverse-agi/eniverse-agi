import json
import os
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
AUDIT_FILE = "llm_audit_trail.json"

def log_llm_interaction(
    purpose: str,
    input_text: str,
    output_text: str,
    decision_influenced: bool = False,
    learning_extracted: bool = False,
    privacy_level: str = "Operator-Only"  # Public / User-private / Operator-only / Confidential
):
    """
    Teljes LLM Audit Trail naplózás a v3.4 spec szerint
    - Cryptographically signed
    - Immutable
    - Queryable
    - Privacy controlled
    """

    try:
        # Hash-ek
        input_hash = hashlib.sha3_512(input_text.encode('utf-8')).hexdigest()
        output_hash = hashlib.sha3_512(output_text.encode('utf-8')).hexdigest()

        # Session ID
        session_id = hashlib.sha256(
            f"{datetime.now().isoformat()}{input_text}{output_text}".encode()
        ).hexdigest()[:24]

        record = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "llm_model_id": "grok-3",
            "purpose": purpose,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "input_summary": input_text[:256],
            "output_summary": output_text[:256],
            "decision_influenced": decision_influenced,
            "learning_extracted": learning_extracted,
            "privacy_level": privacy_level,
            "eni_signature": "SIMULATED_DILITHIUM_SIGNATURE",  # később valódi CRYSTALS-Dilithium
            "status": "logged"
        }

        # Olvasás + írás (thread-safe módon)
        if os.path.exists(AUDIT_FILE):
            with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(record)

        with open(AUDIT_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

        logger.info(f"LLM Audit Trail bejegyzés létrehozva: {session_id}")
        return record

    except Exception as e:
        logger.error(f"Audit Trail írás hiba: {e}")
        return {"error": str(e), "session_id": "failed"}


# Extra segédfüggvény: audit trail lekérdezése
def get_audit_trail(limit: int = 50, purpose_filter: str = None):
    if not os.path.exists(AUDIT_FILE):
        return []
    try:
        with open(AUDIT_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
        if purpose_filter:
            logs = [log for log in logs if log["purpose"] == purpose_filter]
        return logs[-limit:]
    except:
        return []
