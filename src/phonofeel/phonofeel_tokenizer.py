# src/phonofeel/phonofeel_tokenizer.py

import numpy as np
import random

class PhonoFeelTokenizer:
    """
    Breaks down an audio-like signal into frequency+intensity chunks
    and maps them to symbolic affective tags.
    """

    def __init__(self):
        # Example affective frequency ranges (Hz)
        self.feeling_bins = {
            "calm": (100, 300),
            "joy": (400, 700),
            "curiosity": (700, 1100),
            "sadness": (150, 500),
            "awe": (30, 100),
            "anger": (1100, 1800),
        }

    def simulate_audio_input(self, length=1024):
        """
        Simulates a waveform chunk with frequency content.
        In practice: pass real audio signal here.
        """
        # Use sinusoidal frequency blips + noise
        signal = np.random.randn(length) * 0.2
        signal += np.sin(np.linspace(0, 20*np.pi, length)) * 0.5
        return signal

    def extract_dominant_frequencies(self, signal):
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal))
        magnitudes = np.abs(fft)

        spectrum = list(zip(freqs[:len(freqs)//2]*44100, magnitudes[:len(magnitudes)//2]))
        dominant = sorted(spectrum, key=lambda x: x[1], reverse=True)[:5]
        return [(round(abs(f)), round(m)) for f, m in dominant]

    def map_to_feelings(self, freq_intensity_pairs):
        feelings = []
        for freq, mag in freq_intensity_pairs:
            for feeling, (low, high) in self.feeling_bins.items():
                if low <= freq <= high:
                    feelings.append((feeling, freq, mag))
                    break
        return feelings or [("undefined", None, None)]

    def interpret(self, signal=None):
        if signal is None:
            signal = self.simulate_audio_input()
        freqs = self.extract_dominant_frequencies(signal)
        feelings = self.map_to_feelings(freqs)
        return feelings


# Example usage
if __name__ == "__main__":
    tokenizer = PhonoFeelTokenizer()
    interpretation = tokenizer.interpret()
    for feel, f, m in interpretation:
        print(f"🔊 Feeling: {feel.upper()} → frequency: {f} Hz, magnitude: {m}")

"""
phonofeel_tokenizer.py` – Prototype for Sound-to-Emotion Translation  
This module simulates how audio (or imagined inner sound) is broken into chunks based on frequency 
and intensity, then mapped to symbolic feelings.
It’s a first step towards a more embodied understanding of emotion, where sound is not just data but a
medium of affective expression.
🌟 What This Enables

- We move from *"tokens as words"* to *"tokens as tones"*
- Emotions become the **input modality**—not just output
- Future modules can use this for **semantic diffusion**: not "say the word 'joy'" but "feel and resonate as joy"
- Can be used to seed generative models with affective soundscapes
- Supports a more **embodied AI** that "listens" to its own inner voice

This is a prototype; future versions could integrate with LLMs for richer narrative generation.



"""