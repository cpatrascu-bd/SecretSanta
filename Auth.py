from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

UNKNOWN_ERROR_TEXT = 'Ooops, something went wrong, please try again later'
WARNING = 'Warning'
ERROR = 'Error'
MI_SCUZI = 'OOOPS'
NULL_USERNAME = 'Please introduce a username of more than 0 characters'
NULL_PASSWORD = 'Please introduce a password of more than 0 characters'

class AuthMessage(QDialog):
    def __init__(self, type , client=None, parent=None):
        super(AuthMessage, self).__init__(parent)
        self.client = client

        if type == "S":
            self.setWindowTitle("Sign up")
        elif type == 'L':
            self.setWindowTitle("Log in")

        self.edit_username = QLineEdit()
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)

        label_username = QLabel()
        label_username.setText("Username: ")
        label_username.setBuddy(self.edit_username)
        label_password = QLabel()
        label_password.setText("Password: ")
        label_password.setBuddy(self.edit_password)

        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.Ok)
        buttons.addButton(QDialogButtonBox.Cancel)
        if type == 'S':
            buttons.button(QDialogButtonBox.Ok).setText("Sign Up")
            buttons.button(QDialogButtonBox.Ok).clicked.connect(self.sign_user)
        elif type == 'L':
            buttons.button(QDialogButtonBox.Ok).setText("Log in")
            buttons.button(QDialogButtonBox.Ok).clicked.connect(self.log_user)

        buttons.button(QDialogButtonBox.Cancel).setText("Abort")
        buttons.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel)

        layout = QGridLayout()
        layout.addWidget(label_username, 0, 0)
        layout.addWidget(self.edit_username, 0, 1)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.edit_password, 1, 1)
        layout.addWidget(buttons, 2, 0, 1, 2)
        self.setLayout(layout)

    def alert(self, type, title, text):
        alert = QMessageBox()
        if type == WARNING:
            alert.setIcon(QMessageBox.Warning)
        if type == ERROR:
            alert.setIcon(QMessageBox.Critical)
        alert.setWindowTitle(title)
        alert.setText(text)
        alert.exec_()
        return

    def sign_user(self):
        if self.edit_username.text() == "":
            self.alert(WARNING, WARNING, NULL_USERNAME)
            self.edit_username.setFocus()
            return
        if self.edit_password.text() == "":
            self.alert(WARNING, WARNING, NULL_PASSWORD)
            self.edit_password.setFocus()
            return
        """
        ret = self.client.create_user(
            username=self.edit_username.currentText(),
            password=self.edit_password.text()
        )
        """
        ret = False
        if not ret:
            self.alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT)
            return
        self.close()

    def log_user(self):
        """
        ret = self.client.login(
            username=self.edit_username.currentText(),
            password=self.edit_password.text()
        )
        """
        ret = -3
        if ret < 0:
            alert = QMessageBox()
            alert.setWindowTitle("OOOOOPS")

            if ret == -1: #client.UNKNOWN_ERROR:
                alert.setIcon(QMessageBox.Warning)
                alert.setText('Ooops, something went wrong, please try again later')
            else:
                alert.setIcon(QMessageBox.Critical)

            if ret == -2: #client.INVALID_USERNAME:
                alert.setText('You have introduced an invalid username. Please insert a valid one')

            if ret == -3: #client.INVALID_PASSWORD:
                alert.setText('You have introduced an invalid password. Please insert the valid one')

            alert.exec_()
            return
        self.close()

    def cancel(self):
        self.close()


class Authentication(QDialog):
    def __init__(self,width=480, height=540, parent=None):
        super(Authentication, self).__init__(parent)
        self.sign_up_button = QPushButton("Sign Up")
        self.log_in_button = QPushButton("Log In")
        self.sign_up_button.setMaximumWidth(100)
        self.log_in_button.setMaximumWidth(100)
        layout = QVBoxLayout()
        layout.addWidget(self.sign_up_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.log_in_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.sign_up_button.clicked.connect(self.sign_up)
        self.log_in_button.clicked.connect(self.log_in)
        self.setWindowTitle("Secret Santa Authentication")
        self.resize(width,height)

    def sign_up(self):
        dialog = AuthMessage('S', parent=self)
        dialog.exec_()

    def log_in(self):
        dialog = AuthMessage('L', parent=self)
        dialog.exec_()

app = QApplication([])
h = QDesktopWidget.screenGeometry(app.desktop()).height()
w = QDesktopWidget.screenGeometry(app.desktop()).width()
print(h,w)
app.setStyle('Fusion')
app.setWindowIcon(QIcon('santa.jpg'))
auth = Authentication(int(w/4),int(h/4))
auth.show()
app.exec_()