from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pickle
import tensorflow as tf
from chatbot_utils import predict_class, get_response

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load pre-trained model and data
model = tf.keras.models.load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


# API Endpoint for chatbot communication
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    intents_list = predict_class(message, model, words, classes)
    response = get_response(intents_list, intents)
    return jsonify({"response": response})


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
