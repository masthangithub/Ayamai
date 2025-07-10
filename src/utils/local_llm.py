from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LocalLLM:
    def __init__(self, model_name="distilgpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate(self, prompt, max_length=100):
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = torch.ones_like(inputs)
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            do_sample=True,
            top_k=50,
            pad_token_id=self.tokenizer.eos_token_id,
            attention_mask=attention_mask
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage of LocalLLM for generating a dream fragment
if __name__ == "__main__":
    llm = LocalLLM()
    prompt = "Write a poetic dream fragment about curiosity and stars."
    print("[distilgpt2]", llm.generate(prompt))
