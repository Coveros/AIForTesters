import unittest
import os
import json
import tempfile
from user_activity_logger import UserActivityLogger


class TestUserActivityLogger(unittest.TestCase):
    """Test cases for user activity logging functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary log file for testing
        self.test_log_file = tempfile.mktemp(suffix='.log')
        self.logger = UserActivityLogger(log_file=self.test_log_file)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test log file
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
    
    def test_log_user_activity(self):
        """Test basic user activity logging."""
        self.logger.log_user_activity('test_action', details={'test': 'data'})
        
        # Verify log entry was created
        self.assertTrue(os.path.exists(self.test_log_file))
        
        with open(self.test_log_file, 'r') as f:
            log_content = f.read()
            self.assertIn('test_action', log_content)
            self.assertIn('test', log_content)
    
    def test_log_login_attempt_success(self):
        """Test successful login logging."""
        self.logger.log_login_attempt('testuser', success=True)
        
        with open(self.test_log_file, 'r') as f:
            log_content = f.read()
            self.assertIn('login_attempt', log_content)
            self.assertIn('testuser', log_content)
            self.assertIn('true', log_content.lower())
    
    def test_log_login_attempt_failure(self):
        """Test failed login logging."""
        self.logger.log_login_attempt('testuser', success=False, 
                                      details={'reason': 'invalid_credentials'})
        
        with open(self.test_log_file, 'r') as f:
            log_content = f.read()
            self.assertIn('login_attempt', log_content)
            self.assertIn('testuser', log_content)
            self.assertIn('false', log_content.lower())
            self.assertIn('invalid_credentials', log_content)
    
    def test_log_registration(self):
        """Test user registration logging."""
        self.logger.log_registration('newuser', success=True)
        
        with open(self.test_log_file, 'r') as f:
            log_content = f.read()
            self.assertIn('registration', log_content)
            self.assertIn('newuser', log_content)
    
    def test_log_wine_classification(self):
        """Test wine classification logging."""
        wine_data = {'alcohol': 12.5, 'malic_acid': 2.3}
        prediction = 1
        
        self.logger.log_wine_classification(wine_data, prediction)
        
        with open(self.test_log_file, 'r') as f:
            log_content = f.read()
            self.assertIn('wine_classification', log_content)
            self.assertIn('12.5', log_content)
            self.assertIn('2.3', log_content)
            self.assertIn('1', log_content)
    
    def test_log_password_change(self):
        """Test password change logging."""
        self.logger.log_password_change(success=True)
        
        with open(self.test_log_file, 'r') as f:
            log_content = f.read()
            self.assertIn('password_change', log_content)
            self.assertIn('true', log_content.lower())
    
    def test_log_entries_are_json_format(self):
        """Test that log entries are in valid JSON format."""
        self.logger.log_user_activity('test_action', details={'test': 'data'})
        
        with open(self.test_log_file, 'r') as f:
            lines = f.readlines()
            # Get the JSON part of the log entry (after the timestamp and level)
            log_line = lines[0]
            json_part = log_line.split(' - INFO - ')[1].strip()
            
            # Should be valid JSON
            parsed_data = json.loads(json_part)
            self.assertEqual(parsed_data['action'], 'test_action')
            self.assertEqual(parsed_data['details']['test'], 'data')


if __name__ == '__main__':
    unittest.main()