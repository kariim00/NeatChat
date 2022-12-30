import argparse
import select
import socket
import threading
import hashlib

def send_message(sock):
    authenticated = False
    while not authenticated:
        message = input()
        if message == "/quit":
            sock.send(message.encode())
            sock.close()
            break
        elif message.startswith("/register"):
            # Parse the registration command
            _, username, password = message.split()
            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Send the registration command to the server
            sock.send(f"/register {username} {hashed_password}".encode())
            response = sock.recv(1024).decode()
            print(response)
        elif message.startswith("/login"):
            # Parse the login command
            _, entered_username, entered_password = message.split()
            # Hash the entered password
            hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
            # Send the login command to the server
            sock.send(f"/login {entered_username} {hashed_password}".encode())
            response = sock.recv(1024).decode()
            print(response)
        else:
            try:
                sock.send(message.encode())
            except:
                break
    active = True
    while active:
        message = input()
        if message == "/quit":
            sock.send(message.encode())
            sock.close()
            break
        else:
            try:
                sock.send(message.encode())
            except:
                break
def receive_message(sock):
    while True:
        try:
            data, _, _ = select.select([sock], [], [], 0.5)
            if data:
                message = sock.recv(1024).decode()
                print(message)
        except:
            break
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname")
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.hostname, args.port))

    send_thread = threading.Thread(target=send_message, args=(sock,))
    receive_thread = threading.Thread(target=receive_message, args=(sock,))
    send_thread.start()
    receive_thread.start()

if __name__ == "__main__":
    main()
