import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load the data
file_path = r"d:\cardekho.csv"  # Update path if needed
data = pd.read_csv(file_path)

print("Before handling missing values:\n", data.isnull().sum())

# Replace blank spaces (" ") with NaN
data.replace(' ', np.nan, inplace=True)

# Handle missing values
data.fillna(data.median(numeric_only=True), inplace=True)

print("After handling missing values:\n", data.isnull().sum())

# Define features
numeric_features = ['year', 'km_driven', 'mileage(km/ltr/kg)', 'engine', 'max_power', 'seats']
categorical_features = ['name', 'fuel', 'seller_type', 'transmission', 'owner']

# Separate features and target
X = data[numeric_features + categorical_features]
y = data['selling_price']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
    ])

# Create pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Fit the model
model.fit(X_train, y_train)

# Save the full model pipeline
with open('car_price_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Car Price Prediction Model Saved Successfully!")
