import numpy as np
from datetime import datetime

class MetaCognition:
    def __init__(self):
        self.reflection_history = []
        self.confidence_history = []

    def monitor(self, task: str, plan: str, thinking: str, reflection: str, result: str):
        confidence = min(0.95, len(plan) + len(thinking) + len(reflection) + len(result)) / 400
        self.confidence_history.append(confidence)
        drift = len(self.confidence_history) > 3 and (self.confidence_history[-1] - np.mean(self.confidence_history[-3:])) < -0.2
        self.reflection_history.append({"task": task[:80], "confidence": confidence, "drift": drift})
        return {"confidence": confidence, "drift_detected": drift}

meta_cognition = MetaCognition()
