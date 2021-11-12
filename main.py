import nltk
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.python.ops.gen_data_flow_ops import accumulator_apply_gradient
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






current_mood = "neutral"

mood_tags = []



try: 
   #  with open("data.pickle", "rb") as f:
   #     words, labels, training, output = pickle.load(f)
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


# Create the "Bag of Words"  
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
    current_mood = "neutral"
    sadness_score = 0
    anger_score = 0
    happiness_score = 0
    excitement_score = 0
    boredom_score = 0

    def TrainNewModel():
        tf.compat.v1.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)
        model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
        model.save("model.tflearn")
    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    os.system('cls')
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[1].id)

    def DisplayandSpeak():
        print()
        print("ALICE: " + alicemessage)
        print()
        engine.say(alicemessage)
        engine.runAndWait()
        inp = input(user_name + ": ")

    #Main Menu
    menuChoice = 0
    reboot = 0
    clearConsole()


    print("Welcome to A.L.I.C.E")
    print("--------------------")
    print("1. Login")
    print("2. Guest Login")
    print("3. Debug Mode")
    print("4. Train A.L.I.C.E")
    print("5. Exit")
    print("--------------------")
    inp = input("> ")

    if inp.lower() == "1":
        menuChoice = 1
    if inp.lower() == "2":
        menuChoice = 2
    if inp.lower() == "3":
        menuChoice = 3
    if inp.lower() == "4":
        menuChoice = 4


    # Main Menu Choices
    if menuChoice == 1:
        debugMode = 0

        model.load("model.tflearn") #comment out to retrain model!!!!!!  

        exit = 0
        clearConsole()
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

    if menuChoice == 2:
        debugMode = 0
        model.load("model.tflearn")
        exit = 0
        clearConsole()
        print("Welcome, Guest!")
        print("------------------")
        print("")
        username_id = 999
        user_name = "Guest"           

    if menuChoice == 3:
        model.load("model.tflearn")
        exit = 0
        debugMode = 1
        clearConsole()
        print("DEBUG MODE ACTIVE")
        print("------------------")
        print("")
        username_id = 6526
        user_name = "Debug"  

    if menuChoice == 4:
        exit = 1
        TrainNewModel()
        clearConsole()
        print("Model Training Successful!")
        time.sleep(1)
        print()
        
        
    if exit == 0:
        if reboot == 0:
            while True:
                alicemessage = "not updated yet."
                

               
                print("\033[1;37;40m")
                inp = input(user_name + ": ")

                # Terminate
                if inp.lower() == "terminate": #shutdown ALICE
                    break
            
                # No response
                if inp.lower() == "":
                    print("ALICE: No response given.")
           
                # Test message
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

                results = model.predict([bag_of_words(inp, words)])[0]
                results_index = numpy.argmax(results)
                tag = labels[results_index]

                if results[results_index] > 0.7: # if probability is 70% or higher
                

                    # Create Variables
                    current_time = datetime.datetime.now()
                    current_time = datetime.datetime.now()
                    systemValue = ""
                    give_time = current_time.strftime("%I:%M %p")
                    give_date = current_time.strftime("%m-%d-%Y")
                    

                    

                    
                    

                    for tg in data["intents"]:
                        if tg["tag"] == tag:
                            responses = tg['responses']

                    #Show Debug Values
                    if debugMode == 1:
                        print()
                        print("Label: " + '"' + labels[results_index] + '"')
                        print(responses)

        
                    # Display the Date
                    if labels[results_index] == "date":   
                        chosen_response = random.choice(responses)
                        systemValue = give_date

                    if labels[results_index] == "howareyou":
                        chosen_response = random.choice(responses)
                        systemValue = current_mood

                    # Display the Time
                    if labels[results_index] == "time":
                        chosen_response = random.choice(responses)
                        systemValue = give_time
                
                    # Display Emotional Data
                    if labels[results_index] == "displayemotions":

                        happinessScoreString = str(happiness_score)
                        sadnessScoreString = str(sadness_score)
                        angerScoreString = str(anger_score)
                        excitementScoreString = str(excitement_score)
                        boredomScoreString = str(boredom_score)

                        chosen_response = random.choice(responses)
                        systemValue = "[Happiness: " + happinessScoreString + "], [Sadness: " + sadnessScoreString + "], [Anger: " + angerScoreString + "], [Excitement: " + excitementScoreString + "], [Boredom: " + boredomScoreString + "]"

                    # Clear the Screen
                    if labels[results_index] == "clearscreen":
                        clearConsole()
                        chosen_response = random.choice(responses)

                
                  
                    chosen_response = random.choice(responses)
                    
                    if labels[results_index] == "praise":
                        happiness_score = happiness_score + 1
                        chosen_response = random.choice(responses)
                     
                        # Moods/Emotions
                    if labels[results_index] == "howareyou":

                        if sadness_score > 5 and 'sad' in mood_tags:
                            current_mood = "sad"
                        if anger_score > 5 and 'frustrated' in mood_tags:
                            current_mood = "frustrated"
                        if happiness_score > 5:
                            current_mood = "happy"
                        if happiness_score > 10:
                            current_mood = "elated"
                        if excitement_score > 5:
                            current_mood = "excited"
                        if boredom_score > 5:
                            current_mood = "bored"
                        chosen_response = random.choice(responses)
                        systemValue = current_mood

                    # System Data in response
                    if systemValue != "":
                        print()
                        print("\033[1;36;40mALICE: " + chosen_response + systemValue)
                        engine.say(chosen_response + systemValue)
                        engine.runAndWait()

                    # System Data is not in response
                    if systemValue == "":   
                        print()
                        print("\033[1;36;40mALICE: " + chosen_response)
                  #     print("A.L.I.C.E: " + chosen_response)
                        engine.say(chosen_response + systemValue)
                        engine.runAndWait()

                # Not understanding recieved message.    
                else:
                    print()
                    print("\033[1;36;40m A.L.I.C.E: I'm sorry, I don't understand.  \n")
                    engine.say("I'm sorry, I don't understand.")
                    print("")
                    engine.runAndWait()


    # Exit the program
    if exit == 1:
        clearConsole()
        print("Exiting now...")
        time.sleep(3)

    


chat()
    

