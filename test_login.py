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

