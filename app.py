from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model and necessary data files
model = pickle.load(open("./model/svc.pkl", "rb"))

# Load the symptoms DataFrame
sym_des = pd.read_csv("./model/symtoms_df.csv")
precautions = pd.read_csv("./model/precautions_df.csv")
workout = pd.read_csv("./model/workout_df.csv")
description = pd.read_csv("./model/description.csv")
medications = pd.read_csv('./model/medications.csv')
diets = pd.read_csv("./model/diets.csv")

workout.rename(columns={'disease': 'Disease'}, inplace=True)

symptom_columns = ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4']
all_symptoms = pd.unique(sym_des[symptom_columns].values.ravel('K')).tolist()
all_symptoms = [symptom.strip() for symptom in all_symptoms if isinstance(symptom, str) and symptom.strip()]
print(f"All symptoms: {all_symptoms}")
print(f"Number of symptoms: {len(all_symptoms)}")


all_diseases = sym_des['Disease'].unique().tolist()
print(f"All diseases: {all_diseases}")

def get_predicted_value(user_symptoms):
    input_vector = np.zeros(132)  
    for symptom in user_symptoms:
        if symptom in all_symptoms:
            symptom_index = all_symptoms.index(symptom)
            input_vector[symptom_index] = 1
    features = input_vector.reshape(1, -1)
   
    prediction_index = model.predict(features)[0]
    print(f"Raw Model Prediction Index: {prediction_index}")
    prediction = all_diseases[prediction_index]
    return prediction

def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])  # Convert to string
    
    pre_df = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    

    pre = pre_df.values.flatten().tolist() if not pre_df.empty else []
    

    pre = [str(item) for item in pre if isinstance(item, str) and item.strip()]
    

    med = medications[medications['Disease'] == dis]['Medication']
    med = med.tolist() if not med.empty else []
    # med = med.values.tolist()
    
    die = diets[diets['Disease'] == dis]['Diet']
    die = die.tolist() if not die.empty else []
    
    wrkout = workout[workout['Disease'] == dis]['workout']
    wrkout = wrkout.values.tolist()

    return desc, pre, med, die, wrkout



@app.route('/get_symptoms')
def get_symptoms():
    """Return all available symptoms as a JSON response"""
    return jsonify({"symptoms": all_symptoms})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        symptoms = data.get("symptoms", [])
        print(f"Received symptoms: {symptoms}")
        
        input_features = np.zeros((1, len(all_symptoms)))  
        print(f"Initial input features: {input_features}")
        
        for symptom in symptoms:
            if symptom in all_symptoms:
                index = all_symptoms.index(symptom)
                input_features[0, index] = 1
        
        print(f"Prepared input features: {input_features}")
        
        # Predict Disease
        predicted_disease = get_predicted_value(symptoms)
        print(f"Predicted disease: {predicted_disease}")
        
        desc, pre, med, die, wrkout = helper(predicted_disease)
        
        # Convert numpy.int64 to int
        desc = desc.tolist() if isinstance(desc, np.ndarray) else desc
        pre = [str(item) for item in pre[0]] if pre else []
        med = [str(item) for item in med] if med else []
        wrkout = [str(item) for item in wrkout] if wrkout else []
        die = [str(item) for item in die] if die else []
        
        return jsonify({
            "predicted_disease": str(predicted_disease),
            "description": desc,
            "precautions": pre,
            "medications": med,
            "workout": wrkout,
            "diet": die
        })
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        return jsonify({"error": f"KeyError: {str(e)}"})
    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)