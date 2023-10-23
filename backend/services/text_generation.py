from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

MODEL_PATH = "gpt2"
class TextGenerationService:
    def __init__(self):
        self.model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
        self.tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)

    def generate_text(self, input_text, max_length=50):
        # input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        # with torch.no_grad():
        #     output = self.model.generate(input_ids, max_length=max_length, num_return_sequences=1)

        # generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return input_text
