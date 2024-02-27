import socket
import sys
import threading
from datetime import datetime
import errno

# Define IP, port, and header length
IP_address = "192.168.56.1"
port = 1234
HEADER_LENGTH = 10

client_username = input("Enter your username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_address, port))
client_socket.setblocking(False)
username = client_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# Function to handle user input and send messages
def send_message():
    while True:
        message = input(f"{client_username} > ")

        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

# Start the sending thread
send_thread = threading.Thread(target=send_message)
send_thread.daemon = True
send_thread.start()

# Control flag for printing prompt
print_prompt = True

# Receive messages in the main thread
while True:
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            # Handle error with message
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            timestamp = datetime.now().strftime("%I:%M %p")

            # Clear the line and print received messages
            print('\r\033[K', end='')
            print(f"{username} at {timestamp}: {message}")

            # Set flag to print prompt after processing messages
            print_prompt = True

            # Print input prompt if the flag is set
            if print_prompt:
                print(f"\r{client_username} > ", end='', flush=True)
                print_prompt = False

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading Error', str(e))
            sys.exit()

    except Exception as e:
        print('General Error', str(e))
        sys.exit()