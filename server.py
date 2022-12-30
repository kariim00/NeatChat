import argparse
import select
import socket
import threading
import hashlib
import db

clients = []

def handle_client(sock, address, channels):
    clients.append(sock)
    authenticated = False
    using = True
    username = None
    current_channel = None
    while not authenticated:
        try:
            data, _, _ = select.select([sock], [], [], 0.5)
        except select.error:
            print(f"{address} closed connection")
            clients.remove(sock)
            break
        if data:
            try:
                message = sock.recv(1024).decode()            
                if message.startswith("/register"):
                    # Parse the registration command
                    try:
                        _, username, password = message.split()
                        # Hash the password
                        hashed_password = hashlib.sha256(password.encode()).hexdigest()
                        
                        if db.username_taken(username):
                            sock.send("Can't register that one sorry.".encode())
                        else :
                            db.add_user(username, hashed_password)
                            sock.send("Registration successful".encode())
                    except Exception as e:
                        print(e)
                        sock.send("Please send the message in the following format /register username password".encode())
                elif message.startswith("/login"):
                    try:
                        # Parse the login command
                        _, entered_username, entered_password = message.split()
                        # Hash the password
                        entered_password = hashlib.sha256(entered_password.encode()).hexdigest()
                        # Retrieve the stored hashed password from the database
                        stored_password = db.get_user_password(entered_username)
                        if stored_password is None:
                            sock.send("Username not found".encode())
                        else:
                            # Check if the entered password is correct
                            if hashlib.sha256(entered_password.encode()).hexdigest() == stored_password:
                                authenticated = True
                                username = entered_username
                                sock.send("Login successful".encode())
                            else:
                                sock.send("Incorrect password".encode())
                    except Exception as e:
                        print(e)
                        sock.send("Please send the message in the following format /login username password".encode())
                else:
                    sock.send("Please login first.".encode())
            except:
                print(f"{address} closed connection")
                clients.remove(sock)
                using = False
                break
    
    while using:
        try:
            data, _, _ = select.select([sock], [], [], 0.5)
        except select.error:
            print(f"{address} closed connection")
            clients.remove(sock)
            break
        if data:
            try:
                message = sock.recv(1024).decode()            
                # Send the message to all other connected clients
                if message == "" or message == "/quit":
                    print(f"{address} closed connection")
                    clients.remove(sock)
                    break       
                elif message.startswith("/join"):
                    # Parse the join command
                    _, channel_name = message.split()
                    # Check if the channel exists
                    if channel_name not in channels:
                        sock.send(f"Error: channel {channel_name} does not exist".encode())
                    else:
                        # Leave the current channel (if any)
                        if current_channel is not None:
                            channels[current_channel].remove(sock)
                        # Join the new channel
                        current_channel = channel_name
                        channels[current_channel].append(sock)
                        sock.send(f"Successfully joined channel {channel_name}".encode())
                
                elif message.startswith("/leave"):
                    # Leave the current channel (if any)
                    if current_channel is not None:
                        for client in channels[current_channel]:
                            if client != sock:
                                client.send(f"{username}@{current_channel} left the chat.".encode())
                        channels[current_channel].remove(sock)
                        current_channel = None
                        sock.send(f"Successfully left channel".encode())
                        
                    else:
                        sock.send("Error: not currently in a channel".encode())
                elif message.startswith("/create"):
                    # Parse the join command
                    _, channel_name = message.split()
                    # Check if the channel exists
                    if channel_name in channels:
                        sock.send(f"Error: channel {channel_name} already exists".encode())
                    else:
                        # Create the new channel
                        channels[channel_name] = []
                        sock.send(f"Successfully created channel {channel_name}".encode())

                else:    
                    if current_channel == None:
                        sock.send("Error: please join a channel to participate".encode())
                    else:
                        for client in channels[current_channel]:
                            if client != sock:
                                client.send(f"{username}@{current_channel}: {message}".encode())
            except Exception as e:
                print(f"exception is {e}")
                print(f"{address} closed connection")
                clients.remove(sock)
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname")
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    # Initialize the channels dictionary
    channels = {}
    channels["General"] = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.hostname, args.port))
    sock.listen(5)

    while True:
        client, address = sock.accept()
        print(f"{address} connected")
        thread = threading.Thread(target=handle_client, args=(client, address, channels))
        thread.start()

if __name__ == "__main__":
    main()
