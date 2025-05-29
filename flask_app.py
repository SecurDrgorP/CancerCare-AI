from flask import Flask, render_template, request, jsonify
import json
from nlp_processor import NLPProcessor
from data_handler import DataHandler
from response_generator import ResponseGenerator

app = Flask(__name__)

# Initialize components
data_handler = DataHandler()
nlp_processor = NLPProcessor()
response_generator = ResponseGenerator(data_handler)

@app.route('/')
def index():
    """Main page"""
    # Get sample data for display
    cancer_count = len(data_handler.get_cancer_types())
    treatment_count = len(data_handler.get_treatments())
    
    # Get example queries
    example_queries = [
        "What are treatment options for breast cancer stage 2?",
        "Side effects of chemotherapy?",
        "Diet recommendations during radiation?",
        "Recovery time after surgery?",
        "What is immunotherapy for lung cancer?",
        "How does radiation therapy work?",
        "Symptoms of ovarian cancer?",
        "Cost of cancer treatments?"
    ]
    
    return render_template('index.html', 
                         cancer_count=cancer_count,
                         treatment_count=treatment_count,
                         example_queries=example_queries)

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process user query and return response"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter a question.'}), 400
        
        # Extract entities from query
        entities = nlp_processor.extract_entities(query)
        
        # Generate response
        response = response_generator.generate_response(query, entities)
        
        return jsonify({
            'success': True,
            'response': response['text'],
            'entities': entities,
            'related_data': response.get('related_data', {}),
            'intent': response.get('intent', 'general_info')
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing query: {str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    """Get application statistics"""
    try:
        treatments = data_handler.get_treatments()
        treatment_stats = {}
        
        if not treatments.empty:
            # Count treatments by category
            treatment_counts = treatments.groupby('category').size().to_dict()
            treatment_stats = treatment_counts
        
        side_effects = data_handler.get_side_effects()
        side_effect_stats = {}
        
        if not side_effects.empty:
            # Get top side effects by frequency
            top_side_effects = side_effects.nlargest(5, 'frequency')[['side_effect', 'frequency']].to_dict('records')
            side_effect_stats = {se['side_effect']: se['frequency'] for se in top_side_effects}
        
        return jsonify({
            'treatment_categories': treatment_stats,
            'top_side_effects': side_effect_stats
        })
        
    except Exception as e:
        return jsonify({'error': f'Error getting stats: {str(e)}'}), 500

@app.route('/api/data/<data_type>')
def get_data(data_type):
    """Get specific data for display"""
    try:
        if data_type == 'cancer_types':
            data = data_handler.get_cancer_types().to_dict('records')
        elif data_type == 'treatments':
            data = data_handler.get_treatments().to_dict('records')
        elif data_type == 'side_effects':
            data = data_handler.get_side_effects().to_dict('records')
        else:
            return jsonify({'error': 'Invalid data type'}), 400
        
        return jsonify({'data': data})
        
    except Exception as e:
        return jsonify({'error': f'Error getting data: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
