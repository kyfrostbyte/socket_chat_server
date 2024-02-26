import socket
import sys
import threading

IP_address = "10.200.189.117"
Port = 20505

# Connect to the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receive_messages():
    while True:
        try:
            message = server.recv(2048)
            if not message:
                print("Connection to the server closed.")
                sys.exit()
            print(f"Received message: {message.decode()}")
        except socket.error as e:
            # Handle socket errors if needed
            print(f"Socket error: {e}")
            sys.exit()


try:
    server.connect((IP_address, Port))
except Exception as e:
    print(f"Unable to connect to the server: {e}")
    sys.exit()

print("Connected to the server. You can start typing messages.")

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Main loop for sending messages
while True:
    try:
        message = input()
        server.send(message.encode())
    except KeyboardInterrupt:
        print("Client disconnected.")
        server.close()
        sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
