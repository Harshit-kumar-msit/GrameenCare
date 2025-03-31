from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model and necessary data files
model = pickle.load(open("./model/svc.pkl", "rb"))

# Load the symptoms DataFrame
sym_des1 = pd.read_csv("./model/symtoms_df.csv")
precautions = pd.read_csv("./model/precautions_df.csv")
workout = pd.read_csv("./model/workout_df.csv")
description = pd.read_csv("./model/description.csv")
medications = pd.read_csv("./model/medications.csv")
diets = pd.read_csv("./model/diets.csv")
sym_des = pd.read_csv('./model/Training.csv')
print(sym_des.columns)
workout.rename(columns={'disease': 'Disease'}, inplace=True)

# Extract symptom list
# Exclude the 'Disease' column and assume the rest are symptoms
# Get all symptom columns (excluding 'Disease')
symptom_columns = [col for col in sym_des.columns if col != 'prognosis']

all_symptoms = [symptom.strip() for symptom in symptom_columns]

print(symptom_columns)
print(all_symptoms)

print(f"Number of symptoms found: {len(all_symptoms)}")


# Ensure diseases are mapped correctly using your dictionary
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'} 

# Get unique diseases and their corresponding indices
all_diseases2 = sym_des1['Disease'].unique()
print(len(all_diseases2))
# Map the unique diseases to their indices using the dictionary
#all_diseases =[diseases_list.get(disease) for disease in len(all_diseases2)]
# Reverse the diseases_list dictionary to map disease names to keys
reversed_diseases_list = {v: k for k, v in diseases_list.items()}

# Map the diseases correctly using the reversed dictionary
all_diseases = [reversed_diseases_list.get(disease) for disease in all_diseases2]


print(all_diseases)

def get_predicted_value(user_symptoms):
    """Predict the disease based on input symptoms"""
    input_vector = np.zeros(len(all_symptoms))  
    for symptom in user_symptoms:
        if symptom in all_symptoms:
            symptom_index = all_symptoms.index(symptom)
            input_vector[symptom_index] = 1
    
    features = input_vector.reshape(1, -1)
    prediction_index = model.predict(features)[0]
    print(prediction_index)
    # Ensure the predicted index is within the valid range
    if 0 <= prediction_index < len(all_diseases):
        predicted_disease = diseases_list.get(prediction_index)
        print(predicted_disease)
    else:
        predicted_disease = "Unknown Disease"

    return predicted_disease

def clean_list(data):
    """Ensure the data is properly formatted as a list"""
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], str):
        data = data[0].strip("[]").replace("'", "").split(", ")
    return data if isinstance(data, list) else [data]

def helper(dis):
    """Fetch details related to a disease"""
    desc = description[description['Disease'] == dis]['Description']
    desc = desc.values[0] if not desc.empty else "No description available."

    pre_df = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = pre_df.values.flatten().tolist() if not pre_df.empty else []
    pre = [str(item) for item in pre if isinstance(item, str) and item.strip()]

    med = medications[medications['Disease'] == dis]['Medication']
    med = med.tolist() if not med.empty else []

    die = diets[diets['Disease'] == dis]['Diet']
    die = die.tolist() if not die.empty else []

    wrkout = workout[workout['Disease'] == dis]['workout']
    wrkout = wrkout.tolist() if not wrkout.empty else []

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
        
        input_features = np.zeros((1, 132))  
        for symptom in symptoms:
            if symptom in all_symptoms:
                index = all_symptoms.index(symptom)
                input_features[0, index] = 1
        
        # Predict Disease
        predicted_disease = get_predicted_value(symptoms)
        
        # Fetch additional information
        desc, pre, med, die, wrkout = helper(predicted_disease)

        return jsonify({
            "predicted_disease": predicted_disease,
            "description": desc,
            "precautions": pre,
            "medications": clean_list(med),
            "workout": clean_list(wrkout),
            "diet": clean_list(die)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
