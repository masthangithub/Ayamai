# --- Imports ---
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

import random
import math
from transformers import pipeline, set_seed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup


# MYNOTE
#  pip install accelerate     has to be installed before transformers
# with model gpt2 it gives some story. To run  with deepseek. need pip install accelerate.  It need GPU to run.

# --- Config ---
# set_seed(42)

# text_generator = pipeline("text-generation", model="deepseek-ai/DeepSeek-V3-0324")   # Use this for DeepSeek V3
text_generator = pipeline("text-generation", model="gpt2")

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

def extract_relevant_tags(goal, lines, top_n=3):
    # Flatten lines to a single string
    text = " ".join(lines)
    words = list(set(text.split()))
    if not words:
        return []
    vectorizer = TfidfVectorizer().fit([goal] + words)
    goal_vec = vectorizer.transform([goal])
    word_vecs = vectorizer.transform(words)
    sims = cosine_similarity(goal_vec, word_vecs)[0]
    sorted_words = [word for _, word in sorted(zip(sims, words), reverse=True)]
    return sorted_words[:top_n]

# --- Web Scraping for RAG ---
def scrape_web_for_goal(goal, num_results=2):
    """
    Scrape web search results for the goal and return concatenated text content.
    Uses DuckDuckGo for privacy and simplicity.
    """
    import urllib.parse
    search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(goal)}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = [a['href'] for a in soup.select('.result__a') if a.has_attr('href')][:num_results]
    content = ""
    for link in links:
        try:
            page = requests.get(link, headers=headers, timeout=5)
            page_soup = BeautifulSoup(page.text, 'html.parser')
            # Get all paragraph text
            paragraphs = page_soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            content += text + "\n"
        except Exception:
            continue
    return content

# --- Extract RAG tags ---
def extract_rag_tags(goal, web_content, top_n=5):
    # Split web content into sentences/phrases
    import re
    sentences = re.split(r'[.!?]\s+', web_content)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return []
    vectorizer = TfidfVectorizer().fit([goal] + sentences)
    goal_vec = vectorizer.transform([goal])
    sent_vecs = vectorizer.transform(sentences)
    sims = cosine_similarity(goal_vec, sent_vecs)[0]
    sorted_sentences = [sent for _, sent in sorted(zip(sims, sentences), reverse=True)]
    return sorted_sentences[:top_n]

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
def dreaming_ai_core(input_data, goal, iterations=3, use_rag=True):
    surreal_elements = []
    current_input = input_data
    current_tags = ['urban', 'weather', 'emotion']
    rag_tags = []
    web_content = ""
    if use_rag:
        web_content = scrape_web_for_goal(goal)
        rag_tags = extract_rag_tags(goal, web_content, top_n=3)
        current_tags = rag_tags if rag_tags else current_tags
    for i in range(iterations):
        # Step 1: Generate 10 lines of text from HuggingFace pipeline, using both current_input and goal
        if use_rag and web_content:
            # Truncate web_content for prompt length if needed
            context = web_content[:1000]
            prompt = f"{current_input}\nGoal: {goal}\nWeb context: {context}"
        else:
            prompt = f"{current_input}\nGoal: {goal}"
        llm_output = text_generator(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']
        llm_lines = llm_output.split(". ")[:10]
        # Step 2: Extract 5 most relevant lines to the goal
        relevant = extract_relevant_lines(goal, "\n".join(llm_lines), top_n=5)
        # Dynamically update tags with most relevant words to the goal and RAG
        local_tags = extract_relevant_tags(goal, relevant, top_n=3)
        if use_rag and rag_tags:
            current_tags = list(set(local_tags + rag_tags))
        else:
            current_tags = local_tags
        # Step 3: Update surreal_elements with lines most related to the goal
        surreal_elements.extend(relevant)
        # Step 4: Use entropy_linker with updated surreal_elements, focusing on the goal
        def entropy_linker_dynamic(description):
            tags = description['tags']
            semantic_core = description['semantics']
            base_entropy = shannon_entropy(semantic_core)
            entropy_scale = min(int(base_entropy * 2), len(surreal_elements))
            random.shuffle(surreal_elements)
            twist = ", ".join(surreal_elements[:entropy_scale])
            linked_output = f"{semantic_core}. Entropy swelled: {twist}. Goal: {goal}"
            return linked_output
        # Use updated tags in description
        description = {'type': 'text', 'tags': current_tags, 'semantics': current_input}
        entropy_output = entropy_linker_dynamic(description)
        narrative = generate_narrative(entropy_output)
        store_memory(narrative)
        # Step 5: Update input for next iteration
        current_input = narrative
    return narrative

# --- Test Case ---
if __name__ == '__main__':
    test_input = "ayurveda treats old age as disease because of agravated vata and accumulated ama"
    goal = "Find the cure from charaka and sushruta samhitas and others"
    dream = dreaming_ai_core(test_input, goal, iterations=3, use_rag=True)
    print("--- Dream Sequence ---")
    print(dream)
    print("\n--- Memory ---")
    for m in memory:
        print(m)

