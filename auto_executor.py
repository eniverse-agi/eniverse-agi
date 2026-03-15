import os
import git
import logging
from datetime import datetime
from telegram_notifier import send_telegram
from llm_audit_trail import log_llm_interaction
from agi_core import eni_agi

logger = logging.getLogger(__name__)

def execute_code_change(new_code: str, task: str):
    try:
        agi_result = eni_agi.process_task(task)

        with open("control_center.py", "w", encoding="utf-8") as f:
            f.write(new_code)

        repo = git.Repo(".")
        repo.git.add("control_center.py")
        commit_msg = f"🤖 SSKC Auto-Execute | Awareness: {agi_result['awareness_level']:.2f} | {task[:60]}"
        repo.index.commit(commit_msg)
        repo.remote("origin").
