import socket
import pickle
import threading
import sys
import time
import pdb


#TODO
#   1. fix synchronization between recv & send state || Done
#   2. Fix issue where the socket doens't close


#Server properties
IP = 'localhost' #    --> thanathos.hopto.org
PORT = 5555
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
serverSocket.bind((IP, PORT))
serverSocket.listen()


#keep track of all active sockets
socketList = []

#   --> Try to receive data, if it fails, close the socket, remove socket from list
def recv(c):
    try:
        data = pickle.loads(c.recv(4096))
    except OSError as e:
        print(e)
        print("Didn't get anything from", + c)
        c.close()
        socketList.remove(c)

    return data



#   --> Send function, checks if the length of the socketList is greater or equal
#       to 1. gets input from a user and sends it off to all current connections
#       in the socketList using the pickle module. Calls for a receive with said socket
def send():
    
    while len(socketList) >= 1:
        command = input(">> ")

        #In case of quit, close client and server socket in a timely manner
        if command == "quit":
            for c in socketList:
                try:
                    c.send(pickle.dumps("quit"))
                except OSError as e:
                    print(e)
            
            for c in socketList:
                print("Closing sockets...")
                c.close() #Close the client sockets
                time.sleep(1)
            print("Closing Server socket...")
            serverSocket.close() #Close the server socket
            print(socketList[0], "\n", serverSocket)
            time.sleep(3)
            sys.exit()

        try:
            
            for c in socketList:
                c.send(pickle.dumps(command))
            #socketList[-1].send(pickle.dumps(command))

        except Exception as e:
            #socketList[-1].close()
            print(e)
            continue

        #Call for the recv function for every socket in socketList
        for c in socketList:
            print(recv(c))


#        recv(socketList[-1])


#   --> Accept incomming socket connections on a thread
#       Append the socket to the socketList
def connect():
    print("Listening for connections...")
    while True:
        try:
            c, a = serverSocket.accept()
            socketList.append(c)

        except Exception as e:
            print(e)



        if len(socketList) > 0:
            print(socketList[-1])

def main():

    threadSocket = threading.Thread(target=connect, args=(), daemon=True)
    threadSocket.start() #Start connect function on a thread

    while True:
        send() #Calls for a recv after sending

main()
