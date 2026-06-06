from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Model load karein (ensure karein model.pkl aapke folder mein ho)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() # User se JSON data milega
    # Features extract karein
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    
    # Flower ka naam return karein
    flowers = ['Setosa', 'Versicolor', 'Virginica']
    return jsonify({'prediction': flowers[prediction[0]]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
