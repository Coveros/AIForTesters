# ## Classification example using random forest to classify wine types
# ## based on wine attributes
# May 2024

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from sklearn import ensemble, datasets, metrics, model_selection, preprocessing, pipeline

# Perform data engineering to prepare the wine dataset for training and testing

def data_preparation(train_size=0.5):

    # check to make sure the train_size is a percentage greater than 0 and less than 1
    if (train_size <= 0.0 or train_size >= 1.0):
        raise ValueError("train_size must be greater than 0 or less than 1")
    
    try:
        wine_data = pd.read_csv('wine_dataset.csv')
    except:
        raise Exception("Could not load wine dataset")
 
    # Populate your x and y coordinates for your wine data
    try:
        X = wine_data.drop('target', axis =1)
        y = wine_data['target']
    except:
        raise Exception("Could not extract data")

    # Stratify the data by the target labels to ensure that the training and testing datasets 
    # have the same proportion of wine types

    # Split the wine dataset and create inputs (x variables) & labeled outputs (y variables) for supervised training
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=train_size, 
                                                                        stratify=y)
    
    return X_train, X_test, y_train, y_test

# Create a random forest classifier model to train on the wine dataset
 
def model_training(n_estimators=10, max_depth=5, X_train=None, X_test=None, y_train=None, y_test=None):

    # check to make sure the n_estimators is greater than 0
    if (n_estimators <= 0):
        raise Exception("n_estimators must be greater than 0")
    
    # check to make sure the max_depth is greater than 0
    if (max_depth <= 0):
        raise Exception("max_depth must be greater than 0")

    # create random forest structure based on hyperparameters
    model = ensemble.RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)

     # train model on wine data
    model.fit(X_train, y_train)

    return model

# Test the model using the using the testing dataset we created

def validate_model(X_test, y_test, model):

    # Test the model using the using the testing dataset we created
    predicted = model.predict(X_test)

    # Generate a confusion matrix across the three different types of wine to determine the models accuracy
    confusion_matrix = pd.DataFrame(metrics.confusion_matrix(y_test, predicted))

    # Make a heat map image of the confusion matrix results
    _ = sns.heatmap(confusion_matrix, annot=True, cmap="Blues")

    return predicted

# Main function to run the model

if __name__ == "__main__":

    # Model hyperparameters to set:
        # train_size determines what % of a dataset is used for training vs. testing.
        # n_estimators sets the # of decision trees used in random forest.
        # max_depth sets the depth size of each decision tree
 
    train_size = 0.8
    n_estimators = 10
    max_depth = 5

    X_train, X_test, y_train, y_test = data_preparation(train_size)

    model = model_training(n_estimators, max_depth, X_train, X_test, y_train, y_test)

    predicted = validate_model(X_test, y_test, model)

    # Print out metrics to determine how accurate the results of the model training were
    # Accuracy is the proportion of correct predictions
    # Precision is the accuracy of positive predictions
    # Recall is the number of members in class the classifier correctly predicated / total number of members in class
    # f1 score is the harmonic mean of precision and recall ... combines these to give you a score across the two
    
    print("accuracy: {:.3f}".format(metrics.accuracy_score(y_test, predicted)))
    print("precision: {:.3f}".format(metrics.precision_score(y_test, predicted, average='weighted')))
    print("recall: {:.3f}".format(metrics.recall_score(y_test, predicted, average='weighted')))
    print("f1 score: {:.3f}".format(metrics.f1_score(y_test, predicted, average='weighted')))

    # We do not need to dump the model to a file or capture the above metrics as
    # they are automatically saved to a model registry