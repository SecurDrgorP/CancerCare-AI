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

if __name__ == "__main__":
    # Example usage
    example_question = "What is the main cause of lung cancer?"
    example_context = "Lung cancer is a type of cancer that begins in the lungs. Your lungs are two spongy organs in your chest that take in oxygen when you inhale and release carbon dioxide when you exhale. Lung cancer is the leading cause of cancer deaths worldwide. People who smoke have the greatest risk of lung cancer, though lung cancer can also occur in people who have never smoked. The risk of lung cancer increases with the length of time and number of cigarettes you've smoked."

    print(f"Question: {example_question}")
    # print(f"Context: {example_context}") # Context can be very long
    
    answer = run_inference(example_question, example_context)
    print(f"Answer: {answer}")

    example_question_2 = "What are the symptoms of diabetes?"
    example_context_2 = "Diabetes is a chronic (long-lasting) health condition that affects how your body turns food into energy. Common symptoms include frequent urination, increased thirst, and unexplained weight loss. Other symptoms can include fatigue, blurred vision, and slow-healing sores."
    print(f"\nQuestion: {example_question_2}")
    # print(f"Context: {example_context_2}")
    answer_2 = run_inference(example_question_2, example_context_2)
    print(f"Answer: {answer_2}")

    example_question_3 = "Who is Batman?"
    example_context_3 = "Batman is a superhero appearing in American comic books published by DC Comics. The character was created by artist Bob Kane and writer Bill Finger, and debuted in the 27th issue of the comic book Detective Comics on March 30, 1939."
    print(f"\nQuestion: {example_question_3}")
    # print(f"Context: {example_context_3}")
    answer_3 = run_inference(example_question_3, example_context_3)
    print(f"Answer: {answer_3}")

    example_question_4 = "What is the capital of France?"
    example_context_4 = "France is a country in Western Europe. It is known for its wines and sophisticated cuisine. Lascaux is a complex of caves near the village of Montignac, in the department of Dordogne in southwestern France." # Context does not contain the answer
    print(f"\nQuestion: {example_question_4}")
    # print(f"Context: {example_context_4}")
    answer_4 = run_inference(example_question_4, example_context_4)
    print(f"Answer: {answer_4}")

    while True:
        user_question = input("\nEnter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break
        user_context = input("Enter the context for your question: ")
        user_answer = run_inference(user_question, user_context)
        print(f"Answer: {user_answer}")
