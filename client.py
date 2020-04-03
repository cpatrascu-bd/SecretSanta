from enum import Enum


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


class Client():

    def create_user(self, name, password, email):
        if name == 'valid':
            return ReturnCodes.SUCCESS
        if name == 'used_name':
            return ReturnCodes.USED_NAME
        if email == 'used_email':
            return ReturnCodes.USED_EMAIL
        if email == 'invalid_email':
            return ReturnCodes.INVALID_EMAIL
        if name == 'error':
            return ReturnCodes.UNKNOWN_ERROR
        if name == 'wfu':
            return ReturnCodes.WRONG_FORMAT_USERNAME
        if password == 'wfp':
            return ReturnCodes.WRONG_FORMAT_PASSWORD

    def login(self, name, password):
        if name == 'valid':
            return ReturnCodes.SUCCESS
        if name == 'wrong_user':
            return ReturnCodes.INVALID_USER
        if password == 'wrong_password':
            return ReturnCodes.INVALID_PASSWORD
        if name == 'error':
            return ReturnCodes.UNKNOWN_ERROR


# usage example
client = Client()

print(client.create_user('valid','a','a'))
print(client.create_user('used_name', 'a','a'))
print(client.create_user('used_email','a', 'used_email'))
print(client.create_user('invalid_email','a', 'invalid_email'))
print(client.create_user('error', 'a', 'a'))

print()

print(client.login('valid', 'a'))
print(client.login('wrong_user', 'a'))
print(client.login('a', 'wrong_password'))
print(client.login('error', 'a'))




