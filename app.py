from flask import Flask, render_template, redirect, url_for, request, jsonify
import pickle
import numpy as np

model = pickle.load(open("./model/svc.pkl", "rb"))

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = np.array(data["features"]).reshape(1, -1)  
        
        prediction = model.predict(features)
        
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True) 
