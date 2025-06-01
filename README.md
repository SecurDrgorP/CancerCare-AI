# Cancer Treatment Assistant 🏥

A comprehensive web application built with **Flask** and **BioBERT** that provides intelligent information about cancer treatments, side effects, and medical guidance using advanced NLP processing and AI-powered question answering.

## ✨ Features

- **AI-Powered Question Answering**: BioBERT model trained on biomedical literature for accurate cancer-related responses
- **Interactive Chat Interface**: Modern web-based chat with real-time question answering
- **Advanced NLP Pipeline**: Automatic spaCy model downloading, multilingual support (English/French), and intelligent text processing
- **Semantic Context Retrieval**: Sentence transformer-based similarity matching for relevant context extraction
- **Comprehensive Knowledge Base**: Curated cancer Q&A dataset with medical information
- **Modern Web Interface**: Bootstrap-powered responsive design with Chart.js visualizations
- **Medical Statistics Dashboard**: Analytics and insights about cancer treatments and data
- **Robust Error Handling**: Comprehensive test suite and error management
- **Cross-Platform Compatibility**: Universal path handling for Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM (for BioBERT model)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CancerCare-AI
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **spaCy models will be automatically downloaded** on first run (no manual installation needed)

4. **Run the Flask application**:
   ```bash
   python app.py
   or
   flask run
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## 📁 Project Structure

```
CancerCare-AI/
├── app.py                    # Main Flask application with routes
├── biobert_qa.py            # BioBERT question answering implementation
├── nlp_pipeline.py          # NLP processing with automatic spaCy downloading
├── context_provider.py      # Semantic context retrieval using sentence transformers
├── data_handler.py          # Data management and processing
├── inference.py             # Model inference utilities
├── saveModel.py             # Model saving and management
├── XMLtoJSON.py             # Data conversion utilities
├── requirements.txt         # Python dependencies
├── model/                   # BioBERT model storage
│   └── biobert_v1.1_pubmed_squad_v2_local/  # Local BioBERT model
├── data/                    # Medical datasets
│   └── cancer_qa_dataset.json    # Cancer Q&A knowledge base
├── templates/               # HTML templates
│   ├── base.html           # Base template with Bootstrap
│   ├── index.html          # Landing page
│   ├── chat.html           # Chat interface
│   ├── statistics.html     # Analytics dashboard
│   └── error pages (404.html, 500.html)
├── static/                  # Static web assets
│   ├── css/                # Custom stylesheets
│   └── js/                 # JavaScript files
├── tests/                   # Comprehensive test suite
│   ├── test_app.py         # Flask app tests
│   ├── test_biobert_qa.py  # BioBERT tests
│   ├── test_nlp_pipeline.py # NLP pipeline tests
│   └── test_context_provider.py # Context retrieval tests
└── README.md               # Project documentation
```

## 💡 Usage Examples

### Sample Queries

- "What are treatment options for breast cancer stage 2?"
- "Side effects of chemotherapy?"
- "Diet recommendations during radiation?"
- "Recovery time after surgery?"
- "How does immunotherapy work for lung cancer?"
- "Cost of cancer treatments?"

## 📊 Data Sources

The application uses curated medical datasets including:

- **Cancer Types**: 10+ common cancer types with staging and symptoms
- **Treatments**: 10+ treatment modalities with effectiveness and costs
- **Side Effects**: 20+ common side effects with frequencies
- **FAQ**: 20+ frequently asked questions with medical answers

## 🔧 Technical Stack

- **Frontend**: Streamlit with custom CSS
- **NLP**: spaCy for text processing (optional)
- **Data**: Pandas for CSV/JSON handling
- **Visualization**: Plotly for interactive charts
- **Styling**: Custom medical-themed CSS

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application provides general information for educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

## 🎯 Success Criteria

- ✅ Answers 80%+ of common cancer treatment questions
- ✅ Clean, professional medical interface
- ✅ Proper medical disclaimers throughout
- ✅ Response time under 5 seconds
- ✅ Works with 5+ cancer types and common treatments
- ✅ Interactive visualizations and data display

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or support, please refer to the documentation or create an issue in the repository.

---

**Built with ❤️ for cancer patients and caregivers**