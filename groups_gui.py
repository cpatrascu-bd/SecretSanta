from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import auth

GROUP_LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230); background: rgba(0,0,0,100);"
GROUP_CREATE_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,50);"


class CreateGroupGUI(QDialog):
    def __init__(self, client=None, parent=None):
        super(CreateGroupGUI, self).__init__(parent)

        self.parent = parent
        self.client = client

        self.edit_groupname = QLineEdit()
        self.edit_groupname.setStyleSheet(GROUP_CREATE_LINEEDIT_SS)
        self.edit_groupname.setMinimumWidth(int(parent.width / 3))

        self.edit_password = QLineEdit()
        self.edit_password.setStyleSheet(GROUP_CREATE_LINEEDIT_SS)
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setMinimumWidth(int(parent.width / 3))

        self.edit_password2 = QLineEdit()
        self.edit_password2.setStyleSheet(GROUP_CREATE_LINEEDIT_SS)
        self.edit_password2.setEchoMode(QLineEdit.Password)
        self.edit_password2.setMinimumWidth(int(parent.width / 3))

        label_groupname = QLabel()
        label_groupname.setStyleSheet(GROUP_LABEL_STYLE_SHEET)
        label_groupname.setText("Group Name: ")
        label_groupname.setBuddy(self.edit_groupname)
        label_password = QLabel()
        label_password.setStyleSheet(GROUP_LABEL_STYLE_SHEET)
        label_password.setText("Password: ")
        label_password.setBuddy(self.edit_password)

        label_password2 = QLabel()
        label_password2.setStyleSheet(GROUP_LABEL_STYLE_SHEET)
        label_password2.setText("Reenter password: ")
        label_password2.setBuddy(self.edit_password2)

        ok_button = Auth.TransparentButton(text = "Create", font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.clicked.connect(self.create_group)

        cancel_button = Auth.TransparentButton(text="Cancel", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.clicked.connect(self.cancel)
       
        layout = QGridLayout()
        layout.addWidget(label_groupname, 0, 0)
        layout.addWidget(self.edit_groupname, 0, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.edit_password, 1, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(label_password2, 2, 0)
        layout.addWidget(self.edit_password2, 2, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(ok_button, 3, 0)
        layout.addWidget(cancel_button, 3, 1, alignment=Qt.AlignLeft)
        self.setLayout(layout)
        self.resize(int(3 * parent.width / 4), int(3 * parent.height / 4))
        self.setWindowTitle("Create Group")

    def create_group(self):
        pass

    def cancel(self):
        self.close()
