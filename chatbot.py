from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from datetime import datetime
from chatterbot import ChatBot
from tkinter import *
import logging
import random
import os

import chatBot_Client
import chatBot_Server
    
def connect():
    #Method presents GUI for user to connect to host/port and/or recieve connection.
    global main
    global userPort
    global userHost
    main = Tk()

    hostLabel = Label(main, text="HOST:", bg="#88324f", fg="ghost white", font='Helvetica 20 bold')
    portLabel = Label(main, text="PORT:", bg="#88324f", fg="ghost white", font='Helvetica 20 bold')
    hostLabel.place(x= 138, y= 180)
    portLabel.place(x= 138, y= 260)

    label1 = Label(main, text="Recieve connection from external Chat Agent.", font="Helvetica 12 bold", fg="slate blue", bg="ghost white")
    label1.place(x= 50, y=20)

    label2 = Label(main, text="Connect to external connection", font="Helvetica 12 bold", fg="slate blue", bg="ghost white")
    label2.place(x= 82, y=130)

    userHost = StringVar()
    userHostBox = Entry(main, bg="thistle1", textvariable=userHost, width=14)
    userHostBox.place(x = 108, y = 210)

    userPort = int()
    userPortBox = Entry(main, bg="thistle1", textvariable=userPort, width=14)
    userPortBox.place(x = 108, y = 290)

    def recieve(tag):
        root.destroy()
        if tag == 1:
            #Stays open and infinetly searches for any incoming connections.
            chatBot_Server.connect()

    def connection():
        #Attempt to create new connection with the specified credentials [Host/Port].
        host = userHostBox.get()
        port = userPortBox.get()
        chatBot_Client.openConnection(host, int(port))
        root.destroy()
        main.destroy()

    #Button opens up and searches for avaliable external connections.
    recieveButton = Button(main, text="Recieve Connection", font='Helvetica 16 bold', command = lambda: recieve(1))
    recieveButton.place(x=100, y=50)

    #Button opens up and searches for avaliable external connections.
    connectButton = Button(main, text="Search Connection", font='Helvetica 16 bold', command = lambda: connection())
    connectButton.place(x=102, y=350)

    main.title("Connect to chat: ")
    main.geometry("350x450")
    main.resizable('False', 'False')
    main.mainloop()

#Create and start the GUI presentation to the user.
def startGUI():

    #Global attributes.
    global root
    global txtOutput

    #Method resets the chatbot once chat ends.
    def restartChat():
        root.destroy()
        startGUI()

    #Create a GUI using tkinter library, to implement chatbox.
    root = Tk()

    #GUI Attributes for window.
    root.title("Python Chatbot")
    root.resizable('False', 'False')
    root.configure(background="#88324f")
    root.geometry("500x450")

    #Main ChatBox Output window. (Big text field in middle of GUI; with scroll-bar).
    txtFrame = Frame(root, borderwidth=1, relief="sunken")
    txtOutput = Text(txtFrame, wrap = NONE, height = 20, width = 65, borderwidth=0, font='Helvetica 12 bold')
    vscroll = Scrollbar(txtFrame, orient=VERTICAL, command=txtOutput.yview)
    txtOutput['yscroll'] = vscroll.set
    vscroll.pack(side="right", fill="y")
    txtOutput.pack(side="left", fill="both", expand=True)
    txtFrame.place(x=10, y=75)

    #Text label to the left of the user message Entry() box.
    messageLabel = Label(root, text="Message:", bg="#88324f", fg="ghost white", font='Helvetica 20 bold')
    messageLabel.place(x=10, y=400)

    #Chat label to the top left of main chat text box.
    chatLabel = Label(root, text="Chat Overview: ", bg="yellow2", fg="#88324f", font='Helvetica 20 bold')
    chatLabel.place(x=10, y=40)

    #Widgets of the tkinter window.
    userMessage = StringVar()
    userTextBox = Entry(root, bg="thistle1", textvariable=userMessage, width=30)
    userTextBox.place(x = 120, y = 400)
    userTextBox.focus()

    #Output the chat start time/date when chat window loads up.
    displayDateTime(1)

    #Method utilized to send user message to bot, and print it to the main chatbox text window.
    def interact():

        #Get user input from textbox. 
        request = userMessage.get()
        userMessage.set("")

        #Color coordinate user/bot responses.
        txtOutput.tag_config('bot', background="mediumpurple1", foreground="white")
        txtOutput.tag_config('user', background="peach puff", foreground="black")

        def printUser():
            #Print user's input to main text box.
            txtOutput.config(state="normal")
            txtOutput.insert(INSERT,("You:    " + request + "\n"), 'user')
            txtOutput.insert(INSERT,"\n")
            txtOutput.config(state="disabled")

        def printBot():
            #Get bot's response for the user request.
            response = bot.get_response(request)
            #If the bot has a response print it.
            if str(response) != "":
                txtOutput.config(state="normal")
                txtOutput.insert(INSERT,("ChatBot:    " + str(response) + "\n"), 'bot')
                txtOutput.insert(INSERT,"\n")
                txtOutput.config(state="disabled")

            #Otherwise, print [1/5] responses. **FEATURE WORTH 3Pts**
            #When user enters something outside of topic range. 
            else:
                dResponse = ["Didn't quite catch that! Could you repeat it?", "I didn't understand your last message :(",
                             "Lets switch the topic!", "What's your social security number?", "Do you have a favourite sports team?",
                             "When is your birthday?"]

                txtOutput.config(state="normal")
                txtOutput.insert(INSERT,("ChatBot:    " + random.choice(dResponse) + "\n"), 'bot')
                txtOutput.insert(INSERT,"\n")
                txtOutput.config(state="disabled")
                

        if request.lower() == "bye" or request.lower() == "goodbye":
                printUser()
                printBot()
                displayDateTime(2)

                #Disable user entry view to eliminate more messages from being sent after chat end.
                userTextBox.delete(0, 'end')
                userTextBox.insert(INSERT,"Chat Ended!")
                userTextBox['state'] = 'disabled'
                sendButton['state'] = 'disabled'

                #Make button visible to start new chat.
                restartButton.place(x=390, y=40)
                return 0

        else:
            #Else, conversation continues as normal. Proceed with printing user message, and bot's response.
            printUser()
            printBot()

    #Button for user to send their message from textbox to chatbot. 
    sendButton = Button(root, text="Send", font='Helvetica 20 bold', command = lambda: interact())
    sendButton.place(x=420, y=400)

    #Button that starts a new chat in python; Only visible upon chat end.
    restartButton = Button(root, text="New Chat!", font='Helvetica 18 bold', command = lambda: restartChat())

    #Button opens new GUI window to conduct socket programming with another chat agent. 
    socketChatButton = Button(root, text="Socket Chat", font='Helvetica 18 bold', command = lambda: connect())
    socketChatButton.place(x=220, y=40)

    #Keep window running until otherwise. 
    root.mainloop()    

def displayDateTime(tag):

    #Method returns the current date/time.
    #This information will be outputted to the user to determine chat start/end times/dates.
    #Tag 1 = Start Chat, Tag 2 = End chat.
    
    #Fetch current month.
    month = datetime.now().month

    #Fetch current day.
    day = datetime.now().day

    #Fetch current year.
    year = datetime.now().year

    #Fetch current hour.
    hour = datetime.now().hour

    #Fetch current minute.
    minute = datetime.now().minute

    #Utilizing a python dictionary to hold month according to their digit key. 
    months = {1: "Jan",
                2: "Feb",
                3: "March",
                4: "April",
                5: "May",
                6: "June",
                7: "July",
                8: "Aug",
                9: "Sep",
                10: "Oct",
                11: "Nov",
                12: "Dec"}

    #Utilizing a python dictionary to hold hours according to their 24 - Format.
    #Utilizing this dictionary to convert the 24hr time format to 12 for output. 
    formatHour = {0 : 12,
                  1 : 1,
                  2 : 2,
                  3 : 3,
                  4 : 4,
                  5 : 5,
                  6 : 6,
                  7 : 7,
                  8 : 8,
                  9 : 9,
                  10 : 10,
                  11 : 11,
                  12 : 12,
                  13 : 1,
                  14 : 2,
                  15 : 3,
                  16 : 4,
                  17 : 5,
                  18 : 6,
                  19: 7,
                  20 : 8,
                  21 : 9,
                  22 : 10,
                  23 : 11}
    #Dictionary utilized to convert the minute and maintain its string type.
    formatMinute = {1 : "01",
                    2 : "02",
                    3 : "03",
                    4 : "04",
                    5 : "05",
                    6 : "06",
                    7 : "07",
                    8 : "08",
                    9 : "09",
                    10 : "10",
                    11 : "11",
                    12 : "12",
                    13 : "13",
                    14 : "14",
                    15 : "15",
                    16 : "16",
                    17 : "17",
                    18 : "18",
                    19 : "19",
                    20 : "20",
                    21 : "21",
                    22 : "22",
                    23 : "23",
                    24 : "24",
                    25 : "25",
                    26 : "26",
                    27 : "27",
                    28 : "28",
                    29 : "29",
                    30 : "30",
                    31 : "31",
                    32 : "32",
                    33 : "33",
                    34 : "34",
                    35 : "35",
                    36 : "36",
                    37 : "37",
                    38 : "38",
                    39 : "39",
                    40 : "40",
                    41 : "41",
                    42 : "42",
                    43 : "43",
                    44 : "44",
                    45 : "45",
                    46 : "46",
                    47 : "47",
                    48 : "48",
                    49 : "49",
                    50 : "50",
                    51 : "51",
                    52 : "52",
                    53 : "53",
                    54 : "54",
                    55 : "55",
                    56 : "56",
                    57 : "57",
                    58 : "58",
                    59 : "59",
                    00 : "00"}
    
    #Determine AM/PM indicator; depending on hour.
    timeOfDay = ""
    if (hour >= 0 and hour <= 11):
        timeOfDay = "AM"
    else:
        timeOfDay = "PM"
        
    if (tag == 1):
        #Determine the date/time @ which the chat was started.
        output = "Chat Started on " + months[month] + "/" + str(day) + "/" + str(year) + " @ " + str(formatHour[hour]) + ":" + str(formatMinute[minute]) + " " + timeOfDay + "\n"

    elif (tag == 2):
        #Determine the date/time @ which the chat was ended.
        output = "Chat Ended on " + months[month] + "/" + str(day) + "/" + str(year) + " @ " + str(formatHour[hour]) + ":" + str(formatMinute[minute]) + " " + timeOfDay + "\n"

    txtOutput.tag_config('date/time', background="indian red", foreground="yellow")
    txtOutput.config(state="normal")
    txtOutput.insert(INSERT,(output), 'date/time')
    txtOutput.insert(INSERT,"\n")
    txtOutput.config(state="disabled")

#Set logging level to 'CRITICAL' to remove some non-related warning outputs to the terminal.
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

print("---------------------------------------------------")
print("[Initializing Chatbox ...]")

#Initiate a chatbot object.
bot = ChatBot('Friend')

#Set the trainers for the bot.
'''
trainer = ListTrainer(bot)
corpus_trainer = ChatterBotCorpusTrainer(bot)

#current_Minute = datetime.now().minute
#current_Second = datetime.now().second

#Train using a specified corpus.
corpus_trainer.train('chatterbot.corpus.english')

#Open datasets to train the bot.
with open('Data/chats.txt', 'r') as file:
    data = file.readlines()
    trainer.train(data)

'''

print("[Chatbox Initiation Complete!]")
print("---------------------------------------------------")

#Create and start the GUI window when chatbot initalization completes.
startGUI()
