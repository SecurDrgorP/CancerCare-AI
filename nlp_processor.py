import re
import spacy
from typing import Dict, List, Set
import warnings
warnings.filterwarnings("ignore")

class NLPProcessor:
    """Medical NLP processor for extracting cancer-related entities from text"""
    
    def __init__(self):
        """Initialize the NLP processor with medical vocabularies"""
        self.cancer_types = {
            'breast cancer', 'lung cancer', 'prostate cancer', 'colorectal cancer',
            'skin cancer', 'melanoma', 'leukemia', 'lymphoma', 'ovarian cancer',
            'pancreatic cancer', 'liver cancer', 'kidney cancer', 'bladder cancer',
            'brain cancer', 'thyroid cancer', 'cervical cancer', 'endometrial cancer',
            'stomach cancer', 'esophageal cancer', 'oral cancer', 'bone cancer'
        }
        
        self.treatments = {
            'chemotherapy', 'radiation therapy', 'surgery', 'immunotherapy',
            'targeted therapy', 'hormone therapy', 'stem cell transplant',
            'bone marrow transplant', 'cryotherapy', 'photodynamic therapy',
            'radiofrequency ablation', 'brachytherapy', 'proton therapy',
            'car-t cell therapy', 'checkpoint inhibitors', 'monoclonal antibodies'
        }
        
        self.symptoms = {
            'fatigue', 'nausea', 'vomiting', 'hair loss', 'weight loss',
            'appetite loss', 'fever', 'infection', 'anemia', 'bleeding',
            'bruising', 'diarrhea', 'constipation', 'mouth sores',
            'skin changes', 'neuropathy', 'shortness of breath', 'cough',
            'pain', 'swelling', 'headache', 'dizziness', 'confusion'
        }
        
        self.side_effects = {
            'nausea', 'vomiting', 'fatigue', 'hair loss', 'neuropathy',
            'diarrhea', 'constipation', 'mouth sores', 'skin rash',
            'low blood count', 'infection risk', 'bleeding', 'anemia',
            'kidney problems', 'heart problems', 'lung problems',
            'cognitive changes', 'fertility issues', 'bone weakness'
        }
        
        self.stages = {
            'stage 0', 'stage i', 'stage ii', 'stage iii', 'stage iv',
            'stage 1', 'stage 2', 'stage 3', 'stage 4',
            'early stage', 'advanced stage', 'metastatic', 'localized'
        }
        
        # Try to load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except IOError:
            print("Warning: spaCy model 'en_core_web_sm' not found. Using basic text processing.")
            self.nlp = None
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities from text"""
        
        text_lower = text.lower()
        entities = {
            'cancer_types': [],
            'treatments': [],
            'symptoms': [],
            'side_effects': [],
            'stages': []
        }
        
        # Extract cancer types
        for cancer_type in self.cancer_types:
            if cancer_type in text_lower:
                entities['cancer_types'].append(cancer_type.title())
        
        # Extract treatments
        for treatment in self.treatments:
            if treatment in text_lower:
                entities['treatments'].append(treatment.title())
        
        # Extract symptoms
        for symptom in self.symptoms:
            if symptom in text_lower:
                entities['symptoms'].append(symptom.title())
        
        # Extract side effects
        for side_effect in self.side_effects:
            if side_effect in text_lower:
                entities['side_effects'].append(side_effect.title())
        
        # Extract stages
        for stage in self.stages:
            if stage in text_lower:
                entities['stages'].append(stage.title())
        
        # Use spaCy for additional entity extraction if available
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE']:
                    # Skip these for medical context
                    continue
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def classify_query_intent(self, text: str) -> str:
        """Classify the intent of the user query"""
        
        text_lower = text.lower()
        
        # Treatment information
        if any(word in text_lower for word in ['treatment', 'therapy', 'cure', 'heal']):
            return 'treatment_info'
        
        # Side effects
        if any(word in text_lower for word in ['side effect', 'adverse', 'reaction']):
            return 'side_effects'
        
        # Symptoms
        if any(word in text_lower for word in ['symptom', 'sign', 'indicator']):
            return 'symptoms'
        
        # Prognosis
        if any(word in text_lower for word in ['prognosis', 'survival', 'outlook', 'recovery']):
            return 'prognosis'
        
        # Diet and lifestyle
        if any(word in text_lower for word in ['diet', 'food', 'nutrition', 'exercise', 'lifestyle']):
            return 'lifestyle'
        
        # Cost information
        if any(word in text_lower for word in ['cost', 'price', 'expensive', 'insurance']):
            return 'cost'
        
        # General information
        return 'general_info'
    
    def extract_medical_keywords(self, text: str) -> List[str]:
        """Extract relevant medical keywords from text"""
        
        keywords = []
        text_lower = text.lower()
        
        # Common medical terms to look for
        medical_terms = [
            'oncology', 'oncologist', 'tumor', 'malignant', 'benign',
            'metastasis', 'biopsy', 'diagnosis', 'screening', 'prevention',
            'remission', 'relapse', 'chemotherapy', 'radiation', 'surgery',
            'clinical trial', 'second opinion', 'palliative care'
        ]
        
        for term in medical_terms:
            if term in text_lower:
                keywords.append(term.title())
        
        return list(set(keywords))
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for better processing"""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep medical terminology
        text = re.sub(r'[^\w\s\-\.]', '', text)
        
        return text
    
    def get_query_complexity(self, text: str) -> str:
        """Determine the complexity of the user query"""
        
        entities = self.extract_entities(text)
        total_entities = sum(len(entity_list) for entity_list in entities.values())
        
        if total_entities >= 3:
            return 'complex'
        elif total_entities >= 1:
            return 'moderate'
        else:
            return 'simple'
