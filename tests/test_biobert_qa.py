import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from biobert_qa import BioBERT_QA, clean_context


class TestCleanContext(unittest.TestCase):
    """Test cases for clean_context function"""
    
    def test_clean_context_whitespace(self):
        """Test cleaning excessive whitespace"""
        input_text = "This   has    multiple   spaces\n\nand\n\nnewlines"
        expected = "This has multiple spaces and newlines"
        result = clean_context(input_text)
        self.assertEqual(result, expected)
        
    def test_clean_context_bullet_points(self):
        """Test removing bullet points"""
        input_text = "Treatment options: - Surgery - Chemotherapy • Radiation"
        expected = "Treatment options:. Surgery. Chemotherapy. Radiation"
        result = clean_context(input_text)
        self.assertEqual(result, expected)
        
    def test_clean_context_multiple_dots(self):
        """Test replacing multiple dots"""
        input_text = "Side effects include....... nausea and fatigue..."
        expected = "Side effects include. nausea and fatigue."
        result = clean_context(input_text)
        self.assertEqual(result, expected)
        
    def test_clean_context_empty_string(self):
        """Test with empty string"""
        result = clean_context("")
        self.assertEqual(result, "")
        
    def test_clean_context_whitespace_only(self):
        """Test with whitespace only"""
        result = clean_context("   \n\n   ")
        self.assertEqual(result, "")


class TestBioBERTQA(unittest.TestCase):
    """Test cases for BioBERT_QA class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary model directory structure
        self.temp_dir = tempfile.mkdtemp()
        self.model_dir = os.path.join(self.temp_dir, "model", "biobert_v1.1_pubmed_squad_v2_local")
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Create dummy model files
        dummy_files = [
            "config.json",
            "model.safetensors", 
            "tokenizer_config.json",
            "tokenizer.json",
            "vocab.txt",
            "special_tokens_map.json"
        ]
        
        for filename in dummy_files:
            with open(os.path.join(self.model_dir, filename), 'w') as f:
                if filename == "config.json":
                    f.write('{"model_type": "bert"}')
                elif filename == "tokenizer_config.json":
                    f.write('{"tokenizer_class": "BertTokenizer"}')
                else:
                    f.write("dummy content")
                    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        
    @patch('biobert_qa.AutoTokenizer.from_pretrained')
    @patch('biobert_qa.AutoModelForQuestionAnswering.from_pretrained')
    @patch('biobert_qa.torch.device')
    def test_initialization(self, mock_device, mock_model, mock_tokenizer):
        """Test BioBERT_QA initialization"""
        # Mock the components
        mock_tokenizer_instance = MagicMock()
        mock_model_instance = MagicMock()
        mock_device_instance = MagicMock()
        
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_model.return_value = mock_model_instance
        mock_device.return_value = mock_device_instance
        
        # Change to temp directory to test relative path resolution
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            qa_model = BioBERT_QA()
            
            # Check that the model path was set correctly
            expected_path = os.path.join(os.getcwd(), "model", "biobert_v1.1_pubmed_squad_v2_local")
            self.assertEqual(qa_model.model_path, expected_path)
            
            # Check that components were initialized
            self.assertEqual(qa_model.tokenizer, mock_tokenizer_instance)
            self.assertEqual(qa_model.model, mock_model_instance)
            self.assertEqual(qa_model.device, mock_device_instance)
            
            # Check that model was moved to device
            mock_model_instance.to.assert_called_once_with(mock_device_instance)
            
        finally:
            os.chdir(original_cwd)
            
    @patch('biobert_qa.AutoTokenizer.from_pretrained')
    @patch('biobert_qa.AutoModelForQuestionAnswering.from_pretrained')
    @patch('biobert_qa.torch.device')
    @patch('biobert_qa.torch.no_grad')
    @patch('biobert_qa.torch.argmax')
    def test_answer_question_success(self, mock_argmax, mock_no_grad, mock_device, mock_model, mock_tokenizer):
        """Test successful question answering"""
        # Mock tokenizer
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer.return_value = mock_tokenizer_instance
        
        # Mock encode_plus output
        mock_inputs = {
            "input_ids": MagicMock(),
            "attention_mask": MagicMock()
        }
        mock_inputs["input_ids"].tolist.return_value = [[101, 2054, 2003, 3252, 1029, 102, 3252, 2003, 1037, 4168, 102]]
        mock_tokenizer_instance.encode_plus.return_value = mock_inputs
        
        # Mock model
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        
        # Mock model outputs
        mock_outputs = MagicMock()
        mock_outputs.start_logits = MagicMock()
        mock_outputs.end_logits = MagicMock()
        mock_model_instance.return_value = mock_outputs
        
        # Mock device
        mock_device.return_value = MagicMock()
        
        # Mock argmax to return start and end positions
        mock_argmax.side_effect = [6, 9]  # start=6, end=9
        
        # Mock token conversion
        mock_tokenizer_instance.convert_ids_to_tokens.return_value = ["cancer", "is", "a", "disease"]
        mock_tokenizer_instance.convert_tokens_to_string.return_value = "cancer is a disease"
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            qa_model = BioBERT_QA()
            
            question = "What is cancer?"
            context = "Cancer is a disease characterized by uncontrolled cell growth."
            
            result = qa_model.answer_question(question, context)
            
            # Check that we got a meaningful answer
            self.assertEqual(result, "cancer is a disease")
            
            # Verify that encode_plus was called with correct parameters
            mock_tokenizer_instance.encode_plus.assert_called_once_with(
                question, context, add_special_tokens=True, return_tensors="pt"
            )
            
        finally:
            os.chdir(original_cwd)
            
    @patch('biobert_qa.AutoTokenizer.from_pretrained')
    @patch('biobert_qa.AutoModelForQuestionAnswering.from_pretrained')
    @patch('biobert_qa.torch.device')
    @patch('biobert_qa.torch.no_grad')
    @patch('biobert_qa.torch.argmax')
    def test_answer_question_no_answer(self, mock_argmax, mock_no_grad, mock_device, mock_model, mock_tokenizer):
        """Test question answering when no clear answer is found"""
        # Mock tokenizer
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer.return_value = mock_tokenizer_instance
        
        # Mock encode_plus output
        mock_inputs = {
            "input_ids": MagicMock(),
            "attention_mask": MagicMock()
        }
        mock_inputs["input_ids"].tolist.return_value = [[101, 2054, 2003, 3252, 1029, 102]]
        mock_tokenizer_instance.encode_plus.return_value = mock_inputs
        
        # Mock model
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        
        # Mock model outputs
        mock_outputs = MagicMock()
        mock_model_instance.return_value = mock_outputs
        
        # Mock device
        mock_device.return_value = MagicMock()
        
        # Mock argmax to return positions that result in empty answer
        mock_argmax.side_effect = [0, 1]
        
        # Mock token conversion to return [CLS] token
        mock_tokenizer_instance.convert_ids_to_tokens.return_value = ["[CLS]"]
        mock_tokenizer_instance.convert_tokens_to_string.return_value = "[CLS]"
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            qa_model = BioBERT_QA()
            
            question = "What is the capital of Mars?"
            context = "Mars is a planet in our solar system."
            
            result = qa_model.answer_question(question, context)
            
            # Check that we got the no answer message
            self.assertEqual(result, "No clear answer found in the given context.")
            
        finally:
            os.chdir(original_cwd)
            
    @patch('biobert_qa.AutoTokenizer.from_pretrained')
    @patch('biobert_qa.AutoModelForQuestionAnswering.from_pretrained')
    @patch('biobert_qa.torch.device')
    @patch('biobert_qa.torch.no_grad')
    @patch('biobert_qa.torch.argmax')
    def test_answer_question_empty_answer(self, mock_argmax, mock_no_grad, mock_device, mock_model, mock_tokenizer):
        """Test question answering when answer is empty"""
        # Mock tokenizer
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer.return_value = mock_tokenizer_instance
        
        # Mock encode_plus output
        mock_inputs = {
            "input_ids": MagicMock(),
            "attention_mask": MagicMock()
        }
        mock_inputs["input_ids"].tolist.return_value = [[101, 102]]
        mock_tokenizer_instance.encode_plus.return_value = mock_inputs
        
        # Mock model
        mock_model_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        
        # Mock model outputs
        mock_outputs = MagicMock()
        mock_model_instance.return_value = mock_outputs
        
        # Mock device
        mock_device.return_value = MagicMock()
        
        # Mock argmax
        mock_argmax.side_effect = [0, 0]
        
        # Mock token conversion to return empty string
        mock_tokenizer_instance.convert_ids_to_tokens.return_value = []
        mock_tokenizer_instance.convert_tokens_to_string.return_value = ""
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            qa_model = BioBERT_QA()
            
            question = "Empty question?"
            context = "Empty context."
            
            result = qa_model.answer_question(question, context)
            
            # Check that we got the no answer message
            self.assertEqual(result, "No clear answer found in the given context.")
            
        finally:
            os.chdir(original_cwd)


class TestBioBERTQAIntegration(unittest.TestCase):
    """Integration tests for BioBERT_QA (requires actual model)"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures"""
        # Check if the actual model exists
        model_path = os.path.join(os.getcwd(), "model", "biobert_v1.1_pubmed_squad_v2_local")
        cls.model_available = os.path.exists(model_path)
        
    def setUp(self):
        """Skip tests if model not available"""
        if not self.model_available:
            self.skipTest("BioBERT model not available")
            
    def test_real_medical_question(self):
        """Test with real medical question"""
        qa_model = BioBERT_QA()
        
        question = "What causes cancer?"
        context = "Cancer is caused by genetic mutations that lead to uncontrolled cell growth and division."
        
        result = qa_model.answer_question(question, context)
        
        # Check that we get a meaningful answer
        self.assertIsInstance(result, str)
        self.assertGreater(len(result.strip()), 0)
        self.assertNotEqual(result, "No clear answer found in the given context.")
        
    def test_medical_terminology(self):
        """Test with medical terminology"""
        qa_model = BioBERT_QA()
        
        question = "What is chemotherapy?"
        context = "Chemotherapy is a type of cancer treatment that uses drugs to destroy cancer cells."
        
        result = qa_model.answer_question(question, context)
        
        # Check that the answer contains relevant information
        self.assertIsInstance(result, str)
        self.assertIn("drug", result.lower())


if __name__ == '__main__':
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestCleanContext))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestBioBERTQA))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestBioBERTQAIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
