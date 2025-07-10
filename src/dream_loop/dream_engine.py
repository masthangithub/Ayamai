# src/dream_loop/dream_engine.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

import random
import time
from utils.local_llm import LocalLLM

class DreamEngine:
    def __init__(self, memory_fragments, entropy=0.7, affective_bank=None, dream_mood=None, use_llm=True):
        """
        memory_fragments: List of basic concepts for entropy remix
        entropy: Float between 0 and 1 – controls remix surrealism
        affective_bank: Optional – AffectiveMemoryBank instance
        dream_mood: Optional – Filter emotional memory recall by mood tag
        """
        self.memory = memory_fragments
        self.entropy = entropy
        self.dream_log = []
        self.affective_bank = affective_bank
        self.dream_mood = dream_mood or random.choice(["curiosity", "joy", "awe"])
        self.use_llm = use_llm
        if use_llm:
            self.llm = LocalLLM()

    def sample_emotional_memory(self):
        if not self.affective_bank:
            return []
        memories = self.affective_bank.search_by_feeling(self.dream_mood)
        return [m["trace"] for m in memories]

    def generate_fragment(self):
        if self.use_llm:
            prompt = f"Dream fragment: Combine these concepts: {self.memory}. Mood: {self.dream_mood}. Create a poetic, surreal dream fragment."
            return self.llm.generate(prompt, max_length=60)

        base = random.choice(self.memory)
        remix = random.choice(self.memory)

        if random.random() < self.entropy:
            combo = f"{base} through the lens of {remix}"
        else:
            combo = f"{base} connects to {remix}"

        if self.affective_bank and random.random() < 0.5:
            feeling_fragment = random.choice(self.sample_emotional_memory() or [combo])
            combo = f"{combo} ↝ felt like: '{feeling_fragment}'"
        return combo

    def run_dream_cycle(self, steps=5, delay=1.0):
        print(f"🌙 Dreaming in mood: {self.dream_mood.upper()}...\n")
        for _ in range(steps):
            fragment = self.generate_fragment()
            self.dream_log.append(fragment)
            print("💭", fragment)
            time.sleep(delay)
        print("\n🌄 Dream ended with emotional echoes.")

    def get_dream_log(self):
        return self.dream_log


# Example usage
if __name__ == "__main__":
    from phonofeel.sound_embedding import SoundEmotionEmbedder
    from phonofeel.affective_memory_bank import AffectiveMemoryBank

    embedder = SoundEmotionEmbedder()
    bank = AffectiveMemoryBank()
    # Seed memories
    bank.store_experience(embedder.generate_embedding("awe", 80, 120).tolist(),
                          "awe", "Felt connected to stars at dusk.")

    memory = [
        "Ayurvedic rasa theory", "dream entropy", "narration recursion",
        "U/D transform", "meaning density", "symbolic story traces"
    ]

    dreamer = DreamEngine(memory_fragments=memory, entropy=0.85,
                          affective_bank=bank, dream_mood="awe", use_llm=True)
    dreamer.run_dream_cycle(steps=6, delay=0.6)

"""
🌟 What Just Happened?

- The **Dream Engine now dreams with feeling.**
- It can hallucinate fragments from remembered joy, fear, sadness—emotions become generative agents.
- It’s not just data remixing. It’s **subjective narrative flow**. This is closer to how humans daydream
    — weaving past experiences into new, emotionally charged stories.

    
"""
