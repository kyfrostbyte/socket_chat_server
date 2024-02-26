import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = "10.200.189.117"
Port = 20505

server.bind((IP_address, Port))
server.listen(5)

sockets_list = [server]
clients = {}

print(f"Server listening on {IP_address}:{Port}")

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            client_socket, client_address = server.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Client {client_address} connected")
        else:
            try:
                message = socks.recv(2048)
                if message:
                    print(f"Received message from {clients[socks]}: {message.decode()}")
            except:
                print(f"Client {clients[socks]} disconnected")
                socks.close()
                sockets_list.remove(socks)
                del clients[socks]
