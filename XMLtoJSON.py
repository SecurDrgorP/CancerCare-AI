import os
import xml.etree.ElementTree as ET
import pandas as pd

def extract_qa_from_xml(xml_path):
    """Extract question-answer pairs from a single XML file."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        focus = root.find('Focus').text.strip() if root.find('Focus') is not None else "Unknown"

        qa_pairs = []
        for pair in root.findall('.//QAPair'):
            question = pair.find('Question').text.strip()
            answer = pair.find('Answer').text.strip()
            qa_pairs.append({
                'focus': focus,
                'question': question,
                'answer': answer
            })

        return qa_pairs

    except Exception as e:
        print(f"⚠️ Error processing {xml_path}: {e}")
        return []

def extract_all_from_folder(folder_path):
    """Loop through all XML files in a folder and extract Q&A."""
    all_qa = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            full_path = os.path.join(folder_path, filename)
            print(f"📂 Processing: {filename}")
            qa_pairs = extract_qa_from_xml(full_path)
            all_qa.extend(qa_pairs)

    return all_qa

# 🛠️ Set your folder path here:

folder_path = r"C:\Users\HP\OneDrive\Desktop\chatbot2\data\MedQuAD\1_CancerGov_QA"

# 🧠 Extract and save
qa_data = extract_all_from_folder(folder_path)

# ✅ Save to CSV and JSON
df = pd.DataFrame(qa_data)
df.to_csv("CancerCare-AI/cancer_qa_dataset.csv", index=False)
df.to_json("CancerCare-AI/cancer_qa_dataset.json", orient="records", indent=2)

print(f"✅ Extraction complete. {len(df)} Q&A pairs saved.")
