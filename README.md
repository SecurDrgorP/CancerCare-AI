# Cancer Treatment Assistant 🏥

A comprehensive web application built with Python and Streamlit that provides intelligent information about cancer treatments, side effects, and medical guidance using NLP processing.

## ✨ Features

- **Interactive Chat Interface**: Ask questions about cancer treatments in natural language
- **Medical NLP Processing**: Extracts cancer types, treatments, and symptoms from user queries
- **Comprehensive Knowledge Base**: Local CSV/JSON datasets with cancer treatment information
- **Smart Response Generation**: Template-based answers with relevant medical information
- **Data Visualizations**: Interactive charts for treatment options and side effects
- **Medical Disclaimers**: Proper warnings about consulting healthcare professionals
- **Modern UI**: Clean, medical-themed interface with example questions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

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

3. **Download spaCy language model** (optional but recommended):
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
cancer_assistant/
├── app.py                 # Main Streamlit application
├── nlp_processor.py       # NLP functions and entity extraction
├── data_handler.py        # Data loading and management
├── response_generator.py  # Intelligent response generation
├── requirements.txt       # Python dependencies
├── data/                  # Medical data files
│   ├── cancer_types.csv   # Cancer information and stages
│   ├── treatments.csv     # Treatment options and details
│   ├── side_effects.csv   # Side effects and frequencies
│   └── faq.json          # Frequently asked questions
└── README.md             # Project documentation
```

## 💡 Usage Examples

### Sample Queries

- "What are treatment options for breast cancer stage 2?"
- "Side effects of chemotherapy?"
- "Diet recommendations during radiation?"
- "Recovery time after surgery?"
- "How does immunotherapy work for lung cancer?"
- "Cost of cancer treatments?"

### Key Components

1. **Main App (`app.py`)**
   - Streamlit interface with medical theme
   - Query input and response display
   - Sidebar with example questions
   - Treatment overview charts

2. **NLP Processor (`nlp_processor.py`)**
   - Medical entity extraction (cancer types, treatments, symptoms)
   - Query intent classification
   - Text preprocessing and cleanup

3. **Data Handler (`data_handler.py`)**
   - Loads and manages medical datasets
   - Provides search functionality
   - Creates sample data if files are missing

4. **Response Generator (`response_generator.py`)**
   - Generates intelligent, contextual responses
   - Uses templates for different query types
   - Includes medical disclaimers

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

## 🚀 Future Enhancements

- Integration with medical APIs for real-time data
- Machine learning models for better response accuracy
- Multi-language support
- Voice interface capabilities
- Integration with electronic health records
- Personalized treatment recommendations

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is intended for educational and research purposes. Please ensure compliance with medical information regulations in your jurisdiction.

## 📞 Support

For questions or support, please refer to the documentation or create an issue in the repository.

---

**Built with ❤️ for cancer patients and caregivers**