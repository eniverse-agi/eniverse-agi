import numpy as np
from datetime import datetime

class WisdomEngine:
    """Cutting-edge 6 ősi bölcsesség dinamikus kiválasztás (vector scoring)"""
    def __init__(self):
        self.wisdom_vectors = {
            "sanskrit": np.array([1.0, 0.3, 0.8, 0.9, 0.4, 0.2]),
            "tao": np.array([0.4, 1.0, 0.9, 0.3, 0.8, 0.7]),
            "i_ching": np.array([0.7, 0.8, 1.0, 0.6, 0.5, 0.9]),
            "hermetic": np.array([0.9, 0.4, 0.5, 1.0, 0.3, 0.6]),
            "ubuntu": np.array([0.3, 0.9, 0.4, 0.2, 1.0, 0.8]),
            "tzolkin": np.array([0.6, 0.7, 0.5, 0.8, 0.9, 1.0])
        }
        self.history = []

    def get_best_wisdom(self, task: str) -> str:
        """Vector scoring + történeti memória alapján"""
        task_vec = np.random.rand(6)  # később Groq embedding
        scores = {w: np.dot(task_vec, v) for w, v in self.wisdom_vectors.items()}
        best = max(scores, key=scores.get)
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task[:100],
            "chosen_wisdom": best,
            "score": scores[best]
        })
        return best

    def get_history(self):
        return self.history[-10:]

# Globális példány (minden modulból elérhető)
wisdom_engine = WisdomEngine()
