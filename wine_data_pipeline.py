import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import ensemble, datasets, metrics, model_selection, preprocessing, pipeline

# # Load an existing dataset that has information on wine attributes as discussed below
def data_extraction():
    try:
        wine_data = pd.read_csv('wine_raw.csv')
    except:
        raise Exception("Could not load wine dataset")
    
    return wine_data

# # Cleanup the data and analyze it for fit for purpose
def data_analysis(wine_data):

    # Remove duplicate samples
    wine_data = wine_data.drop_duplicates()

    try:
        X = wine_data.drop('target', axis =1)
        y = wine_data['target']
    except:
        raise Exception("Could not extract data")

    # Replace missing alcohol values with mean
    X = X.fillna(X['alcohol'].mean())

    return X, y

# # Transform data into relevant features for machine learning
def feature_engineering(X, y):

    # remove the country code that is not relevant for the model
    X = X.drop('country_code', axis =1 )
    return X

def dataset_development(X, y):
    wine_data = pd.concat([X, y], axis=1)
    try:
        wine_data.to_csv('wine_dataset.csv', index=False)
    except:
        raise Exception("Could not save wine dataset")

# Main function to run data pipeline

if __name__ == "__main__":

    # Load wine characteristics from raw database
    wine_data = data_extraction()

    # Analyze the wine characteristics and clean up date
    X, y = data_analysis(wine_data)

    # Transform the wine characteristics into relevant features for machine learning
    X = feature_engineering(X, y)

    # Build your dataset and save it to file for use during training
    dataset_development(X, y)


