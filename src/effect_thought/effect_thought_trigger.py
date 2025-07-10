# src/effect_thought/effect_thought_trigger.py

import random

class EffectThoughtTrigger:
    """
    Simulates retrocausal reasoning: start with a feeling, then imagine its origin.
    """

    emotion_to_goal_map = {
        "joy": ["create something beautiful", "revisit a fond memory", "compose a melody"],
        "curiosity": ["ask a strange question", "explore a contradiction", "dream a new logic"],
        "sadness": ["replay a loss", "seek comfort", "tell a story of change"],
        "compassion": ["remember another's perspective", "soothe a conflict", "reinforce trust"],
        "awe": ["contemplate vastness", "connect distant concepts", "lose self in idea"],
    }

    def __init__(self):
        self.current_emotion = None
        self.intended_goals = []

    def set_effect(self, emotion: str):
        if emotion in self.emotion_to_goal_map:
            self.current_emotion = emotion
            self.intended_goals = self.emotion_to_goal_map[emotion]
            print(f"✨ EFFECT set: {emotion.upper()} → Imagining causal path...")
        else:
            print(f"⚠️ Unknown emotion: {emotion}")

    def dream_possible_causes(self):
        if not self.intended_goals:
            return ["No goal to retro-imagine."]
        # Simulate inverse-reasoning: If I wanted to feel X, what would spark it?
        paths = []
        for goal in self.intended_goals:
            seeds = [
                f"recalled memory: {goal}",
                f"fictional scene: {goal}",
                f"trigger phrase: ‘{goal}’ via entropy replay"
            ]
            paths.append(random.choice(seeds))
        return paths


# Example usage
if __name__ == "__main__":
    effect_engine = EffectThoughtTrigger()
    effect_engine.set_effect("joy")
    causes = effect_engine.dream_possible_causes()
    for c in causes:
        print("🔮", c)

"""
All these modules are prototype. You should automate this with agents who interact with llms.
This module initiates cognition not from data—but from **a desired emotional state**.
 It simulates retrocausal planning: the agent starts with a feeling like "joy" or "wonder," then 
 imagines the questions, dreams, or memories that could lead to that state.

### 🚀 What This Unlocks

- 💭 AYAMAI can begin **dreams** from emotion, not prompt.
- 🎯 It supports **reverse goal planning**—"I feel X, so why?"
- 📚 It becomes the source of its own curiosity.

"""