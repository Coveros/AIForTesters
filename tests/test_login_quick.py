"""
Quick unit tests for login functionality that can run without browser automation.
These tests focus on the critical security and functionality aspects.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from wine import app
import sqlite3

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page_loads(client):
    """Test that login page loads correctly"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Please Login:' in response.data
    assert b'type="password"' in response.data  # Verify password field is masked

def test_valid_login_redirects_to_wine_page(client):
    """Test that valid login redirects to wine classification page"""
    response = client.post('/login', data={'username': 'jefferyepayne', 'password': 'TestTest'})
    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data
    assert b'Predict Your Wine Variety' in response.data

def test_invalid_login_shows_error(client):
    """Test that invalid login shows error message"""
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 200
    assert b'Incorrect username/password!' in response.data
    assert b'Please Login:' in response.data  # Should stay on login page

def test_empty_credentials_shows_login_page(client):
    """Test that empty credentials keep user on login page"""
    response = client.post('/login', data={'username': '', 'password': ''})
    assert response.status_code == 200
    assert b'Please Login:' in response.data

def test_unauthenticated_redirect(client):
    """Test that unauthenticated users are redirected to login"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Please Login:' in response.data

def test_register_page_has_masked_passwords(client):
    """Test that register page has properly masked password fields"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'type="password"' in response.data
    # Should have at least two password fields (password and confirm)
    assert response.data.count(b'type="password"') >= 2

def test_database_has_test_user():
    """Verify test user exists in database"""
    conn = sqlite3.connect('wineusers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = ?', ('jefferyepayne',))
    account = cursor.fetchone()
    conn.close()
    assert account is not None
    assert account[1] == 'jefferyepayne'
    assert account[2] == 'TestTest'