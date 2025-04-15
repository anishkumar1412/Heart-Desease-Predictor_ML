import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib  # Import joblib for saving the model

# Load the dataset
heartdata = pd.read_csv("heart.csv")

# Separate features and target
X = heartdata.drop(columns='target', axis=1)
y = heartdata['target']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

# Create and fit the SVM model
svm_model = SVC(kernel='linear', probability=True)  # Enable probability for later use
svm_model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred_svm = svm_model.predict(X_test)

# Calculate accuracy of the model
acc_svm = accuracy_score(y_test, y_pred_svm)
print("SVM accuracy:", acc_svm)

# Save the trained model as a .pkl file
joblib.dump(svm_model, "svm_model.pkl")
print("Model saved as svm_model.pkl")

# Make predictions on a single example
example = [[71, 0, 0, 112, 149, 0, 1, 125, 0, 1.6, 1, 0, 2]]
prediction = svm_model.predict(example)
if prediction[0] == 0:
    print("Patient does not have any heart disease")
else:
    print("Patient has heart disease and needs more tests")

# Calculate F1 score
f1_svm = classification_report(y_test, y_pred_svm)
print("SVM F1 score:")
print(f1_svm)

# Calculate confusion matrix
cm_svm = confusion_matrix(y_test, y_pred_svm)
print("SVM confusion matrix:")
print(cm_svm)