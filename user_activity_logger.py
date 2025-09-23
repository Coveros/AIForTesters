import logging
import json
import os
from datetime import datetime
from functools import wraps

# Make Flask imports optional for testing
try:
    from flask import session, request
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    session = None
    request = None

class UserActivityLogger:
    """Logger for user interactions in the wine classification application."""
    
    def __init__(self, log_file='user_activity.log', log_level=logging.INFO):
        self.log_file = log_file
        self.logger = logging.getLogger('user_activity')
        self.logger.setLevel(log_level)
        
        # Remove existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create file handler
        handler = logging.FileHandler(log_file)
        handler.setLevel(log_level)
        
        # Create formatter for structured logging
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def log_user_activity(self, action, details=None, user_id=None, username=None):
        """Log user activity with structured data."""
        if HAS_FLASK and session:
            if user_id is None and 'id' in session:
                user_id = session.get('id')
            if username is None and 'username' in session:
                username = session.get('username')
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user_id': user_id,
            'username': username,
            'ip_address': request.remote_addr if HAS_FLASK and request else None,
            'user_agent': request.headers.get('User-Agent') if HAS_FLASK and request else None,
            'details': details or {}
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def log_login_attempt(self, username, success, details=None):
        """Log login attempts."""
        self.log_user_activity(
            action='login_attempt',
            details={
                'success': success,
                'attempted_username': username,
                **(details or {})
            },
            username=username if success else None
        )
    
    def log_logout(self, username=None):
        """Log user logout."""
        self.log_user_activity(
            action='logout',
            username=username
        )
    
    def log_registration(self, username, success, details=None):
        """Log user registration attempts."""
        self.log_user_activity(
            action='registration',
            details={
                'success': success,
                'username': username,
                **(details or {})
            },
            username=username if success else None
        )
    
    def log_wine_classification(self, wine_data, prediction):
        """Log wine classification requests."""
        self.log_user_activity(
            action='wine_classification',
            details={
                'wine_characteristics': wine_data,
                'prediction': prediction
            }
        )
    
    def log_profile_access(self):
        """Log profile page access."""
        self.log_user_activity(action='profile_access')
    
    def log_password_change(self, success, details=None):
        """Log password change attempts."""
        self.log_user_activity(
            action='password_change',
            details={
                'success': success,
                **(details or {})
            }
        )
    
    def log_contact_form(self, success=True):
        """Log contact form submissions."""
        self.log_user_activity(
            action='contact_form',
            details={'success': success}
        )

# Global logger instance
activity_logger = UserActivityLogger()