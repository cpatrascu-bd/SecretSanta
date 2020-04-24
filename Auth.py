from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from client import *
from alerts import *
import dashboard

LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230);"
AUTH_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,50);"


class TransparentButton(QPushButton):
    def __init__(self, text="", font_size=14, parent=None):
        super(TransparentButton, self).__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.opacity = 0.6
        self.font_size = font_size
        self.setText(text)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawRoundedRect(self.rect(), 10, 10)
        painter.setOpacity(1)
        painter.setPen(QPen(Qt.darkRed))
        font = QFont("SansSerif", self.font_size)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(self.rect()), Qt.AlignCenter, self.text())

    def enterEvent(self, event: QEvent) -> None:
        self.opacity = 0.1

    def leaveEvent(self, event: QEvent) -> None:
        self.opacity = 0.6


class AuthForm(QDialog):
    def __init__(self, auth_type, santa_client=None, parent=None):
        super(AuthForm, self).__init__(parent)
        self.client = santa_client
        self.parent = parent
        self.display_help_info = False
        self.setModal(True)

        if auth_type == "S":
            self.setWindowTitle("Sign up")
        elif auth_type == 'L':
            self.setWindowTitle("Log in")

        self.edit_username = QLineEdit()
        self.edit_username.setStyleSheet(AUTH_LINEEDIT_SS)
        self.edit_username.setMinimumWidth(int(parent.width / 3))

        self.edit_password = QLineEdit()
        self.edit_password.setStyleSheet(AUTH_LINEEDIT_SS)
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setMinimumWidth(int(parent.width / 3))

        label_username = QLabel()
        label_username.setStyleSheet(LABEL_STYLE_SHEET)
        label_username.setText("Username: ")
        label_username.setBuddy(self.edit_username)
        label_password = QLabel()
        label_password.setStyleSheet(LABEL_STYLE_SHEET)
        label_password.setText("Password: ")
        label_password.setBuddy(self.edit_password)

        ok_button = TransparentButton(font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        if auth_type == 'S':
            self.edit_password2 = QLineEdit()
            self.edit_password2.setStyleSheet(AUTH_LINEEDIT_SS)
            self.edit_password2.setEchoMode(QLineEdit.Password)
            self.edit_password2.setMinimumWidth(int(parent.width / 3))
            label_password2 = QLabel()
            label_password2.setStyleSheet(LABEL_STYLE_SHEET)
            label_password2.setText("Reenter password: ")
            label_password2.setBuddy(self.edit_password2)

            self.edit_email = QLineEdit()
            self.edit_email.setStyleSheet(AUTH_LINEEDIT_SS)
            self.edit_email.setMinimumWidth(int(parent.width / 3))
            label_email = QLabel()
            label_email.setStyleSheet(LABEL_STYLE_SHEET)
            label_email.setText("Email: ")
            label_email.setBuddy(self.edit_email)

            ok_button.setText("Sign Up")
            ok_button.clicked.connect(self.sign_user)
        elif auth_type == 'L':
            ok_button.setText("Log In")
            ok_button.clicked.connect(self.log_user)

        cancel_button = TransparentButton(text="Cancel", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.clicked.connect(self.cancel)

        layout = QGridLayout()
        layout.addWidget(label_username, 0, 0)
        layout.addWidget(self.edit_username, 0, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.edit_password, 1, 1, alignment=Qt.AlignHCenter)
        if auth_type == 'S':
            layout.addWidget(label_password2, 2, 0)
            layout.addWidget(self.edit_password2, 2, 1, alignment=Qt.AlignHCenter)
            layout.addWidget(label_email, 3, 0)
            layout.addWidget(self.edit_email, 3, 1, alignment=Qt.AlignHCenter)
            layout.addWidget(ok_button, 4, 0)
            layout.addWidget(cancel_button, 4, 1, alignment=Qt.AlignLeft)
        else:
            layout.addWidget(ok_button, 2, 0)
            layout.addWidget(cancel_button, 2, 1, alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.resize(int(3 * parent.width / 4), int(3 * parent.height / 4))
        self.edit_username.setFocus()

    def sign_user(self):
        if self.edit_username.text() == "":
            alert(WARNING, WARNING, NULL_USERNAME, parent=self)
            self.edit_username.setFocus()
            return
        if self.edit_password.text() == "":
            alert(WARNING, WARNING, NULL_PASSWORD, parent=self)
            self.edit_password.setFocus()
            return
        if self.edit_password2.text() != self.edit_password.text():
            alert(WARNING, WARNING, PASSWORD_MISSMATCH, parent=self)
            self.edit_password2.setFocus()
            return
        if self.edit_email.text() == "":
            alert(WARNING, WARNING, NULL_EMAIL, parent=self)
            self.edit_email.setFocus()
            return

        ret = self.client.create_user(
            self.edit_username.text(),
            self.edit_password.text(),
            self.edit_email.text()
        )

        if ret == ReturnCodes.SUCCESS:
            self.close()
        if ret == ReturnCodes.USED_NAME:
            alert(WARNING, WARNING, "Name is already used by another user!", parent=self)
            self.edit_name.setFocus()
            return
        if ret == ReturnCodes.USED_EMAIL:
            alert(WARNING, WARNING, "Email is already used by another user!", parent=self)
            self.edit_email.setFocus()
            return
        if ret == ReturnCodes.INVALID_EMAIL:
            alert(WARNING, WARNING, "Email is invalid. Please provide another one!", parent=self)
            self.edit_email.setFocus()
            return
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return
        if ret == ReturnCodes.WRONG_FORMAT_USERNAME:
            alert(ERROR, ERROR, "Username format is invalid. It should have at least 3 characters", parent=self)
            self.edit_username.setFocus()
            return
        if ret == ReturnCodes.WRONG_FORMAT_PASSWORD:
            alert(ERROR, ERROR, "Password format in invalid. It should have more than 6 characters"
                                " and at least one of each of the following: digit, uppercase letter, "
                                "lowercase letter, symbol(%,@,#,7,etc.)", parent=self)
            self.edit_password.setFocus()

    def log_user(self):

        if self.edit_username.text() == "":
            alert(WARNING, WARNING, NULL_USERNAME, parent=self)
            self.edit_username.setFocus()
            return
        if self.edit_password.text() == "":
            alert(WARNING, WARNING, NULL_PASSWORD, parent=self)
            self.edit_password.setFocus()
            return

        ret = self.client.login(
            self.edit_username.text(),
            self.edit_password.text()
        )

        if ret == ReturnCodes.SUCCESS:
            dash = dashboard.Dashboard(width=self.parent.width, height=self.parent.height, papa=self.parent,
                                       client=self.client)
            self.close()
            self.parent.hide()
            dash.exec_()

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, WARNING, MI_SCUZI, parent=self)
            return
        if ret == ReturnCodes.INVALID_USER:
            alert(ERROR, ERROR, INVALID_USER, parent=self)
            self.edit_username.setFocus()
            return
        if ret == ReturnCodes.INVALID_PASSWORD:
            alert(ERROR, ERROR, INVALID_PASSWORD, parent=self)
            self.edit_password.setFocus()
            self.edit_password.clear()

    def cancel(self):
        dash = dashboard.Dashboard(width=self.parent.width, height=self.parent.height, papa=self.parent,
                                   client=self.client)
        self.close()
        self.parent.hide()
        dash.exec_()


class Authentication(QDialog):
    def __init__(self, width=480, height=540, santa_client=None, parent=None):
        super(Authentication, self).__init__(parent)

        self.client = santa_client

        self.sign_up_button = TransparentButton("Sign Up")
        self.log_in_button = TransparentButton("Log In")
        self.exit_button = TransparentButton("Exit")
        self.width = width
        self.height = height
        self.set_button_sizes(self.sign_up_button)
        self.set_button_sizes(self.log_in_button)
        self.set_button_sizes(self.exit_button)
        """
        self.help_messages= {self.sign_up_button.text(): "Create a new account for " \
                                                         "accessing the facilites of this application",
                             self.log_in_button.text(): "Connect using an existing account",
                             self.exit_button.text(): "Leave the santa business for another time"}

        self.info_label = QLabel()
        self.info_label.setText("Welcome to the HoHoHo world of Secret Santa!")
        self.setStyleSheet("color: red; background-color: rgba(0,0,0,153)")
        self.info_label.setMaximumHeight(int(height/15))
        """
        self.display_help_info = False

        layout = QVBoxLayout()
        layout.addWidget(self.sign_up_button, alignment=Qt.AlignHCenter)
        layout.addWidget(self.log_in_button, alignment=Qt.AlignHCenter)
        layout.addWidget(self.exit_button, alignment=Qt.AlignHCenter)

        self.setLayout(layout)
        self.sign_up_button.clicked.connect(self.sign_up)
        self.log_in_button.clicked.connect(self.log_in)
        self.exit_button.clicked.connect(self.close)
        self.setWindowTitle("Secret Santa")
        self.resize(width, height)

    def sign_up(self):
        dialog = AuthForm('S', santa_client=self.client, parent=self)
        dialog.show()

    def log_in(self):
        dialog = AuthForm('L', santa_client=self.client, parent=self)
        dialog.show()

    def set_button_sizes(self, button):
        button.setMinimumHeight(int(self.height / 12))
        button.setMinimumWidth(int(self.width / 10))


if __name__ == "__main__":
    app = QApplication([])
    h = QDesktopWidget.screenGeometry(app.desktop()).height()
    w = QDesktopWidget.screenGeometry(app.desktop()).width()
    client = Client()
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon('santa.jpg'))
    app.setStyleSheet(open('appStyleSheet.css').read())
    auth = Authentication(int(w / 2), int(h / 2), santa_client=client)
    auth.show()
    app.exec_()
