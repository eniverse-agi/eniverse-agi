class ENIScript:
    def __init__(self):
        self.memory = {}

    def execute(self, command: str):
        parts = command.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "eni.think":
            return f"🧠 Swarm Intelligence Core aktiválva: {args}"
        elif cmd == "eni.consensus":
            return f"⛓️ PoI Mesh konszenzus: {args}"
        elif cmd == "eni.reward":
            parts = args.split(",")
            if len(parts) != 2:
                return "❌ Hibás formátum! Használat: eni.reward agent_neve,pontok"
            agent, pts_str = parts
            try:
                pts = int(pts_str.strip())
            except ValueError:
                return "❌ Hiba: a pontok számnak kell lennie!"
            self.memory[agent.strip()] = self.memory.get(agent.strip(), 0) + pts
            return f"💰 Intelligence Bonding: {agent.strip()} +{pts} pont"
        elif cmd == "eni.report":
            return f"📊 XAI jelentés + LLM Audit Trail kész"
        else:
            return f"✅ ENI Script végrehajtva: {command}"
