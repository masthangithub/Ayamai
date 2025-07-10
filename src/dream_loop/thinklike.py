# --- Imports ---
import sys
import os
import random
import requests
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from requests.exceptions import ConnectionError

# --- Gemini API Integration (reuse from dreamlike_3_gemini_1.py) ---
GOOGLE_API_KEY = "AIzaSyD94317UFjtBvLDslOgP0Brh7heA-8KAQU"  # Use your actual API key

def gemini_api_generate(prompt, api_key=GOOGLE_API_KEY, max_tokens=100, model_name="gemini-1.5-flash-latest", retries=3, retry_delay=2):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens}
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            try:
                candidates = data.get("candidates", [])
                if candidates:
                    content = candidates[0].get("content", None)
                    if isinstance(content, dict) and "parts" in content:
                        parts = content["parts"]
                        if parts and isinstance(parts[0], dict) and "text" in parts[0]:
                            return parts[0]["text"]
                    elif isinstance(content, str):
                        return content
                    elif isinstance(content, dict) and "role" in content:
                        return "[Gemini API returned only a role, no narrative text. Try a different model or check your API key/quota.]"
                if "promptFeedback" in data:
                    return f"[Gemini API feedback: {data['promptFeedback']}]"
                return f"[Unrecognized Gemini API response: {data}]"
            except Exception as e:
                return f"[Error parsing Gemini API response: {e}]"
        except ConnectionError as ce:
            print(f"[Gemini API ConnectionError: {ce}. Retrying {attempt+1}/{retries}...]")
            time.sleep(retry_delay)
        except Exception as e:
            return f"[Gemini API error: {e}]"
    return "[Failed to connect to Gemini API after multiple attempts. Please check your network, API key, and endpoint/model name.]"

# --- ThoughtPath Class ---
class ThoughtPath:
    def __init__(self, hypothesis, memory=None):
        self.hypothesis = hypothesis
        self.memory = memory or []
        self.status = "active"  # or "ruled_out" or "accepted"
        self.reasoning = []

# --- Data Search (Web/LLM) ---
def search_for_data(hypothesis, goal):
    """
    Use Gemini to search for supporting or contradicting data for a hypothesis.
    """
    prompt = f"Problem: {goal}\nHypothesis: {hypothesis}\nList possible supporting and contradicting evidence, and reasoning."
    result = gemini_api_generate(prompt)
    return result

def extract_relevant_lines(hypothesis, generated_text, top_n=5):
    lines = [line.strip() for line in generated_text.split('\n') if line.strip()]
    if not lines:
        return []
    vectorizer = TfidfVectorizer().fit([hypothesis] + lines)
    input_vec = vectorizer.transform([hypothesis])
    line_vecs = vectorizer.transform(lines)
    sims = cosine_similarity(input_vec, line_vecs)[0]
    sorted_lines = [line for _, line in sorted(zip(sims, lines), reverse=True)]
    return sorted_lines[:top_n]

# --- Adversarial Test ---
def adversarial_test(hypothesis, data_lines):
    """
    If any line contains strong contradiction, rule out. Otherwise, support.
    """
    contradiction_keywords = ["contradict", "ruled out", "not likely", "no evidence", "disproven", "unlikely"]
    for line in data_lines:
        if any(kw in line.lower() for kw in contradiction_keywords):
            return False, line
    return True, None

# --- Thinking Process ---
def thinking_process(problem, initial_hypotheses, max_steps=3):
    paths = [ThoughtPath(h) for h in initial_hypotheses]
    for step in range(max_steps):
        for path in paths:
            if path.status != "active":
                continue
            data = search_for_data(path.hypothesis, problem)
            relevant = extract_relevant_lines(path.hypothesis, data, top_n=5)
            path.memory.extend(relevant)
            supported, reason = adversarial_test(path.hypothesis, relevant)
            if not supported:
                path.status = "ruled_out"
                path.reasoning.append(f"Ruled out due to: {reason}")
            else:
                path.reasoning.append("Supported by data.")
    # Collect accepted paths
    solutions = [p for p in paths if p.status == "active"]
    return solutions, paths

# --- Example Usage ---
if __name__ == '__main__':
    problem = "Why do I feel sleepy after eating?"
    initial_hypotheses = [
        "Diabetes",
        "Metabolism problem",
        "Inflammation from exercise",
        "Food ingredient effect"
    ]
    solutions, all_paths = thinking_process(problem, initial_hypotheses, max_steps=3)
    print("--- Final Solutions (Not Ruled Out) ---")
    for s in solutions:
        print(f"Possible solution: {s.hypothesis}")
        print("Memory:", s.memory)
        print("Reasoning:", s.reasoning)
        print()
    print("--- All Thought Paths ---")
    for p in all_paths:
        print(f"Hypothesis: {p.hypothesis} | Status: {p.status}")
        print("Memory:", p.memory)
        print("Reasoning:", p.reasoning)
        print()
