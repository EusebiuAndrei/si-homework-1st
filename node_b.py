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

my_username = 'B'
MODE = ''
KEY = ''
cyphertext = []
nr_of_blocks = -1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# log in with username B
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# start communicating
start_communicating = False
while nr_of_blocks != 0:
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

                node = 'A'
                node = node.encode('utf-8')
                node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(node_header)
                client_socket.send(node)

                message = 'The communication can start!'
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header)
                client_socket.send(message)

                start_communicating = True

                print(f"{username} > {KEY}")

            if username == 'A':
                if start_communicating is False:
                    message = message.decode('utf-8')
                    MODE = message
                    send_mode('K', MODE)
                # here starts communicating
                else:
                    if nr_of_blocks == -1:
                        nr_of_blocks = int(message.decode('utf-8').strip())
                    else:
                        cyphertext.append(message)
                        nr_of_blocks -= 1

                print(f"{username} > {message}")


    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()

plaintext = ''
if MODE == 'ECB':
    plaintext = si.ecb_decrypt(cyphertext, KEY.encode('utf-8'))
else:
    plaintext = si.ofb_decrypt(cyphertext, KEY.encode('utf-8'))
print(f"Textul primit decriptat este: {plaintext}")
