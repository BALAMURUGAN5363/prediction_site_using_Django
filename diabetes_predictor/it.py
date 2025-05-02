import pickle
from sklearn.linear_model import LogisticRegression
import os

# Dummy model (Replace with your trained model)
model = LogisticRegression()
model.fit([[0,1], [1,0]], [0,1])  # Training with dummy data

# Ensure directory exists
model_dir = "D:/workspace/myapp/models/"
os.makedirs(model_dir, exist_ok=True)

# Save model
model_path = os.path.join(model_dir, "diabetes_model.pkl")
with open(model_path, "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully at:", model_path)
