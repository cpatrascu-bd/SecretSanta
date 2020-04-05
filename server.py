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
CREDENTIALS = './users.json'
EMAIL_SCRIPT = './script.py'
GROUPS = './groups/'
TEMPLATES = './templates/'
REQUESTS = './requests.json'

# Socket specific declarations
MAX_BUFFER = 4096
MAX_CLIENTS = 10
HOST = '127.0.0.1'
PORT = 9001
sock = socket.socket()

# Data kept in the program's memory
tokens = {}
groups = {}


def init():
    # Create the necessary folders and the socket to listen for MAX_CLIENTS connections at the same time
    if not os.path.isdir(GROUPS):
        os.mkdir(GROUPS)

    if not os.path.isdir(TEMPLATES):
        os.mkdir(TEMPLATES)

    try:
        sock.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))

    sock.listen(MAX_CLIENTS)


def get_file_content(file):
    with open(file, 'r') as f:
        content = json.load(f)
    return content


def insert_into_file(file, data):
    # Insert entry into file
    if not os.path.isfile(file):
        with open(file, 'w') as f:
            array = [data]
            json.dump(array, f)
    else:
        content = get_file_content(file)
        with open(file, 'w') as f:
            content.append(data)
            json.dump(content, f)


def remove_from_file(file, data):
    # Remove an entry from the file
    content = get_file_content(file)
    content.remove(data)

    with open(file, 'w') as f:
        json.dump(content, f)


def generate_token(username, userhash):
    # Generate a unique token based on username and password hash. Adding a date string for security reasons
    m = hashlib.sha256()
    m.update("".join([username, str(datetime.now()), userhash]).encode('utf-8'))
    return m.hexdigest()


def create_account(username, password_hash, email):
    # Create a new account entry if username has not already been taken
    data = {'username': username, 'password': password_hash, 'email': email}

    if os.path.isfile(CREDENTIALS):
        accounts = json.loads(open(CREDENTIALS).read())
        for account in accounts:
            if account['username'] == username:
                return FAIL, 'Username already taken'

    insert_into_file(CREDENTIALS, data)
    return SUCCESS, 'Account successfully created'


def login(username, password_hash):
    # Check if the account exists and return a token if so
    if not os.path.isfile(CREDENTIALS):
        return FAIL, 'Incorrect username'

    accounts = json.loads(open(CREDENTIALS).read())
    for account in accounts:
        if account['username'] == username and account['password'] == password_hash:
            tokens[username] = generate_token(username, password_hash)
            return SUCCESS, tokens[username]
        elif account['username'] == username and account['password'] != password_hash:
            return FAIL, 'Incorrect password'

    return FAIL, 'Incorrect username'


def create_group(name, password_hash, token):
    # Check for valid data, make username admin of the group and set the first value of the file to be the password hash
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    filename = GROUPS + name + '.json'
    if os.path.isfile(filename):
        return FAIL, 'Group name already exists'

    groups[name] = [key for key, value in tokens.items() if value == token][0]

    insert_into_file(filename, password_hash)
    return SUCCESS, 'Group {} created'.format(name.split('.')[0])


def create_template(name, token, text):
    # Check for valid data and write content to file
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    filename = TEMPLATES + name + '.json'
    if os.path.isfile(filename):
        return FAIL, 'Template name already exists'

    insert_into_file(filename, text)
    return SUCCESS, 'Template {} created'.format(name.split('.')[0])


def get_groups(token):
    # List the groups folder in order to get all templates names
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    return SUCCESS, [name.split('.')[0] for name in os.listdir(GROUPS)]


def get_group(name, token):
    # Get a specific group data by retrieving the file content

    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    return SUCCESS, get_file_content(GROUPS + name + '.json')


def get_templates(token):
    # List the template folder in order to get all templates names
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    return SUCCESS, [name.split('.')[0] for name in os.listdir(TEMPLATES)]


def get_template(name, token):
    # Get a specific template by retrieving the file content
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    return SUCCESS, get_file_content(TEMPLATES + name + '.json')[0]


def add_to_group(username, group, password_hash, token):
    # Check integrity of the user and data and then, if password is correct, add to group
    if username not in tokens.keys() or tokens[username] != token:
        return FAIL, 'Token not valid. Please re-authenticate'

    if group not in [name.split('.')[0] for name in os.listdir(GROUPS)]:
        return FAIL, 'Group does not exist'

    content = get_file_content(GROUPS + group + '.json')
    if content[0] != password_hash:
        return FAIL, 'Incorrect password'
    if username in content[1:]:
        return FAIL, 'Username already enrolled'

    insert_into_file(GROUPS + group + '.json', username)
    return SUCCESS, 'User added to group'


def request_join(username, group, token):
    # Check user privileges and if data is valid and then add the request to the file
    if username not in tokens.keys() or tokens[username] != token:
        return FAIL, 'Token not valid. Please re-authenticate'

    if group not in [name.split('.')[0] for name in os.listdir(GROUPS)]:
        return FAIL, 'Group does not exist'

    # Check for duplicate request
    data = {'username': username, 'group': group}
    if os.path.isfile(REQUESTS) and data in get_file_content(REQUESTS):
        return FAIL, 'Request already exists'

    insert_into_file(REQUESTS, data)
    return SUCCESS, 'Request submitted'


def request_accept(username, group, token):
    # Check user privileges and if data is valid and then remove the request from file while adding user to group
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    if group not in [name.split('.')[0] for name in os.listdir(GROUPS)]:
        return FAIL, 'Group does not exist'

    data = {'username': username, 'group': group}
    if os.path.isfile(REQUESTS) and data not in get_file_content(REQUESTS):
        return FAIL, 'Request does not exist'

    if username in get_file_content(GROUPS + group + '.json')[1:]:
        remove_from_file(REQUESTS, data)
        return FAIL, 'Username already enrolled'

    # Check if the user accepting is the group's admin
    user = [user for user, tok in tokens.items() if token == tok]
    if user and groups[group] == user[0]:
        remove_from_file(REQUESTS, data)
        insert_into_file(GROUPS + group + '.json', username)
        return SUCCESS, 'Request accepted'

    return FAIL, 'User not admin of the group'


def request_deny(username, group, token):
    # Check user privileges and if data is valid and then remove the request from file
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    if group not in [name.split('.')[0] for name in os.listdir(GROUPS)]:
        return FAIL, 'Group does not exist'

    data = {'username': username, 'group': group}
    if os.path.isfile(REQUESTS) and data not in get_file_content(REQUESTS):
        return FAIL, 'Request does not exists'

    user = [user for user, tok in tokens.items() if token == tok]
    if user and groups[group] == user[0]:
        remove_from_file(REQUESTS, data)
        return SUCCESS, 'Request denied'

    return FAIL, 'User not admin of the group'


def parse_command(data):
    # Split a command received from socket into multiples tokens by " "
    items = data.split(" ")

    try:
        if items[0] == 'CREATE':
            if items[1] == 'ACCOUNT':
                return create_account(items[2], items[3], items[4])
            if items[1] == 'GROUP':
                return create_group(items[2], items[3], items[4])
            if items[1] == 'TEMPLATE':
                return create_template(items[2], items[3], " ".join([word for word in items[4:]]))

        if items[0] == 'FETCH':
            if items[1] == 'GROUPS':
                return get_groups(items[2])
            if items[1] == 'GROUP':
                return get_group(items[2], items[3])
            if items[1] == 'TEMPLATES':
                return get_templates(items[2])
            if items[1] == 'TEMPLATE':
                return get_template(items[2], items[3])

        if items[0] == 'AUTH':
            return login(items[1], items[2])

        if items[0] == 'REQUEST':
            if items[1] == 'JOIN':
                return request_join(items[2], items[3], items[4])
            if items[1] == 'JOINP':
                return add_to_group(items[2], items[3], items[4], items[5])
            if items[1] == 'ACCEPT':
                return request_accept(items[2], items[3], items[4])
            if items[1] == 'DENY':
                return request_deny(items[2], items[3], items[4])
    except error as e:
        print('Too few arguments\n{}'.format(str(e)))


def connection_thread(conn, address):
    # Define the behavior of a threat
    data = conn.recv(MAX_BUFFER).decode('utf-8').rstrip()
    print("{} from client {}".format(data, address))

    status, response = parse_command(data)
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
