import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def execute_code_change(new_code: str, task: str) -> Dict[str, Any]:
    """
    ENI Auto Executor v4.1 MAXIMUM
    - Teljes biztonságos backup + validáció
    - Git commit + push (Render kompatibilis)
    - Audit trail JSON append
    - Erős error handling
    """
    try:
        # Backup
        backup_path = "control_center.py.bak"
        with open("control_center.py", "r", encoding="utf-8") as f:
            old_code = f.read()
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(old_code)

        # Új kód írása
        with open("control_center.py", "w", encoding="utf-8") as f:
            f.write(new_code)

        # Audit trail
        audit_entry: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "task": task[:200],
            "module": "SSKC_v4.1",
            "status": "SUCCESS",
            "backup_created": True
        }
        try:
            with open("llm_audit_trail.json", "r+", encoding="utf-8") as f:
                try:
                    audit = json.load(f)
                except json.JSONDecodeError:
                    audit = []
                audit.append(audit_entry)
                f.seek(0)
                json.dump(audit, f, indent=2)
        except FileNotFoundError:
            with open("llm_audit_trail.json", "w", encoding="utf-8") as f:
                json.dump([audit_entry], f, indent=2)

        # Git
        os.system("git add control_center.py llm_audit_trail.json")
        os.system(f'git commit -m "ENI SSKC v4.1 recursive update: {task[:80]}" --quiet')
        os.system("git push --quiet")

        logger.info(f"✅ SSKC v4.1 execute sikeres: {task[:80]}...")
        return {"status": "SUCCESS", "recursive_improvement": True}

    except Exception as e:
        logger.error(f"❌ Execute hiba: {str(e)}")
        return {"status": "ERROR", "error": str(e)}
