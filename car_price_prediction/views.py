from django.shortcuts import render
import numpy as np
import pickle
import pandas as pd

try:
    with open('car_price_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
        print("Car Price Model Loaded Successfully")
except Exception as e:
    print("Error loading model:", e)
    model = None 

def predict_car_price(request):
    if request.method == 'POST':
        try:
            # Map owner values to match training data
            owner_mapping = {
                "First Owner": "First",
                "Second Owner": "Second",
                "Third Owner": "Third",
                "Fourth & Above Owner": "Fourth & Above"
            }
            
            owner_value = request.POST.get("owner")
            mapped_owner = owner_mapping.get(owner_value, owner_value)

            input_values = {
                "name": request.POST.get("name"),
                "year": float(request.POST.get("year")),
                "km_driven": float(request.POST.get("km_driven")),
                "fuel": request.POST.get("fuel"),
                "seller_type": request.POST.get("seller_type"),
                "transmission": request.POST.get("transmission"),
                "owner": mapped_owner,  # Use mapped owner value
                "mileage(km/ltr/kg)": float(request.POST.get("mileage")),
                "engine": float(request.POST.get("engine")),
                "max_power": float(request.POST.get("max_power")),
                "seats": float(request.POST.get("seats"))
            }

            # Create DataFrame with a single row
            input_df = pd.DataFrame([input_values])

            # Make prediction
            if model is None:
                return render(request, 'car_price_prediction/form.html', {'result': "Model not loaded properly."})

            # Make prediction using the pipeline
            predicted_price = model.predict(input_df)[0]
            formatted_price = "{:,.2f}".format(predicted_price)
            result = f"Predicted Car Price: ₹{formatted_price}"

            return render(request, 'car_price_prediction/form.html', {'result': result})

        except Exception as e:
            return render(request, 'car_price_prediction/form.html', {'result': f"Error: {str(e)}"})

    return render(request, 'car_price_prediction/form.html')