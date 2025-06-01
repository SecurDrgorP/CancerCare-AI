import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import json
import tempfile

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context_provider import LocalContextRetriever


class TestLocalContextRetriever(unittest.TestCase):
    """Test cases for LocalContextRetriever class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary JSON file for testing
        self.test_data = [
            {
                "question": "What are the side effects of chemotherapy?",
                "answer": "Chemotherapy can cause nausea, vomiting, fatigue, hair loss, and increased infection risk."
            },
            {
                "question": "How does radiation therapy work?",
                "answer": "Radiation therapy uses high-energy beams to destroy cancer cells and shrink tumors."
            },
            {
                "question": "What is immunotherapy?",
                "answer": "Immunotherapy helps the immune system fight cancer by boosting or restoring immune function."
            }
        ]
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        
    def tearDown(self):
        """Clean up test fixtures"""
        os.unlink(self.temp_file.name)
        
    @patch('context_provider.nltk.download')
    @patch('context_provider.SentenceTransformer')
    def test_initialization(self, mock_sentence_transformer, mock_nltk_download):
        """Test LocalContextRetriever initialization"""
        mock_model = MagicMock()
        mock_sentence_transformer.return_value = mock_model
        mock_model.encode.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]
        
        retriever = LocalContextRetriever(self.temp_file.name)
        
        # Check that nltk download was called
        mock_nltk_download.assert_called_once_with('punkt', quiet=True)
        
        # Check that data was loaded correctly
        self.assertEqual(len(retriever.questions), 3)
        self.assertEqual(len(retriever.answers), 3)
        self.assertEqual(retriever.questions[0], "What are the side effects of chemotherapy?")
        
    @patch('context_provider.nltk.download')
    @patch('context_provider.SentenceTransformer')
    @patch('context_provider.util.pytorch_cos_sim')
    def test_get_best_answer_chunks(self, mock_cos_sim, mock_sentence_transformer, mock_nltk_download):
        """Test getting best answer chunks"""
        # Mock the sentence transformer and similarity calculation
        mock_model = MagicMock()
        mock_sentence_transformer.return_value = mock_model
        mock_model.encode.side_effect = [
            [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],  # For initialization
            [0.2, 0.3, 0.4]  # For query encoding
        ]
        
        # Mock similarity scores
        mock_similarities = MagicMock()
        mock_similarities.topk.return_value.indices.tolist.return_value = [0, 1]
        mock_cos_sim.return_value = [mock_similarities]
        
        retriever = LocalContextRetriever(self.temp_file.name)
        result = retriever.get_best_answer_chunks("side effects", top_k=2)
        
        # Check that we get the expected number of answers
        self.assertEqual(len(result), 2)
        self.assertIn("Chemotherapy can cause nausea", result[0])
        
    @patch('context_provider.nltk.download')
    @patch('context_provider.SentenceTransformer')
    @patch('context_provider.sent_tokenize')
    def test_split_into_sentences(self, mock_sent_tokenize, mock_sentence_transformer, mock_nltk_download):
        """Test sentence splitting"""
        mock_sentence_transformer.return_value = MagicMock()
        mock_sent_tokenize.return_value = [
            "Chemotherapy can cause nausea and vomiting.", 
            "It may also lead to fatigue and hair loss."
        ]
        
        retriever = LocalContextRetriever(self.temp_file.name)
        text = "Chemotherapy can cause nausea and vomiting. It may also lead to fatigue and hair loss."
        result = retriever.split_into_sentences(text)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Chemotherapy can cause nausea and vomiting.")
        self.assertEqual(result[1], "It may also lead to fatigue and hair loss.")
        
    def test_file_not_found(self):
        """Test behavior when JSON file is not found"""
        with self.assertRaises(FileNotFoundError):
            LocalContextRetriever("nonexistent_file.json")
            
    @patch('context_provider.nltk.download')
    @patch('context_provider.SentenceTransformer')
    def test_empty_json_file(self, mock_sentence_transformer, mock_nltk_download):
        """Test behavior with empty JSON file"""
        # Create empty JSON file
        empty_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump([], empty_file)
        empty_file.close()
        
        try:
            mock_model = MagicMock()
            mock_sentence_transformer.return_value = mock_model
            mock_model.encode.return_value = []
            
            retriever = LocalContextRetriever(empty_file.name)
            
            # Check that empty lists are handled
            self.assertEqual(len(retriever.questions), 0)
            self.assertEqual(len(retriever.answers), 0)
            
        finally:
            os.unlink(empty_file.name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
