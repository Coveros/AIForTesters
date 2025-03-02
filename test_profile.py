from seleniumbase import BaseCase

class ProfileTests(BaseCase):
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
    
    def test_change_invalid_password(self):
        # Login before test begins
        self.login()

        # Open the profile page
        self.open("http://127.0.0.1:5000/profile")

        # Type in invalid password to change
        self.type("#current_password", "TestTest1")
        self.type("#new_password", "TestTest2")
        self.type("#confirm_password", "TestTest2")

        # Click the change password button
        self.click('button[type="submit"]')
        self.assert_text("Current password is incorrect!")

        self.logout()