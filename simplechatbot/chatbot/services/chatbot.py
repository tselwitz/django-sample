from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch


class ChatBot:
    def __init__(self):
        self.device = (
            "cuda" if torch.cuda.is_available else "cpu"
        )  # the device to load the model onto


class DevBot(ChatBot):
    def __init__(self):
        self.model = pipeline("question-answering")
        self.context = """America has changed dramatically during recent years. Not only has the number of 
    graduates in traditional engineering disciplines such as mechanical, civil, 
    electrical, chemical, and aeronautical engineering declined, but in most of 
    the premier American universities engineering curricula now concentrate on 
    and encourage largely the study of engineering science. As a result, there 
    are declining offerings in engineering subjects dealing with infrastructure, 
    the environment, and related issues, and greater concentration on high 
    technology subjects, largely supporting increasingly complex scientific 
    developments. While the latter is important, it should not be at the expense 
    of more traditional engineering.

    Rapidly developing economies such as China and India, as well as other 
    industrial countries in Europe and Asia, continue to encourage and advance 
    the teaching of engineering. Both China and India, respectively, graduate 
    six and eight times as many traditional engineers as does the United States. 
    Other industrial countries at minimum maintain their output, while America 
    suffers an increasingly serious decline in the number of engineering graduates 
    and a lack of well-educated engineers."""
        self.name = "HuggingFaceQuestionAnsweringPipeline"

    def __call__(self, query):
        return self.model(
            question=query,
            context=self.context,
        )["answer"]


class ProdBot(ChatBot):
    def __init__(self, model):
        super().__init__()
        self.model = AutoModelForCausalLM.from_pretrained(model)
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.name = model

    def __call__(self, query):
        messages = [{"role": "user", "content": query}]

        encodeds = self.tokenizer.apply_chat_template(messages, return_tensors="pt")

        model_inputs = encodeds.to(self.device)
        self.model.to(self.device)

        generated_ids = self.model.generate(
            model_inputs, max_new_tokens=1000, do_sample=True
        )
        decoded = self.tokenizer.batch_decode(generated_ids)
        return decoded[0]
