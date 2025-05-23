import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

file_path = r"d:\diabetes_prediction_dataset.csv"
data = pd.read_csv(file_path)

data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})

print("Before handling missing values:\n", data.isnull().sum())

data.fillna(data.median(numeric_only=True), inplace=True)  

print("After handling missing values:\n", data.isnull().sum())

X = data[['gender', 'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']]
y = data['diabetes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open('diabetes_model_rf.pkl', 'wb') as f:
    pickle.dump((model, scaler), f)

print("Random Forest Model and Scaler Saved Successfully!")

