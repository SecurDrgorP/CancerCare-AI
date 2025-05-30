# biobert_qa.py
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

class BioBERT_QA:
    def __init__(self):
        # Replace with your actual path (adjust if Linux)
        self.model_path = r"C:\Users\HP\Downloads\biobert_v1.1_pubmed_squad_v2_local"
        self.device = torch.device("cpu")  # or "cuda" if using GPU
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_path)
        self.model.to(self.device)

    def answer_question(self, question, context):
        inputs = self.tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        start = torch.argmax(outputs.start_logits)
        end = torch.argmax(outputs.end_logits) + 1
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(input_ids[start:end])
        )
        if not answer.strip() or "[CLS]" in answer:
            return "No clear answer found in the given context."
        return answer
