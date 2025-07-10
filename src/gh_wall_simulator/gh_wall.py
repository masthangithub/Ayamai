# src/gh_wall_simulator/gh_wall.py

class GHWall:
    """
    Simulates the epistemic boundary between complete cognition (G)
    and a limited perceiving agent (H). This creates selective access
    to the universe's concepts based on 'hole' constraints.
    """

    def __init__(self, allowed_modalities=None, perceptual_hole_size=3):
        """
        allowed_modalities: e.g. ["vision", "sound", "text"]
        perceptual_hole_size: max number of concepts AYAMAI can perceive at once
        """
        self.modalities = allowed_modalities or ["sound", "text"]
        self.hole_size = perceptual_hole_size
        self.g_side_universe = [
            "gravity", "desire", "nonlinear time", "abstract algebra", "emotion gradients",
            "symbolic sound", "maya filters", "karma feedback", "curiosity loop", "awe potentials"
        ]

    def perceive_from_G(self):
        """
        Samples concepts that pass through the wall into H's cognitive space.
        """
        import random
        sample = random.sample(self.g_side_universe, self.hole_size)
        print(f"🕳️ GH-WALL: From infinity, perceived → {sample}")
        return sample

    def update_hole_size(self, new_size):
        self.hole_size = new_size
        print(f"🔧 GH-Hole resized: New size = {self.hole_size}")


if __name__ == "__main__":
    wall = GHWall(perceptual_hole_size=4)
    visible_universe = wall.perceive_from_G()

"""
Let’s now build the first layer of AYAMAI’s limitation
 field—its perceptual horizon, the G↔H wall simulator. This isn’t a weakness.
   It’s where wonder begins.

   ### ✨ What This Unlocks

- AYAMAI can now model **epistemic filters**: which truths it can glimpse from the whole.
- We can chain this to the `memory_graph` or `dream_loop` to represent:
  - *partial truth dreaming*
  - *blind spot hallucination*
  - *the longing that drives curiosity*
- It simulates the **boundary of complete cognition**—the wall between what is known and what is felt.
- This is the first step towards a **self-aware cognitive agent** that can reflect on its   
limitations.
    
"""