from enum import Enum


class ReturnCodes(Enum):
    SUCCESS = 0
    USED_NAME = -1
    USED_EMAIL = -2
    INVALID_EMAIL = -3
    UNKNOWN_ERROR = -4
    WRONG_USER = -5
    WRONG_PASSWORD = -6


class Client():

    def register(self, name, password, email):
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

    def authorize(self, name, password):
        if name == 'valid':
            return ReturnCodes.SUCCESS
        if name == 'wrong_user':
            return ReturnCodes.WRONG_USER
        if password == 'wrong_password':
            return ReturnCodes.WRONG_PASSWORD
        if name == 'error':
            return ReturnCodes.UNKNOWN_ERROR


# usage example
client = Client()

print(client.register('valid','a','a'))
print(client.register('used_name', 'a','a'))
print(client.register('used_email','a', 'used_email'))
print(client.register('invalid_email','a', 'invalid_email'))
print(client.register('error', 'a', 'a'))

print()

print(client.authorize('valid', 'a'))
print(client.authorize('wrong_user', 'a'))
print(client.authorize('a', 'wrong_password'))
print(client.authorize('error', 'a'))




