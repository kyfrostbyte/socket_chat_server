import socket
import select

# Define IP, port, and header length
IP_address = "192.168.56.1"
port = 1234
HEADER_LENGTH = 10

# Create an instance of the socket and set correct attributes
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP_address, port))

# Instruct the server to be prepared to accept client connection requests
server_socket.listen()
print(f"Now listening on: {IP_address}")

# Creates a list to manage the all sockets (server + each client)
sockets_list = [server_socket]

# Create a dictionary to contain client information. Key = client socket, value = userdata
clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        # Handle no data errors
        if not len(message_header):
            return False

        # If data is good, return the message
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    # Handle unexpected errors
    except:
        print("Bad message")
        return False


# Server Logic
while True:
    # Parameters are sockets that need to read from, written to, and potential errors
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for socket in read_sockets:
        # Handle new connections
        if socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)

            # Handle user disconnect
            if user is False:
                continue

            # Add new connections to socket list and client dictionary
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(
                f"Accepted new connection from: {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        # Handle data from existing connections
        else:
            message = receive_message(socket)

            # If user disconnects, remove user from socket_list
            if message is False:
                print(f"Connection closed from {clients[socket]['data'].decode('utf-8')}")
                sockets_list.remove(socket)
                del clients[socket]
                continue

            user = clients[socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                # For all users that are not the user that sent the message, send them the message
                if client_socket != socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # Handle sockets that throw an error
    for socket in exception_sockets:
        sockets_list.remove(socket)
        del clients[socket]
