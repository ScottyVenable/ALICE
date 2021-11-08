import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import datetime
from datetime import date
import numpy
import tflearn
import tensorflow as tf
import random
import json
import pickle
import os
import pyttsx3
engine = pyttsx3.init()
import winsound
import tkinter
from tkinter import *


#Watson Text to Speech
watson_url = 'https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/8649019b-bdd5-4a5e-ad23-0f352e69b044'
watson_apikey = 'mTYI4JL4Zyo8TtocRfoVnuqBce-11iEYwA8dyjvETFVt'

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(watson_apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(watson_url)



with open("intents.json") as file:
    data = json.load(file)

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


try: 
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
    #scotty.py
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
    
        if intent["tag"] not in labels:
                labels.append(intent["tag"])
    
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    
    labels = sorted(labels)
    
    training = []
    output = []
    
    out_empty = [0 for _ in range(len(labels))]
    
    for x, doc in enumerate(docs_x):
        bag = []
    
        wrds = [stemmer.stem(w.lower()) for w in doc]
    
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
    
        training.append(bag)
        output.append(output_row)
    
    
    training = numpy.array(training)
    output = numpy.array(output)
    
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
    

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn") #comment out to retrain model!!!!!!
    #scotty.py
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
                
    return numpy.array(bag)


def chat():
    os.system('cls')
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[1].id)


# WATSON TEXT TO SPEECH    
#    with open('./speech.wav', 'wb') as audio_file:
#        res = tts.synthesize("Welcome. My name is ALICE, I am the Always Learning Interactive Companion Engine. How can I help you today?", accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()
#        audio_file.write(res.content)
    

    username_id = 0
    logon_successful = 0
    
    inp = input("Username: ")
    
    if inp.lower() == "scotty":
        username_id = 1
    
    if inp.lower() == "liam":
        username_id = 2
        
    inp = input("Password: ")
    
    # Login Scotty
    if username_id == 1 and inp.lower() == "scotty2hotty":
        logon_successful = 1
        user_name = "Scotty"
        
    #Login Liam
    if username_id == 2 and inp.lower() == "fortnite":
        logon_successful = 1
        user_name = "Liam"
    
    if logon_successful != 1:
        os.system('cls')
        print("LOGIN FAILED")
        inp = input("> ")
    else:
        os.system('cls')
        print("Login Successful!")
        print("Welcome, "+user_name+"!")
        print("------------------")
        print("")
    
        
        
    
    
    
        while True:
            inp = input(user_name + ": ")
            if inp.lower() == "terminate": #shutdown ALICE
                break
            
            if inp.lower() == "cls":
                os.system('cls')
            
            if inp.lower() == "":
                print("ALICE: No response given.")
            
            results = model.predict([bag_of_words(inp, words)])[0]
            results_index = numpy.argmax(results)
            tag = labels[results_index]
            
            if results[results_index] > 0.7: # if probability is 70% or higher
            
                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg['responses']
                
                chosen_response = random.choice(responses)
                
                print("")
                print("ALICE: " + chosen_response)
                print("")
                engine.say(chosen_response)
                engine.runAndWait()
                
            else:
                print("ALICE: I'm sorry, I don't understand.")
                engine.say("I'm sorry, I don't understand.")
                print("")
                engine.runAndWait()
    
chat()
    

