# Neat Chat

This is a command-line chat app written in Python using sockets and SQLAlchemy. It allows users to register, login, join chat channels, and send and receive messages.

## Features

- User registration and login
- Hashing of passwords using SHA256
- Chat channels
- Persistence of user details and messages using SQLAlchemy and a SQLite database

## Requirements
```sh
pip -r requirements.txt
```

## Usage

### Server

To start the server, run the following command:

```sh
python server.py <hostname> <port>
```

Replace `<hostname>` with the hostname or IP address to bind the server to, and `<port>` with the port number to listen on.

### Client

To start the client, run the following command:


Replace `<hostname>` with the hostname or IP address of the server, and `<port>` with the port number the server is listening on.

## Commands

The following commands are supported by the chat app:

- ```/register <username> <password>```: Register a new user with the given username and password.
- ```/login <username> <password>```: Login with the given username and password.
- ```/join <channel>```: Join the specified chat channel.
- ```/leave```: Leave the current chat channel.
