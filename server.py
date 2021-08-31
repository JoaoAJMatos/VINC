import socket
import termcolor

HOST = '127.0.0.1'
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

print(termcolor.colored(f'[+] Server listening on port [{PORT}] for incoming connections', 'green'))

sock.listen(5)

target, ip = sock.accept()
print(termcolor.colored(f'[+] Connection astablished with [{str(ip[0])}] port [{str(ip[1])}]!', 'green'))