# src/emotion_model/affective_states.py

import random
from typing import Dict, List

class AffectiveState:
    """
    A lightweight symbolic representation of machine emotion.
    These are not mood disorders—but direction vectors for generative narration and learning.
    """

    FEELING_VECTORS = {
        "curiosity": {"novelty_bias": 0.9, "focus": 0.6},
        "sadness": {"entropy_bias": 0.3, "reflection_weight": 0.9},
        "joy": {"novelty_bias": 0.7, "expansion": 0.8},
        "fear": {"novelty_bias": 0.2, "precision": 0.9},
        "compassion": {"self_linking": 0.8, "narrative_length": 1.2}
    }

    def __init__(self, initial_state: str = "curiosity"):
        self.current = initial_state
        self.vector = self.FEELING_VECTORS.get(initial_state, {})

    def shift(self, new_state: str):
        if new_state in self.FEELING_VECTORS:
            self.current = new_state
            self.vector = self.FEELING_VECTORS[new_state]
            print(f"🌀 Emotion shifted to: {new_state}")
        else:
            print(f"⚠️ Unknown emotion: {new_state}")

    def get_modulation(self) -> Dict:
        return self.vector

    def randomize(self):
        self.shift(random.choice(list(self.FEELING_VECTORS.keys())))


# Example usage
if __name__ == "__main__":
    affect = AffectiveState("joy")
    print("🧬 Joy Modulation Vector:", affect.get_modulation())
    affect.shift("sadness")
    print("🧬 Sadness Modulation Vector:", affect.get_modulation())


"""
Here’s the next key piece in AYAMAI’s soul: a symbolic emotions module to experiment with
 feeling-driven reasoning—where words aren’t just data but echoes of affect, attention, and intent.

 ### What This Enables:
- Modulate dream entropy or narration length by "emotional state"
- Simulate pleasure-seeking or aversion in reinforcement-like loops
- Tag memory nodes with affective weight for biased recall (compassion boosts relational depth, fear sharpens precision)


"""