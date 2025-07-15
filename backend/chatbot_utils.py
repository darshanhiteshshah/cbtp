import nltk
import numpy as np
import random
import json
import requests
import pickle
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Clean user input
def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens]
    return tokens


# Convert to bag-of-words
def bag_of_words(text, vocab):
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    return np.array(bow)


# Predict intent
def predict_class(text, model, words, classes):
    bow = bag_of_words(text, words)
    res = model.predict(np.array([bow]))[0]
    threshold = 0.6
    results = [[i, r] for i, r in enumerate(res) if r > threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return [classes[r[0]] for r in results]


# Generate Response
def get_response(intents_list, intents_json):
    if not intents_list:
        return "Sorry, I didn't understand that."

    tag = intents_list[0]

    if tag == "joke":
        joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        return f"{joke['setup']} ... {joke['punchline']}"

    if tag == "weather":
        city = "Mumbai"
        api_key = "{ OpenWeatherMap API Key}"  
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if "main" in response:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"The current temperature in {city} is {temp}°C with {desc}."
        return "Unable to fetch weather info."

    if tag == "quote":
        quote = requests.get("https://api.quotable.io/random").json()
        return f'"{quote["content"]}" — {quote["author"]}'

    if tag == "fact":
        fact = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        return fact["text"]

    if tag == "advice":
        advice = requests.get("https://api.adviceslip.com/advice").json()
        return advice["slip"]["advice"]

    if tag == "news":
        api_key = "{GNews API Key}"  
        url = f"https://gnews.io/api/v4/top-headlines?token={api_key}&lang=en&country=in"
        response = requests.get(url).json()
        if "articles" in response and response["articles"]:
            top = response["articles"][0]
            return f"Top headline: {top['title']} \nRead more: {top['url']}"
        return "Couldn't fetch news."

    for intent in intents_json["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "I'm not sure how to help with that."
