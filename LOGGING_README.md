# User Activity Logging Configuration

The user activity logging system captures all user interactions with the wine classification application and saves them to structured log files for analysis by log management systems.

## Features

- **Structured Logging**: All log entries are in JSON format for easy parsing
- **Comprehensive Coverage**: Logs all user interactions including login, logout, registration, wine classification, profile access, password changes, and contact form submissions
- **Security-Aware**: Avoids logging sensitive information like passwords
- **Analysis-Ready**: Includes timestamps, user identification, IP addresses, and detailed activity context

## Log File Location

By default, logs are written to `user_activity.log` in the application directory.

## Log Format

Each log entry includes:
- `timestamp`: ISO format timestamp
- `action`: Type of user activity
- `user_id`: Database user ID (when available)
- `username`: Username (when available) 
- `ip_address`: Client IP address
- `user_agent`: Browser user agent string
- `details`: Action-specific details

## Sample Log Entries

```json
{"timestamp": "2024-01-15T10:30:45.123456", "action": "login_attempt", "user_id": 123, "username": "johndoe", "ip_address": "192.168.1.100", "user_agent": "Mozilla/5.0...", "details": {"success": true, "attempted_username": "johndoe"}}

{"timestamp": "2024-01-15T10:35:12.789012", "action": "wine_classification", "user_id": 123, "username": "johndoe", "ip_address": "192.168.1.100", "user_agent": "Mozilla/5.0...", "details": {"wine_characteristics": {"alcohol": 12.5, "malic_acid": 2.3, ...}, "prediction": 1}}

{"timestamp": "2024-01-15T10:40:00.456789", "action": "logout", "user_id": 123, "username": "johndoe", "ip_address": "192.168.1.100", "user_agent": "Mozilla/5.0...", "details": {}}
```

## Actions Logged

1. **login_attempt** - Both successful and failed login attempts
2. **logout** - User logout actions  
3. **registration** - User registration attempts
4. **wine_classification** - Wine prediction requests with input data
5. **profile_access** - Profile page views
6. **password_change** - Password change attempts
7. **contact_form** - Contact form submissions

## Log Rotation

For production use, implement log rotation using logrotate or Python's RotatingFileHandler:

```python
from logging.handlers import RotatingFileHandler

# Example: Rotate when log file reaches 10MB, keep 5 backup files
handler = RotatingFileHandler('user_activity.log', maxBytes=10*1024*1024, backupCount=5)
```

## Privacy and Security

- Passwords are never logged
- Only successful login attempts include username in the main fields
- Failed attempts include attempted username in details only
- All logging respects user privacy while providing audit capability

## Integration with Log Management Systems

The JSON format makes these logs easy to ingest into systems like:
- Elasticsearch/ELK Stack
- Splunk
- Fluentd
- AWS CloudWatch
- Azure Monitor

## Configuration

Modify logging behavior by creating a custom UserActivityLogger instance:

```python
from user_activity_logger import UserActivityLogger

# Custom configuration
logger = UserActivityLogger(
    log_file='/var/log/wine_app/user_activity.log',
    log_level=logging.DEBUG
)
```