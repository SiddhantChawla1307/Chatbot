import nltk
from ai_client import get_faqs

import random
from nltk.stem import WordNetLemmatizer #lemmatizer converts words into base form
from nltk.tokenize import word_tokenize #breaking sentences into indivitual words
lemmatizer = WordNetLemmatizer() #lemmatizer tool
print("Welcome to ChatBot")
def preprocess(sentence):
    tokens = word_tokenize(sentence.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens] #converting word into base form
    return tokens
responses = {"greeting": ["Hi!", "Hello!", "Hey!"],"name": ["I am a chatbot built using NLTK."]}

def get_intent(user_input):
    tokens = preprocess(user_input)
    if "hello" in tokens or "hi" in tokens or 'hey' in tokens:
        return "greeting" #return the value of the key
    elif "name" in tokens:
        return "name"
    elif "bye" in tokens:
        return "bye"
    else:
        return "unknown"

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit" or user_input.lower() == 'bye':
        print("Bot: Bye! See you later.")
        break

    intent = get_intent(user_input) #function called
    #print("DEBUG :",intent)

    if intent in responses:
        print("Bot:", random.choice(responses[intent]))
        #responses[intent] = list of replies for the intent
        #random.choice() = randomly choosing a response from given list
    else:
        # AI Responses
        print(f"Bot:", get_faqs(user_input))




