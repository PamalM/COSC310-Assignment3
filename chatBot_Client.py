from tkinter import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import chatbot
import socket

def openConnection(host, port):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    #Recieve message buffer from server.
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
    
    #Create a GUI using tkinter library, to implement chatbox.
    root = Tk()
    #GUI Attributes for window.
    root.title("Python Chatbot")
    root.resizable('False', 'False')
    root.configure(background="Slate blue")
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
    chatLabel = Label(root, text=f"HOST IP:{host} -- PORT#: {port} ", bg="yellow2", fg="#88324f", font='Helvetica 20 bold')
    chatLabel.place(x=10, y=40)

    #Widgets of the tkinter window.
    userMessage = StringVar()
    userTextBox = Entry(root, bg="thistle1", textvariable=userMessage, width=30)
    userTextBox.place(x = 120, y = 400)
    userTextBox.focus()

    #Output the chat start time/date when chat window loads up.
    chatbot.displayDateTime(1)

    def interact():

        #Get user input from textbox. 
        request = chatbot.bot.get_response("Hey!")
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

    #Button for user to send their message from textbox to chatbot. 
    sendButton = Button(root, text="Send", font='Helvetica 20 bold', command = lambda: interact())
    sendButton.place(x=420, y=400)

    #Keep window running until otherwise. 
    root.mainloop()
