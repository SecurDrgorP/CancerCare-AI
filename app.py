from flask import Flask, render_template, request, jsonify
from data_handler import DataHandler
from biobert_qa import BioBERT_QA
from nlp_pipeline import pipeline_pretraitement_requete

from context_provider import LocalContextRetriever

app = Flask(__name__)

# Initialize BioBERT model for question answering
context_provider = LocalContextRetriever("data/cancer_qa_dataset.json")
biobert_model = BioBERT_QA()

# Initialize components
data_handler = DataHandler()

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

@app.route('/api/query', methods=['POST'])
def process_query():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'error': 'Veuillez entrer une question.'}), 400

        nlp_result = pipeline_pretraitement_requete(query)
        entities = nlp_result['entites']
        tokens = nlp_result['tokens']

        print(f"\n🔎 Query received: {query}")

        # Get best matching context answer from JSON
        answer_blocks = context_provider.get_best_answer_chunks(query)
        print("🔍 Top context block(s):")
        for block in answer_blocks:
            print(block[:200], "...")

        candidate_sentences = []
        for block in answer_blocks:
            candidate_sentences.extend(context_provider.split_into_sentences(block))

        print(f"🧠 Extracted {len(candidate_sentences)} candidate sentences.")
        final_answer = "No clear answer found."

        for sentence in candidate_sentences:
            print(f"\n🧩 Sentence: {sentence}")
            answer = biobert_model.answer_question(query, context=sentence)
            print(f"🤖 Answer: {answer}")
            if answer and isinstance(answer, str) and len(answer.strip()) > 5 and "no clear answer" not in answer.lower():
                final_answer = answer
                break

        return jsonify({
            'success': True,
            'response': final_answer,
            'entities': entities,
            'tokens': tokens,
            'intent': 'biobert_json_match'
        })

    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
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
