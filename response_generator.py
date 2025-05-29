from typing import Dict, List, Any
import random
from data_handler import DataHandler

class ResponseGenerator:
    """Generate intelligent responses for cancer treatment queries"""
    
    def __init__(self, data_handler: DataHandler):
        """Initialize with data handler"""
        self.data_handler = data_handler
        
        # Response templates for different types of queries
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
        
        # Medical disclaimers
        self.disclaimers = [
            "\n\n⚠️ **Please note:** This information is for educational purposes only. Always consult with your healthcare team for personalized medical advice.",
            "\n\n⚠️ **Important:** Individual cases vary significantly. Your healthcare provider can give you the most accurate information for your specific situation.",
            "\n\n⚠️ **Reminder:** This is general information only. Your oncologist can provide treatment recommendations tailored to your specific diagnosis and health status."
        ]
    
    def generate_response(self, query: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Generate a comprehensive response based on query and extracted entities"""
        
        # Determine query intent
        intent = self._determine_intent(query, entities)
        
        # Generate main response
        response_text = self._generate_main_response(query, entities, intent)
        
        # Collect related data
        related_data = self._collect_related_data(entities)
        
        # Add medical disclaimer
        response_text += random.choice(self.disclaimers)
        
        return {
            'text': response_text,
            'intent': intent,
            'entities': entities,
            'related_data': related_data
        }
    
    def _determine_intent(self, query: str, entities: Dict[str, List[str]]) -> str:
        """Determine the intent of the query"""
        
        query_lower = query.lower()
        
        # Treatment information
        if any(word in query_lower for word in ['treatment', 'therapy', 'cure', 'heal', 'options']):
            return 'treatment_info'
        
        # Side effects
        if any(word in query_lower for word in ['side effect', 'adverse', 'reaction', 'symptoms']):
            return 'side_effects'
        
        # Prognosis
        if any(word in query_lower for word in ['prognosis', 'survival', 'outlook', 'recovery', 'rate']):
            return 'prognosis'
        
        # Lifestyle
        if any(word in query_lower for word in ['diet', 'food', 'nutrition', 'exercise', 'lifestyle']):
            return 'lifestyle'
        
        # Cost
        if any(word in query_lower for word in ['cost', 'price', 'expensive', 'insurance']):
            return 'cost'
        
        return 'general_info'
    
    def _generate_main_response(self, query: str, entities: Dict[str, List[str]], intent: str) -> str:
        """Generate the main response text"""
        
        response_parts = []
        
        # Start with appropriate template
        if intent in self.templates:
            template = random.choice(self.templates[intent])
            
            # Fill in template variables
            if entities.get('cancer_types'):
                cancer_type = entities['cancer_types'][0]
                template = template.format(cancer_type=cancer_type)
            elif entities.get('treatments'):
                treatment = entities['treatments'][0]
                template = template.format(treatment=treatment)
            
            response_parts.append(template)
        
        # Add specific information based on intent and entities
        if intent == 'treatment_info':
            response_parts.extend(self._generate_treatment_info(entities))
        elif intent == 'side_effects':
            response_parts.extend(self._generate_side_effects_info(entities))
        elif intent == 'prognosis':
            response_parts.extend(self._generate_prognosis_info(entities))
        elif intent == 'lifestyle':
            response_parts.extend(self._generate_lifestyle_info(entities))
        elif intent == 'cost':
            response_parts.extend(self._generate_cost_info(entities))
        else:
            response_parts.extend(self._generate_general_info(entities, query))
        
        return '\n\n'.join(response_parts)
    
    def _generate_treatment_info(self, entities: Dict[str, List[str]]) -> List[str]:
        """Generate treatment information"""
        
        info_parts = []
        
        # If cancer type is specified
        if entities.get('cancer_types'):
            cancer_type = entities['cancer_types'][0]
            cancer_info = self.data_handler.search_cancer_info(cancer_type)
            
            if cancer_info:
                treatments = cancer_info.get('treatments', '')
                info_parts.append(f"**Main treatments:** {treatments}")
                
                if cancer_info.get('survival_rate'):
                    info_parts.append(f"**Survival rate:** {cancer_info['survival_rate']}")
        
        # If specific treatments mentioned
        if entities.get('treatments'):
            for treatment in entities['treatments']:
                treatment_data = self.data_handler.search_treatments(treatment_type=treatment)
                if not treatment_data.empty:
                    treatment_info = treatment_data.iloc[0]
                    info_parts.append(f"**{treatment}:**")
                    info_parts.append(f"- Effectiveness: {treatment_info.get('effectiveness', 'Varies')}")
                    info_parts.append(f"- Duration: {treatment_info.get('duration', 'Varies')}")
                    info_parts.append(f"- Used for: {treatment_info.get('cancer_types', 'Multiple types')}")
        
        if not info_parts:
            info_parts.append("Treatment options depend on cancer type, stage, and individual factors. Common approaches include surgery, chemotherapy, radiation therapy, immunotherapy, and targeted therapy.")
        
        return info_parts
    
    def _generate_side_effects_info(self, entities: Dict[str, List[str]]) -> List[str]:
        """Generate side effects information"""
        
        info_parts = []
        
        if entities.get('treatments'):
            for treatment in entities['treatments']:
                side_effects = self.data_handler.get_side_effects_for_treatment(treatment)
                
                if side_effects:
                    info_parts.append(f"**{treatment} side effects:**")
                    for se in side_effects[:5]:  # Limit to top 5
                        frequency = se.get('frequency', 'Unknown')
                        severity = se.get('severity', 'Variable')
                        info_parts.append(f"- {se['side_effect']}: {frequency}% frequency, {severity} severity")
                else:
                    # Generic side effects
                    treatment_data = self.data_handler.search_treatments(treatment_type=treatment)
                    if not treatment_data.empty:
                        se_list = treatment_data.iloc[0].get('side_effects', 'Varies by individual')
                        info_parts.append(f"**{treatment} side effects:** {se_list}")
        
        if not info_parts:
            info_parts.append("Side effects vary depending on the specific treatment and individual factors. Common side effects across cancer treatments include fatigue, nausea, hair loss, and changes in blood counts.")
        
        # Add general advice
        info_parts.append("\n**Managing side effects:**")
        info_parts.append("- Report all side effects to your healthcare team")
        info_parts.append("- Many side effects can be prevented or managed")
        info_parts.append("- Side effects are usually temporary")
        
        return info_parts
    
    def _generate_prognosis_info(self, entities: Dict[str, List[str]]) -> List[str]:
        """Generate prognosis information"""
        
        info_parts = []
        
        if entities.get('cancer_types'):
            cancer_type = entities['cancer_types'][0]
            cancer_info = self.data_handler.search_cancer_info(cancer_type)
            
            if cancer_info:
                if cancer_info.get('survival_rate'):
                    info_parts.append(f"**5-year survival rate for {cancer_type}:** {cancer_info['survival_rate']}")
                
                if cancer_info.get('stage'):
                    info_parts.append(f"**Stage:** {cancer_info['stage']}")
        
        # General prognosis factors
        info_parts.append("\n**Factors affecting prognosis:**")
        info_parts.append("- Type and stage of cancer")
        info_parts.append("- Overall health and age")
        info_parts.append("- Response to treatment")
        info_parts.append("- Access to specialized care")
        
        info_parts.append("\n**Important notes:**")
        info_parts.append("- Statistics are based on large groups and may not reflect individual outcomes")
        info_parts.append("- New treatments are continuously improving outcomes")
        info_parts.append("- Each person's situation is unique")
        
        return info_parts
    
    def _generate_lifestyle_info(self, entities: Dict[str, List[str]]) -> List[str]:
        """Generate lifestyle and nutrition information"""
        
        info_parts = []
        
        info_parts.append("**General nutrition guidelines during treatment:**")
        info_parts.append("- Maintain adequate protein intake for healing")
        info_parts.append("- Stay hydrated with plenty of fluids")
        info_parts.append("- Eat small, frequent meals if experiencing nausea")
        info_parts.append("- Include fruits and vegetables when tolerated")
        
        info_parts.append("\n**Physical activity:**")
        info_parts.append("- Light exercise as tolerated and approved by your team")
        info_parts.append("- Walking is often beneficial")
        info_parts.append("- Rest when needed")
        
        info_parts.append("\n**Additional recommendations:**")
        info_parts.append("- Avoid alcohol during treatment")
        info_parts.append("- Practice good hygiene to prevent infections")
        info_parts.append("- Get adequate sleep")
        info_parts.append("- Consider counseling or support groups")
        
        return info_parts
    
    def _generate_cost_info(self, entities: Dict[str, List[str]]) -> List[str]:
        """Generate cost information"""
        
        info_parts = []
        
        if entities.get('treatments'):
            for treatment in entities['treatments']:
                treatment_data = self.data_handler.search_treatments(treatment_type=treatment)
                if not treatment_data.empty:
                    cost_range = treatment_data.iloc[0].get('cost_range', 'Varies significantly')
                    info_parts.append(f"**{treatment} cost range:** {cost_range}")
        
        info_parts.append("\n**Important cost considerations:**")
        info_parts.append("- Costs vary widely by location and facility")
        info_parts.append("- Insurance coverage varies by plan")
        info_parts.append("- Financial assistance programs may be available")
        info_parts.append("- Consider getting cost estimates before treatment")
        
        info_parts.append("\n**Resources for financial assistance:**")
        info_parts.append("- Hospital financial counselors")
        info_parts.append("- Cancer organization grant programs")
        info_parts.append("- Pharmaceutical company patient assistance programs")
        info_parts.append("- Government programs (Medicare, Medicaid)")
        
        return info_parts
    
    def _generate_general_info(self, entities: Dict[str, List[str]], query: str) -> List[str]:
        """Generate general information response"""
        
        info_parts = []
        
        # Search FAQ for relevant information
        faq_results = self.data_handler.search_faq(query)
        
        if faq_results:
            info_parts.append("**Relevant information:**")
            for faq in faq_results[:2]:  # Limit to 2 most relevant
                info_parts.append(f"**Q:** {faq['question']}")
                info_parts.append(f"**A:** {faq['answer']}\n")
        
        # Add entity-specific information
        if entities.get('cancer_types'):
            cancer_type = entities['cancer_types'][0]
            cancer_info = self.data_handler.search_cancer_info(cancer_type)
            if cancer_info:
                info_parts.append(f"**About {cancer_type}:**")
                if cancer_info.get('symptoms'):
                    info_parts.append(f"Common symptoms: {cancer_info['symptoms']}")
                if cancer_info.get('common_age'):
                    info_parts.append(f"Most common age group: {cancer_info['common_age']}")
        
        if not info_parts:
            info_parts.append("I'd be happy to help with cancer treatment information. You can ask about specific cancer types, treatments, side effects, or general questions about cancer care.")
        
        return info_parts
    
    def _collect_related_data(self, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Collect related data for visualization"""
        
        related_data = {}
        
        # Collect treatment data
        if entities.get('cancer_types') or entities.get('treatments'):
            cancer_type = entities.get('cancer_types', [None])[0]
            treatment_type = entities.get('treatments', [None])[0]
            
            treatments = self.data_handler.search_treatments(cancer_type, treatment_type)
            if not treatments.empty:
                related_data['treatments'] = treatments.to_dict('records')
        
        # Collect side effects data
        if entities.get('treatments'):
            side_effects_freq = {}
            for treatment in entities['treatments']:
                side_effects = self.data_handler.get_side_effects_for_treatment(treatment)
                for se in side_effects:
                    side_effects_freq[se['side_effect']] = se.get('frequency', 0)
            
            if side_effects_freq:
                related_data['side_effects'] = side_effects_freq
        
        return related_data
