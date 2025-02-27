# -*- coding: utf-8 -*-
"""Assignment chapter 4

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Op2idQbBAG1IxpIyq7qK4s5EPB_qqIy1
"""

from google.colab import files

# Prompt to upload the file manually
uploaded = files.upload()

import pandas as pd

# Load the newly uploaded file
df = pd.read_csv("wheat_seeds_clean.csv")  # No need for /mnt/data/ path

# Display the first few rows
df.head()

# Check for missing values
print("Missing Values:\n", df.isnull().sum())

# Display dataset info
print("\nDataset Info:")
df.info()

df.fillna(df.mean(), inplace=True)  # Fill missing values with column means

from sklearn.model_selection import train_test_split

# Assuming the last column is the target (class labels)
X = df.iloc[:, :-1].values  # Features (all columns except last)
y = df.iloc[:, -1].values   # Target labels (last column)

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train_std = sc.fit_transform(X_train)
X_test_std = sc.transform(X_test)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

tree = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=1)
tree.fit(X_train, y_train)

y_pred_tree = tree.predict(X_test)
print(f"Decision Tree Accuracy: {accuracy_score(y_test, y_pred_tree) * 100:.2f}%")

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
knn.fit(X_train_std, y_train)

y_pred_knn = knn.predict(X_test_std)
print(f"k-NN Accuracy: {accuracy_score(y_test, y_pred_knn) * 100:.2f}%")

from sklearn.svm import SVC

svm = SVC(kernel='linear', C=1.0, random_state=1)
svm.fit(X_train_std, y_train)

y_pred_svm = svm.predict(X_test_std)
print(f"SVM Accuracy: {accuracy_score(y_test, y_pred_svm) * 100:.2f}%")

from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=25, random_state=1)
forest.fit(X_train, y_train)

y_pred_forest = forest.predict(X_test)
print(f"Random Forest Accuracy: {accuracy_score(y_test, y_pred_forest) * 100:.2f}%")

# Select two features (adjust indices if needed)
X_selected = df.iloc[:, [0, 1]].values  # First two features only
y_selected = df.iloc[:, -1].values      # Target labels

# Split for visualization models
X_train_sel, X_test_sel, y_train_sel, y_test_sel = train_test_split(X_selected, y_selected, test_size=0.2, random_state=1, stratify=y_selected)

# Train classifiers using **only 2 selected features**
tree_sel = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=1)
tree_sel.fit(X_train_sel, y_train_sel)

knn_sel = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
knn_sel.fit(X_train_sel, y_train_sel)

svm_sel = SVC(kernel='linear', C=1.0, random_state=1)
svm_sel.fit(X_train_sel, y_train_sel)

forest_sel = RandomForestClassifier(n_estimators=25, random_state=1)
forest_sel.fit(X_train_sel, y_train_sel)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os

# Ensure the folder exists for saving figures
os.makedirs("images", exist_ok=True)

# Function to plot and save decision boundaries
def plot_and_save(X, y, classifier, filename):
    plt.figure()

    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # Plot decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(
        np.arange(x1_min, x1_max, 0.02),
        np.arange(x2_min, x2_max, 0.02)
    )

    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.scatter(X[:, 0], X[:, 1], c=y, marker='o', edgecolor='black')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(classifier.__class__.__name__)

    # Save the figure
    plt.savefig(f"images/{filename}.png", dpi=300)
    plt.show()

# Generate and save figures for classifiers
plot_and_save(X_train_sel, y_train_sel, tree_sel, "Decision_Tree")
plot_and_save(X_train_sel, y_train_sel, knn_sel, "KNN")
plot_and_save(X_train_sel, y_train_sel, svm_sel, "SVM")
plot_and_save(X_train_sel, y_train_sel, forest_sel, "Random_Forest")

import glob
from google.colab import files

# Get list of all PNG files
figure_files = glob.glob("images/*.png")

# Download each file
for file in figure_files:
    files.download(file)