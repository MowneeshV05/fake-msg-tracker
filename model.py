# model.py - Machine Learning Model for Scam Message Classification

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def load_dataset(filepath="data/messages.csv"):
    # Read the CSV file containing messages and labels using pandas
    dataframe = pd.read_csv(filepath)
    
    # Return the loaded table
    return dataframe


def train_model(filepath="data/messages.csv"):
    # Step 1: Load the training data from CSV
    data = load_dataset(filepath)
    
    # Extract the message text column as inputs (X)
    text_data = data["text"]
    
    # Extract the labels column as targets (y) where 1 is Scam and 0 is Safe
    labels = data["label"]
    
    # Step 2: Initialize TF-IDF Vectorizer to convert text words into numerical scores
    # lowercase=True converts all words to lowercase
    # stop_words='english' removes common filler words like 'the', 'is', 'at'
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
    
    # Learn the vocabulary and transform message texts into numerical vectors
    feature_matrix = vectorizer.fit_transform(text_data)
    
    # Step 3: Initialize the Logistic Regression model
    # max_iter=1000 gives the solver enough iterations to find optimal weights
    classifier = LogisticRegression(max_iter=1000)
    
    # Train the classifier using the numerical vectors and corresponding labels
    classifier.fit(feature_matrix, labels)
    
    # Step 4: Return both the trained model and the vectorizer
    return classifier, vectorizer


def predict_message(message_text, classifier, vectorizer):
    # Convert the single input message into the same TF-IDF numerical vector format
    message_vector = vectorizer.transform([message_text])
    
    # Get probability distribution: [probability_of_safe, probability_of_scam]
    probabilities = classifier.predict_proba(message_vector)[0]
    
    # Extract safe probability percentage (rounded to 1 decimal place)
    safe_percentage = round(float(probabilities[0] * 100), 1)
    
    # Extract scam probability percentage (rounded to 1 decimal place)
    scam_percentage = round(float(probabilities[1] * 100), 1)
    
    # Determine the label based on which probability is higher
    if scam_percentage >= 50.0:
        prediction = "Scam"
    else:
        prediction = "Safe"
        
    # Return results in a clean dictionary
    return {
        "prediction": prediction,
        "scam_probability": scam_percentage,
        "safe_probability": safe_percentage
    }
