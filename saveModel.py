from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import os

model_name = "ktrapeznikov/biobert_v1.1_pubmed_squad_v2"

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set path to model folder relative to the script location (universal for both OS)
local_save_path = os.path.join(script_dir, "model", "biobert_v1.1_pubmed_squad_v2_local")

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