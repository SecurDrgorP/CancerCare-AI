import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp_pipeline import (
    nettoyage_normalisation,
    tokenisation_lemmatisation_stopwords,
    ner_medical,
    pipeline_pretraitement_requete,
    download_spacy_model,
    load_spacy_model
)


class TestNLPPipeline(unittest.TestCase):
    """Test cases for NLP pipeline functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_text_en = "What are the side effects of chemotherapy?"
        self.test_text_fr = "Quels sont les effets secondaires de la chimiothérapie?"
        self.test_text_mixed = "Cancer treatment with radiation therapy."
        
    def test_nettoyage_normalisation_english(self):
        """Test text cleaning and normalization for English"""
        input_text = "What are the SIDE-EFFECTS of chemotherapy?! 😊"
        expected = "what are the side effects of chemotherapy"
        result = nettoyage_normalisation(input_text, "en")
        self.assertEqual(result, expected)
        
    def test_nettoyage_normalisation_french(self):
        """Test text cleaning and normalization for French"""
        input_text = "Quels sont les effets secondaires de la chimiothérapie?!"
        expected = "quels sont les effets secondaires de la chimiothérapie"
        result = nettoyage_normalisation(input_text, "fr")
        self.assertEqual(result, expected)
        
    def test_nettoyage_normalisation_special_chars(self):
        """Test cleaning with special characters"""
        input_text = "Cancer   treatment!!!   @#$%"
        expected = "cancer treatment"
        result = nettoyage_normalisation(input_text, "en")
        self.assertEqual(result, expected)
        
    @patch('nlp_pipeline.nlp_en')
    def test_tokenisation_lemmatisation_stopwords_english(self, mock_nlp_en):
        """Test tokenization, lemmatization, and stopword removal for English"""
        # Mock spaCy doc and tokens
        mock_token1 = MagicMock()
        mock_token1.lemma_ = "side"
        mock_token1.is_stop = False
        mock_token1.is_punct = False
        mock_token1.is_space = False
        
        mock_token2 = MagicMock()
        mock_token2.lemma_ = "effect"
        mock_token2.is_stop = False
        mock_token2.is_punct = False
        mock_token2.is_space = False
        
        mock_token3 = MagicMock()
        mock_token3.lemma_ = "the"
        mock_token3.is_stop = True
        mock_token3.is_punct = False
        mock_token3.is_space = False
        
        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_token1, mock_token2, mock_token3]))
        mock_nlp_en.return_value = mock_doc
        
        result = tokenisation_lemmatisation_stopwords("side effects", "en")
        expected = ["side", "effect"]
        self.assertEqual(result, expected)
        
    @patch('nlp_pipeline.nlp_en')
    def test_ner_medical_english(self, mock_nlp_en):
        """Test named entity recognition for English"""
        # Mock spaCy entities
        mock_ent1 = MagicMock()
        mock_ent1.text = "chemotherapy"
        mock_ent1.label_ = "TREATMENT"
        
        mock_ent2 = MagicMock()
        mock_ent2.text = "cancer"
        mock_ent2.label_ = "CONDITION"
        
        mock_doc = MagicMock()
        mock_doc.ents = [mock_ent1, mock_ent2]
        mock_nlp_en.return_value = mock_doc
        
        result = ner_medical("chemotherapy for cancer", "en")
        expected = [
            {"text": "chemotherapy", "label": "TREATMENT"},
            {"text": "cancer", "label": "CONDITION"}
        ]
        self.assertEqual(result, expected)
        
    @patch('nlp_pipeline.detect')
    @patch('nlp_pipeline.ner_medical')
    @patch('nlp_pipeline.tokenisation_lemmatisation_stopwords')
    @patch('nlp_pipeline.nettoyage_normalisation')
    def test_pipeline_pretraitement_requete_english(self, mock_clean, mock_tokens, mock_ner, mock_detect):
        """Test the complete preprocessing pipeline for English"""
        # Mock all dependencies
        mock_detect.return_value = "en"
        mock_clean.return_value = "clean text"
        mock_tokens.return_value = ["token1", "token2"]
        mock_ner.return_value = [{"text": "entity", "label": "LABEL"}]
        
        input_text = "What are side effects?"
        result = pipeline_pretraitement_requete(input_text)
        
        # Verify the structure
        self.assertIn("langue_detectee", result)
        self.assertIn("texte_original", result)
        self.assertIn("texte_nettoye", result)
        self.assertIn("tokens", result)
        self.assertIn("entites", result)
        
        # Verify values
        self.assertEqual(result["langue_detectee"], "en")
        self.assertEqual(result["texte_original"], input_text)
        self.assertEqual(result["texte_nettoye"], "clean text")
        self.assertEqual(result["tokens"], ["token1", "token2"])
        self.assertEqual(result["entites"], [{"text": "entity", "label": "LABEL"}])
        
    @patch('nlp_pipeline.detect')
    @patch('nlp_pipeline.ner_medical')
    @patch('nlp_pipeline.tokenisation_lemmatisation_stopwords')
    @patch('nlp_pipeline.nettoyage_normalisation')
    def test_pipeline_pretraitement_requete_french(self, mock_clean, mock_tokens, mock_ner, mock_detect):
        """Test the complete preprocessing pipeline for French"""
        mock_detect.return_value = "fr"
        mock_clean.return_value = "texte propre"
        mock_tokens.return_value = ["mot1", "mot2"]
        mock_ner.return_value = [{"text": "entité", "label": "ETIQUETTE"}]
        
        input_text = "Quels sont les effets secondaires?"
        result = pipeline_pretraitement_requete(input_text)
        
        self.assertEqual(result["langue_detectee"], "fr")
        self.assertEqual(result["texte_original"], input_text)
        
    @patch('nlp_pipeline.detect')
    def test_pipeline_language_detection_fallback(self, mock_detect):
        """Test language detection fallback to English"""
        # Test when detect raises exception
        mock_detect.side_effect = Exception("Detection failed")
        
        with patch('nlp_pipeline.nettoyage_normalisation') as mock_clean, \
             patch('nlp_pipeline.tokenisation_lemmatisation_stopwords') as mock_tokens, \
             patch('nlp_pipeline.ner_medical') as mock_ner:
            
            mock_clean.return_value = "clean"
            mock_tokens.return_value = []
            mock_ner.return_value = []
            
            result = pipeline_pretraitement_requete("Some text")
            self.assertEqual(result["langue_detectee"], "en")
            
    @patch('nlp_pipeline.detect')
    def test_pipeline_unsupported_language_fallback(self, mock_detect):
        """Test fallback to English for unsupported languages"""
        mock_detect.return_value = "de"  # German - not supported
        
        with patch('nlp_pipeline.nettoyage_normalisation') as mock_clean, \
             patch('nlp_pipeline.tokenisation_lemmatisation_stopwords') as mock_tokens, \
             patch('nlp_pipeline.ner_medical') as mock_ner:
            
            mock_clean.return_value = "clean"
            mock_tokens.return_value = []
            mock_ner.return_value = []
            
            result = pipeline_pretraitement_requete("Deutscher Text")
            self.assertEqual(result["langue_detectee"], "en")
            
    @patch('subprocess.check_call')
    def test_download_spacy_model_success(self, mock_subprocess):
        """Test successful spaCy model download"""
        mock_subprocess.return_value = None
        
        # Should not raise exception
        download_spacy_model("en_core_web_sm")
        mock_subprocess.assert_called_once()
        
    @patch('subprocess.check_call')
    def test_download_spacy_model_failure(self, mock_subprocess):
        """Test spaCy model download failure"""
        mock_subprocess.side_effect = Exception("Download failed")
        
        with self.assertRaises(Exception):
            download_spacy_model("invalid_model")
            
    @patch('spacy.load')
    def test_load_spacy_model_success(self, mock_spacy_load):
        """Test successful spaCy model loading"""
        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp
        
        result = load_spacy_model("en_core_web_sm")
        self.assertEqual(result, mock_nlp)
        
    @patch('spacy.load')
    @patch('nlp_pipeline.download_spacy_model')
    def test_load_spacy_model_download_on_missing(self, mock_download, mock_spacy_load):
        """Test spaCy model download when model is missing"""
        # First call raises OSError, second call succeeds
        mock_spacy_load.side_effect = [OSError("Model not found"), MagicMock()]
        
        result = load_spacy_model("en_core_web_sm")
        
        # Verify download was called
        mock_download.assert_called_once_with("en_core_web_sm")
        # Verify load was called twice
        self.assertEqual(mock_spacy_load.call_count, 2)


class TestNLPPipelineIntegration(unittest.TestCase):
    """Integration tests for NLP pipeline with real spaCy models"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures"""
        # These tests will only run if spaCy models are available
        try:
            import spacy
            cls.nlp_en = spacy.load("en_core_web_sm")
            cls.spacy_available = True
        except OSError:
            cls.spacy_available = False
            
    def setUp(self):
        """Skip tests if spaCy models not available"""
        if not self.spacy_available:
            self.skipTest("spaCy models not available")
            
    def test_real_english_processing(self):
        """Test with real English text and spaCy model"""
        text = "Chemotherapy causes nausea and fatigue in cancer patients."
        result = pipeline_pretraitement_requete(text)
        
        # Check structure
        self.assertIn("langue_detectee", result)
        self.assertIn("tokens", result)
        self.assertIn("entites", result)
        
        # Check language detection
        self.assertEqual(result["langue_detectee"], "en")
        
        # Check tokens are not empty
        self.assertGreater(len(result["tokens"]), 0)
        
        # Check that medical terms are tokenized
        tokens_lower = [token.lower() for token in result["tokens"]]
        self.assertIn("chemotherapy", tokens_lower)
        
    def test_medical_terminology_extraction(self):
        """Test extraction of medical terminology"""
        text = "Breast cancer treatment includes surgery, chemotherapy, and radiation therapy."
        result = pipeline_pretraitement_requete(text)
        
        # Check that medical terms are preserved in tokens
        tokens_lower = [token.lower() for token in result["tokens"]]
        medical_terms = ["cancer", "treatment", "surgery", "chemotherapy", "radiation", "therapy"]
        
        for term in medical_terms:
            self.assertIn(term, tokens_lower)


if __name__ == '__main__':
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestNLPPipeline))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestNLPPipelineIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)