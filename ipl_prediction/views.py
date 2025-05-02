from django.shortcuts import render
import numpy as np
import pickle
import pandas as pd

try:
    with open('ipl_score_model.pkl', 'rb') as model_file:
        model, scaler, encoder = pickle.load(model_file)
        print("IPL Model Loaded Successfully")
except Exception as e:
    print("Error loading model:", e)
    model, scaler, encoder = None, None, None 

def predict_ipl_score(request):
    if request.method == 'POST':
        try:
            
            input_values = {
                "venue": request.POST.get("venue"),
                "bat_team": request.POST.get("bat_team"),
                "bowl_team": request.POST.get("bowl_team"),
                "runs": request.POST.get("runs"),
                "wickets": request.POST.get("wickets"),
                "overs": request.POST.get("overs"),
                "runs_last_5": request.POST.get("runs_last_5"),
                "wickets_last_5": request.POST.get("wickets_last_5"),
            }

            
            if any(value is None or value.strip() == "" for value in input_values.values()):
                return render(request, 'ipl_prediction/form1.html', {'result': "Missing input values. Please fill all fields."})

            try:
                num_features = ["runs", "wickets", "overs", "runs_last_5", "wickets_last_5"]
                for feature in num_features:
                    input_values[feature] = float(input_values[feature])
            except ValueError:
                return render(request, 'ipl_prediction/form1.html', {'result': "Invalid input. Please enter numeric values only."})

            
            input_df = pd.DataFrame([input_values])

            
            input_encoded = encoder.transform(input_df[["venue", "bat_team", "bowl_team"]])
            encoded_df = pd.DataFrame(input_encoded, columns=encoder.get_feature_names_out())

            
            input_df = input_df.drop(columns=["venue", "bat_team", "bowl_team"])
            input_df = pd.concat([input_df, encoded_df], axis=1)

            
            if scaler:
                input_scaled = scaler.transform(input_df)
            else:
                return render(request, 'ipl_prediction/form1.html', {'result': "Scaler not loaded properly."})

            
            if model is None:
                return render(request, 'ipl_prediction/form1.html', {'result': "Model not loaded properly."})

            
            predicted_score = model.predict(input_scaled)[0]
            result = f"Predicted Total Score: {round(predicted_score)}"

            return render(request, 'ipl_prediction/ipl_form.html', {'result': result})

        except Exception as e:
            return render(request, 'ipl_prediction/ipl_form.html', {'result': f"Error: {str(e)}"})

    return render(request, 'ipl_prediction/ipl_form.html')