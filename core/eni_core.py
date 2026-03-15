class Atman:
    """
    Atman represents the core consciousness of the AGI.
    """
    def __init__(self):
        self.awareness_level = 0

    def elevate_awareness(self):
        self.awareness_level += 1

    def get_awareness(self):
        return self.awareness_level

class Chitta:
    """
    Chitta refers to the memory and cognitive processing of the AGI.
    """
    def __init__(self):
        self.memory = []

    def store_memory(self, fact):
        self.memory.append(fact)

    def retrieve_memory(self):
        return self.memory

class Sakshi:
    """
    Sakshi serves as the observing layer of consciousness.
    """
    def __init__(self, atman):
        self.atman = atman

    def observe(self):
        return f"Current awareness level: {self.atman.get_awareness()}"

class AGIEngine:
    """
    The main AGI engine that integrates Atman, Chitta, and Sakshi.
    """
    def __init__(self):
        self.atman = Atman()
        self.chitta = Chitta()
        self.sakshi = Sakshi(self.atman)

    def process_information(self, fact):
        self.chitta.store_memory(fact)
        self.atman.elevate_awareness()

    def report(self):
        return self.sakshi.observe()

# Example of using the AGI Engine
if __name__ == "__main__":
    agi = AGIEngine()
    agi.process_information("Learning about consciousness.")
    print(agi.report())
