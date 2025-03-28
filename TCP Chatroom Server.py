import socket
import threading
import time

SERVER_IP = 'localhost'
SERVER_PORT = 9999

stop_flag = threading.Event()

# manage client's hosts and chatroom users
clients = []            # client's connections list
nicknames = []          # chatroom users list

# remove terminating clients and users, return resources to O.S.
def clean(client):
    index = clients.index(client)
    clients.remove(client)
    nickname = nicknames[index]
    broadcast(f'{nickname} left the chat!'.encode())
    nicknames.remove(nickname)
    client.close()
    print(f'We have {len(clients)} guests')

# broadcast all messages and notifications to every client
def broadcast(message):
    for client in clients:
        try:
            client.send(message)  # send the message to all clients
        except:
            clean(client)  # if there's an error, clean the client

# handle server connections
def server_handle(client):
    while not stop_flag.is_set():
        try:
            message = client.recv(1024).decode()  # receive message from client
            if message.lower() == 'exit':
                clean(client)
                break
            else:
                broadcast(message.encode())  # broadcast the received message
        except Exception as e:
            print(f"Error: {e}")
            clean(client)
            break

if __name__ == '__main__':
    finish = False
    # create a socket object for server and wait for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    print(f"Server started on {SERVER_IP}:{SERVER_PORT}...")
    
    while True:
        # accept incoming connections
        client_conn, client_addr = server_socket.accept()
        print(f"New connection from {client_addr}")
        
        # ask for client's nickname
        client_conn.send("Please enter your nickname:".encode())
        nickname = client_conn.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client_conn)
        
        # notify all clients about the new user
        broadcast(f'{nickname} joined the chat!'.encode())
        
        # start a new thread to handle the client's communication
        thread = threading.Thread(target=server_handle, args=(client_conn,))
        thread.start()
