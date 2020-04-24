from PyQt5.QtWidgets import QMessageBox

UNKNOWN_ERROR_TEXT = 'Ooops, something went wrong, please try again later'
WARNING = 'Warning'
ERROR = 'Error'
SUCCESS = 'Success'
MI_SCUZI = 'OOOPS'
NULL_USERNAME = 'Please introduce a username of more than 0 characters'
NULL_PASSWORD = 'Please introduce a password of more than 0 characters'
NULL_EMAIL = 'Please introduce an email of more than 0 characters'
PASSWORD_MISSMATCH = 'Passwords are not identical'
INVALID_USER = 'You have introduced an invalid username. Please insert a valid one'
INVALID_PASSWORD = 'You have introduced an invalid password. Please insert the valid one'
NOT_AUTH = 'You are not authenticated!!!'
TEMPLATE_NAME_NULL = "Template name can't be empty"
TEMPLATE_TEXT_NULL = "Template text can't be empty"
CONNECTION_ERROR = "Could not establish connection with the server, please try again later"
RELOGIN_ERR = "There is a problem with your login session. Please log in again!"
USED_NAME = "The name is already used, please provide another one!"
GROUP_NAME_NULL = "Group name can't be empty"
GROUP_PASSWORD_NULL = "Group password can't be empty"
GROUP_CREATE_SUCCESS = "Group created successfully"
TEMPLATE_CREATE_SUCCESS = "Template created successfully"


def alert(type, title, text, parent=None):
    alert_msg = QMessageBox(parent=parent)
    if type == WARNING:
        alert_msg.setIcon(QMessageBox.Warning)
    if type == ERROR:
        alert_msg.setIcon(QMessageBox.Critical)
    if type == SUCCESS:
        alert_msg.setIcon(QMessageBox.Information)
    alert_msg.setWindowTitle(title)
    alert_msg.setText(text)
    alert_msg.show()
    return