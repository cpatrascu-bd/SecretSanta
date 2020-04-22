from utils import *
class Client():
    def __init__(self):
        self.token = ""
        self.username = ''
        self.requests = []

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
            self.logout()
            return ReturnCodes.SUCCESS
        else:
            if answer[2:] == 'Incorrect username':
                return ReturnCodes.INVALID_USER
            if answer[2:] == 'Incorrect password':
                return ReturnCodes.INVALID_PASSWORD
        return ReturnCodes.UNKNOWN_ERROR

    def create_group(self, name, password):
        passwordHash = Utils.encrypt_string(password)
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'CREATE GROUP ' + name + ' ' + passwordHash + ' ' + self.token
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        else:
            if answer[2:] == 'Token not valid. Please re-authenticate':
                self.logout()
                return ReturnCodes.RELOGIN
            if answer[2:] == 'Group name already exists':
                return ReturnCodes.USED_GROUP_NAME
            return ReturnCodes.UNKNOWN_ERROR

    def create_template(self, name, text):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'CREATE TEMPLATE ' + name + ' ' + self.token + ' ' + text
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'Template name already exists':
            return ReturnCodes.USED_TEMPLATE_NAME
        return ReturnCodes.UNKNOWN_ERROR

    def join_group_with_pass(self, group_name, group_pass):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        password_hash = Utils.encrypt_string(group_pass)
        message = 'REQUEST JOINP ' + ' '.join([self.username, group_name, password_hash, self.token])
        answer = Utils.send_message_to_server(message)
        print(answer)
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'Token not valid. Please re-authenticate':
            self.logout
            return ReturnCodes.RELOGIN
        if answer[2:] == 'Group does not exist':
            return ReturnCodes.INVALID_GROUP
        if answer[2:] == 'Incorrect password':
            return ReturnCodes.INVALID_PASSWORD
        if answer[2:] == 'Username already enrolled':
            return ReturnCodes.ALREADY_ENROLLED
        return ReturnCodes.UNKNOWN_ERROR

    def request_join_group(self, group_name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'REQUEST JOIN ' + ' '.join([self.username, group_name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'Token not valid. Please re-authenticate':
            self.logout()
            return ReturnCodes.RELOGIN
        if answer[2:] == 'Group does not exist':
            return ReturnCodes.INVALID_GROUP
        if answer[2:] == 'Request already exists':
            return ReturnCodes.REQUEST_ALREADY_EXISTS
        return ReturnCodes.UNKNOWN_ERROR

    def get_requests(self):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'FETCH REQUESTS ' + self.token
        answer = Utils.send_message_to_server(message)
        if answer[0] == '1':
            # TODO get requests from answer
            return ReturnCodes.SUCCESS, self.requests

    def answer_request(self, index, type):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        request = self.requests[index]
        message = 'REQUEST ' + type + ' ' + ' '.join[request[0] + request[1] + request[2]]
        answer = Utils.send_message_to_server(message)
        return_code = Utils.request_answer_check(answer)
        if return_code == ReturnCodes.RELOGIN:
            self.logout()
        return return_code

    def get_groups(self):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'FETCH GROUPS ' + self.token
        answer = Utils.send_message_to_server(message)
        if answer[0] == '0':
            return Utils.get_error_check(answer)
        groups = answer[3:-1].replace("'", '').split(", ")
        return ReturnCodes.SUCCESS, groups

    def get_group(self, name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'FETCH GROUP ' + name + ' ' + self.token
        answer = Utils.send_message_to_server(message)
        if answer[0] == '0':
            return Utils.get_error_check(answer)
        group_users = answer[3:-1].replace("'", '').split(", ")
        return ReturnCodes.SUCCESS, group_users

    def get_templates(self):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'FETCH TEMPLATES ' + self.token
        answer = Utils.send_message_to_server(message)
        if answer[0] == '0':
            return Utils.get_error_check(answer)
        templates = answer[3:-1].replace("'", '').split(", ")
        return ReturnCodes.SUCCESS, templates

    def get_template(self, name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'FETCH TEMPLATE ' + name + ' ' + self.token
        answer = Utils.send_message_to_server(message)
        if answer[0] == '0':
            return Utils.get_error_check(answer)
        return ReturnCodes.SUCCESS, answer[2:]

    def exit_group(self, group_name):
        return self.remove_user(self.username, group_name)

    def remove_user(self, username, group_name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'REQUEST REMOVE ' + ' '.join([username, group_name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'User not in group':
            return ReturnCodes.INVALID_USER
        if answer[2:] == 'Group does not exist':
            return ReturnCodes.INVALID_GROUP
        if answer[2:] == 'User not admin of the group':
            return ReturnCodes.NOT_ADMIN
        return ReturnCodes.UNKNOWN_ERROR

    def delete_group(self, group_name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'REQUEST DELETE ' + ' '.join([group_name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'Group does not exist':
            return ReturnCodes.INVALID_GROUP
        if answer[2:] == 'User not admin of the group':
            return ReturnCodes.NOT_ADMIN
        return ReturnCodes.UNKNOWN_ERROR

    def logout(self):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'REQUEST LOGOUT ' + self.token
        answer = Utils.send_message_to_server(message)
        self.token = ''
        self.username = ''
        self.requests = []
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        return ReturnCodes.UNKNOWN_ERROR



















