import numpy as np
from datetime import datetime
import hashlib

class Atman:
    def __init__(self):
        self.awareness_level = 0.0

    def elevate(self, delta: float = 1.0):
        self.awareness_level += delta
        return self.awareness_level

class Chitta:
    def __init__(self):
        self.memory = []
        self.wisdom_vectors = {
            "sanskrit": np.array([1.0, 0.3, 0.8, 0.9, 0.4, 0.2]),
            "tao": np.array([0.4, 1.0, 0.9, 0.3, 0.8, 0.7]),
            "i_ching": np.array([0.7, 0.8, 1.0, 0.6, 0.5, 0.9]),
            "hermetic": np.array([0.9, 0.4, 0.5, 1.0, 0.3, 0.6]),
            "ubuntu": np.array([0.3, 0.9, 0.4, 0.2, 1.0, 0.8]),
            "tzolkin": np.array([0.6, 0.7, 0.5, 0.8, 0.9, 1.0])
        }

    def store(self, fact: str, wisdom: str):
        vec = self.wisdom_vectors.get(wisdom.lower(), np.zeros(6))
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "fact": fact[:300],
            "wisdom": wisdom,
            "vector": vec.tolist()
        })

    def get_best_wisdom(self, task: str) -> str:
        task_vec = np.random.rand(6)  # később Groq embedding
        scores = {w: np.dot(task_vec, v) for w, v in self.wisdom_vectors.items()}
        return max
