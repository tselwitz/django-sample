from transformers import AutoModelForCausalLM, AutoTokenizer
from config import *


class ChatBot:
    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained(CHATBOT_PRETRAINED_MODEL)
        self.tokenizer = AutoTokenizer.from_pretrained(CHATBOT_PRETRAINED_MODEL)

    def answer_question(self, message):
        messages = [
            {"role": "user", "content": message},
        ]
        encodeds = self.tokenizer.apply_chat_template(messages, return_tensors="pt")

        model_inputs = encodeds.to(self.device)
        self.model.to(self.device)

        generated_ids = self.model.generate(
            model_inputs, max_new_tokens=1000, do_sample=True
        )
        decoded = self.tokenizer.batch_decode(generated_ids)
        return decoded
