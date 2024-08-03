from flask import Flask, request, jsonify
import requests
from flask_cors import CORS 
import logging

app = Flask(__name__)
CORS(app)

KERAS_REST_API_URL = "http://35.223.122.225:5000/predict"

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        date1 = data['date']
        latp = data['lat']
        longp = data['lng']

        app.logger.debug(f"Received data: {data}")

        # Print the fetched latitude and longitude
        print(f"Latitude: {latp}, Longitude: {longp}")

        mydata = {'date': date1, 'latp': latp, 'longp': longp}
        r = requests.post(KERAS_REST_API_URL, json=mydata)

        app.logger.debug(f"Response from Keras REST API: {r.text}")

        r_json = r.json()

        if r_json["success"]:
            prediction = r_json["predictions"]
            prediction = str(prediction)
            # Print the prediction value
            print(f"Prediction: {prediction}")

            # Define the message based on prediction
            if prediction == "[[[1]]]":
                result_message = "Flood detected in this area."
            elif prediction == "[[[0]]]":
                result_message = "No flood detected"
            else:
                result_message = "Unknown prediction result."

            return jsonify({'success': True, 'predictions': prediction, 'message': result_message})
        else:
            return jsonify({'success': False, 'error': 'Request failed'})
    except Exception as e:
        app.logger.error(f"Error during prediction: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3002)
