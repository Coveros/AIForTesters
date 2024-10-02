from seleniumbase import BaseCase

class HomeTest(BaseCase):
    def test_home_page(self):
        # open home page
        self.open("http://127.0.0.1:5000/")
        # assert page title
        self.assert_title("Wine Type Prediction")

    def test_predict_variety_0(self):
        # open home page
        self.open("http://127.0.0.1:5000/")
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
        self.click("button:contains('Predict')")

        # assert prediction
        self.assert_text("The wine type is variety #0")
        
    def test_predict_variety_1(self):
        # open home page
        self.open("http://127.0.0.1:5000/")
        # enter values into form
        self.type("#alcohol", "12")
        self.type("#malic_acid", "2")
        self.type("#ash", "2")
        self.type("#alcalinity_of_ash", "15")
        self.type("#magnesium", "100")
        self.type("#total_phenols", "2")
        self.type("#flavanoids", "1")
        self.type("#nonflavanoid_phenols", "0.5")
        self.type("#proanthocyanins", "1")
        self.type("#color_intensity", "3")
        self.type("#hue", "1")
        self.type("#od280_od315_of_diluted_wines", "2")
        self.type("#proline", "500")

        # click predict button
        self.click("button:contains('Predict')")
        # assert prediction
        self.assert_text("The wine type is variety #1")
