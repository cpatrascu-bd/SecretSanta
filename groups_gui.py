from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from alerts import *
from client import *
import auth
import templates_gui

GROUP_NAME_SS = "font-weight: bold; font-size: 30px; color: DarkRed"
GROUP_LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230); background: rgba(0,0,0,100);"
GROUP_CREATE_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,50);"
GROUP_LIST_VIEW_SS = "color:white; border: none; font-size: 18px; background: rgba(0,0,0,100);"
JOINER_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,50);"
JOINER_LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230); background: rgba(0,0,0,100);"


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

        ok_button = auth.TransparentButton(text="Create", font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.clicked.connect(self.create_group)

        cancel_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
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
        self.width = 3 * parent.width / 4
        self.height = 3 * parent.height / 4
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
        ret = self.client.create_group(self.edit_groupname.text(), self.edit_password.text())

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent.parent)
            self.close()
            self.parent.return_to_login()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent.parent)
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


class Joiner(QDialog):

    def __init__(self, group, outer_join=False, santa_client=None, parent=None):
        super(Joiner, self).__init__(parent)
        self.setModal(True)

        self.group = group
        self.client = santa_client
        self.parent = parent
        self.outer_join = outer_join

        self.edit_password = QLineEdit()
        self.edit_password.setStyleSheet(JOINER_LINEEDIT_SS)
        self.edit_password.setMinimumWidth(int(parent.width / 5))
        self.edit_password.setEchoMode(QLineEdit.Password)

        label_password = QLabel()
        label_password.setStyleSheet(JOINER_LABEL_STYLE_SHEET)
        label_password.setText("Password: ")
        label_password.setBuddy(self.edit_password)

        join_pwd_button = auth.TransparentButton(text="Join with password", font_size=10, parent=self)
        join_pwd_button.setMaximumWidth(int(parent.width / 5))
        join_pwd_button.setMinimumHeight(int(parent.height / 15))
        join_pwd_button.clicked.connect(self.join_password)

        join_button = auth.TransparentButton(text="Join Request", font_size=10, parent=self)
        join_button.setMaximumWidth(int(parent.width / 5))
        join_button.setMinimumHeight(int(parent.height / 15))
        join_button.clicked.connect(self.join)

        layout = QGridLayout()
        layout.addWidget(label_password, 0, 0)
        layout.addWidget(self.edit_password, 0, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(join_pwd_button, 1, 0)
        layout.addWidget(join_button, 1, 1)

        self.setLayout(layout)
        self.width = 3 * parent.width / 8
        self.height = 3 * parent.height / 8
        self.resize(self.width, self.height)
        self.edit_password.setFocus()

    def join_password(self):
        ret = self.client.join_group_with_pass(self.group, self.edit_password.text())
        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent)
        if ret == ReturnCodes.INVALID_GROUP:
            alert(ERROR, ERROR, JOIN_INVALID_GROUP, parent=self.parent)
        if ret == ReturnCodes.INVALID_PASSWORD:
            alert(ERROR, ERROR, INVALID_PASSWORD, parent=self)
            return
        if ret == ReturnCodes.ALREADY_ENROLLED:
            alert(WARNING, WARNING, ALREADY_ENROLLED, parent=self.parent)
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return
        if ret == ReturnCodes.SUCCESS:
            alert(SUCCESS, SUCCESS, SUCCESSFUL_JOIN + self.group, parent=self.parent)
        if not self.outer_join:
            self.parent.refresh_users_list()
            self.parent.add_leave_button()
        self.close()

    def join(self):
        ret = self.client.request_join_group(self.group)
        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent.parent)
        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent.parent)
        if ret == ReturnCodes.INVALID_GROUP:
            alert(ERROR, ERROR, JOIN_INVALID_GROUP, parent=self.parent.parent)
        if ret == ReturnCodes.REQUEST_ALREADY_EXISTS:
            alert(WARNING, WARNING, REQUEST_EXISTS, parent=self.parent.parent)
        if ret == ReturnCodes.SUCCESS:
            alert(SUCCESS, SUCCESS, SUCCESSFUL_JOIN_REQUEST, parent=self.parent.parent)
        self.close()
        self.parent.close()


class ViewRequests(QDialog):
    def __init__(self, requests, client=None, parent=None, group=None):
        super(ViewRequests, self).__init__(parent)
        self.setModal(True)

        self.parent = parent
        self.client = client
        self.width = parent.width
        self.height = parent.height
        self.group = group

        self.list_requests = QListView()
        self.list_requests.setStyleSheet(GROUP_LIST_VIEW_SS)
        self.list_requests.setEditTriggers(QAbstractItemView.NoEditTriggers)

        accept_button = auth.TransparentButton(text="Acept", font_size=10, parent=self)
        accept_button.setMaximumWidth(int(parent.width / 10))
        accept_button.setMinimumHeight(int(parent.height / 15))
        accept_button.clicked.connect(self.accept_request)

        reject_button = auth.TransparentButton(text="Reject", font_size=10, parent=self)
        reject_button.setMaximumWidth(int(parent.width / 10))
        reject_button.setMinimumHeight(int(parent.height / 15))
        reject_button.clicked.connect(self.reject_request)

        cancel_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.setMinimumHeight(int(parent.height / 15))
        cancel_button.clicked.connect(self.close)

        layout = QGridLayout()

        layout.addWidget(self.list_requests, 0, 0, 5, 1)
        layout.addWidget(accept_button, 0, 1)
        layout.addWidget(reject_button, 1, 1)
        layout.addWidget(cancel_button, 2, 1)

        self.model = QStringListModel()
        self.model.setStringList(requests)
        self.list_requests.setModel(self.model)
        self.setLayout(layout)
        self.resize(self.width, self.height)
        self.setWindowTitle("View Requests")

    def accept_request(self):
        if not self.list_requests.selectedIndexes():
            alert(WARNING, WARNING, NO_INDEX_SELECTED, parent=self)
            return

        idx = self.list_requests.selectedIndexes()[0]
        username = self.model.itemData(idx)[0]
        ret = self.client.answer_request(username, self.group, Answer.ACCEPT)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return
        if ret == ReturnCodes.CONNECTION_ERROR:
            alert(ERROR, ERROR, CONNECTION_ERROR, parent=self)
            return
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return
        alert(SUCCESS, SUCCESS, "request accepted", parent=self)
        self.refresh_list()
        self.parent.refresh_users_list()

    def reject_request(self):
        if not self.list_requests.selectedIndexes():
            alert(WARNING, WARNING, NO_INDEX_SELECTED, parent=self)
            return

        idx = self.list_requests.selectedIndexes()[0]
        username = self.model.itemData(idx)[0]
        ret = self.client.answer_request(username, self.group, Answer.DENY)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return
        if ret == ReturnCodes.CONNECTION_ERROR:
            alert(ERROR, ERROR, CONNECTION_ERROR, parent=self)
            return
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return
        alert(SUCCESS, SUCCESS, "request reejected", parent=self)
        self.refresh_list()

    def refresh_list(self):
        ret, requests = self.client.get_requests(self.group)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        if ret == ReturnCodes.SUCCESS:
            self.model.setStringList(requests)


class ViewGroup(QDialog):
    def __init__(self, group_name, group_members, santa_client=None, parent=None):
        super(ViewGroup, self).__init__(parent)
        self.setModal(True)

        self.parent = parent
        self.client = santa_client
        self.width = parent.width
        self.height = parent.height
        self.group_name = group_name
        self.admin_view = self.client.if_admin()

        self.list_members = QListView()
        self.list_members.setStyleSheet(GROUP_LIST_VIEW_SS)
        self.list_members.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_members.setMaximumWidth(int(2 * parent.width / 3))

        self.model = QStringListModel()
        self.model.setStringList(group_members)
        self.list_members.setModel(self.model)

        group_name_label = QLabel(text=group_name)
        group_name_label.setStyleSheet(GROUP_NAME_SS)

        close_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
        close_button.setMaximumWidth(int(parent.width / 10))
        close_button.setMinimumHeight(int(parent.height / 15))
        close_button.clicked.connect(self.exit)

        self.layout = QGridLayout()
        self.layout.addWidget(group_name_label, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.list_members, 1, 0, 10, 1)

        self.join_button = None

        if self.admin_view:
            remove_user_button = auth.TransparentButton(text="Remove User", font_size=10, parent=self)
            remove_user_button.setMaximumWidth(int(parent.width / 10))
            remove_user_button.setMinimumHeight(int(parent.height / 15))
            remove_user_button.clicked.connect(self.remove_user)

            delete_group_button = auth.TransparentButton(text="Delete Group", font_size=10, parent=self)
            delete_group_button.setMaximumWidth(int(parent.width / 10))
            delete_group_button.setMinimumHeight(int(parent.height / 15))
            delete_group_button.clicked.connect(self.delete_group)

            send_emails_button = auth.TransparentButton(text="Send Emails", font_size=10, parent=self)
            send_emails_button.setMaximumWidth(int(parent.width / 10))
            send_emails_button.setMinimumHeight(int(parent.height / 15))
            send_emails_button.clicked.connect(self.send_emails)

            join_requests_button = auth.TransparentButton(text="Join Requests", font_size=10, parent=self)
            join_requests_button.setMaximumWidth(int(parent.width / 10))
            join_requests_button.setMinimumHeight(int(parent.height / 15))
            join_requests_button.clicked.connect(self.see_requests)

            self.layout.addWidget(join_requests_button, 2, 1)
            self.layout.addWidget(remove_user_button, 3, 1)
            self.layout.addWidget(delete_group_button, 4, 1)
            self.layout.addWidget(send_emails_button, 5, 1)
        else:
            if self.client.check_if_in_group(group_name):
                self.add_leave_button()
            else:
                join_group_button = auth.TransparentButton(text="Join group", font_size=10, parent=self)
                join_group_button.setMaximumWidth(int(parent.width / 5))
                join_group_button.setMinimumHeight(int(parent.height / 15))
                join_group_button.clicked.connect(self.join_group)
                self.join_button = join_group_button
                self.layout.addWidget(join_group_button, 5, 1)

        self.layout.addWidget(close_button, 8, 1)

        self.setLayout(self.layout)
        self.setWindowTitle("Group " + group_name)
        self.resize(self.width, self.height)

    def join_group(self):
        if self.client.check_if_in_group(self.group_name):
            alert(WARNING, WARNING, ALREADY_IN_GROUP, parent=self)
            return
        joiner = Joiner(self.group_name, santa_client=self.client, parent=self)
        joiner.show()

    def add_leave_button(self):
        leave_group_button = auth.TransparentButton(text="Leave group", font_size=10, parent=self)
        leave_group_button.setMaximumWidth(int(self.parent.width / 5))
        leave_group_button.setMinimumHeight(int(self.parent.height / 15))
        leave_group_button.clicked.connect(self.leave_group)
        if self.join_button:
            self.join_button.deleteLater()
        self.layout.addWidget(leave_group_button, 5, 1)

    def refresh_users_list(self):
        ret, group = self.client.get_group(self.group_name)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent)
            self.close()

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        if ret == ReturnCodes.SUCCESS:
            self.model.setStringList(group)

    def remove_user(self):
        if not self.list_members.selectedIndexes():
            alert(WARNING, WARNING, NO_INDEX_SELECTED, parent=self)
            return
        idx = self.list_members.selectedIndexes()[0]
        username = self.model.itemData(idx)[0]
        ret = self.client.remove_user(username, self.group_name)
        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.INVALID_USER:
            alert(ERROR, ERROR, INVALID_DELETE_USER, parent=self)
            return

        if ret == ReturnCodes.NOT_ADMIN:
            alert(WARNING, WARNING, NOT_ADMIN, parent=self)
            return

        if ret == ReturnCodes.YOU_ADMIN:
            alert(WARNING, WARNING, YOU_ADMIN, parent=self)
            return

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        if ret == ReturnCodes.SUCCESS:
            alert(SUCCESS, SUCCESS, REMOVE_USER_SUCCESS, parent=self)
            self.refresh_users_list()

    def delete_group(self):
        ret = self.client.delete_group(self.group_name)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.INVALID_GROUP:
            alert(ERROR, ERROR, INVALID_DELETE_GROUP, parent=self)
            return

        if ret == ReturnCodes.NOT_ADMIN:
            alert(ERROR, ERROR, NOT_ADMIN, parent=self)
            return

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        if ret == ReturnCodes.SUCCESS:
            alert(SUCCESS, SUCCESS, SUCCESSFUL_DELETE_GROUP, parent=self.parent)
            self.parent.refresh_groups_list()
            self.close()

    def send_emails(self):
        ret, templates = self.client.get_templates()
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return
        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self)
            self.return_to_login()
            return
        vt = templates_gui.ViewTemplates(templates_gui.SELECT_TEMPLATE, templates,
                                         client=self.client, parent=self, group=self.group_name)
        vt.show()

    def see_requests(self):
        ret, requests = self.client.get_requests(self.group_name)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent)
            self.close()

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        sr = ViewRequests(requests, client=self.client, parent=self, group=self.group_name)
        sr.show()

    def leave_group(self):
        ret = self.client.exit_group(self.group_name)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self.parent)
            self.close()
            return

        if ret == ReturnCodes.YOU_ADMIN:
            alert(ERROR, ERROR, YOU_ADMIN, parent=self)

        if ret == ReturnCodes.SUCCESS:
            alert(SUCCESS, SUCCESS, LEAVE_GROUP_SUCCESS, parent=self.parent)
            self.close()
            self.refresh_users_list()

    def exit(self):
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
        self.list_groups.setMaximumWidth(int(2 * parent.width / 3))

        self.list_groups.doubleClicked.connect(self.select_group)

        ok_button = auth.TransparentButton(text="View", font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.setMinimumHeight(int(parent.height / 15))
        ok_button.clicked.connect(self.view_group)

        join_button = auth.TransparentButton(text="Join", font_size=10, parent=self)
        join_button.setMaximumWidth(int(parent.width / 10))
        join_button.setMinimumHeight(int(parent.height / 15))
        join_button.clicked.connect(self.join_group)

        cancel_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.setMinimumHeight(int(parent.height / 15))
        cancel_button.clicked.connect(self.cancel)

        layout = QGridLayout()

        layout.addWidget(self.list_groups, 0, 0, 4, 1)
        layout.addWidget(ok_button, 0, 1)
        layout.addWidget(join_button, 1, 1)
        layout.addWidget(cancel_button, 2, 1)

        self.model = QStringListModel()
        self.model.setStringList(groups)
        self.list_groups.setModel(self.model)

        self.setLayout(layout)
        self.resize(self.width, self.height)
        self.setWindowTitle("View Groups")

    def refresh_groups_list(self):
        ret, groups = self.client.get_groups()

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent.parent)
            self.close()
            self.parent.return_to_login()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent.parent)
            self.close()
            self.parent.return_to_login()
            return

        self.model.setStringList(groups)

    def select_group(self):
        self.view_group()

    def join_group(self):
        if not self.list_groups.selectedIndexes():
            alert(WARNING, WARNING, NO_INDEX_SELECTED, parent=self)
            return
        idx = self.list_groups.selectedIndexes()[0]
        group_name = self.model.itemData(idx)[0]

        if self.client.check_if_in_group(group_name):
            alert(WARNING, WARNING, ALREADY_IN_GROUP, parent=self)
            return

        joiner = Joiner(group_name, outer_join=True, santa_client=self.client, parent=self)
        joiner.show()

    def cancel(self):
        self.close()

    def view_group(self):
        if not self.list_groups.selectedIndexes():
            alert(WARNING, WARNING, NO_INDEX_SELECTED, parent=self)
            return
        idx = self.list_groups.selectedIndexes()[0]
        group_name = self.model.itemData(idx)[0]
        ret, group = self.client.get_group(group_name)

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent)
            self.close()
            self.parent.return_to_login()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.parent)
            self.close()
            self.parent.return_to_login()

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        vg = ViewGroup(group_name, group, santa_client=self.client, parent=self)
        vg.show()
