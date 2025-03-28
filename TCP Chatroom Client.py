import socket
import threading
import time

SERVER_IP = 'localhost'
SERVER_PORT = 9999

stop_flag = threading.Event()

# If error() occurs, or 'exit' returns from server, disconnect server and exit
def receive():
    while not stop_flag.is_set():
        try:
            message = client.recv(1024).decode()  # Receive message from the server
            if message == 'exit':
                print("Server has closed the connection.")
                stop_flag.set()  # Set stop flag to end the loop
            else:
                print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            stop_flag.set()

if __name__ == '__main__':

    nickname = input('Choose your nickname: ')

    # Create a socket object for client service
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client.connect((SERVER_IP, SERVER_PORT))

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        while True:
            time.sleep(0.05)
            message = input('>> ')
            if message.lower() == 'exit':
                client.send(message.encode())  # Send 'exit' message to server
                client.close()
                stop_flag.set()
                receive_thread.join()
                break
            else:
                client.send(f'{nickname} says: {message}'.encode())  # Send message to server

    except Exception as e:
        print(f"Error connecting to the server: {e}")
        stop_flag.set()

