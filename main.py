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
import subprocess
import time




with open("intents.json") as file:
    data = json.load(file)

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)






try: 
    # with open("data.pickle", "rb") as f:
       # words, labels, training, output = pickle.load(f)
    scotty.py

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
    
    words = [stemmer.stem(w.lower()) for w in words if w != "?" and "!"]
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

            alicemessage = "not updated yet."

            def DisplayandSpeak():
                print()
                print("ALICE: " + alicemessage)
                print()
                engine.say(alicemessage)
                engine.runAndWait()
                inp = input(user_name + ": ")

            inp = input(user_name + ": ")

            #terminate
            if inp.lower() == "terminate": #shutdown ALICE
                break
            
            #no response
            if inp.lower() == "":
                print("ALICE: No response given.")
           
            #test message
            if inp.lower() == "test message":
                alicemessage = "Okay. Let's see if this new function is working."
                DisplayandSpeak();

            #display ALICE's current stored message.
            if inp.lower() == "alicemessage":
                print(alicemessage)

            #BLACKBEAR protocol (sleep/hibernate)
            if inp.lower() == "execute blackbear protocol":
                alicemessage = "Enter password to execute the blackbear protocol."
                DisplayandSpeak()
                print()
                
                if username_id == 1 and inp.lower() == "password":
                    alicemessage = "blackbear protocol requested. executing in 3 seconds..."
                    DisplayandSpeak()
                    time.sleep(3)
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    clearConsole()
                    print("ALICE: Welcome back!")
            asktime = ["what time is it?", "what is the time?", "tell me the time?"]
            if inp.lower() in asktime:
                current_time = datetime.datetime.now()
                alicemessage = "The current time is " + current_time.strftime("%I:%M %p")
                DisplayandSpeak()



            results = model.predict([bag_of_words(inp, words)])[0]
            results_index = numpy.argmax(results)
            tag = labels[results_index]
            
            if results[results_index] > 0.7: # if probability is 70% or higher
            
                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg['responses']
                    if tg["tag"] == time:
                        current_time = datetime.datetime.now()
                        responses = tg['responses'] + " " + current_time
                
                chosen_response = random.choice(responses)
                
                print("")
                print("ALICE: " + chosen_response)
                print("")
                engine.say(chosen_response)
                engine.runAndWait()
                
            else:
                print()
                print("ALICE: I'm sorry, I don't understand.")
                engine.say("I'm sorry, I don't understand.")
                print("")
                engine.runAndWait()
    
chat()
    

