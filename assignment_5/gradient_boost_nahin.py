# -*- coding: utf-8 -*-
"""Gradient Boost_Nahin.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xqc_gBh-O-Z1T0eRDDncqSzMYWg8mHD5
"""

import pandas as pd

# Load Mushroom Dataset from UCI
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"

# Define column names from dataset documentation
columns = [
    'class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
    'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color', 'stalk-shape',
    'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring',
    'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-type', 'veil-color',
    'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat'
]

# Read the CSV
df = pd.read_csv(url, header=None, names=columns)

# Show top rows
df.head()

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Replace missing values ('?') if any
df = df.replace('?', pd.NA).dropna()

# Apply Label Encoding to all columns
label_encoders = {}
for col in df.columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Split features and target
X = df.drop('class', axis=1)
y = df['class']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import xgboost as xgb
from sklearn.metrics import accuracy_score
import time

# Convert data to DMatrix (optional, XGBoost-specific format)
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Set basic XGBoost parameters
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'error',
    'verbosity': 0
}

# Measure training time
start_time = time.time()

# Train model
xgb_model = xgb.train(params, dtrain, num_boost_round=100)

end_time = time.time()
training_time = end_time - start_time

# Make predictions
y_pred_prob = xgb_model.predict(dtest)
y_pred = (y_pred_prob > 0.5).astype(int)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"XGBoost Accuracy: {accuracy * 100:.2f}%")
print(f"Training Time: {training_time:.4f} seconds")