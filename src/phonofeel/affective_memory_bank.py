# src/phonofeel/affective_memory_bank.py

import uuid
import datetime

class AffectiveMemoryBank:
    """
    Stores emotional experiences as time-stamped symbolic events.
    Each memory has an embedding vector, a feeling tag, and a narrative trace.
    """

    def __init__(self):
        self.memory_log = []

    def store_experience(self, vector_embedding, feeling: str, trace: str):
        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "feeling": feeling,
            "embedding": vector_embedding,
            "trace": trace
        }
        self.memory_log.append(record)
        print(f"🧠 Stored affective memory ({feeling}): {trace[:40]}...")

    def search_by_feeling(self, feeling: str, limit=5):
        matches = [m for m in self.memory_log if m["feeling"] == feeling]
        return matches[:limit]

    def random_sample(self, limit=3):
        import random
        return random.sample(self.memory_log, min(limit, len(self.memory_log)))

    def get_all(self):
        return self.memory_log


# Example usage
if __name__ == "__main__":
    bank = AffectiveMemoryBank()

    # Simulated input
    from sound_embedding import SoundEmotionEmbedder
    embedder = SoundEmotionEmbedder()

    vec = embedder.generate_embedding("joy", 512, 58)
    bank.store_experience(vec.tolist(), "joy", "Danced freely under fading light.")

    vec2 = embedder.generate_embedding("sadness", 300, 45)
    bank.store_experience(vec2.tolist(), "sadness", "Watched memory dissolve in rain.")

    for mem in bank.search_by_feeling("joy"):
        print(f"💖 Joyful Memory → {mem['trace']}")

"""
This  build the memory bank that holds affective sound–emotion embeddings and lets them re-emerge
 when dreaming or narrating.

### 💠 `affective_memory_bank.py` — Emotional Episodic Memory Layer (AYAMAI v0.3)

This module stores experiences that carry emotional resonance—not just facts,
 but fragments charged with feeling. Later, the `dream_loop/` module will recall them based on 
 dream mood, entropy, or recursive loops.

This allows AYAMAI to:
- Store emotional experiences as time-stamped symbolic events
- Search memories by feeling tag
- Randomly sample memories for creative generation


"""