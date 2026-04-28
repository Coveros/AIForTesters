from seleniumbase import BaseCase

class ActivityLogTests(BaseCase):
    def login(self):
        # open login page
        self.open("http://127.0.0.1:5000/login")
        self.type("#username", "jefferyepayne")
        self.type("#password", "TestTest")
        self.click('button[type="submit"]')
        self.wait_for_text("Logged in successfully!")

    def logout(self):
        self.click_link("Logout")
        self.assert_element("#username")

    def test_activity_log_shows_on_profile(self):
        # Login to generate a login event
        self.login()

        # Open the profile page
        self.open("http://127.0.0.1:5000/profile")

        # Validate the activity log section is present
        self.assert_text("Activity Log")

        # Validate at least one login entry exists in the log
        self.assert_text("login")

        self.logout()

    def test_activity_log_shows_logout(self):
        # Login then logout to generate both events
        self.login()
        self.logout()

        # Login again to view the profile
        self.login()

        # Open the profile page
        self.open("http://127.0.0.1:5000/profile")

        # Validate both login and logout entries appear in the log
        self.assert_text("login")
        self.assert_text("logout")

        self.logout()
