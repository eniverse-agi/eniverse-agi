class ENIScript:
    def execute(self, command: str):
        if command.startswith("eni.think"):
            return f"✅ Gondolkodás indítva: {command[10:]}"
        return f"✅ Parancs végrehajtva: {command}"
