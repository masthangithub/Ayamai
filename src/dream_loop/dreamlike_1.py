# --- Imports ---
import random
import math
from transformers import pipeline, set_seed

# --- Config ---
set_seed(42)
text_generator = pipeline("text-generation", model="gpt2")

# --- Data Description Mapper (Mock) ---
def describe_input(data):
    """
    Simulates micro-description tagging from mixed input.
    """
    if isinstance(data, str):
        return {
            'type': 'text',
            'tags': ['urban', 'weather', 'emotion'],
            'semantics': data,
        }
    return {'type': 'unknown', 'tags': [], 'semantics': ''}

# --- Entropy Engine (Enhanced) ---
def shannon_entropy(text):
    """
    Calculate Shannon entropy for a string.
    """
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return -sum([p * math.log2(p) for p in prob])

def entropy_linker(description):
    """
    Introduce irrational twists based on entropy weights and patterns.
    """
    tags = description['tags']
    semantic_core = description['semantics']
    base_entropy = shannon_entropy(semantic_core)

    surreal_elements = [
        "floating child",
        "talking fog",
        "echoes becoming birds",
        "time folding in corners",
        "clouds whispering secrets",
        "buildings bending inward",
        "umbrellas reversing rain",
        "neon shadows dancing"
    ]
    entropy_scale = min(int(base_entropy * 2), len(surreal_elements))
    random.shuffle(surreal_elements)
    twist = ", ".join(surreal_elements[:entropy_scale])

    linked_output = f"{semantic_core}. Entropy swelled: {twist}."
    return linked_output

# --- Narrator Loop ---
def generate_narrative(entropy_text):
    """
    Generates poetic, dream-like narrative.
    """
    output = text_generator(entropy_text, max_length=50, num_return_sequences=1)[0]['generated_text']
    return output

# --- Memory Store (Simulated) ---
memory = []

def store_memory(segment):
    memory.append(segment)
    return True

# --- Dream Generation Loop ---
def dreaming_ai_core(input_data):
    description = describe_input(input_data)
    entropy_output = entropy_linker(description)
    narrative = generate_narrative(entropy_output)
    store_memory(narrative)
    return narrative

# --- Test Case ---
if __name__ == '__main__':
    test_input = "a grand father walking on river bank with grand son"
    dream = dreaming_ai_core(test_input)
    print("--- Dream Sequence ---")
    print(dream)
    print("\n--- Memory ---")
    for m in memory:
        print(m)

