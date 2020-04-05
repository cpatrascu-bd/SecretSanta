from enum import Enum
import re
import hashlib
import socket

HOST = '127.0.0.1'
PORT = 9001

class ReturnCodes(Enum):
    SUCCESS = 0
    USED_NAME = -1
    USED_EMAIL = -2
    INVALID_EMAIL = -3
    UNKNOWN_ERROR = -4
    WRONG_FORMAT_USERNAME = -5
    WRONG_FORMAT_PASSWORD = -6
    INVALID_USER = -7
    INVALID_PASSWORD = -8
    CONNECTION_ERROR = -9

class Utils():
    email_pattern = re.compile(".+@.+\..+")

    @staticmethod
    def encrypt_string(string):
        sha_signature = hashlib.sha256(string.encode()).hexdigest()
        return sha_signature

    @staticmethod
    def send_message_to_server(message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(message.encode())
                data = s.recv(1024)
            return data.decode()
        except:
            return 'communication_error'


class Client():
    def __init__(self):
        self.token = ""

    def create_user(self, name, password, email):

        if len(name) < 3:
            return ReturnCodes.WRONG_FORMAT_USERNAME
        if len(password) < 6:
            return ReturnCodes.WRONG_FORMAT_PASSWORD
        if not Utils.email_pattern.match(email):
            return ReturnCodes.INVALID_EMAIL

        sha_password = Utils.encrypt_string(password)
        message = "CREATE ACCOUNT " + name + " " + sha_password + " " + email
        answer = Utils.send_message_to_server(message)

        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR

        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        else:
            if answer[2:] == 'Username already taken':
                return ReturnCodes.USED_NAME
            if answer[2:] == 'Email already taken':
                return ReturnCodes.USED_EMAIL
        return ReturnCodes.UNKNOWN_ERROR

    def login(self, name, password):
        sha_password = Utils.encrypt_string(password)
        message = "AUTH " + name + " " + sha_password
        answer = Utils.send_message_to_server(message)
        if answer == 'connection_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '1':
            self.token = answer[2:]
            return ReturnCodes.SUCCESS
        else:
            if answer[2:] == 'Invalid username':
                return ReturnCodes.INVALID_USER
            if answer[2:] == 'Invalid password':
                return ReturnCodes.INVALID_PASSWORD
        return ReturnCodes.UNKNOWN_ERROR





