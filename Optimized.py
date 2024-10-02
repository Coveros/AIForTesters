import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.datasets import load_wine

# Load the wine dataset
wine = load_wine()
X = pd.DataFrame(wine.data, columns=wine.feature_names)
y = wine.target

train_size = .7
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=train_size, stratify=y)
param_grid = {
    'n_estimators': [10, 50, 100, 200, 500],
    'max_depth': [0, 5, 10, 20, 30]
}

grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

results = grid_search.cv_results_
scores = results['mean_test_score'].reshape(len(param_grid['n_estimators']), len(param_grid['max_depth']))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n_estimators_list = param_grid['n_estimators']
max_depth_list = param_grid['max_depth']

X, Y = np.meshgrid(n_estimators_list, max_depth_list)

ax.plot_surface(X, Y, scores)
ax.set_xlabel('Number of Trees')
ax.set_ylabel('Max Depth')
ax.set_zlabel('Accuracy')
plt.show()

# Access the best parameters and score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print("Best parameters:", best_params)
print("Best score:", best_score)


