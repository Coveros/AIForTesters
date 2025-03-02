from seleniumbase import BaseCase

class ClassifierTests(BaseCase):
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

    def test_predict_variety_0(self):

        self.login()

        # open classifier page
        self.open("http://127.0.0.1:5000/predict")
        
        # enter values into form
        self.type("#alcohol", "14")
        self.type("#malic_acid", "1")
        self.type("#ash", "10")
        self.type("#alcalinity_of_ash", "15")
        self.type("#magnesium", "125")
        self.type("#total_phenols", "2")
        self.type("#flavanoids", "2")
        self.type("#nonflavanoid_phenols", "0.5")
        self.type("#proanthocyanins", "1")
        self.type("#color_intensity", "7")
        self.type("#hue", "0.7")
        self.type("#od280_od315_of_diluted_wines", "2")
        self.type("#proline", "1000")

        # click predict button
        self.click("button[type=submit]")

        # assert prediction
        self.assert_text("The wine type is variety #0")

        self.logout()