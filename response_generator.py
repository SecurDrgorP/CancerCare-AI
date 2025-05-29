from typing import Dict, List, Any
import random
from data_handler import DataHandler

class ResponseGenerator:
    """Generate intelligent responses for cancer treatment queries"""
    
    def __init__(self, data_handler: DataHandler = None):
        self.data_handler = data_handler

        # Templates
        self.templates = {
            'treatment_info': [
                "Based on your query about {cancer_type}, here are the main treatment options:",
                "For {cancer_type}, the following treatments are commonly used:",
                "Treatment options for {cancer_type} typically include:"
            ],
            'side_effects': [
                "Common side effects of {treatment} include:",
                "Patients receiving {treatment} may experience:",
                "The following side effects are associated with {treatment}:"
            ],
            'general_info': [
                "Here's what I found about your query:",
                "Based on current medical knowledge:",
                "According to available information:"
            ],
            'prognosis': [
                "Regarding prognosis for {cancer_type}:",
                "The outlook for {cancer_type} depends on several factors:",
                "Survival rates for {cancer_type} vary based on:"
            ],
            'lifestyle': [
                "For lifestyle and dietary recommendations:",
                "Regarding nutrition and lifestyle during treatment:",
                "Here are some general wellness guidelines:"
            ]
        }

        # Disclaimers
        self.disclaimers = [
            "\n\n⚠️ **Please note:** This information is for educational purposes only. Always consult with your healthcare team for personalized medical advice.",
            "\n\n⚠️ **Important:** Individual cases vary significantly. Your healthcare provider can give you the most accurate information for your specific situation.",
            "\n\n⚠️ **Reminder:** This is general information only. Your oncologist can provide treatment recommendations tailored to your specific diagnosis and health status."
        ]
    
    def generate_response(self, query: str, entities: Dict[str, List[str]], tokens: List[str] = None) -> Dict[str, Any]:
        """Unified response generator: keyword + classic intent-based logic"""
        intent = self._determine_intent(query, entities)
        
        # Priorité : logique par mots-clés s'ils sont détectés
        rule_based_response = self._rule_based_response(tokens)
        if rule_based_response:
            return rule_based_response
        
        # Sinon : logique par intent + data handler
        response_text = self._generate_main_response(query, entities, intent)
        related_data = self._collect_related_data(entities)
        response_text += random.choice(self.disclaimers)
        
        return {
            'text': response_text,
            'intent': intent,
            'entities': entities,
            'related_data': related_data
        }

    def _rule_based_response(self, tokens: List[str]) -> Dict[str, Any] | None:
        if not tokens:
            return None
        
        t = set(token.lower() for token in tokens)
        response, intent = None, None

        # Anglais
        if 'breast' in t and 'cancer' in t and 'stage' in t:
            response = "Treatment for stage 2 breast cancer typically includes surgery, chemotherapy, radiation therapy, and hormone therapy depending on receptor status."
            intent = "treatment_options"
        elif 'chemotherapy' in t and ('side' in t or 'effects' in t):
            response = "Common side effects of chemotherapy include fatigue, nausea, vomiting, hair loss, and increased risk of infection."
            intent = "side_effects"
        elif 'diet' in t and 'radiation' in t:
            response = "During radiation therapy, a balanced diet rich in proteins, vitamins, and hydration is recommended to support recovery."
            intent = "diet_recommendation"
        elif 'recovery' in t and 'surgery' in t:
            response = "Recovery time after cancer surgery can vary but typically ranges from a few weeks to a few months depending on the procedure."
            intent = "recovery_time"
        elif 'immunotherapy' in t:
            response = "Immunotherapy boosts the body's natural defenses to fight cancer by targeting specific cancer cell markers."
            intent = "immunotherapy"
        elif 'radiation' in t and 'work' in t:
            response = "Radiation therapy works by using high-energy rays to destroy or damage cancer cells while sparing normal tissues."
            intent = "treatment_mechanism"
        elif 'symptom' in t and 'ovarian' in t:
            response = "Symptoms of ovarian cancer can include bloating, pelvic pain, difficulty eating, and frequent urination."
            intent = "symptoms"
        elif 'cost' in t and 'treatments' in t:
            response = "Cancer treatment costs vary widely depending on location, type of cancer, insurance, and treatment duration."
            intent = "cost"

        # Français
        elif 'cancer' in t and 'sein' in t and 'stade' in t:
            response = "Le traitement du cancer du sein de stade 2 inclut généralement une chirurgie, une chimiothérapie, une radiothérapie et une hormonothérapie selon le profil tumoral."
            intent = "treatment_options"
        elif 'chimiothérapie' in t and ('effet' in t or 'secondaire' in t):
            response = "Les effets secondaires fréquents de la chimiothérapie incluent la fatigue, les nausées, la perte de cheveux et un risque accru d'infection."
            intent = "side_effects"
        elif 'régime' in t and 'radiothérapie' in t:
            response = "Pendant la radiothérapie, une alimentation équilibrée, riche en protéines, vitamines et hydratation est recommandée."
            intent = "diet_recommendation"
        elif 'récupération' in t and 'chirurgie' in t:
            response = "Le temps de récupération après une chirurgie dépend du type d'intervention, généralement quelques semaines à quelques mois."
            intent = "recovery_time"
        elif 'immunothérapie' in t:
            response = "L'immunothérapie renforce les défenses naturelles du corps pour lutter contre le cancer en ciblant des marqueurs spécifiques."
            intent = "immunotherapy"
        elif 'fonctionne' in t and 'radiothérapie' in t:
            response = "La radiothérapie utilise des rayons à haute énergie pour détruire ou endommager les cellules cancéreuses."
            intent = "treatment_mechanism"
        elif 'symptôme' in t and 'ovaire' in t:
            response = "Les symptômes du cancer de l’ovaire incluent ballonnements, douleurs pelviennes, troubles digestifs et mictions fréquentes."
            intent = "symptoms"
        elif 'coût' in t and 'traitement' in t:
            response = "Le coût du traitement du cancer varie selon le pays, le type de cancer, la couverture d’assurance et la durée des soins."
            intent = "cost"

        if response:
            return {
                'text': response,
                'intent': intent,
                'entities': [],
                'related_data': {}
            }

        return None

    def _determine_intent(self, query: str, entities: Dict[str, List[str]]) -> str:
        query_lower = query.lower()

        if any(word in query_lower for word in ['treatment', 'therapy', 'cure', 'heal', 'options']):
            return 'treatment_info'
        if any(word in query_lower for word in ['side effect', 'adverse', 'reaction', 'symptoms']):
            return 'side_effects'
        if any(word in query_lower for word in ['prognosis', 'survival', 'outlook', 'recovery', 'rate']):
            return 'prognosis'
        if any(word in query_lower for word in ['diet', 'food', 'nutrition', 'exercise', 'lifestyle']):
            return 'lifestyle'
        if any(word in query_lower for word in ['cost', 'price', 'expensive', 'insurance']):
            return 'cost'

        return 'general_info'

    # 🔁 Les fonctions _generate_main_response, _generate_treatment_info, _generate_side_effects_info,
    # _generate_prognosis_info, _generate_lifestyle_info, _generate_cost_info,
    # _generate_general_info, _collect_related_data restent inchangées
    # Tu peux les garder telles qu’elles sont dans ton ancien fichier
