from enum import Enum
import re
import hashlib
import socket

HOST = '127.0.0.1'
PORT = 9001
DELIMITER = b'\x0a'.decode('utf-8')

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
    USED_GROUP_NAME = -10
    RELOGIN = -11
    USED_TEMPLATE_NAME = -12
    INVALID_GROUP = -13
    REQUEST_ALREADY_EXISTS = -14
    NOT_ADMIN = -15
    ALREADY_ENROLLED = -16
    INVALID_REQUEST = -17
    NOT_AUTH = -18
    YOU_ADMIN = -19

class Answer():
    ACCEPT = 'ACCEPT'
    DENY = 'DENY'


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
    @staticmethod
    def get_error_check(answer):
        if answer[2:] == 'Token not valid. Please re-authenticate':
            return ReturnCodes.RELOGIN, []
        return ReturnCodes.UNKNOWN_ERROR, []
    @staticmethod
    def request_answer_check(answer):
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'Token not valid. Please re-authenticate':
            return ReturnCodes.RELOGIN
        if answer[2:] == 'Group does not exist':
            return ReturnCodes.INVALID_GROUP
        if answer[2:] == 'Request does not exist':
            return ReturnCodes.INVALID_REQUEST
        if answer[2:] == 'Username already enrolled':
            return ReturnCodes.ALREADY_ENROLLED
        if answer[2:] == 'User not admin of the group':
            return ReturnCodes.NOT_ADMIN
        return ReturnCodes.UNKNOWN_ERROR




