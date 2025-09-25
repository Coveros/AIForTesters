from seleniumbase import BaseCase

class LoginTests(BaseCase):
    def test_valid_login(self):
        # open login page
        self.open("http://127.0.0.1:5000/login")

        # enter values into form
        self.type("#username", "jefferyepayne")
        self.type("#password", "TestTest")

        # click login button
        self.click('button[type="submit"]')

        # validate login was successful
        self.assert_text("Logged in successfully!")

    def test_invalid_username(self):
        """Test login with invalid username"""
        # open login page
        self.open("http://127.0.0.1:5000/login")

        # enter invalid username and valid password
        self.type("#username", "invaliduser")
        self.type("#password", "TestTest")

        # click login button
        self.click('button[type="submit"]')

        # validate error message is displayed
        self.assert_text("Incorrect username/password!")
        # ensure we're still on login page
        self.assert_element("#username")

    def test_invalid_password(self):
        """Test login with valid username but invalid password"""
        # open login page
        self.open("http://127.0.0.1:5000/login")

        # enter valid username and invalid password
        self.type("#username", "jefferyepayne")
        self.type("#password", "WrongPassword")

        # click login button
        self.click('button[type="submit"]')

        # validate error message is displayed
        self.assert_text("Incorrect username/password!")
        # ensure we're still on login page
        self.assert_element("#username")

    def test_empty_credentials(self):
        """Test login with empty username and password"""
        # open login page
        self.open("http://127.0.0.1:5000/login")

        # try to submit form without entering anything
        self.click('button[type="submit"]')

        # HTML5 validation should prevent submission with required fields empty
        # We should still be on the login page
        self.assert_element("#username")
        self.assert_element("#password")

    def test_password_field_is_masked(self):
        """Test that password field properly masks input"""
        # open login page
        self.open("http://127.0.0.1:5000/login")

        # verify password field has correct type attribute
        password_field = self.find_element("#password")
        field_type = password_field.get_attribute("type")
        self.assertEqual(field_type, "password", "Password field should have type='password'")

        # type in password field and verify it's masked
        self.type("#password", "TestPassword123")
        
        # The actual text content should not be visible in plain text
        # We can check that the input type is password which ensures masking
        self.assert_attribute("#password", "type", "password")

    def test_unauthenticated_redirect_to_login(self):
        """Test that unauthenticated users are redirected to login page"""
        # try to access the main wine classification page without logging in
        self.open("http://127.0.0.1:5000/")

        # should be redirected to login page
        self.assert_element("#username")
        self.assert_element("#password")
        self.assert_text("Please Login:")

    def test_login_error_message_visibility(self):
        """Test that error messages are prominently displayed"""
        # open login page
        self.open("http://127.0.0.1:5000/login")

        # enter invalid credentials
        self.type("#username", "wronguser")
        self.type("#password", "wrongpass")

        # click login button
        self.click('button[type="submit"]')

        # check that error message is visible and prominent
        self.assert_text("Incorrect username/password!")
        
        # The error message should be displayed in bold (based on template)
        error_element = self.find_element("//b[contains(text(), 'Incorrect username/password!')]")
        self.assertTrue(error_element.is_displayed(), "Error message should be prominently displayed")

