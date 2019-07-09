import socket
import pickle
import threading
import sys
import time

#TODO
#   1. fix synchronization between recv & send state || Done


#Server properties
IP = '' #    --> thanathos.hopto.org
PORT = 6666
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
socket.bind((IP, PORT))
socket.listen()


#keep track of all active sockets
socketList = []

#   --> Try to receive data, if it fails, close the socket
def recv(c):
    try:
        data = pickle.loads(c.recv(4096))
        print(data)
    except:
        c.close()
        print("Didn't get anything")
        sys.exit()


#   --> Send function, checks if the length of the socketList is greater or equal
#       to 1. gets input from a user and sends it off to the most recent connection
#       in the socketList using the pickle module. Calls for a receive with said socket
def send():
    
    if len(socketList) >= 1:
        while True:
            try:
                command = input(">> ")
                if command == "quit":

                    for c in socketList:
                        c.close()

                    socket.close()
                    time.sleep(10)
                    sys.close()

                socketList[-1].send(pickle.dumps(command))

            except Exception as e:
                socketList[-1].close()
                print(e)

            recv(socketList[-1])


#   --> Accept incomming socket connections on a thread
#       Append the socket to the socketList
def connect():
    print("Listening for connections...")
    while True:
        try:
            c, a = socket.accept()
            socketList.append(c)

        except Exception as e:
            print(e)



        if len(socketList) > 0:
            print(socketList[-1])

def main():

    threadSocket = threading.Thread(target=connect, args=(), daemon=True)
    threadSocket.start()


    while True:
        send() #Calls for a recv after sending

main()
