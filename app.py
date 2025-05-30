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
    """Landing page with overview"""
    # Get sample data for display
    cancer_count = len(data_handler.get_cancer_types())
    treatment_count = len(data_handler.get_treatments())
    side_effect_count = len(data_handler.get_side_effects())
    
    # Get example queries for landing page
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
                         example_queries=example_queries,
                         cancer_count=cancer_count,
                         treatment_count=treatment_count,
                         side_effect_count=side_effect_count)

@app.route('/chat')
def chat():
    """Full-page chat interface"""
    return render_template('chat.html')

@app.route('/statistics')
def statistics():
    """Statistics and Analytics page"""
    # Get comprehensive data for statistics display
    cancer_count = len(data_handler.get_cancer_types())
    treatment_count = len(data_handler.get_treatments())
    side_effect_count = len(data_handler.get_side_effects())
    query_count = 1247  # This could be stored in a database in a real application
    
    # Get example queries for the statistics page
    example_queries = [
        "What are treatment options for breast cancer stage 2?",
        "Side effects of chemotherapy?",
        "Diet recommendations during radiation?",
        "Recovery time after surgery?",
        "What is immunotherapy for lung cancer?",
        "How does radiation therapy work?",
        "Symptoms of ovarian cancer?",
        "Cost of cancer treatments?",
        "Nutrition during cancer treatment?",
        "Mental health support for cancer patients?"
    ]
    
    return render_template('statistics.html',
                         cancer_count=cancer_count,
                         treatment_count=treatment_count,
                         side_effect_count=side_effect_count,
                         query_count=query_count,
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

from flask import Flask, render_template, request, jsonify
import json
from nlp_processor import NLPProcessor
from data_handler import DataHandler
from response_generator import ResponseGenerator
from nlp_pipeline import pipeline_pretraitement_requete
from biobert_qa import BioBERTPlaceholder
biobert_model = BioBERTPlaceholder()




app = Flask(__name__)

# Initialize components
data_handler = DataHandler()
nlp_processor = NLPProcessor()
response_generator = ResponseGenerator(data_handler)

@app.route('/')
def index():
    """Landing page with overview"""
    # Get sample data for display
    cancer_count = len(data_handler.get_cancer_types())
    treatment_count = len(data_handler.get_treatments())
    side_effect_count = len(data_handler.get_side_effects())
    
    # Get example queries for landing page
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
                         example_queries=example_queries,
                         cancer_count=cancer_count,
                         treatment_count=treatment_count,
                         side_effect_count=side_effect_count)

@app.route('/chat')
def chat():
    """Full-page chat interface"""
    return render_template('chat.html')

# @app.route('/statistics')
# def statistics():
#     """Statistics and Analytics page"""
#     # Get comprehensive data for statistics display
#     cancer_count = len(data_handler.get_cancer_types())
#     treatment_count = len(data_handler.get_treatments())
#     side_effect_count = len(data_handler.get_side_effects())
#     query_count = 1247  # This could be stored in a database in a real application

@app.route('/statistics')
def statistics():
    return render_template("statistics.html", cancer_count=52, treatment_count=210, side_effect_count=103)

 
    # Get example queries for the statistics page
    example_queries = [
        "What are treatment options for breast cancer stage 2?",
        "Side effects of chemotherapy?",
        "Diet recommendations during radiation?",
        "Recovery time after surgery?",
        "What is immunotherapy for lung cancer?",
        "How does radiation therapy work?",
        "Symptoms of ovarian cancer?",
        "Cost of cancer treatments?",
        "Nutrition during cancer treatment?",
        "Mental health support for cancer patients?"
    ]
    
    return render_template('statistics.html',
                         cancer_count=cancer_count,
                         treatment_count=treatment_count,
                         side_effect_count=side_effect_count,
                         query_count=query_count,
                         example_queries=example_queries)

@app.route('/api/query', methods=['POST'])
def process_query():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'error': 'Veuillez entrer une question.'}), 400

        # NLP preprocessing
        nlp_result = pipeline_pretraitement_requete(query)
        entities = nlp_result['entites']
        tokens = nlp_result['tokens']

        # TODO: use real context later
        dummy_context = "Cancer is treated using chemotherapy, radiation, surgery, and targeted therapies."
        biobert_answer = biobert_model.answer_question(query, context=dummy_context)

        return jsonify({
            'success': True,
            'response': biobert_answer,
            'entities': entities,
            'tokens': tokens,
            'intent': 'biobert_test'
        })

    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement : {str(e)}'}), 500

    
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
