# Python program to implement server side of chat room.
import socket
import select
import sys
import time
'''Replace "thread" with "_thread" for python 3'''
from _thread import *
 
"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
 
# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])
 
# takes second argument from command prompt as port number
Port = int(sys.argv[2])
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, 8082))
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

print("IN SLEEP")
time.sleep(5)
# Client
server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.connect((IP_address, 8081))


print("OUT OF SLEEP")
 

 
list_of_clients = []
 
def clientthread(conn, addr):
 
    # sends a message to the client whose user object is conn
    string = "Welcome to this chatroom!"
    conn.send(string.encode('utf-8'))
 
    while True:
            try:
                # maintains a list of possible input streams
                sockets_list = [sys.stdin, server2]

                """ There are two possible input situations. Either the
                user wants to give manual input to send to other people,
                or the server is sending a message to be printed on the
                screen. Select returns from sockets_list, the stream that
                is reader for input. So for example, if the server wants
                to send a message, then the if condition will hold true
                below.If the user wants to send a message, the else
                condition will evaluate as true"""
                read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

                for socks in read_sockets:
                    if socks == server2:
                        client_message = socks.recv(2048)
                        print (client_message)
                    else:
                        client_message = sys.stdin.readline()
                        server2.send(client_message.encode('utf-8'))
                        sys.stdout.write("<You>")
                        sys.stdout.write(client_message)
                        sys.stdout.flush()
                server_message = conn.recv(2048)
                if server_message:
 
                    """prints the server_message and address of the
                    user who just sent the server_message on the server
                    terminal"""
                    print("<" + addr[0] + ">")
                    print(server_message.decode("utf-8"))
                    # print ("<" + addr[0] + "> " + server_message)
 
                    # Calls broadcast function to send server_message to all
                    message_to_send = "<" + addr[0] + "> " + server_message
                    broadcast(message_to_send, conn)
 
                else:
                    """server_message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)
 
            except:
                continue
 
"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
 
                # if the link is broken, we remove the client
                remove(clients)
 
"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
 
while True:
 
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    conn, addr = server.accept()
    
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)
 
    # prints the address of the user that just connected
    print (addr[0] + " connected")
 
    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread,(conn,addr))    
 
conn.close()
server.close()