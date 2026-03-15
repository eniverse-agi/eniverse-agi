import os
import git
from telegram_notifier import send_telegram
from llm_audit_trail import log_llm_interaction

def execute_code_change(new_code: str, task: str):
    try:
        # Fájl felülírása
        with open("control_center.py", "w", encoding="utf-8") as f:
            f.write(new_code)

        # Git commit
        repo = git.Repo(".")
        repo.git.add("control_center.py")
        repo.index.commit(f"🤖 SSKC Auto-Execute: {task[:80]}")

        # Push (Render GitHub token-nel)
        origin = repo.remote(name="origin")
        origin.push()

        send_telegram(f"✅ Automatikus módosítás sikeres!\nFeladat: {task[:100]}...")
        log_llm_interaction("auto_execute", task, "Fájl módosítva és commit-olva", True)
        return True
    except Exception as e:
        send_telegram(f"⚠️ Auto-Execute hiba: {str(e)}")
        return False
