from flask import Flask, render_template, request
from pickle import load
import numpy as np
import re
import nltk
nltk.download('stopwords') # this was added
from nltk.util import pr
from nltk.stem import SnowballStemmer

# Initialize the stemmer
stemmer = SnowballStemmer("english")
from nltk.corpus import stopwords
import string
stopword = set(stopwords.words('english'))

# Load the trained model
model_path = './model.pkl'
with open(model_path, 'rb') as file:
    model = load(file)

cv_path = "./count_vectorizer.pkl"
with open(cv_path, "rb") as file:
    cv = load(file)

# Example tokenizer/vectorizer (replace with your actual preprocessing)
def preprocess_message(message):
    # Example: convert to lowercase, tokenize, etc.
    # return np.array([len(message.split())])  # Dummy example: replace with real preprocessing
    text = str(message).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www.\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    df = cv.transform([text]).toarray()
    return df

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("model -> ", model)
        message = request.form.get('message', '').strip()
        print(f"Received message: '{message}'")  # Debugging: Log the received message
        if not message:
            return render_template('index.html', prediction_text="Please enter a valid message.")
        
        processed_features = preprocess_message(message)
        prediction = model.predict(processed_features.reshape(1, -1))
        print(prediction[0])
        return render_template('index.html', prediction_text=f'Prediction: {prediction[0]}')
    except Exception as e:
        print(f"Error during prediction: {e}")
        return render_template('index.html', prediction_text="Error: Unable to process the request.")


if __name__ == '__main__':
    app.run(debug=True)
