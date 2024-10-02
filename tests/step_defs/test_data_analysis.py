from pytest_bdd import scenario, scenarios, given, when, then
from sklearn import datasets
from functools import partial

from wine_data_pipeline import data_extraction, data_analysis, feature_engineering, dataset_development

# Setup test for validating the number of rows and columns in the dataset
@scenario("..\\features\\data_analysis_feature_file.feature", "Validate the number of rows and columns in the dataset are correct")
def test_database():
    pass

@given('I have loaded a wine dataset into a variable')
def load_in_dataset():
    global wine
    # Load an existing dataset that has information on wine attributes as discussed below
    wine = data_extraction()
    if (wine.empty):
        raise ValueError("Database Not Found")
        exit()

@when('I have separated the data into input attributes and output labels')
def split_up_data():
    global X, y
    # Populate your x and y coordinates for your wine data
    X, y = data_analysis(wine)

@then('The number of rows in the input data is 178 and the number of rows in the output data is 178 AND the number of attributes is 14')
def check_training_and_test_dataset_sizes():
    assert X.shape == (178, 14), "segment data should return a dataframe with 14 columns"
    assert y.shape == (178,), "segment data should return a dataframe with 1 column"
    
# Setup tests for validating that any duplicate rows are removed
@scenario("..\\features\\data_analysis_feature_file.feature", "Validate duplicates have been removed")
def test_duplicate_rows():
    pass

@given('I have loaded a wine dataset into a variable')
def load_in_dataset():
    global wine
    # Load an existing dataset that has information on wine attributes as discussed below
    wine = data_extraction()
    if (wine.empty):
        raise ValueError("Database Not Found")
        exit()

@when('I have separated the data into attributes and labels and removed duplicates')
def split_up_data():
    global X, y
    # Populate your x and y coordinates for your wine data
    X, y = data_analysis(wine)

@then('No duplicates are in the dataset')
def check_for_duplicate_rows():
    assert len(wine.drop_duplicates()) == 178, "There are no duplicates in the dataset"

