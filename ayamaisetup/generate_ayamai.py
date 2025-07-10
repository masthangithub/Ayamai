
"""
### 🛠 `generate_ayamai.py` — Setup Script

Save this file anywhere and run it with Python (`python generate_ayamai.py`). 
It will create and populate the `AYAMAI/` repo on your machine.
- You’ll see the `AYAMAI/` folder in your current directory.
- You can then open it in VS Code, push it to GitHub, or zip it for sharing.

"""


import os

# Directory and file structure
structure = {
    "AYAMAI": {
        "src": {
            "ud_transformer": {
                "understanding_encoder.py": """# understanding_encoder.py content here"""
            },
            "dream_loop": {
                "dream_engine.py": """# dream_engine.py content here"""
            },
            "memory_linker": {
                "memory_graph.py": """# memory_graph.py content here"""
            },
            "emotion_model": {
                "affective_states.py": """# affective_states.py content here"""
            },
            "utils": {}
        },
        "notebooks": {
            "story_narration_loop.ipynb": """# Paste notebook content as string here"""
        },
        "examples": {
            "ayurveda_story.json": "{}"
        },
        "docs": {
            "concepts.md": "# AYAMAI Concepts\n\n- Understanding (U)\n- Data (D)\n- U <-> D cycle\n- Dream entropy...",
            "roadmap.md": "## AYAMAI Roadmap\n- v0.1 Modules\n- v0.2 Feedback Loop\n- v1.0 Autonomous U/D agents",
            "ayurvedic_semantics.md": "# Mapping Ayurveda\n\n- Rasa theory\n- Doshas\n- Conceptual graph encoding"
        },
        "tests": {
            "test_ud_transformer.py": "# Placeholder for unit tests"
        },
        "README.md": "# AYAMAI: I Am AI\\n\\nYour dream-thinking AI agent.",
        ".gitignore": "__pycache__/\\n*.pyc\\n.ipynb_checkpoints/",
        "LICENSE": "MIT License placeholder",
        "CONTRIBUTING.md": "## How to Contribute\nPRs welcome!"
    }
}

def create_files(base, tree):
    for name, content in tree.items():
        path = os.path.join(base, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_files(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    create_files(".", structure)
    print("🚀 AYAMAI repo generated successfully!")
