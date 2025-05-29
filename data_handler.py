import pandas as pd
import json
import os
from typing import Dict, List, Optional, Any
import logging

class DataHandler:
    """Handler for loading and managing cancer treatment data"""
    
    def __init__(self):
        """Initialize the data handler and load all datasets"""
        self.data_dir = "data"
        self.cancer_types_df = None
        self.treatments_df = None
        self.side_effects_df = None
        self.faq_data = None
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        self._load_all_data()
        self._create_sample_data_if_missing()
    
    def _load_all_data(self):
        """Load all data files"""
        try:
            self._load_cancer_types()
            self._load_treatments()
            self._load_side_effects()
            self._load_faq()
        except Exception as e:
            logging.warning(f"Error loading data: {e}")
            self._create_sample_data_if_missing()
    
    def _load_cancer_types(self):
        """Load cancer types data"""
        file_path = os.path.join(self.data_dir, "cancer_types.csv")
        if os.path.exists(file_path):
            self.cancer_types_df = pd.read_csv(file_path)
        else:
            self.cancer_types_df = self._create_sample_cancer_types()
    
    def _load_treatments(self):
        """Load treatments data"""
        file_path = os.path.join(self.data_dir, "treatments.csv")
        if os.path.exists(file_path):
            self.treatments_df = pd.read_csv(file_path)
        else:
            self.treatments_df = self._create_sample_treatments()
    
    def _load_side_effects(self):
        """Load side effects data"""
        file_path = os.path.join(self.data_dir, "side_effects.csv")
        if os.path.exists(file_path):
            self.side_effects_df = pd.read_csv(file_path)
        else:
            self.side_effects_df = self._create_sample_side_effects()
    
    def _load_faq(self):
        """Load FAQ data"""
        file_path = os.path.join(self.data_dir, "faq.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.faq_data = json.load(f)
        else:
            self.faq_data = self._create_sample_faq()
    
    def _create_sample_data_if_missing(self):
        """Create sample data files if they don't exist"""
        
        # Create cancer types data
        if self.cancer_types_df is None or self.cancer_types_df.empty:
            self.cancer_types_df = self._create_sample_cancer_types()
            self.cancer_types_df.to_csv(os.path.join(self.data_dir, "cancer_types.csv"), index=False)
        
        # Create treatments data
        if self.treatments_df is None or self.treatments_df.empty:
            self.treatments_df = self._create_sample_treatments()
            self.treatments_df.to_csv(os.path.join(self.data_dir, "treatments.csv"), index=False)
        
        # Create side effects data
        if self.side_effects_df is None or self.side_effects_df.empty:
            self.side_effects_df = self._create_sample_side_effects()
            self.side_effects_df.to_csv(os.path.join(self.data_dir, "side_effects.csv"), index=False)
        
        # Create FAQ data
        if self.faq_data is None:
            self.faq_data = self._create_sample_faq()
            with open(os.path.join(self.data_dir, "faq.json"), 'w') as f:
                json.dump(self.faq_data, f, indent=2)
    
    def _create_sample_cancer_types(self) -> pd.DataFrame:
        """Create sample cancer types data"""
        data = [
            {
                "cancer_type": "Breast Cancer",
                "stage": "Stage II",
                "symptoms": "Breast lump, skin changes, nipple discharge",
                "treatments": "Surgery, Chemotherapy, Radiation therapy, Hormone therapy",
                "survival_rate": "85-90%",
                "common_age": "50-60 years"
            },
            {
                "cancer_type": "Lung Cancer",
                "stage": "Stage III",
                "symptoms": "Persistent cough, chest pain, shortness of breath",
                "treatments": "Surgery, Chemotherapy, Radiation therapy, Immunotherapy",
                "survival_rate": "15-25%",
                "common_age": "65-75 years"
            },
            {
                "cancer_type": "Prostate Cancer",
                "stage": "Stage I",
                "symptoms": "Difficulty urinating, blood in urine, pelvic pain",
                "treatments": "Active surveillance, Surgery, Radiation therapy",
                "survival_rate": "95-100%",
                "common_age": "60-70 years"
            },
            {
                "cancer_type": "Colorectal Cancer",
                "stage": "Stage II",
                "symptoms": "Changes in bowel habits, blood in stool, abdominal pain",
                "treatments": "Surgery, Chemotherapy, Radiation therapy, Targeted therapy",
                "survival_rate": "70-80%",
                "common_age": "50-70 years"
            },
            {
                "cancer_type": "Ovarian Cancer",
                "stage": "Stage III",
                "symptoms": "Abdominal bloating, pelvic pain, difficulty eating",
                "treatments": "Surgery, Chemotherapy, Targeted therapy",
                "survival_rate": "40-50%",
                "common_age": "50-65 years"
            }
        ]
        return pd.DataFrame(data)
    
    def _create_sample_treatments(self) -> pd.DataFrame:
        """Create sample treatments data"""
        data = [
            {
                "treatment_name": "Chemotherapy",
                "category": "Systemic Therapy",
                "cancer_types": "Breast, Lung, Colorectal, Ovarian",
                "side_effects": "Nausea, Hair loss, Fatigue, Low blood counts",
                "duration": "3-6 months",
                "effectiveness": "60-80%",
                "cost_range": "$10,000-$100,000"
            },
            {
                "treatment_name": "Radiation Therapy",
                "category": "Local Therapy",
                "cancer_types": "Breast, Lung, Prostate, Brain",
                "side_effects": "Skin irritation, Fatigue, Local pain",
                "duration": "5-7 weeks",
                "effectiveness": "70-90%",
                "cost_range": "$15,000-$50,000"
            },
            {
                "treatment_name": "Surgery",
                "category": "Local Therapy",
                "cancer_types": "Breast, Lung, Prostate, Colorectal",
                "side_effects": "Pain, Infection risk, Scarring",
                "duration": "1-3 weeks recovery",
                "effectiveness": "80-95%",
                "cost_range": "$20,000-$100,000"
            },
            {
                "treatment_name": "Immunotherapy",
                "category": "Targeted Therapy",
                "cancer_types": "Lung, Melanoma, Kidney, Bladder",
                "side_effects": "Flu-like symptoms, Skin rash, Diarrhea",
                "duration": "6-12 months",
                "effectiveness": "20-50%",
                "cost_range": "$50,000-$200,000"
            },
            {
                "treatment_name": "Hormone Therapy",
                "category": "Targeted Therapy",
                "cancer_types": "Breast, Prostate",
                "side_effects": "Hot flashes, Mood changes, Bone loss",
                "duration": "5-10 years",
                "effectiveness": "70-85%",
                "cost_range": "$5,000-$30,000"
            }
        ]
        return pd.DataFrame(data)
    
    def _create_sample_side_effects(self) -> pd.DataFrame:
        """Create sample side effects data"""
        data = [
            {"side_effect": "Nausea", "frequency": 80, "severity": "Moderate", "treatments": "Chemotherapy, Radiation"},
            {"side_effect": "Fatigue", "frequency": 90, "severity": "Mild to Severe", "treatments": "All treatments"},
            {"side_effect": "Hair Loss", "frequency": 70, "severity": "Cosmetic", "treatments": "Chemotherapy"},
            {"side_effect": "Low Blood Counts", "frequency": 60, "severity": "Serious", "treatments": "Chemotherapy"},
            {"side_effect": "Skin Irritation", "frequency": 50, "severity": "Mild", "treatments": "Radiation therapy"},
            {"side_effect": "Diarrhea", "frequency": 40, "severity": "Moderate", "treatments": "Chemotherapy, Immunotherapy"},
            {"side_effect": "Neuropathy", "frequency": 30, "severity": "Moderate", "treatments": "Chemotherapy"},
            {"side_effect": "Mouth Sores", "frequency": 25, "severity": "Moderate", "treatments": "Chemotherapy, Radiation"}
        ]
        return pd.DataFrame(data)
    
    def _create_sample_faq(self) -> Dict:
        """Create sample FAQ data"""
        return {
            "general": [
                {
                    "question": "What are the most common types of cancer?",
                    "answer": "The most common types of cancer include breast cancer, lung cancer, prostate cancer, colorectal cancer, and skin cancer. These account for about 60% of all cancer diagnoses."
                },
                {
                    "question": "How is cancer staged?",
                    "answer": "Cancer staging describes the size and extent of cancer. The TNM system is commonly used: T (tumor size), N (lymph nodes), M (metastasis). Stages range from 0 (in situ) to IV (advanced)."
                }
            ],
            "treatment": [
                {
                    "question": "What are the main types of cancer treatment?",
                    "answer": "Main cancer treatments include surgery (removing tumors), chemotherapy (drugs that kill cancer cells), radiation therapy (high-energy rays), immunotherapy (boosting immune system), and targeted therapy (drugs targeting specific cancer features)."
                },
                {
                    "question": "How long does cancer treatment take?",
                    "answer": "Treatment duration varies widely depending on cancer type, stage, and treatment plan. It can range from a few weeks for surgery to several months or years for systemic therapies."
                }
            ],
            "side_effects": [
                {
                    "question": "What are common side effects of chemotherapy?",
                    "answer": "Common chemotherapy side effects include nausea, vomiting, hair loss, fatigue, low blood counts, increased infection risk, mouth sores, and neuropathy. Side effects vary by specific drugs used."
                }
            ]
        }
    
    def get_cancer_types(self) -> pd.DataFrame:
        """Get all cancer types data"""
        return self.cancer_types_df
    
    def get_treatments(self) -> pd.DataFrame:
        """Get all treatments data"""
        return self.treatments_df
    
    def get_side_effects(self) -> pd.DataFrame:
        """Get all side effects data"""
        return self.side_effects_df
    
    def search_cancer_info(self, cancer_type: str) -> Optional[Dict]:
        """Search for specific cancer type information"""
        if self.cancer_types_df is not None:
            results = self.cancer_types_df[
                self.cancer_types_df['cancer_type'].str.contains(cancer_type, case=False, na=False)
            ]
            if not results.empty:
                return results.iloc[0].to_dict()
        return None
    
    def search_treatments(self, cancer_type: str = None, treatment_type: str = None) -> pd.DataFrame:
        """Search for treatments based on criteria"""
        df = self.treatments_df.copy()
        
        if cancer_type:
            df = df[df['cancer_types'].str.contains(cancer_type, case=False, na=False)]
        
        if treatment_type:
            df = df[df['treatment_name'].str.contains(treatment_type, case=False, na=False)]
        
        return df
    
    def get_side_effects_for_treatment(self, treatment: str) -> List[Dict]:
        """Get side effects for a specific treatment"""
        results = []
        if self.side_effects_df is not None:
            side_effects = self.side_effects_df[
                self.side_effects_df['treatments'].str.contains(treatment, case=False, na=False)
            ]
            results = side_effects.to_dict('records')
        return results
    
    def search_faq(self, query: str) -> List[Dict]:
        """Search FAQ for relevant questions and answers"""
        results = []
        if self.faq_data:
            for category, faqs in self.faq_data.items():
                for faq in faqs:
                    if (query.lower() in faq['question'].lower() or 
                        query.lower() in faq['answer'].lower()):
                        results.append({
                            'category': category,
                            'question': faq['question'],
                            'answer': faq['answer']
                        })
        return results
