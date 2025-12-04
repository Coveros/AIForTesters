from seleniumbase import BaseCase

class AdminTests(BaseCase):
    def login(self):
        # open login page
        self.open("http://127.0.0.1:5000/login")
        self.type("#username", "jefferyepayne")
        self.type("#password", "TestTest")
        self.click('button[type="submit"]')
        self.wait_for_text("Logged in successfully!")
        self.assert_text("Logged in successfully!")

    def logout(self):
        self.click_link("Logout")
        self.assert_element("#username")

    def test_admin_page_accessible(self):
        """Test that the admin page is accessible after login"""
        self.login()
        
        # Navigate to admin page
        self.click_link("Admin")
        
        # Verify admin page elements
        self.assert_text("Activity Log")
        self.assert_element("table")
        
        self.logout()

    def test_admin_page_shows_login_activity(self):
        """Test that login activity is logged and shown on admin page"""
        self.login()
        
        # Navigate to admin page
        self.click_link("Admin")
        
        # Verify login activity is shown
        self.assert_text("login")
        self.assert_text("Successful login")
        
        self.logout()

    def test_admin_page_requires_login(self):
        """Test that admin page redirects to login if not logged in"""
        # Try to access admin page directly without login
        self.open("http://127.0.0.1:5000/admin")
        
        # Should be redirected to login page
        self.assert_element("#username")
        self.assert_element("#password")
