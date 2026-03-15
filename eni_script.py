import json
from datetime import datetime

class ENIScript:
    def __init__(self):
        self.history = []  # Audit trail támogatáshoz

    def execute(self, command: str) -> str:
        cmd = command.strip().lower()
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "status": "executed"
        })

        if cmd.startswith("eni.think"):
            result = f"🧠 Gondolkodás elindítva: {command[10:].strip()}"
        
        elif cmd.startswith("eni.consensus"):
            result = f"🤝 Konszenzus kezdeményezve: {command[13:].strip()}"
        
        elif cmd.startswith("eni.reward"):
            try:
                parts = command[11:].strip().split(",")
                agent = parts[0].strip()
                points = int(parts[1].strip())
                result = f"🏆 Jutalmazás: {agent} kapott {points} pontot"
            except:
                result = "⚠️ Hibás reward formátum (pl. eni.reward agent,10)"
        
        elif cmd.startswith("eni.act"):
            result = f"⚡ Akció végrehajtva: {command[8:].strip()}"
        
        elif cmd.startswith("eni.report"):
            result = f"📋 Jelentés kész: {command[11:].strip()}"
        
        elif cmd.startswith("eni.improve"):
            result = f"🔧 Önfejlesztés indítva: {command[12:].strip()}"
        
        else:
            result = f"✅ Parancs végrehajtva: {command}"

        # Audit trail naplózás (a rendszer automatikusan használja)
        self._log_audit(command, result)
        return result

    def _log_audit(self, command: str, result: str):
        """Belső audit trail támogatás"""
        try:
            with open("llm_audit_trail.json", "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "type": "eni_script",
            "command": command,
            "result": result[:200]
        })
        
        with open("llm_audit_trail.json", "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def get_history(self):
        """Későbbi használatra (pl. chat history vagy Telegram összefoglaló)"""
        return self.history
