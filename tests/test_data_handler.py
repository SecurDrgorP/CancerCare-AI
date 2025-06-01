import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import tempfile

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_handler import DataHandler


class TestDataHandler(unittest.TestCase):
    """Test cases for DataHandler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary CSV files for testing
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test cancer types data
        self.cancer_types_data = pd.DataFrame({
            'cancer_type': ['Breast Cancer', 'Lung Cancer', 'Prostate Cancer'],
            'category': ['Solid Tumor', 'Solid Tumor', 'Solid Tumor'],
            'prevalence': [12.5, 11.4, 9.5]
        })
        self.cancer_types_file = os.path.join(self.temp_dir, 'cancer_types.csv')
        self.cancer_types_data.to_csv(self.cancer_types_file, index=False)
        
        # Create test treatments data
        self.treatments_data = pd.DataFrame({
            'treatment': ['Chemotherapy', 'Radiation Therapy', 'Surgery'],
            'category': ['Systemic', 'Local', 'Local'],
            'effectiveness': [8.5, 7.8, 9.2]
        })
        self.treatments_file = os.path.join(self.temp_dir, 'treatments.csv')
        self.treatments_data.to_csv(self.treatments_file, index=False)
        
        # Create test side effects data
        self.side_effects_data = pd.DataFrame({
            'side_effect': ['Nausea', 'Fatigue', 'Hair Loss'],
            'frequency': [85, 92, 70],
            'severity': ['Moderate', 'Mild', 'Mild']
        })
        self.side_effects_file = os.path.join(self.temp_dir, 'side_effects.csv')
        self.side_effects_data.to_csv(self.side_effects_file, index=False)
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    @patch('data_handler.pd.read_csv')
    def test_get_cancer_types(self, mock_read_csv):
        """Test getting cancer types data"""
        mock_read_csv.return_value = self.cancer_types_data
        
        handler = DataHandler()
        result = handler.get_cancer_types()
        
        # Check that data is returned correctly
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertIn('cancer_type', result.columns)
        self.assertEqual(result.iloc[0]['cancer_type'], 'Breast Cancer')
        
    @patch('data_handler.pd.read_csv')
    def test_get_treatments(self, mock_read_csv):
        """Test getting treatments data"""
        mock_read_csv.return_value = self.treatments_data
        
        handler = DataHandler()
        result = handler.get_treatments()
        
        # Check that data is returned correctly
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertIn('treatment', result.columns)
        self.assertEqual(result.iloc[0]['treatment'], 'Chemotherapy')
        
    @patch('data_handler.pd.read_csv')
    def test_get_side_effects(self, mock_read_csv):
        """Test getting side effects data"""
        mock_read_csv.return_value = self.side_effects_data
        
        handler = DataHandler()
        result = handler.get_side_effects()
        
        # Check that data is returned correctly
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertIn('side_effect', result.columns)
        self.assertEqual(result.iloc[0]['side_effect'], 'Nausea')
        
    @patch('data_handler.pd.read_csv')
    def test_file_not_found_error(self, mock_read_csv):
        """Test behavior when CSV file is not found"""
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        handler = DataHandler()
        
        # Should return empty DataFrame when file not found
        result = handler.get_cancer_types()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)
        
    @patch('data_handler.pd.read_csv')
    def test_empty_csv_file(self, mock_read_csv):
        """Test behavior with empty CSV file"""
        mock_read_csv.return_value = pd.DataFrame()
        
        handler = DataHandler()
        result = handler.get_cancer_types()
        
        # Should return empty DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)
        
    @patch('data_handler.pd.read_csv')
    def test_malformed_csv_data(self, mock_read_csv):
        """Test behavior with malformed CSV data"""
        # Create malformed data (missing columns)
        malformed_data = pd.DataFrame({
            'wrong_column': ['value1', 'value2']
        })
        mock_read_csv.return_value = malformed_data
        
        handler = DataHandler()
        result = handler.get_cancer_types()
        
        # Should still return DataFrame even if columns are different
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        
    def test_data_handler_initialization(self):
        """Test DataHandler initialization"""
        handler = DataHandler()
        
        # Check that handler is initialized correctly
        self.assertIsInstance(handler, DataHandler)
        
    @patch('data_handler.pd.read_csv')
    def test_multiple_calls_same_data(self, mock_read_csv):
        """Test that multiple calls return consistent data"""
        mock_read_csv.return_value = self.cancer_types_data
        
        handler = DataHandler()
        result1 = handler.get_cancer_types()
        result2 = handler.get_cancer_types()
        
        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2)
        
    @patch('data_handler.pd.read_csv')
    def test_data_types_preservation(self, mock_read_csv):
        """Test that data types are preserved correctly"""
        # Create data with specific types
        typed_data = pd.DataFrame({
            'cancer_type': ['Breast Cancer', 'Lung Cancer'],
            'prevalence': [12.5, 11.4],  # float
            'count': [1000, 900]  # int
        })
        mock_read_csv.return_value = typed_data
        
        handler = DataHandler()
        result = handler.get_cancer_types()
        
        # Check data types are preserved
        self.assertEqual(result['prevalence'].dtype, float)
        self.assertEqual(result['count'].dtype, int)


class TestDataHandlerIntegration(unittest.TestCase):
    """Integration tests for DataHandler with real files"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures"""
        # Check if actual data files exist
        data_dir = os.path.join(os.getcwd(), "data")
        cls.cancer_types_exists = os.path.exists(os.path.join(data_dir, "cancer_types.csv"))
        cls.treatments_exists = os.path.exists(os.path.join(data_dir, "treatments.csv"))
        cls.side_effects_exists = os.path.exists(os.path.join(data_dir, "side_effects.csv"))
        
    def test_real_cancer_types_file(self):
        """Test with real cancer types file"""
        if not self.cancer_types_exists:
            self.skipTest("cancer_types.csv not found")
            
        handler = DataHandler()
        result = handler.get_cancer_types()
        
        # Check that we get valid data
        self.assertIsInstance(result, pd.DataFrame)
        if len(result) > 0:
            # Check that expected columns exist (flexible check)
            columns = result.columns.tolist()
            self.assertGreater(len(columns), 0)
            
    def test_real_treatments_file(self):
        """Test with real treatments file"""
        if not self.treatments_exists:
            self.skipTest("treatments.csv not found")
            
        handler = DataHandler()
        result = handler.get_treatments()
        
        # Check that we get valid data
        self.assertIsInstance(result, pd.DataFrame)
        if len(result) > 0:
            columns = result.columns.tolist()
            self.assertGreater(len(columns), 0)
            
    def test_real_side_effects_file(self):
        """Test with real side effects file"""
        if not self.side_effects_exists:
            self.skipTest("side_effects.csv not found")
            
        handler = DataHandler()
        result = handler.get_side_effects()
        
        # Check that we get valid data
        self.assertIsInstance(result, pd.DataFrame)
        if len(result) > 0:
            columns = result.columns.tolist()
            self.assertGreater(len(columns), 0)
            
    def test_all_data_methods_return_dataframes(self):
        """Test that all data methods return pandas DataFrames"""
        handler = DataHandler()
        
        cancer_types = handler.get_cancer_types()
        treatments = handler.get_treatments()
        side_effects = handler.get_side_effects()
        
        # All should return DataFrames regardless of file existence
        self.assertIsInstance(cancer_types, pd.DataFrame)
        self.assertIsInstance(treatments, pd.DataFrame)
        self.assertIsInstance(side_effects, pd.DataFrame)


if __name__ == '__main__':
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestDataHandler))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestDataHandlerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
