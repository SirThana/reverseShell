import socket
import pickle
import threading
import sys
import pdb

#TODO
#   1. fix synchronization between recv & send state || Done!


#Server properties
IP = '192.168.178.60'
PORT = 7777
socket = socket.socket()
socket.bind((IP, PORT))
socket.listen()


#Socket list
socketList = []


def recv(c):
    global socketList
    try:
        data = pickle.loads(c.recv(4096))
        print(data)
    except:
        c.close()
        print("Didn't get shit")
        sys.exit()

def send():
    
    while True:
        for socket in socketList:
            try:
                command = input(">> ")
                command = str(command)
                socket.send(pickle.dumps(command))

            except Exception as e:
                socket.close()
                print(e)

            recv(socket)


#Accept incomming socket connections on a thread
def connect(x, p):
    global socket
    global socketList
    print("thread started")
    while True:
        try:
            c, a = socket.accept()
            socketList.append(c)

        except Exception as e:
            print(e)



        if len(socketList) > 0:
            print(socketList[-1])

def main():

    threadSocket = threading.Thread(target=connect, args=(0, 1), daemon=True)
    threadSocket.start()


    while True:
        send()

    """
    while True:
        for clientSocket in socketList:
            send(clientSocket)
    """

main()
