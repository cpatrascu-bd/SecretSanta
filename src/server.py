#! python3.8

import socket
import json
import os
import hashlib
import time
import email_script as mailer
from validate_email import validate_email
from _thread import *

# Global values
SUCCESS = 1
FAIL = 0
DELIMITER = b'\x15'.decode('utf-8')
DAYS_LIMIT = 345600

# File specific declarations
CREDENTIALS = 'users/users.json'
EMAIL_SCRIPT = './script.py'
GROUPS = './groups/'
TEMPLATES = './templates/'
REQUESTS = 'requests/requests.json'
LOG = 'logs/logs.txt'

# Socket specific declarations
MAX_BUFFER = 4096
MAX_CLIENTS = 10
HOST = '127.0.0.1'
PORT = 9001
sock = socket.socket()

# Session tokens for authenticated users and groups timeouts
tokens = {}
timeouts = {}


def init():
    # Create the necessary folders and the socket to listen for MAX_CLIENTS connections at the same time
    if not os.path.isdir(GROUPS):
        os.mkdir(GROUPS)

    if not os.path.isdir(TEMPLATES):
        os.mkdir(TEMPLATES)
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    if not os.path.isdir('users'):
        os.mkdir('users')
    if not os.path.isdir('requests'):
        os.mkdir('requests')

    try:
        sock.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))

    sock.listen(MAX_CLIENTS)


def get_file_content(file):
    # Retrieve json file content
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


def generate_token(username, password_hash):
    # Generate a unique token based on username and password hash. Adding a date string for security reasons
    m = hashlib.sha256()
    m.update("".join([username, str(time.time()), password_hash]).encode('utf-8'))
    return m.hexdigest()


def get_user_token(token):
    return [user for user, tok in tokens.items() if tok == token][0]


def create_account(username, password_hash, email):
    # Create a new account entry if username has not already been taken
    ret = validate_email(email, check_mx=True, verify=True, smtp_timeout=5)
    if not ret:
        return FAIL, 'Email address does not exist'
    if not ret:
        return FAIL, 'Email domain does not exist'

    data = {'username': username, 'password': password_hash, 'email': email}

    if os.path.isfile(CREDENTIALS):
        for account in json.loads(open(CREDENTIALS).read()):
            if account['username'] == username:
                return FAIL, 'Username already taken'

    insert_into_file(CREDENTIALS, data)
    return SUCCESS, 'Account successfully created'


def login(username, password_hash):
    # Check if the account exists and return a token if so
    if not os.path.isfile(CREDENTIALS):
        return FAIL, 'Incorrect username'

    for account in json.loads(open(CREDENTIALS).read()):
        if account['username'] == username and account['password'] == password_hash:
            tokens[username] = generate_token(username, password_hash)
            return SUCCESS, tokens[username]
        elif account['username'] == username and account['password'] != password_hash:
            return FAIL, 'Incorrect password'

    return FAIL, 'Incorrect username'


def logout(token):
    # Log out the user by removing the session token
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    del tokens[get_user_token(token)]
    return SUCCESS, 'User successfully logged out'


def create_group(name, password_hash, token):
    # Check for valid data, make username admin of the group and set the first value of the file to be the password hash
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    filename = GROUPS + name + '.json'
    if os.path.isfile(filename):
        return FAIL, 'Group name already exists'

    insert_into_file(filename, password_hash)
    insert_into_file(filename, get_user_token(token))

    return SUCCESS, 'Group {} created'.format(name.split('.')[0])


def get_group_admin(name):
    return get_file_content(GROUPS + name + '.json')[1]


def get_admin_email(name):
    return [item['email'] for item in get_file_content(CREDENTIALS) if item['username'] == name][0]


def get_groups(token):
    # List the groups folder in order to get all templates names
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    return SUCCESS, [name.split('.')[0] for name in os.listdir(GROUPS)]


def valid_token_group(group, token):
    # Check if token and groups exists
    code, msg = get_groups(token)
    if code == FAIL:
        return code, msg

    if group not in msg:
        return FAIL, 'Group does not exist'

    return SUCCESS, 'All good'


def get_group(name, token):
    # Get a specific group data by retrieving the file content
    code, msg = valid_token_group(name, token)
    if code == FAIL:
        return code, msg

    return SUCCESS, get_file_content(GROUPS + name + '.json')[1:]


def delete_group(name, token):
    # Check if token belongs to group owner and delete the whole group file
    if name not in get_groups(token)[1]:
        return FAIL, 'Group does not exist'

    if token not in tokens.values() or get_group_admin(name) not in tokens.keys()\
       or tokens[get_group_admin(name)] != token:
        return FAIL, 'Token not valid. Please re-authenticate'

    os.remove(GROUPS + name + '.json')
    return SUCCESS, 'Group successfully removed'


def group_timeout(name, token):
    # Check user to be group admin
    code, msg = valid_token_group(name, token)
    if code == FAIL:
        return code, msg

    if get_group_admin(name) != get_user_token(token):
        return FAIL, 'User not admin of the group'

    if name not in timeouts.keys() or timeouts[name] - time.time() > DAYS_LIMIT:
        timeouts[name] = time.time()
        return SUCCESS, 'Request successfully submitted'

    return FAIL, 'You can send emails only once in 4 days'


def add_to_group(username, group, password_hash, token):
    # Check integrity of the user and data and then, if password is correct, add to group
    if username not in tokens.keys() or tokens[username] != token:
        return FAIL, 'Token not valid. Please re-authenticate'

    if group not in get_groups(token)[1]:
        return FAIL, 'Group does not exist'

    content = get_file_content(GROUPS + group + '.json')
    if content[0] != password_hash:
        return FAIL, 'Incorrect password'
    if username in content[1:]:
        return FAIL, 'Username already enrolled'

    insert_into_file(GROUPS + group + '.json', username)
    return SUCCESS, 'User added to group'


def create_template(name, text, token):
    # Check for valid data and write content to file
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    filename = TEMPLATES + name + '.json'
    if os.path.isfile(filename):
        return FAIL, 'Template name already exists'

    insert_into_file(filename, text)
    return SUCCESS, 'Template {} created'.format(name.split('.')[0])


def get_templates(token):
    # List the template folder in order to get all templates names
    if token not in tokens.values():
        return FAIL, 'Token not valid. Please re-authenticate'

    return SUCCESS, [name.split('.')[0] for name in os.listdir(TEMPLATES)]


def get_template(name, token):
    # Get a specific template by retrieving the file content
    code, msg = get_templates(token)
    if code == FAIL:
        return code, msg

    if name not in msg:
        return FAIL, 'Template does not exist'

    return SUCCESS, get_file_content(TEMPLATES + name + '.json')[0]


def get_requests(group, token):
    # Check if token is valid and retrieve all join requests for the group
    code, msg = valid_token_group(group, token)
    if code == FAIL:
        return code, msg

    if get_user_token(token) != get_group_admin(group):
        return FAIL, 'User not group\'s admin'

    requests = [request for request in get_file_content(REQUESTS) if request['group'] == group]

    return SUCCESS, requests


def request_join(username, group, token):
    # Check user privileges and if data is valid and then add the request to the file
    if username not in tokens.keys() or tokens[username] != token:
        return FAIL, 'Token not valid. Please re-authenticate'

    if group not in get_groups(token)[1]:
        return FAIL, 'Group does not exist'

    filename = GROUPS + group + '.json'
    if os.path.isfile(filename) and username in get_file_content(filename)[1:]:
        return FAIL, 'Username already enrolled in group'

    data = {'username': username, 'group': group}
    if os.path.isfile(REQUESTS) and data in get_file_content(REQUESTS):
        return FAIL, 'Request already exists'

    insert_into_file(REQUESTS, data)
    return SUCCESS, 'Request submitted'


def request_unjoin(username, group, token):
    # Check user privileges and if data is valid and then remove group from group
    code, msg = valid_token_group(group, token)
    if code == FAIL:
        return code, msg

    if get_user_token(token) != get_group_admin(group) and get_user_token(token) != username:
        return FAIL, 'User does not have enough privileges'

    if username == get_group_admin(group):
        return FAIL, 'Admin can not leave the group'

    filename = GROUPS + group + '.json'
    if username not in get_file_content(filename)[1:]:
        return FAIL, 'Username not in group'

    remove_from_file(filename, username)
    return SUCCESS, 'Username successfully removed from group'


def request_accept(username, group, token):
    # Check user privileges and if data is valid and then remove the request from file while adding user to group
    code, msg = valid_token_group(group, token)
    if code == FAIL:
        return code, msg

    data = {'username': username, 'group': group}
    if os.path.isfile(REQUESTS) and data not in get_file_content(REQUESTS):
        return FAIL, 'Request does not exist'

    if username in get_file_content(GROUPS + group + '.json')[1:]:
        remove_from_file(REQUESTS, data)
        return FAIL, 'Username already enrolled'

    # Check if the user accepting is the group's admin
    if get_group_admin(group) == get_user_token(token):
        remove_from_file(REQUESTS, data)
        insert_into_file(GROUPS + group + '.json', username)
        return SUCCESS, 'Request accepted'

    return FAIL, 'User not admin of the group'


def request_deny(username, group, token):
    # Check user privileges and if data is valid and then remove the request from file
    code, msg = valid_token_group(group, token)
    if code == FAIL:
        return code, msg

    data = {'username': username, 'group': group}
    if os.path.isfile(REQUESTS) and data not in get_file_content(REQUESTS):
        return FAIL, 'Request does not exists'

    if get_group_admin(group) == get_user_token(token):
        remove_from_file(REQUESTS, data)
        return SUCCESS, 'Request denied'

    return FAIL, 'User not admin of the group'


def send_emails(group, data, flag, token):
    # Check user privileges and call the script. If it fails, reset the timeout
    code, msg = valid_token_group(group, token)
    if code == FAIL:
        return code, msg

    if get_group_admin(group) != get_user_token(token):
        return FAIL, 'User does not have enough privileges'

    if flag == 'True':
        template_file = 'temp.json'
        insert_into_file(template_file, data)
    else:
        template_file = TEMPLATES + data + '.json'

    code = mailer.run(group, GROUPS + group + '.json', template_file, get_admin_email(get_group_admin(group)))
    if code == FAIL and group in timeouts.keys():
        del timeouts[group]

    if flag == 'True':
        os.remove('temp.json')


def parse_command(data):
    # Split a command received from socket into multiples tokens by " "
    items = data.split(DELIMITER)

    try:
        if items[0] == 'CREATE':
            if items[1] == 'ACCOUNT':
                return create_account(items[2], items[3], items[4])
            if items[1] == 'GROUP':
                return create_group(items[2], items[3], items[4])
            if items[1] == 'TEMPLATE':
                return create_template(items[2], items[3], ' '.join([word for word in items[4:]]))

        if items[0] == 'FETCH':
            if items[1] == 'GROUPS':
                return get_groups(items[2])
            if items[1] == 'GROUP':
                return get_group(items[2], items[3])
            if items[1] == 'TEMPLATES':
                return get_templates(items[2])
            if items[1] == 'TEMPLATE':
                return get_template(items[2], items[3])
            if items[1] == 'REQUESTS':
                return get_requests(items[2], items[3])

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
            if items[1] == "UNJOIN":
                return request_unjoin(items[2], items[3], items[4])

        if items[0] == 'DELETE':
            if items[1] == 'GROUP':
                return delete_group(items[2], items[3])

        if items[0] == 'LOGOUT':
            return logout(items[1])

        if items[0] == 'SEND' and items[1] == 'EMAILS':
            start_new_thread(send_emails, (items[2], items[3], items[4], items[5]))
            return group_timeout(items[2], items[5])

        return FAIL, 'Command does not exist'
    except IndexError:
        return FAIL, 'Too few arguments'


def connection_thread(conn, address):
    # Define the behavior of a threat
    data = conn.recv(MAX_BUFFER).decode('utf-8').rstrip()
    status, response = parse_command(data)

    with open(LOG, 'a') as log:
        log.write("{} from client {}\n".format(data.replace(DELIMITER, '\t'), address))
        log.write('Response: {} {}\n\n'.format(status, response))

    conn.send(bytes("{} {}".format(status, response).encode('utf-8')))
    conn.close()


def main():
    init()

    while True:
        try:
            client, address = sock.accept()
            start_new_thread(connection_thread, (client, address))
        except Exception as e:
            print('Closing server due to unexpected error\n{}'.format(str(e)))
            sock.close()


main()
