from django.shortcuts import render
import numpy as np
import pickle

try:
    with open('diabetes_model.pkl', 'rb') as model_file:
        model, scaler, imputer = pickle.load(model_file)
        print(" Model Loaded Successfully")
except Exception as e:
    print("Error loading model:", e)
    model, scaler, imputer = None, None, None  

def predict_diabetes(request):
    if request.method == 'POST':
        try:
            
            input_values = [
                request.POST.get('gender'),
                request.POST.get('age'),
                request.POST.get('hypertension'),
                request.POST.get('heart_disease'),
                request.POST.get('bmi'),
                request.POST.get('HbA1c_level'),
                request.POST.get('blood_glucose_level')
            ]

            
            if any(value is None or value.strip() == "" for value in input_values):
                return render(request, 'diabetes_predictor/form.html', {'result': "Missing input values. Please fill all fields."})

            
            try:
                input_data = np.array([float(value) for value in input_values]).reshape(1, -1)
            except ValueError:
                return render(request, 'diabetes_predictor/form.html', {'result': "Invalid input. Please enter numeric values only."})

            
            if imputer:
                input_data = imputer.transform(input_data)

            
            if scaler:
                input_data = scaler.transform(input_data)

            
            if model is None:
                return render(request, 'diabetes_predictor/form.html', {'result': "Model not loaded properly."})

            
            prediction = model.predict(input_data)
            predicted_value = int(prediction[0])
            result_mapping = {0: " Not Diabetic", 1: " Diabetic"}
            result = result_mapping.get(predicted_value, " Unknown Prediction")

            return render(request, 'diabetes_predictor/form.html', {'result': result})

        except Exception as e:
            return render(request, 'diabetes_predictor/form.html', {'result': f"Error: {str(e)}"})

    return render(request, 'diabetes_predictor/form.html')

