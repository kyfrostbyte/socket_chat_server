# Overview
This program is a basic terminal chat application that uses a server-to-peer connection to allow for sending messages back and forth. I decided to build this project
so that I had a better understanding of how networks work behind the scenes. Although I have experiences with interacting with servers, it was predominantly on the client 
side. I wanted to understand what the server is doing to make it all possible. 

The program is pretty simple, and consists of just 2 files. In order to use it simply run the socket_server.py file, followed by the client.py file. When the client.py
file is ran, it will prompt the user for a username, and that will be their designated name for the chat session. You can run the client.py file in multiple terminals 
on the same computer if desired, or you could run them on separate computers as well. You will need to adjust the IP_address value in both the client and socket_server
to run on your own machine.  Open the CMD, run the 'ipconfig' command, and use the IPv4 address.

Once the server is started, it is constantly listening for connection attempts. Verification is given if a connection to a client has been established. When a client sends a message,
the server will then broadcast that message to the other clients.

When working on the project, I tested the server by connecting clients from the same computer, from different computers, and from a virtual machine. 
It all works fine, assuming each computer is on the same network. I believe some modifications would need to be made in terms of the IP address, and potentially editing some 
firewall settings in order to make it function across multiple networks.



[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

The program uses a client/server architecture. The server_socket is bound to a port and an IP address. Each socket can be considered as a mailbox, each IP is the location of the mailbox,
and the port describes the type of mail that goes in the mailbox. The server socket acts as a junction between the client sockets. Once it is running, the clients establish a connection via the designated port and IP.
Each time a client sends a message the information goes to the server, where it is then redirected to the other clients. This is a TCP connection, which works well with something like a chat application
where data integrity is crucial.

The format of each message consists of two parts: The header and the data. The header indicates the length of the data, so that the recipient can have an expectation of how many bytes it is.
Each message is encoded using UTF-8 to convert it to bytes prior to sending. Once it is received, it then will be decoded and the message can be displayed. This basically ensures that
the sender and receiver agree on the size of the message, which helps ensure that proper communication is occurring between the two parties.


# Development Environment

I built the program using python, inside the PyCharm IDE. The following libraries are used:

- socket 
- select
- sys
- threading
- datetime
- errno

The socket library is the biggest piece of the puzzle and provides the backbone for the program, and each other one plays a small role in 
improving the program in some way. For example, the threading library is used to prevent blocking from occurring, so that the clients can receive
messages in real time, without the need for refreshing via an input. The datetime library is used to place timestamps on incoming messages, and the errno
library is used for the error handling.

I also created a virtual machine using Virtual Box to experiment with communicating with clients that were not being run directly on the host computer.

# Useful Websites

* [Geeks for Geeks](https://www.geeksforgeeks.org/simple-chat-room-using-python/)
* [Python Programming](https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/)
* [Real Python](https://realpython.com/python-sockets/)
* [Virtual Box](https://www.virtualbox.org/)
* [Packt Pub](https://subscription.packtpub.com/book/cloud-and-networking/9781786463999/1/ch01lvl1sec15/writing-a-simple-tcp-echo-client-server-application)
* [Digital Ocean](https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client)

# Future Work

* Add command functionality for commands like \quit, \clients, \clear, etc
* Implement some sort of authentication for the clients, like a password to enter the chat
* Make it work with computers running on separate networks
* Implement a save chat feature which exports a .txt
* Add moderation controls for the server, with things like removing certain clients, or restricting certain types of messages
* Add a 'whisper' feature to directly message a specific person, instead of broadcasting to all clients
* Improve formatting in terminal to make it look more professional and legible 
* Connect to some sort of backend database to store chat history