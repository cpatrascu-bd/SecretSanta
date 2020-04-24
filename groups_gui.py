from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Alerts import *
from client import *
import Auth

GROUP_LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230); background: rgba(0,0,0,100);"
GROUP_CREATE_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,50);"
GROUP_LIST_VIEW_SS = "color:white; border: none; background: rgba(0,0,0,100);"
JOINER_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,50);"
JOINER_LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230); background: rgba(0,0,0,100);"


class Joiner(QDialog):
    def __init__(self, group, santa_client=None, parent=None):
        super(Joiner, self).__init__(parent)
        self.setModal(True)

        self.group = group
        self.client = santa_client
        self.parent = parent

        self.edit_password = QLineEdit()
        self.edit_password.setStyleSheet(JOINER_LINEEDIT_SS)
        self.edit_password.setMinimumWidth(int(parent.width / 5))

        label_password = QLabel()
        label_password.setStyleSheet(JOINER_LABEL_STYLE_SHEET)
        label_password.setText("Password: ")
        label_password.setBuddy(self.edit_password)

        join_pwd_button = Auth.TransparentButton(text="Join with password", font_size=10, parent=self)
        join_pwd_button.setMaximumWidth(int(parent.width/5))
        join_pwd_button.clicked.connect(self.join_password)

        join_button = Auth.TransparentButton(text="Join Request", font_size=10, parent=self)
        join_button.setMaximumWidth(int(parent.width / 5))
        join_button.clicked.connect(self.join)

        layout = QGridLayout()
        layout.addWidget(label_password, 0, 0)
        layout.addWidget(self.edit_password, 0, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(join_pwd_button, 1, 0)
        layout.addWidget(join_button, 1, 1)

        self.setLayout(layout)
        self.resize(int(3 * parent.width / 8), int(3 * parent.height / 8))
        self.edit_password.setFocus()

    def join_password(self):
        pass

    def join(self):
        pass


class CreateGroupGUI(QDialog):
    def __init__(self, santa_client=None, parent=None):
        super(CreateGroupGUI, self).__init__(parent)
        self.setModal(True)

        self.parent = parent
        self.client = santa_client

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

        ok_button = Auth.TransparentButton(text="Create", font_size=10, parent=self)
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
        self.edit_groupname.setFocus()

    def create_group(self):
        if self.edit_groupname.text() == "":
            alert(WARNING, WARNING, GROUP_NAME_NULL, parent=self)
            return
        if self.edit_password.text() == "":
            alert(WARNING, WARNING, GROUP_PASSWORD_NULL, parent=self)
            return
        if self.edit_password2.text() != self.edit_password.text():
            alert(WARNING, WARNING, PASSWORD_MISSMATCH, parent=self)
            return
        ret = self.client.create_group(self.edit_groupname.text(),self.edit_password.text())

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self)
            self.close()
            self.parent.return_to_login()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self)
            self.close()
            self.parent.return_to_login()
            return

        if ret == ReturnCodes.CONNECTION_ERROR:
            alert(WARNING, WARNING, CONNECTION_ERROR, parent=self)

        if ret == ReturnCodes.USED_GROUP_NAME:
            alert(WARNING, WARNING, USED_NAME, parent=self)

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)

        if ret == ReturnCodes.SUCCESS:
            alert(SUCCESS, SUCCESS, GROUP_CREATE_SUCCESS, parent=self.parent)
            self.close()
        pass

    def cancel(self):
        self.close()


class ViewGroups(QDialog):
    def __init__(self, groups, client=None, parent=None):
        super(ViewGroups, self).__init__(parent)
        self.setModal(True)

        self.parent = parent
        self.client = client
        self.width = parent.width
        self.height = parent.height

        self.list_groups = QListView()
        self.list_groups.setStyleSheet(GROUP_LIST_VIEW_SS)
        self.list_groups.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.list_groups.doubleClicked.connect(self.select_group)

        ok_button = Auth.TransparentButton(text="View", font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.clicked.connect(self.view_group)

        join_button = Auth.TransparentButton(text="Join", font_size=10, parent=self)
        join_button.setMaximumWidth(int(parent.width / 10))
        join_button.clicked.connect(self.join_group)

        cancel_button = Auth.TransparentButton(text="Cancel", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.clicked.connect(self.cancel)

        layout = QGridLayout()

        layout.addWidget(self.list_groups, 0, 0, 4, 1)
        layout.addWidget(ok_button, 0, 1)
        layout.addWidget(cancel_button, 1, 1)
        layout.addWidget(join_button, 2, 1)

        self.model = QStringListModel()
        self.model.setStringList(groups)
        self.list_groups.setModel(self.model)

        self.setLayout(layout)
        self.resize(self.width, self.height)
        self.setWindowTitle("View Groups")

    def select_group(self):
        self.view_group()

    def join_group(self):
        print("join")
        idx = self.list_groups.selectedIndexes()[0]
        group_name = self.model.itemData(idx)[0]
        print(group_name)
        joiner = Joiner(group_name, santa_client=self.client, parent=self)
        joiner.show()

        # self.setDisabled()
        pass

    def cancel(self):
        self.close()

    def view_group(self):
        idx = self.list_groups.selectedIndexes()[0]
        group_name = self.model.itemData(idx)[0]
        ret, group = self.client.get_group(group_name)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self)
            self.close()
            self.parent.return_to_login()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self)
            self.close()
            self.parent.return_to_login()

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        tb = QTextBrowser()
        tb.setText(group_name)

        pass