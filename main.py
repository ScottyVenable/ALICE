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
import re
import math
from os.path import exists
import shutil




with open("EVE.json") as file:
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
    chatlog = []
    chatlogNum = 1


    textcolorRed = '\033[1;37;40m'
    textcolorALICE = '\033[1;36;40m'
    textcolorUsername = '\033[1;33;40m'
    textcolorWhite = '\033[1;37;40m'
    textcolorGray = '\033[1;30;40m'
    textcolorGreen = '\033[1;32;40m'

    programVersion = 0.1
    programVersionStr = str(programVersion)
    programnameBanner = textcolorALICE + "-------A.L.I.C.E (v" + programVersionStr + ")-------" + textcolorWhite

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


    # Login
    if menuChoice == 1:
        while True:

            # Setup
            debugMode = 0
            model.load("model.tflearn") #comment out to retrain model!!!!!!  
            exit = 0
            clearConsole()
            username_id = 0
            logon_successful = 0

            print("----LOGIN----")
            inp = input("Username: " + textcolorGray)
    
            if inp.lower() == "scotty":
                username_id = 1
    
            if inp.lower() == "liam":
                username_id = 2
        
            print()
            password = input(textcolorWhite + "Password: " + textcolorGray)
            print(textcolorWhite)
    
            # Login Users
            if username_id == 1 and password == "scotty2hotty":
                logon_successful = 1
                user_name = "Scotty"
            if username_id == 2 and password == "fortnite":
                logon_successful = 1
                user_name = "Liam"
    
            clearConsole()
            loading = "Logging in"
            print(loading)
            engine.say("Logging in")
            engine.runAndWait()
            time.sleep(0.5)
            clearConsole()
            print(loading + ".")
            time.sleep(0.5)
            clearConsole()
            print(loading + "..")
            time.sleep(0.5)
            clearConsole()

            time.sleep(2)

            if logon_successful != 1:
                
                print(textcolorRed + "Login Failed" + textcolorWhite)
                engine.say("login failed")
                engine.runAndWait()
                time.sleep(3)
                print()
                print("Try again? (y/n)")
                engine.say("try again?")
                engine.runAndWait()
                tryagain = input("> ")
                if tryagain == "n":
                    sys.exit()
            
            else:
                exit = 0
                print()
                print(textcolorGreen + "Login Successful!" + textcolorWhite)
                engine.say("login successful!")
                engine.runAndWait()
                print()
                print("Welcome, " + textcolorUsername + user_name + textcolorWhite + "!")
                engine.say("welcome " + user_name)
                engine.runAndWait()
                time.sleep(1)
                clearConsole()
                print(programnameBanner)
                break

    # Guest
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

    # Debug
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

    # Train
    if menuChoice == 4:
        exit = 1
        clearConsole()
        print("Deleting previous training model...")
        os.remove("model.tflearn.data-00000-of-00001")
        os.remove("model.tflearn.index")
        os.remove("model.tflearn.meta")
        time.sleep(2)
        print("SUCCESS: Previous model removed!")
        time.sleep(1)
        clearConsole()
        print("Getting ready to train neural network data...")
        time.sleep(1)
        print("Please do not terminate until finished!")
        time.sleep(3)
        clearConsole()
        TrainNewModel()
        clearConsole()
        print("Model Training Successful!")
        time.sleep(1)
        print()
        
        
    if exit == 0:
        if reboot == 0:
            while True:
                textcolorRed = '\033[1;37;40m'
                textcolorALICE = '\033[1;36;40m'
                textcolorUsername = '\033[1;33;40m'
                textcolorWhite = '\033[1;37;40m'
                textcolorGray = '\033[1;30;40m'

                errorCodesList = ["first_error", "Duplicate file already exists.", "File creation aborted."]
                alicemessage = "not updated yet."
                errorMessage = False

                # Math Substrings
                mathProblem = ""
                isMathProblem = False

                mathAddition = ["+", "plus"]
                mathSubtraction = ["-", "minus"]
                mathMultiply = ["*", "times"]
                mathDivide = ["/", "divided by"]
                print()
                inp = input(textcolorUsername + user_name + ": " + textcolorWhite)
         
                # ADD TO TEXT LOG
         #       chatlog.append(user_name + ": " + inp + "/n") 

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

                #Start a prediction
                results = model.predict([bag_of_words(inp, words)])[0]
                results_index = numpy.argmax(results)
                tag = labels[results_index]

                # if probability is 70% or higher
                if results[results_index] > 0.7: 

                    # Create Variables
                    current_time = datetime.datetime.now()
                    current_time = datetime.datetime.now()
                    systemValue = ""
                    give_time = current_time.strftime("%I:%M %p")
                    give_date = current_time.strftime("%m-%d-%Y")
                    
                    # Get responses from intents file
                    for tg in data["intents"]:
                        if tg["tag"] == tag:
                            responses = tg['responses']

                    #Show Debug Values
                    if debugMode == 1:
                        print()
                        print("Label: " + '"' + labels[results_index] + '"')
                        print(responses)

        
                    # Display the date
                    if labels[results_index] == "date":   
                        chosen_response = random.choice(responses)
                        systemValue = give_date

                    # Display current mood
                    if labels[results_index] == "howareyou":
                        chosen_response = random.choice(responses)
                        systemValue = current_mood

                    # Display the time
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
                        alicemessage = "Displaying current emotional data: \n"

                        systemValue = "\n \n  [Happiness: " + happinessScoreString + "],\n [Sadness: " + sadnessScoreString + "],\n [Anger: " + angerScoreString + "],\n [Excitement: " + excitementScoreString + "],\n [Boredom: " + boredomScoreString + "]"

                    # Clear the Screen
                    if labels[results_index] == "clearscreen":
                        clearConsole()
                        print(programnameBanner)
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

                    if labels[results_index] == "math":
                        mathString = inp
                        map(int, re.findall(r'\d+', mathString))
                        [mathString]
                        print(mathString)

                    if labels[results_index] == "createfile":
                        print()                    
                        alicemessage = "What would you like to name the file? Please include the file extension."
                        print(textcolorALICE + "ALICE: " + textcolorWhite + alicemessage)
                        engine.say(alicemessage)
                        engine.runAndWait()
                        print(textcolorGray)
                        fileName = input("File Name: ")
                        if fileName == "!abort":
                            alicemessage = "File creation aborted."
                            print()
                            print(textcolorALICE + "ALICE: " + textcolorWhite + alicemessage)
                            engine.say("file creation aborted.")
                            errorMessage = True
                            errorCode = 2
                            engine.runAndWait()

                        if fileName != "!abort":
                            fileFolder = "files"
                            fileFolder = (os.path.join(fileFolder, fileName))
                            fileExists = os.path.exists(fileFolder)
                            if not os.path.exists("files"):
                                os.makedirs("files")
                            
                            if fileExists == False:
                                print(fileFolder)
                                open(fileFolder, 'x')
                                systemValue = fileName
                                chosen_response = random.choice(responses)
                                errorMessage = False
                        
                            if fileExists == True:
                                errorMessage = True
                                errorCode = 1

                    if labels[results_index] == "createchatlog":               
                        fileFolder = "chatlogs"
                        chatlogStr = str(chatlogNum)
                        fileName = "chatlog" + chatlogStr + ".txt"
                        fileFolder = (os.path.join(fileFolder, fileName))
                        fileExists = os.path.exists(fileFolder)
                        if not os.path.exists("chatlogs"):
                            os.makedirs("chatlogs")

                        if fileExists == False:
                            print(fileFolder)
                            open(fileFolder, 'x')
                            systemValue = fileName

                            output_file = open(fileFolder, 'w')

                            for chatlog in chatlog:
                                output_file.write(chatlog)

                            output_file.close()
                            chatlogNum = chatlogNum + 1

                            chosen_response = random.choice(responses)
                            errorMessage = False
                            
                        
                        if fileExists == True:
                            chatlogNum = chatlogNum + 1

                    chosen_response = random.choice(responses)

                    # System Data in response
                    if systemValue != "":
                        if errorMessage == False:
                            print()
                            print(textcolorALICE + "ALICE: " + textcolorWhite + chosen_response + systemValue)
                            engine.say(chosen_response + systemValue)
                            engine.runAndWait()
                        if errorMessage == True:
                            print()
                            print(textcolorRed + " An error has occurred! (00" + fileErrorCode + ")")
                            print(errorCodesList[errorCode])

                    # System Data is not in response
                    if systemValue == "":
                        if errorMessage == False:
                            print()
                            print(textcolorALICE + "ALICE: " + textcolorWhite + chosen_response)
                      #     print("A.L.I.C.E: " + chosen_response)
                            engine.say(chosen_response + systemValue)
                            engine.runAndWait()
                        if errorMessage == True:
                            print()
                            errorCodeasStr = str(errorCode)

                            print(textcolorRed + "An error has occurred!")
                            print("error code: (" + errorCodeasStr + ")")
                            print('"' + errorCodesList[errorCode] + '"')

                            engine.say("An error has occurred! " + errorCodesList[errorCode])
                            engine.runAndWait()

                # Not understanding recieved message.    
                else:
                    print()
                    print(textcolorALICE + "ALICE: I'm sorry, I don't understand.  \n")
                    engine.say("I'm sorry, I don't understand.")
                    engine.runAndWait()


    # Exit the program
    if exit == 1:
        clearConsole()
        print("Exiting now...")
        time.sleep(3)

    


chat()
    

