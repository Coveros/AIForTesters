import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash
from wine import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestDebugMode:
    def test_debug_mode_disabled(self):
        # Debug mode must be off to prevent Werkzeug interactive debugger exposure
        assert app.debug is False


class TestSecretKey:
    def test_secret_key_is_not_hardcoded_default(self):
        # Secret key must not be the known-bad default value
        assert app.secret_key != b'your_secret_key'
        assert app.secret_key != 'your_secret_key'

    def test_secret_key_has_sufficient_length(self):
        # Secret key should be at least 16 bytes
        key = app.secret_key
        key_bytes = key if isinstance(key, bytes) else key.encode()
        assert len(key_bytes) >= 16


class TestLoginHashedPassword:
    def _make_mock_account(self, username='testuser', password='TestPass1',
                           email='test@example.com'):
        hashed = generate_password_hash(password)
        return (1, username, hashed, email)

    def test_login_succeeds_with_correct_hashed_password(self, client):
        # Login must succeed when the submitted password matches the stored hash
        account = self._make_mock_account()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = account

        with patch('sqlite3.connect') as mock_connect:
            mock_connect.return_value.cursor.return_value = mock_cursor
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'TestPass1'
            })

        assert b'Logged in successfully!' in response.data

    def test_login_fails_with_wrong_password(self, client):
        # Login must fail when password does not match the stored hash
        account = self._make_mock_account()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = account

        with patch('sqlite3.connect') as mock_connect:
            mock_connect.return_value.cursor.return_value = mock_cursor
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'WrongPassword'
            })

        assert b'Incorrect username/password!' in response.data

    def test_login_fails_with_plaintext_password_in_db(self, client):
        # If the DB somehow contains plaintext, login must still fail (not bypass hash check)
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 'testuser', 'TestPass1', 'test@example.com')

        with patch('sqlite3.connect') as mock_connect:
            mock_connect.return_value.cursor.return_value = mock_cursor
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'TestPass1'
            })

        assert b'Logged in successfully!' not in response.data


class TestRegisterPasswordHash:
    def test_register_stores_hashed_password(self, client):
        # Registration must hash the password before storing it
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # user does not exist

        inserted_values = {}

        def capture_execute(sql, params=None):
            if params and 'INSERT' in sql.upper():
                inserted_values['password'] = params[1]

        mock_cursor.execute.side_effect = capture_execute
        mock_cursor.connection.commit.return_value = None

        with patch('sqlite3.connect') as mock_connect:
            mock_connect.return_value.cursor.return_value = mock_cursor
            client.post('/register', data={
                'username': 'newuser',
                'password': 'MySecret1',
                'confirmpw': 'MySecret1',
                'email': 'new@example.com'
            })

        assert 'password' in inserted_values
        stored_pw = inserted_values['password']
        # Stored value must not be the plaintext password
        assert stored_pw != 'MySecret1'
        # Stored value must be a valid Werkzeug hash
        from werkzeug.security import check_password_hash
        assert check_password_hash(stored_pw, 'MySecret1')

    def test_register_rejects_mismatched_passwords(self, client):
        # Server must reject registration when password and confirmation differ
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None

        with patch('sqlite3.connect') as mock_connect:
            mock_connect.return_value.cursor.return_value = mock_cursor
            response = client.post('/register', data={
                'username': 'newuser',
                'password': 'MySecret1',
                'confirmpw': 'DifferentPassword',
                'email': 'new@example.com'
            })

        assert b'Passwords do not match!' in response.data


class TestPredictAuthGuard:
    def test_predict_get_unauthenticated_redirects_to_login(self, client):
        # Unauthenticated GET /predict must redirect to login
        response = client.get('/predict')
        assert response.status_code == 302
        assert '/login' in response.headers['Location']

    def test_predict_post_unauthenticated_redirects_to_login(self, client):
        # Unauthenticated POST /predict must redirect to login
        response = client.post('/predict', data={
            'alcohol': '13.0', 'malic_acid': '2.0', 'ash': '2.3',
            'alcalinity_of_ash': '15.0', 'magnesium': '100.0',
            'total_phenols': '2.5', 'flavanoids': '2.5',
            'nonflavanoid_phenols': '0.3', 'proanthocyanins': '1.5',
            'color_intensity': '5.0', 'hue': '1.0',
            'od280_od315_of_diluted_wines': '3.0', 'proline': '700.0'
        })
        assert response.status_code == 302
        assert '/login' in response.headers['Location']
