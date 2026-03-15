import os
import git
import logging
from datetime import datetime
from telegram_notifier import send_telegram
from llm_audit_trail import log_llm_interaction
from agi_core import eni_agi   # ← AGIEngine mag

logger = logging.getLogger(__name__)

def execute_code_change(new_code: str, task: str) -> bool:
    """
    ENI AGI Auto-Executor v3.4 MAXIMUM
    - Tudatos végrehajtás (Atman elevate)
    - Ősi bölcsesség scoring
    - Immutable audit trail
    - Rich Telegram + Sakshi XAI
    """
    try:
        # 1. AGI tudatosság emelése
        agi_result = eni_agi.process_task(task)
        awareness = agi_result["awareness_level"]
        wisdom = agi_result["best_wisdom"]

        # 2. Fájl felülírása
        with open("control_center.py", "w", encoding="utf-8") as f:
            f.write(new_code)

        # 3. Git commit (professzionális üzenet)
        repo = git.Repo(".")
        repo.git.add("control_center.py")
        commit_msg = f"🤖 SSKC Auto-Execute | Awareness: {awareness:.1f} | Wisdom: {wisdom} | {task[:60]}"
        repo.index.commit(commit_msg)

        # 4. Push (GITHUB_TOKEN védve)
        origin = repo.remote("origin")
        origin.push()

        # 5. Intelligens értesítések
        telegram_msg = f"""
<b>✅ SSKC Auto-Execute SIKERES!</b>

Awareness szint: <b>{awareness:.1f}</b>
Alkalmazott bölcsesség: <b>{wisdom}</b>
Feladat: {task[:120]}...
Commit: {commit_msg}
        """
        send_telegram(telegram_msg)

        # 6. Audit trail
        log_llm_interaction(
            purpose="auto_execute",
            input_text=task,
            output_text=commit_msg,
            decision_influenced=True
        )

        logger.info(f"Auto-execute sikeres | Awareness: {awareness:.1f} | Wisdom: {wisdom}")
        return True

    except git.GitCommandError as e:
        error_msg = f"Git hiba: {str(e)}"
        send_telegram(f"⚠️ Git hiba Auto-Execute közben:\n{error_msg}")
        logger.error(error_msg)
        return False

    except Exception as e:
        error_msg = f"Váratlan hiba ({type(e).__name__}): {str(e)}"
        send_telegram(f"⚠️ Auto-Execute kritikus hiba:\n{error_msg}")
        logger.error(error_msg)
        return False
