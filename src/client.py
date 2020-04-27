from utils import *
import ast


class Client:
    def __init__(self):
        self.token = ""
        self.username = ''
        self.requests = []
        self.current_group_admin = False
        self.in_last_group = False

    @staticmethod
    def create_user(name, password, email):

        if len(name) < 3:
            return ReturnCodes.WRONG_FORMAT_USERNAME
        if len(password) < 6:
            return ReturnCodes.WRONG_FORMAT_PASSWORD
        if not Utils.check_email(email):
            return ReturnCodes.INVALID_EMAIL

        sha_password = Utils.encrypt_string(password)
        message = DELIMITER.join(['CREATE', 'ACCOUNT', name, sha_password, email])
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
        message = DELIMITER.join(['AUTH', name, sha_password])
        answer = Utils.send_message_to_server(message)
        if answer == 'connection_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '1':
            self.token = answer[2:]
            self.username = name
            return ReturnCodes.SUCCESS
        else:
            if answer[2:] == 'Incorrect username':
                return ReturnCodes.INVALID_USER
            if answer[2:] == 'Incorrect password':
                return ReturnCodes.INVALID_PASSWORD
        return ReturnCodes.UNKNOWN_ERROR

    def create_group(self, name, password):
        password_hash = Utils.encrypt_string(password)
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = DELIMITER.join(['CREATE', 'GROUP', name, password_hash, self.token])
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
        message = DELIMITER.join(['CREATE', 'TEMPLATE', name, text, self.token])
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
        message = DELIMITER.join(['REQUEST', 'JOINP', self.username, group_name, password_hash, self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'Token not valid. Please re-authenticate':
            self.logout()
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
        message = DELIMITER.join(['REQUEST', 'JOIN', self.username, group_name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
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

    def get_requests(self, group_name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH, []
        message = DELIMITER.join(['FETCH', 'REQUESTS', group_name, self.token])
        answer = Utils.send_message_to_server(message)

        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR, []

        if answer[0] == '1':
            requests = [request['username'] for request in ast.literal_eval(answer[2:])]
            return ReturnCodes.SUCCESS, requests
        if answer[2:] == 'Group does not exist':
            return ReturnCodes.INVALID_GROUP, []
        if answer[2:] == 'You are not admin of the group':
            return ReturnCodes.NOT_ADMIN, []

    def answer_request(self, username, group_name, ans_type):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = 'REQUEST' + DELIMITER + ans_type + DELIMITER + DELIMITER.join([username, group_name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        return_code = Utils.request_answer_check(answer)
        if return_code == ReturnCodes.RELOGIN:
            self.logout()
        return return_code

    def get_groups(self):
        if self.token == '':
            return ReturnCodes.NOT_AUTH, []
        message = 'FETCH' + DELIMITER + 'GROUPS' + DELIMITER + self.token
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '0':
            return Utils.get_error_check(answer)

        groups = ast.literal_eval(answer[2:])
        return ReturnCodes.SUCCESS, groups

    def get_group(self, name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH, []
        message = DELIMITER.join(['FETCH', 'GROUP', name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '0':
            return Utils.get_error_check(answer)

        group_users = ast.literal_eval(answer[2:])
        if self.username == group_users[0]:
            self.current_group_admin = True
        else:
            self.current_group_admin = False

        if self.username in group_users:
            self.in_last_group = True
        else:
            self.in_last_group = False
        return ReturnCodes.SUCCESS, group_users

    def get_templates(self):
        if self.token == '':
            return ReturnCodes.NOT_AUTH, []
        message = 'FETCH' + DELIMITER + 'TEMPLATES' + DELIMITER + self.token
        answer = Utils.send_message_to_server(message)
        if answer[0] == '0':
            return Utils.get_error_check(answer)
        templates = ast.literal_eval(answer[2:])
        return ReturnCodes.SUCCESS, templates

    def get_template(self, name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH, []
        message = DELIMITER.join(['FETCH', 'TEMPLATE', name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR, []
        if answer[0] == '0':
            return Utils.get_error_check(answer)
        return ReturnCodes.SUCCESS, answer[2:]

    def exit_group(self, group_name):
        return self.remove_user(self.username, group_name)

    def remove_user(self, username, group_name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = DELIMITER.join(['REQUEST', 'UNJOIN', username, group_name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[2:] == 'Token not valid. Please re-authenticate':
            return ReturnCodes.RELOGIN
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'Username not in group':
            return ReturnCodes.INVALID_USER
        if answer[2:] == 'Group does not exist':
            return ReturnCodes.INVALID_GROUP
        if answer[2:] == 'You are not admin of the group':
            return ReturnCodes.NOT_ADMIN
        if answer[2:] == 'Admin can not leave the group':
            return ReturnCodes.YOU_ADMIN
        return ReturnCodes.UNKNOWN_ERROR

    def delete_group(self, group_name):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        message = DELIMITER.join(['DELETE', 'GROUP', group_name, self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR

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
        message = 'LOGOUT' + DELIMITER + self.token
        answer = Utils.send_message_to_server(message)
        self.token = ''
        self.username = ''
        self.requests = []
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        return ReturnCodes.UNKNOWN_ERROR

    def send_emails(self, group_name, template_name="", text_template="", flag=False):
        if self.token == '':
            return ReturnCodes.NOT_AUTH
        if flag:
            message = DELIMITER.join(['SEND', 'EMAILS', group_name, text_template, str(flag), self.token])
        else:
            message = DELIMITER.join(['SEND', 'EMAILS', group_name, template_name, str(flag), self.token])
        answer = Utils.send_message_to_server(message)
        if answer == 'communication_error':
            return ReturnCodes.CONNECTION_ERROR
        if answer[0] == '1':
            return ReturnCodes.SUCCESS
        if answer[2:] == 'User not admin of the group':
            return ReturnCodes.NOT_ADMIN
        if answer[2:] == 'You can send emails only once in 4 days':
            return ReturnCodes.WAIT

        return ReturnCodes.UNKNOWN_ERROR

    def if_admin(self):
        return self.current_group_admin

    def in_current_group(self):
        return self.in_last_group

    def check_if_in_group(self, group_name):
        code, users = self.get_group(group_name)
        if code == ReturnCodes.SUCCESS:
            if self.username in users:
                return True
        return False
