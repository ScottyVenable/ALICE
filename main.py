import nltk
from nltk.stem.lancaster import LancasterStemmer
from numpy.lib.function_base import delete
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
import pwinput
import re
import urlopen
import vlc
import time
from pygame import mixer



introVoices = ["intro_1", "intro_2", "intro_3", "intro_4", "intro_5"]

with open("EVE.json") as file:
    data = json.load(file)

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def removeTrainingModel():
    clearConsole()
    print("What is the name of the model you would like to delete?")
    print(textcolorGray + "(type 'model' if you didn't rename the previous model.)" + textcolorWhite)
    print()
    modelName = input("> " + textcolorGray)

    
    os.remove(modelName + ".tflearn.data-00000-of-00001")
    os.remove(modelName + ".tflearn.index")
    os.remove(modelName + ".tflearn.meta")
    print()
    time.sleep(2)

    def loadingDeleteModel():

        voiceMute = False
        voicewait = False
        def Speak(voicefile):
            if voiceMute == False:
                mixer.init()
                voicepath = "voicelines/" + voicefile + ".mp3"
                mixer.music.load(voicepath)
                mixer.music.play()
                if voicewait == True:
                    while mixer.music.get_busy():  # wait for music to finish playing
                        time.sleep(1)

        textcolorRed = '\033[1;31;40m'
        textcolorALICE = '\033[1;36;40m'
        textcolorUsername = '\033[1;33;40m'
        textcolorWhite = '\033[1;37;40m'
        textcolorGray = '\033[1;30;40m'
        textcolorGreen = '\033[1;32;40m'

        loadingMessage = "Deleting previous training data"
        loadingSuccess = textcolorGreen + "Training model deleted!" + textcolorWhite
        loadingFailed = textcolorRed + "Training model deletion failed!" + textcolorWhite
        dotCount = 20
        clearConsole()
        deleteWait = 0
        print(loadingMessage)

        while deleteWait < dotCount:
            deleteWait = deleteWait + 1
            time.sleep(0.02)
            clearConsole()
            loadingMessage+=str(".")
            print(loadingMessage)

        Speak("training_model_deleted")
        loadingMessage+=str(loadingSuccess)
        print(textcolorGreen + "Success!")
        time.sleep(3)
        exit = 1

    loadingDeleteModel()
    time.sleep(3)
    clearConsole()

def updateTrainingModel():
    voiceMute = False
    voicewait = False
    def Speak(voicefile):
        if voiceMute == False:
            mixer.init()
            voicepath = "voicelines/" + voicefile + ".mp3"
            mixer.music.load(voicepath)
            mixer.music.play()
            if voicewait == True:
                while mixer.music.get_busy():  # wait for sound to finish playing
                    time.sleep(1)

    textcolorRed = '\033[1;31;40m'
    textcolorALICE = '\033[1;36;40m'
    textcolorUsername = '\033[1;33;40m'
    textcolorWhite = '\033[1;37;40m'
    textcolorGray = '\033[1;30;40m'
    textcolorGreen = '\033[1;32;40m'
    modelRename = ""
    while modelRename == "":
        print(textcolorWhite + "Would you like to rename the model? (y/n)")
        print()
        modelRename = input("> " + textcolorGray)
        if modelRename.lower() == "y" or modelRename.lower() == "yes":
            clearConsole()
            print(textcolorWhite + "What would you like to name the new model?")
            newModelName = input("> " + textcolorGray)
            time.sleep(2)
            Speak("success")
            print(textcolorGreen + "Success!")
            print()
            time.sleep(0.5)
            print(textcolorWhite + "Model has been named: " + textcolorUsername)
            time.sleep(1)
        if modelRename.lower() == "n" or modelRename.lower() == "no":
            newModelName = "model"
    
    Speak("prepare_to_train")
    print("Getting ready to train neural network data...")
    time.sleep(1)
    Speak("do_not_terminate")
    print(textcolorRed + "Please do not terminate until finished!" + textcolorWhite)
    time.sleep(3)
    clearConsole()
    
    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save(newModelName + ".tflearn")

    clearConsole()
    print(textcolorGreen + "Model Training Successful!" + textcolorGreen)
    time.sleep(1)


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
def populateColors():
    textcolorRed = '\033[1;31;40m'
    textcolorALICE = '\033[1;36;40m'
    textcolorUsername = '\033[1;33;40m'
    textcolorWhite = '\033[1;37;40m'
    textcolorGray = '\033[1;30;40m'
    textcolorGreen = '\033[1;32;40m'

isSuccessful = False
dotCount = 18

loadMessage = "default"
loadActive = False
def loadingAnimation():
    textcolorRed = '\033[1;31;40m'
    textcolorALICE = '\033[1;36;40m'
    textcolorUsername = '\033[1;33;40m'
    textcolorWhite = '\033[1;37;40m'
    textcolorGray = '\033[1;30;40m'
    textcolorGreen = '\033[1;32;40m'
    loadingSuccess = textcolorGreen + "Success!" + textcolorWhite
    loadingFailed = textcolorRed + "Failed!" + textcolorWhite
    clearConsole()
    deleteWait = 0
    print(loadingMessage)

    while deleteWait < dotCount:
        deleteWait = deleteWait + 1
        time.sleep(0.02)
        clearConsole()
        loadingMessage+=str(".")
        print(loadingMessage)
    if isSuccessful == True:
        loadingMessage+=str(loadingSuccess)
        time.sleep(3)
    if isSuccessful == False:
        loadingMessage+=str(loadingFailed)
        time.sleep(3)







def chat():
    from alicecommands import baseCommands
    numberList = [1,2,3,4,5,6,7,8,9]
    numberGen = 1
    chatlogNum = 0
    current_mood = "neutral"
    sadness_score = 0
    anger_score = 0
    happiness_score = 0
    excitement_score = 0
    boredom_score = 0
    chatlog = []

    while numberGen < 5:
        chatlogNum = chatlogNum + random.choice(numberList)
        numberGen = numberGen + 1


    textcolorRed = '\033[1;31;40m'
    textcolorALICE = '\033[1;36;40m'
    textcolorUsername = '\033[1;33;40m'
    textcolorWhite = '\033[1;37;40m'
    textcolorGray = '\033[1;30;40m'
    textcolorGreen = '\033[1;32;40m'
    consoleSize = 'mode 70, 35'
    os.system(consoleSize)

    programVersion = 0.2
    programVersionStr = str(programVersion)
    programnameBanner = textcolorALICE + "--------------------------A.L.I.C.E (v0." + programVersionStr + ")--------------------------" + textcolorWhite

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

    clearConsole()
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[1].id)

    def DisplayandSpeak():
        print()
        print(textcolorALICE + "ALICE: " + textcolorWhite + alicemessage)
        print()
        engine.say(alicemessage)
        engine.runAndWait()
        inp = input(textcolorUsername + user_name + ": ")

    menuChoice = 0
    reboot = 0
    clearConsole()
    print(textcolorALICE)
    voicefile = ""
    voicewait = False
    voiceMute = False
    def Speak(voicefile):
        if voiceMute == False:
            mixer.init()
            voicepath = "voicelines/" + voicefile + ".mp3"
            mixer.music.load(voicepath)
            mixer.music.play()
            if voicewait == True:
                while mixer.music.get_busy():  # wait for music to finish playing
                    time.sleep(1)
    def muteVoicePrompt():
        muteOption = input("Mute (y/n): ")
        if muteOption == "y":
            voiceMute = True
        if muteOption == "n":
            voiceMute = False
        clearConsole()


    #Main Menu
    def MainMenu():
        textcolorRed = '\033[1;31;40m'
        textcolorALICE = '\033[1;36;40m'
        textcolorUsername = '\033[1;33;40m'
        textcolorWhite = '\033[1;37;40m'
        textcolorGray = '\033[1;30;40m'
        textcolorGreen = '\033[1;32;40m'
        voiceMute = False
        def muteVoicePrompt():
            muteOption = input("Mute (y/n): ")
            if muteOption == "y":
                voiceMute = True
            if muteOption == "n":
                voiceMute = False
            clearConsole()
        muteVoicePrompt()
        
        print(textcolorGray + "(v0." + programVersionStr + ")" + textcolorALICE)
        print("""
                         `` ``          `` ``               
                        `    `          `   ``              
                         `````   ....   `````               
                            ``  `-  -`  ``                  
                       `.``  .`` .... ``.  ``.`             
               ```    .. `-  ` `  .. `` `  -` ..    ```     
             ``   `   `...-` ``  `--` ``  `-...`   `   ``   
             ``   ```   `  .-..` -``- `..-.  `   ```   ``   
               ```   `.``.  -``-  ``  -``-  . ```   ```     
                    `  ```  `..        ..   ``` ``          
                  ..`.-```-...          ...-```-.`..        
                  ..`.-```-...          ....```-.`..        
                    `  ```  `..        ..`  ```  `          
               ```   `.``.  -``-  ``  -``-  .````   ```     
             ``   ```   `  .-..` -``- `..-.  `   ```   ``   
             ``   `   `...-` ``` `--` ``` `-...`   `   ``   
               ```    .. `-  ` `  .. `` `  -` ..    ```     
                       ````  .`` .... ``.  ````             
                            ``  `-  -`  ``                  
                         `````   ....   `````               
                        `    `          `   ``              
                         `` ``          `` `` """)
        Speak(random.choice(introVoices))
        time.sleep(1)
        print("""                   _            _____        _____       ______ """)
        time.sleep(0.05)
        print("""       /\         | |          |_   _|      / ____|     |  ____| """)
        time.sleep(0.05)
        print("""      /  \        | |            | |       | |          | |__    """)
        time.sleep(0.05)
        print("""     / /\ \       | |            | |       | |          |  __|   """)
        time.sleep(0.05)
        print("""    / ____ \   _  | |____   _   _| |_   _  | |____   _  | |____  """)
        time.sleep(0.05)
        print("""   /_/    \_\ (_) |______| (_) |_____| (_)  \_____| (_) |______| """)
        time.sleep(1)
        print()
        print(textcolorGray + """                     (C) 2021 Cadential Studios""" + textcolorWhite)
        time.sleep(2.5)
        print()
        print("""               """+textcolorALICE+"""[ LOGIN ]"""+textcolorGreen+"""     [ UPDATE ]"""+textcolorRed+"""     [ EXIT ]                """)   
        print()
        voicewait = True
        if voiceMute == False:
            Speak("desiredintent")
    MainMenu()
    mainmenu = True
    inp = input(textcolorWhite+"""                      > """ + textcolorALICE).upper()
    print(textcolorWhite)
    if inp.lower() == "update":
        menuChoice = 3
        exit = 1
    if inp.lower() == "!debug":
        menuChoice = 2
    if inp.lower() == "login":
        menuChoice = 1
    if inp.lower() == "exit":
        exit = 1



    if menuChoice == 1:
        
        while True:
            consoleSize = 'mode 43, 35'
            os.system(consoleSize)
            debugMode = 0
            model.load("model.tflearn")  
            exit = 0
            clearConsole()
            username_id = 0
            logon_successful = 0
            
            print("-------------------LOGIN-------------------")
            print()
            inp = input("Username: " + textcolorGray)
    
            if inp == "scotty":
                username_id = 1
                voicefile = "welcome_scotty"
            if inp == "guest":
                username_id = 0
                voicefile = "welcome_guest"
            if inp == "liam":
                username_id = 2
        
            password = pwinput.pwinput(prompt=textcolorWhite + "Password: " + textcolorGray, mask='*')
            
            print(textcolorWhite)
    
            # Login Users
            if username_id == 1 and password == "scotty2hotty":
                logon_successful = 1
                user_name = "Scotty"
                password = "scotty2hotty"
                admin = 1
            if username_id == 2 and password == "fortnite":
                logon_successful = 1
                user_name = "Liam"
                password = "fortnite"
                admin = 0
            if username_id == 0 and password == "guest":
                logon_successful = 1
                user_name = "Guest"
                password = "guest"
                admin = 0
    
            clearConsole()
            dotCount = 23
                    


            if logon_successful != 1:   
                exit = 0
                isSuccessful = False
                loadMessage = "Logging in"
                def loginLoadFailed():
                    textcolorRed = '\033[1;31;40m'
                    textcolorALICE = '\033[1;36;40m'
                    textcolorUsername = '\033[1;33;40m'
                    textcolorWhite = '\033[1;37;40m'
                    textcolorGray = '\033[1;30;40m'
                    textcolorGreen = '\033[1;32;40m'                
                    
                    dotCount = 16
                    loadMessage = "Logging in"
                    
                    loadingSuccess = textcolorGreen + "LOGIN SUCCESSFUL!" + textcolorWhite
                    loadingFailed = textcolorRed + "LOGIN FAILED!" + textcolorWhite
                
                    clearConsole()
                    deleteWait = 0
                    Speak("loggingin")
                    print(loadMessage)

                    while deleteWait < dotCount:
                        deleteWait = deleteWait + 1
                        time.sleep(0.07)
                        clearConsole()
                        loadMessage+=str(".")
                        print(loadMessage)

                    Speak("login_failed")
                    isSuccessful = False

                    if isSuccessful == True:
                        loadMessage+=str(loadingSuccess)
                        print("Success")
                        time.sleep(3)
                    if isSuccessful == False:
                        loadMessage+=str(loadingFailed)
                        clearConsole()
                        print(loadMessage)
                        time.sleep(3)

                    else:
                        print("Other")
                        time.sleep(3)
                loginLoadFailed()  

                print()
                Speak("pleasetryagain")
                print("Please try again.")
                time.sleep(1)
                clearConsole()
            
            else:
                exit = 0
                voicewait = False
                loadMessage = "Logging in"

                loadActive = True

                def loginLoadSuccess():
                    textcolorRed = '\033[1;31;40m'
                    textcolorALICE = '\033[1;36;40m'
                    textcolorUsername = '\033[1;33;40m'
                    textcolorWhite = '\033[1;37;40m'
                    textcolorGray = '\033[1;30;40m'
                    textcolorGreen = '\033[1;32;40m'
                
                    Speak("loggingin")
                    dotCount = 16
                    loadMessage = "Logging in"
                    loadingSuccess = textcolorGreen + "LOGIN SUCCESSFUL!" + textcolorWhite
                    loadingFailed = textcolorRed + "LOGIN FAILED!" + textcolorWhite
                
                    clearConsole()
                    deleteWait = 0
                    print(loadMessage)

                    while deleteWait < dotCount:
                        deleteWait = deleteWait + 1
                        time.sleep(0.07)
                        clearConsole()
                        loadMessage+=str(".")
                        print(loadMessage)

                    Speak("login_successful")
                    isSuccessful = True

                    if isSuccessful == True:
                        loadMessage+=str(loadingSuccess)
                        clearConsole()
                        print(loadMessage)
                        time.sleep(3)
                    if isSuccessful == False:
                        loadMessage+=str(loadingFailed)
                        clearConsole()
                        print(loadMessage)
                        time.sleep(3)
                
                loginLoadSuccess() 
                
                Speak("welcome_" + user_name.lower())

                print("Welcome, " + textcolorUsername + user_name + textcolorWhite + "!")
                currentUserPassword = password


                time.sleep(3)
                clearConsole()
                consoleSize = 'mode 70, 35'
                os.system(consoleSize)
                print(programnameBanner)
                break
    if menuChoice == 2:
        model.load("model.tflearn")
        exit = 0
        debugMode = 1
        clearConsole()
        print("DEBUG MODE ACTIVE")
        print("------------------")
        print("")
        username_id = 6526
        user_name = "Debug"  
    if menuChoice == 3:
        clearConsole()
        def TrainingModelCreationV2():
            clearConsole()
            print(textcolorGreen + "Preparing to update the learning model!")
            time.sleep(2)
            updateTrainingModel()
        TrainingModelCreationV2()
    if menuChoice == 4:
        clearConsole()
        

        
    if exit == 0:
        if reboot == 0:
            enterPassword = False
            pwAction = ""
            while True:
                consoleSize = 'mode 70, 35'
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

                #USER CHAT
                
                if enterPassword == False:
                    userChat = input(textcolorUsername + user_name + ": " + textcolorWhite)
                    userChatCommand = str(userChat)
                if enterPassword == True:
                    passwordInput = pwinput.pwinput(prompt=textcolorWhite + "    Password: " + textcolorGray, mask='*')
                    if passwordInput == currentUserPassword:
                        passwordCorrect = True
                        enterPassword = False
                        if pwAction == "terminate":
                            clearConsole()
                            print(textcolorRed+"A.L.I.C.E is shutting down...")
                            time.sleep(2)
                            break
                            
                    if passwordInput != currentUserPassword:
                        passwordCorrect = False
                        enterPassword = False 
                        print(textcolorRed + "  --PASSWORD INCORRECT--" + textcolorWhite)
         
                # ADD TO TEXT LOG
                current_time = datetime.datetime.now()
                chatlogTime = current_time.strftime("%I:%M:%S %p")
                chatlog.append("("+ chatlogTime + ") - " + user_name + ": " + userChat)
                
                if userChat.lower() == "kiki":
                    baseCommands.testCommand()

                # Terminate
            
                # No response
                if userChat.lower() == "":
                    print("ALICE: No response given.")
           
                # Test message
                if userChat.lower() == "test message":
                    alicemessage = "Okay. Let's see if this new function is working."
                    DisplayandSpeak();

                #display ALICE's current stored message.
                if userChat.lower() == "alicemessage":
                    print(alicemessage)

                #BLACKBEAR protocol (sleep/hibernate)
                if userChat.lower() == "execute blackbear protocol":
                
                    if admin == 1:
                        alicemessage = "Enter password to execute the blackbear protocol."
                        DisplayandSpeak()
                        print()
                        if userChat.lower() == "password":
                            alicemessage = "blackbear protocol requested. executing in 3 seconds..."
                            DisplayandSpeak()
                            time.sleep(3)
                            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                            clearConsole()
                            print("ALICE: Welcome back!")
                    if admin == 0:
                        alicemessage = "You do not have the proper permissions"
                        DisplayandSpeak()
                        time.sleep(1)

                #Start a prediction
                results = model.predict([bag_of_words(userChat, words)])[0]
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

                    if labels[results_index] == "terminate":
                        chosen_response = random.choice(responses)
                        pwAction = "terminate"
                        enterPassword = True
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
                        mathString = userChat
                        map(int, re.findall(r'\d+', mathString))
                        [mathString]
                        print(mathString)

                    if labels[results_index] == "createfile":
                        print()                    
                        alicemessage = "What would you like to name the file?"
                        print(textcolorALICE + "ALICE: " + textcolorWhite + alicemessage)
                        engine.say(alicemessage)
                        engine.runAndWait()
                        print()
                        alicemessage = "Please include the file extension."
                        print(textcolorALICE + "ALICE: " + textcolorWhite + alicemessage)
                        engine.say(alicemessage)
                        engine.runAndWait()
                        print()
                        fileName = input(textcolorGray + "      file name: " + textcolorGreen)
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
                                print()
                                print(textcolorGray + "       location: " + textcolorGreen + fileFolder)
                                open(fileFolder, 'x')
                                systemValue = fileName
                                chosen_response = random.choice(responses)
                                errorMessage = False
                        
                            if fileExists == True:
                                errorMessage = True
                                errorCode = 1

                    if labels[results_index] == "createchatlog":    
                        current_time = datetime.datetime.now()
                        fileDate = current_time.strftime("%m%d%Y")
                        fileTime = current_time.strftime("%H%M")
                        fileFolder = "chatlogs"
                        chatlogStr = str(chatlogNum)
                        fileName = "chatlog_" + chatlogStr + fileTime + fileDate + ".txt"
                        fileFolder = (os.path.join(fileFolder, fileName))
                        fileExists = os.path.exists(fileFolder)
                        if not os.path.exists("chatlogs"):
                            os.makedirs("chatlogs")

                        if fileExists == False:
                            open(fileFolder, 'x')

                            output_file = open(fileFolder, 'w')

                            for chatlogitems in chatlog:
                                output_file.write(chatlogitems)
                                output_file.write("\n")
                            output_file.close()

                            chatlogNum = chatlogNum + 1

                            chatlogDisplay = (textcolorGray + "file name: " + textcolorGreen + fileName)
                            print(chatlogDisplay)
                            print()
                            chosen_response = random.choice(responses)

                            errorMessage = False                           
                        
                        if fileExists == True:
                            chatlogNum = chatlogNum + 1

                    if labels[results_index] == "createnewtrainingmodel":
                        chosen_response = random.choice(responses)
                        updateTrainingModel()

                    if labels[results_index] == "admininquiry":
                        if admin == 0:
                            systemValue = "Standard"
                        if admin == 1:
                            systemValue = "Administrator"

                        chosen_response = random.choice(responses)

                    chosen_response = random.choice(responses)

                    # System Data in response
                    if systemValue != "":
                        if errorMessage == False:
                            print()
                            print(textcolorALICE + "ALICE: " + textcolorWhite + chosen_response + textcolorGray + systemValue + textcolorWhite)
                            engine.say(chosen_response + systemValue)
                            engine.runAndWait()
                            current_time = datetime.datetime.now()
                            chatlogTime = current_time.strftime("%I:%M:%S %p")
                            chatlog.append("("+chatlogTime + ") - " + "ALICE: " + chosen_response + systemValue)

                        if errorMessage == True:
                            print()
                            print(textcolorRed + " An error has occurred! (00" + fileErrorCode + ")")
                            print(errorCodesList[errorCode])

                    # System Data is not in response
                    if systemValue == "":
                        if errorMessage == False:
                            current_time = datetime.datetime.now()
                            chatlogTime = current_time.strftime("%I:%M:%S %p")
                            chatlog.append("("+chatlogTime + ") - " + "ALICE: " + chosen_response)
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
                    current_time = datetime.datetime.now()
                    chatlogTime = current_time.strftime("%I:%M:%S %p")
                    print(textcolorALICE + "ALICE: I'm sorry, I don't understand.")
                    chatlog.append("("+chatlogTime + ") - " + "ALICE: I'm sorry, I don't understand.")
                    engine.say("I'm sorry, I don't understand.")
                    engine.runAndWait()


    # Exit the program
    if exit == 1:
        clearConsole()
        print("Exiting now...")
        time.sleep(3)

    


chat()
    

