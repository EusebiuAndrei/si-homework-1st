import socket
import select
import errno
import sys

import si


def send_mode(node, message):
    node = node.encode('utf-8')
    node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(node_header)
    client_socket.send(node)

    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header)
    client_socket.send(message)


HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

my_username = 'A'
MODE = ''
KEY = ''

while MODE != 'ECB' and MODE != 'OFB':
    MODE = input("Select the aes mode: ").upper()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# log in with username A
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# send messages to B and K
send_mode('B', MODE)
send_mode('K', MODE)

# start communicating
start_communicating = False
while start_communicating is False:
    message = input(f"{my_username} > ")

    if message:
        node = message[0]
        message = message[2:]

        node = node.encode('utf-8')
        node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(node_header)
        client_socket.send(node)

        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header)
        client_socket.send(message)

    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username):
                print("Connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length)

            if username == 'K':
                KEY = si.aes_basic_decrypt(message, si.key).decode('utf-8')
                print(f"{username} > {KEY}")

            if username == 'B':
                start_communicating = True
                print(f"{username} > {message.decode('utf-8')}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()

# here starts communicating
plaintext = input("Send text safely: ")
if plaintext.lower() == 'file':
    f = open("demo.txt", "r")
    plaintext = f.read()

cyphertext = ''
if MODE == 'ECB':
    cyphertext = si.ecb_encrypt(plaintext.encode('utf-8'), KEY.encode('utf-8'))
else:
    cyphertext = si.ofb_encrypt(plaintext.encode('utf-8'), KEY.encode('utf-8'))

node = 'B'.encode('utf-8')
node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(node_header)
client_socket.send(node)

message = f"{len(cyphertext)}".encode('utf-8')
message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(message_header)
client_socket.send(message)

for block in cyphertext:
    node = 'B'.encode('utf-8')
    node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(node_header)
    client_socket.send(node)

    message = block
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header)
    client_socket.send(message)
