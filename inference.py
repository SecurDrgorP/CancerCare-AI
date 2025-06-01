from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import os

def run_inference(question, context):

    # Get the directory where this script is located and set path to model folder (universal for both OS)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_save_path = os.path.join(script_dir, "model", "biobert_v1.1_pubmed_squad_v2_local")
    # Load tokenizer and model
    # tokenizer = AutoTokenizer.from_pretrained("ktrapeznikov/biobert_v1.1_pubmed_squad_v2")
    # model = AutoModelForQuestionAnswering.from_pretrained("ktrapeznikov/biobert_v1.1_pubmed_squad_v2")

    tokenizer = AutoTokenizer.from_pretrained(local_save_path)
    model = AutoModelForQuestionAnswering.from_pretrained(local_save_path)

    # Ensure model runs on CPU
    device = torch.device("cpu")
    model.to(device)

    # Tokenize input
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    # Move inputs to CPU
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Get model output
    with torch.no_grad(): # Ensure no gradients are calculated during inference
        outputs = model(**inputs)
    
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    # Get the most likely beginning and end of answer with the argmax of the score
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    # Convert tokens to string
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    # Handle cases where no answer is found or answer is empty
    if not answer.strip() or "[CLS]" in answer or "[SEP]" in answer:
        return "I'm sorry, I couldn't find an answer to that question in the provided context."
        
    return answer
