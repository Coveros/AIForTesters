Feature: End to end data pipeline
    As a data scientist
    I want to be able to create automatically create quality datasets
    So that I can use them for model training and testing

Scenario: Validate final dataset shape
    Given I have extracted, cleaned, engineered, and saved a dataset
    When I load the dataset
    Then The number of rows in the dataset is 178 and the number of columns is 14
