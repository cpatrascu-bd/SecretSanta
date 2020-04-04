#! python3.8

import socket
import json
import os
import hashlib
from datetime import datetime
from _thread import *

# Global values
SUCCESS = 1
FAIL = 0

# File specific declarations
CREDS_FILE = './utilizatori.json'
EMAIL_SCRIPT = './script.py'
GROUPS = './groups/'
TEMPLATES = './templates/'

# Socket specific declarations
MAX_BUFFER = 4096
MAX_CLIENTS = 10
HOST = '127.0.0.1'
PORT = 9001
sock = socket.socket()

# Data kept in the program's memory
tokens = {}


def init():
    # Put the socket to listen for MAX_CLIENTS connections at the same time
    try:
        sock.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))

    sock.listen(MAX_CLIENTS)


def generate_token(username, userhash):
    # Generate a unique token based on username and password hash. Adding a date string for security reasons
    m = hashlib.sha256()
    m.update("".join([username, str(datetime.now()), userhash]).encode('utf-8'))
    return m.hexdigest()


def update_file(file, data):
    # Update a json file by either initializing or appending data to it
    if not os.path.isfile(file):
        with open(file, 'w') as f:
            array = [data]
            json.dump(array, f)
    else:
        with open(file, 'r') as f:
            content = json.load(f)
        with open(file, 'w') as f:
            content.append(data)
            json.dump(content, f)


def create_account(username, userhash, email):
    # Create a new account entry if username has not already been taken
    data = {'username': username, 'hash': userhash, 'email': email}

    if os.path.isfile(CREDS_FILE):
        accounts = json.loads(open(CREDS_FILE).read())

        for account in accounts:
            if account['username'] == username:
                return FAIL, 'Username already taken'
            if account['email'] == email:
                return FAIL, 'Email already taken'

    update_file(CREDS_FILE, data)
    return SUCCESS, 'Account successfully created'


def login(username, userhash):
    # Check if the account exists and return a token if so
    if not os.path.isfile(CREDS_FILE):
        return FAIL, 'Invalid username'

    accounts = json.loads(open(CREDS_FILE).read())
    for account in accounts:
        if account['username'] == username:
            if account['hash'] == userhash:
                tokens['username'] = generate_token(username, userhash)
                return SUCCESS, tokens['username']
            else:
                return FAIL, 'Invalid password'

    return FAIL, 'Invalid username'




def parse_command(data):
    # Split a command received from socket into multiples tokens by " "
    items = data.split(" ")

    try:
        if items[0] == "CREATE":
            if items[1] == "ACCOUNT":
                return create_account(items[2], items[3], items[4])

        if items[0] == "AUTH":
            return login(items[1], items[2])
    except error as e:
        print('Too few arguments\n{}'.format(str(e)))


def connection_thread(conn, address):
    # Define the behavior of a threat
    data = conn.recv(MAX_BUFFER).decode('utf-8').rstrip()
    print("{} from client {}".format(data, address))

    status, response = parse_command(data)
    print(response)
    conn.send(bytes("{} {}".format(status, response).encode('utf-8')))
    conn.close()


def main():
    init()

    while True:
        try:
            client, address = sock.accept()
            print("New connection from {}".format(address))
            start_new_thread(connection_thread, (client, address))
        except error as e:
            print('Closing server due to unexpected error\n{}'.format(str(e)))
            sock.close()


main()
