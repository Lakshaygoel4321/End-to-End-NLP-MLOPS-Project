from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import pickle
import numpy as np
import nltk
import re
import string
import sys
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from flask_cors import CORS
from src.exception import USvisaException
from src.logger import logging
from src.constants import *

# Setup
nltk.download('stopwords')


app = Flask(__name__)
CORS(app)  # Allow React to communicate with Flask

# Load model
#model = joblib.load(MODEL_OUTPUT_PATH)

#tokenizer = joblib.load(TOKEN_FILE_PATH)

# Load tokenizer
with open('preprocessing.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


# Preprocessing function
def data_cleaning(text):
    try:
        logging.info("Started data_cleaning")
        stemmer = nltk.SnowballStemmer("english")
        stopword = set(stopwords.words('english'))

        text = str(text).lower()
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'<.*?>+', '', text)
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        text = re.sub(f"[{re.escape(string.punctuation)}]", '', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\w*\d\w*', '', text)

        words = [word for word in text.split() if word not in stopword]
        stemmed = [stemmer.stem(word) for word in words]
        cleaned_text = " ".join(stemmed)

        logging.info("Finished data_cleaning")
        return cleaned_text
    except Exception as e:
        raise USvisaException(e, sys) from e

# API endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        tweet_text = data.get('tweet', '')

        if not tweet_text:
            return {'error': 'No tweet provided'}, 400

        tweet_clean = data_cleaning(tweet_text)
        seq = tokenizer.texts_to_sequences([tweet_clean])
        padded_seq = pad_sequences(seq, maxlen=150)

        pred = model.predict(padded_seq)
        sentiment = "Negative" if pred[0] == 1 else "Positive"
        return {'sentiment': sentiment}, 200
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
