import json
import re
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util

class LocalContextRetriever:
    def __init__(self, json_path):
        nltk.download('punkt', quiet=True)  # ✅ download once at startup

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.questions = [item['question'] for item in self.data]
        self.answers = [item['answer'] for item in self.data]
        self.embeddings = self.model.encode(self.questions, convert_to_tensor=True)

    def get_best_answer_chunks(self, query, top_k=1):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        best_indices = similarities.topk(k=top_k).indices.tolist()
        return [self.answers[i] for i in best_indices]

    def split_into_sentences(self, text):
        cleaned = re.sub(r'\n+', ' ', text)
        return [s.strip() for s in sent_tokenize(cleaned) if len(s.strip()) > 20 and not s.lower().startswith("key point")]
