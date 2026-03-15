import os
import git
import logging
from datetime import datetime
from telegram_notifier import send_telegram
from llm_audit_trail import log_llm_interaction

logger = logging.getLogger(__name__)

def execute_code_change(new_code: str, task: str):
    """
    Intelligens, hibatűrő automatikus végrehajtó
    - Git commit + push
    - Telegram értesítés
    - Audit trail
    - Teljes kivételkezelés
    """
    try:
        # 1. Fájl felülírása
        with open("control_center.py", "w", encoding="utf-8") as f:
            f.write(new_code)

        # 2. Git commit (token-nel)
        repo = git.Repo(".")
        repo.git.add("control_center.py")
        commit_message = f"🤖 SSKC Auto-Execute [{datetime.now().strftime('%H:%M')}] - {task[:80]}"
        repo.index.commit(commit_message)

        # 3. Push (GITHUB_TOKEN-ból)
        with repo.git.custom_environment(GIT_ASKPASS="echo", GIT_USERNAME="ENI-SSKC-Agent", GIT_PASSWORD=os.environ.get("GITHUB_TOKEN", "")):
            origin = repo.remote(name="origin")
            origin.push()

        # 4. Értesítések
        success_msg = f"✅ Automatikus módosítás sikeres!\nFeladat: {task[:100]}\nCommit: {commit_message}"
        send_telegram(success_msg)
        log_llm_interaction("auto_execute", task, success_msg, True)

        logger.info(f"Auto-execute sikeres: {task[:50]}")
        return True

    except git.GitCommandError as e:
        error_msg = f"Git hiba: {str(e)}"
        send_telegram(f"⚠️ Git hiba Auto-Execute közben:\n{error_msg}")
        logger.error(error_msg)
        return False

    except Exception as e:
        error_msg = f"Váratlan hiba: {type(e).__name__} - {str(e)}"
        send_telegram(f"⚠️ Auto-Execute hiba: {error_msg}")
        logger.error(error_msg)
        return False
