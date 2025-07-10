# --- Imports ---
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

import random
import math
from transformers import pipeline, set_seed
from utils.local_llm import LocalLLM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def extract_relevant_lines(input_text, generated_text, top_n=5):
    lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
    if not lines:
        return []
    vectorizer = TfidfVectorizer().fit([input_text] + lines)
    input_vec = vectorizer.transform([input_text])
    line_vecs = vectorizer.transform(lines)
    sims = cosine_similarity(input_vec, line_vecs)[0]
    sorted_lines = [line for _, line in sorted(zip(sims, lines), reverse=True)]
    return sorted_lines[:top_n]

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

# --- Dream Generation Loop (Dynamic Surreal Elements) ---
def dreaming_ai_core(input_data, iterations=3):
    llm = LocalLLM()
    surreal_elements = []
    current_input = input_data
    for i in range(iterations):
        # Step 1: Generate 10 lines of text from LLM
        llm_output = llm.generate(current_input, max_length=500)
        llm_lines = llm_output.split(". ")[:10]
        # Step 2: Extract 5 most relevant lines to input_data
        relevant = extract_relevant_lines(current_input, "\n".join(llm_lines), top_n=5)
        # Step 3: Update surreal_elements
        surreal_elements.extend(relevant)
        # Step 4: Use entropy_linker with updated surreal_elements
        def entropy_linker_dynamic(description):
            tags = description['tags']
            semantic_core = description['semantics']
            base_entropy = shannon_entropy(semantic_core)
            entropy_scale = min(int(base_entropy * 2), len(surreal_elements))
            random.shuffle(surreal_elements)
            twist = ", ".join(surreal_elements[:entropy_scale])
            linked_output = f"{semantic_core}. Entropy swelled: {twist}."
            return linked_output
        description = describe_input(current_input)
        entropy_output = entropy_linker_dynamic(description)
        narrative = generate_narrative(entropy_output)
        store_memory(narrative)
        # Step 5: Update input for next iteration
        current_input = narrative
    return narrative

# --- Test Case ---
if __name__ == '__main__':
    test_input = "a grand father walking on river bank with grand son"
    dream = dreaming_ai_core(test_input, iterations=3)
    print("--- Dream Sequence ---")
    print(dream)
    print("\n--- Memory ---")
    for m in memory:
        print(m)

