from seleniumbase import BaseCase

class RegistrationTests(BaseCase):
    def test_register_invalid_email(self):

        # Open the registration page
        self.open("http://127.0.0.1:5000/register")

        # Type in information to register
        self.type("#username", "fredflintstone")
        self.type("#password", "TestTest")
        self.type("#confirmpw", "TestTest")

        # Type in an invalid email address
        self.type("#email", "fredflintstone")

        # Click the register button
        self.click('button[type="submit"]')

        # Validate the error message
        self.assert_text("Invalid email address!")