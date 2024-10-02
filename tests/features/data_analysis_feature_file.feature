Feature: Split data into inputs and output class
    As a data scientist
    I want to be able to load a wine database and split it into inputs and output arrays
    So that I can create datasets for training and testing

Scenario: Validate the number of rows and columns in the dataset are correct
    Given I have loaded a wine dataset into a variable
    When I have separated the data into input attributes and output labels
    Then The number of rows in the input data is 178 and the number of rows in the output data is 178 AND the number of attributes is 14

Scenario: Validate duplicates have been removed
    Given I have loaded a wine dataset into a variable
    When I have separated the data into attributes and labels and removed duplicates
    Then No duplicates are in the dataset

Scenario: Validate country code has been dropped
    Given I have loaded a wine dataset into a variable
    When I have separated the data into attributes and labels and dropped the country code column
    Then The country code column is not in the dataset