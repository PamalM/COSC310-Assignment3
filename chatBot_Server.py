import socket

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Specific port for our connection.
    #Creates a connection @ HOST IP: 0.0.0.0, and PORT #: 1234.
    s.bind(('0.0.0.0', 1234))

    #Max. queue of 5 clients @ a time.
    s.listen(5)

    #Listen forever for connections.
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")

        get = clientsocket.recv(1024)
        
        print(f"Recieved: '{get.decode('utf-8')} from {address}'")
        
        #Send information to client socket object.
        clientsocket.send(bytes(bot.get_response(get), "utf-8"))


