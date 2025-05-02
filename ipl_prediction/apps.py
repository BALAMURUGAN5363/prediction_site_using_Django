import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pickle

file_path = r"D:\\ipl_data.csv"  
data = pd.read_csv(file_path)

print("Before handlingc:\n", data.isnull().sum())

data.fillna(data.median(numeric_only=True), inplace=True)  

print("After handling:\n", data.isnull().sum())

features = ["venue", "bat_team", "bowl_team", "runs", "wickets", "overs", "runs_last_5", "wickets_last_5"]
target = "total"
X = data[features]
y = data[target]

encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

X_encoded = encoder.fit_transform(X[['venue', 'bat_team', 'bowl_team']])
encoded_columns = encoder.get_feature_names_out(["venue", "bat_team", "bowl_team"])
X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_columns)

X = X.drop(columns=["venue", "bat_team", "bowl_team"])
X = pd.concat([X, X_encoded_df], axis=1)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open("ipl_score_model.pkl", "wb") as f:
    pickle.dump((model, scaler, encoder), f)

print("Random Forest Model and Scaler Saved Successfully")


