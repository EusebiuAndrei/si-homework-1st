import socket
import select

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}
nodes = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, excepetion_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            nodes[user['data']] = client_socket
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            node = receive_message(notified_socket)
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del nodes[clients[notified_socket]['data']]
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data']}")

            if node['data'] in nodes:
                print(f"Message for {node['data']}, ook: {node['data'] in nodes}")
                # nodes[node['data']].send(user['header'] + user['data'] + message['header'] + message['data'])
                print(node, user, message)
                nodes[node['data']].send(user['header'])
                nodes[node['data']].send(user['data'])
                nodes[node['data']].send(message['header'])
                nodes[node['data']].send(message['data'])
            else:
                print(f"Message for {node['data']}, ook: {node['data'] in nodes}")
                user = "Server".encode('utf-8')
                user_header = f"{len(user):<{HEADER_LENGTH}}".encode('utf-8')
                message = f"The node {node['data']} is not connected".encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                notified_socket.send(user_header + user + message_header + message)

            # for client_socket in clients:
            #     if client_socket != notified_socket:
            #         client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in excepetion_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        del nodes[clients[notified_socket]['data']]

