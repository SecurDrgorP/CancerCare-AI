class BioBERTPlaceholder:
    """Placeholder for a future BioBERT model."""

    def __init__(self):
        # Plus tard : charger le vrai modèle ici
        pass

    def answer_question(self, question: str, context: str = "") -> str:
        # Simule une réponse pour test
        return f"[BIOBERT placeholder] No trained model yet. You asked: '{question}'"
