from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import os
import platform

model_name = "ktrapeznikov/biobert_v1.1_pubmed_squad_v2"

# Determine OS and set path accordingly
if platform.system() == "Windows":
    local_save_path = r"c:\Users\mot\Documents\Master\NLP\CancerCare-AI\data\datasets\biobert_v1.1_pubmed_squad_v2_local"
else:  # Assuming Linux or other Unix-like systems
    # For Linux, a path in the user's home directory is common.
    # You can customize 'NLP_models/CancerCare-AI_data' to your preference.
    home_dir = os.path.expanduser("~")
    local_save_path = os.path.join(home_dir, "NLP_models", "CancerCare-AI_data", "biobert_v1.1_pubmed_squad_v2_local")

# Create directory if it doesn't exist
if not os.path.exists(local_save_path):
    os.makedirs(local_save_path)

    # Load from Hub and save locally
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    
    tokenizer.save_pretrained(local_save_path)
    model.save_pretrained(local_save_path)
    print(f"Model and tokenizer saved to {local_save_path}")
else:
    print(f"Model and tokenizer already exist at {local_save_path}")

# Then in your run_inference function, you would load from local_save_path
# tokenizer = AutoTokenizer.from_pretrained(local_save_path)
# model = AutoModelForQuestionAnswering.from_pretrained(local_save_path)