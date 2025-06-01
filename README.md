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

3. **Download and save the BioBERT model locally** (REQUIRED - run this first):
   ```bash
   python scripts/saveModel.py
   ```
   This will download the BioBERT model (~1.3GB) and save it locally in the `model/` directory.

4. **spaCy models will be automatically downloaded** on first run (no manual installation needed)

5. **Run the Flask application**:
   ```bash
   python app.py
   ```
   or
   ```bash
   flask run
   ```

6. **Open your browser** and navigate to `http://localhost:5000`

## 📁 Project Structure

```
CancerCare-AI/
├── app.py                    # Main Flask application with routes
├── biobert_qa.py            # BioBERT question answering implementation
├── nlp_pipeline.py          # NLP processing with automatic spaCy downloading
├── context_provider.py      # Semantic context retrieval using sentence transformers
├── data_handler.py          # Data management and processing
├── requirements.txt         # Python dependencies
├── scripts/                 # Setup and utility scripts
│   └── saveModel.py         # BioBERT model download and setup script
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

### Web Interface

1. **Landing Page** (`/`): Overview with example queries and statistics
2. **Chat Interface** (`/chat`): Full-page chat with AI-powered responses
3. **Statistics Dashboard** (`/statistics`): Analytics and treatment insights

### API Endpoints

- `POST /api/chat`: Send questions and receive AI-generated answers
- `GET /api/statistics`: Retrieve treatment and cancer statistics

### Sample Queries

- "What are treatment options for breast cancer stage 2?"
- "Side effects of chemotherapy?"
- "Diet recommendations during radiation?"
- "Recovery time after surgery?"
- "What is immunotherapy for lung cancer?"
- "How does radiation therapy work?"
- "Symptoms of ovarian cancer?"
- "Cost of cancer treatments?"

### Key Components

1. **Flask Application (`app.py`)**
   - RESTful API with multiple routes
   - Template rendering with Jinja2
   - Integration with AI models and data handlers
   - Error handling and logging

2. **BioBERT QA System (`biobert_qa.py`)**
   - Loads pre-trained BioBERT model from local storage
   - Performs extractive question answering
   - Optimized for biomedical text understanding
   - GPU/CPU compatibility with automatic device detection

3. **NLP Pipeline (`nlp_pipeline.py`)**
   - Automatic spaCy model downloading (en_core_web_sm, fr_core_news_sm)
   - Multilingual text processing (English/French)
   - Language detection and normalization
   - Medical entity extraction and text cleaning

4. **Context Provider (`context_provider.py`)**
   - Sentence transformer-based semantic search
   - Finds most relevant context from knowledge base
   - Uses all-MiniLM-L6-v2 model for embeddings
   - Efficient similarity matching and ranking

5. **Data Handler (`data_handler.py`)**
   - Manages medical datasets and knowledge base
   - Provides structured access to cancer information
   - Statistics generation and data aggregation

## 🧪 Testing

The project includes a comprehensive test suite covering all major components.

### Running Tests

1. **Run all tests**:
   ```bash
   pytest
   ```

2. **Run tests with verbose output**:
   ```bash
   pytest -v
   ```

3. **Run specific test file**:
   ```bash
   pytest tests/test_biobert_qa.py
   ```

4. **Run tests with coverage report**:
   ```bash
   pytest --cov=. --cov-report=html
   ```

### Test Structure

- **`test_biobert_qa.py`**: Tests BioBERT model initialization, question answering, and error handling
- **`test_nlp_pipeline.py`**: Tests NLP processing, language detection, and spaCy model management
- **`test_context_provider.py`**: Tests semantic search, embedding generation, and context retrieval
- **`test_data_handler.py`**: Tests data loading, management, and statistics generation

### Test Coverage

The test suite covers:
- ✅ Model loading and initialization
- ✅ Question answering accuracy
- ✅ NLP pipeline processing
- ✅ Context retrieval functionality
- ✅ Data handling and management
- ✅ Error handling and edge cases
- ✅ API endpoint responses

## 📊 Data Sources

The application uses curated medical datasets including:

- **Cancer Types**: 10+ common cancer types with staging and symptoms
- **Treatments**: 10+ treatment modalities with effectiveness and costs
- **Side Effects**: 20+ common side effects with frequencies
- **FAQ**: 20+ frequently asked questions with medical answers

## 🔧 Technical Stack

- **Backend**: Flask web framework with Jinja2 templating
- **AI/ML**: BioBERT (Transformers), Sentence Transformers, PyTorch
- **NLP**: spaCy (with automatic model downloading), NLTK, langdetect
- **Frontend**: HTML5, Bootstrap 5, Chart.js, Custom CSS/JavaScript
- **Data Processing**: Pandas, NumPy for data manipulation
- **Visualization**: Chart.js for interactive web charts, Matplotlib/Seaborn for analytics
- **Testing**: pytest with comprehensive test coverage
- **Dependencies**: See `requirements.txt` for complete list
- **Model Storage**: Local BioBERT model (~1.3GB) for offline operation

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application provides general information for educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

## 🎯 Success Criteria

- ✅ AI-powered question answering using BioBERT for biomedical accuracy
- ✅ Modern, responsive web interface with professional medical design
- ✅ Comprehensive test suite with good coverage
- ✅ Automatic dependency management (spaCy models)
- ✅ Cross-platform compatibility (Windows, macOS, Linux)
- ✅ Proper medical disclaimers throughout the application
- ✅ Fast response times with local model inference
- ✅ Semantic context retrieval for relevant information

## 🚀 Future Enhancements

- **Enhanced AI Models**: Integration with newer biomedical language models
- **Real-time Data**: Connection to medical databases and research APIs
- **Personalized Responses**: User profile-based recommendations
- **Multi-language Support**: Expansion beyond English and French
- **Mobile App**: React Native or Flutter mobile application
- **Voice Interface**: Speech-to-text and text-to-speech capabilities
- **Clinical Integration**: EHR integration and clinical decision support
- **Advanced Analytics**: Machine learning for treatment outcome predictions

## 🔧 Troubleshooting

### Common Issues

1. **Model Download Issues**:
   ```bash
   # If saveModel.py fails, try manually:
   python scripts/saveModel.py
   ```

2. **spaCy Model Problems**:
   ```bash
   # Manual installation if auto-download fails:
   python -m spacy download en_core_web_sm
   python -m spacy download fr_core_news_sm
   ```

3. **Memory Issues**:
   - Ensure at least 4GB RAM available
   - Close other applications when running BioBERT
   - Consider using smaller batch sizes

4. **Port Already in Use**:
   ```bash
   # Use a different port:
   export FLASK_RUN_PORT=5001
   flask run
   ```

5. **Import Errors**:
   ```bash
   # Reinstall dependencies:
   pip install -r requirements.txt --force-reinstall
   ```

### Testing Issues

If tests fail, check:
- All dependencies are installed: `pip install -r requirements.txt`
- BioBERT model is downloaded: `python scripts/saveModel.py`
- Python version compatibility (3.8+)

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