from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from client import *
from alerts import *
import auth
import groups_gui
import templates_gui


class Dashboard(QDialog):
    def __init__(self, width=480, height=540, papa=None, client=None):
        super(Dashboard, self).__init__()
        self.width = width
        self.height = height

        self.papa = papa
        self.client = client

        self.create_group_button = auth.TransparentButton("Create Group")
        self.view_groups_button = auth.TransparentButton("View Groups")
        self.create_template_button = auth.TransparentButton("Create Template")
        self.view_templates_button = auth.TransparentButton("View Templates")
        self.exit_button = auth.TransparentButton("Logout")
        self.set_buttons()

        unsername_label = QLabel("User: " + self.client.username)
        unsername_label.setStyleSheet("color:white; font-size:18px")

        layout = QGridLayout()
        layout.addWidget(self.create_group_button, 0, 0)
        layout.addWidget(self.create_template_button, 0, 1)
        layout.addWidget(self.view_groups_button, 1, 0)
        layout.addWidget(self.view_templates_button, 1, 1)
        layout.addWidget(self.exit_button, 2, 1, alignment=Qt.AlignRight)
        layout.addWidget(unsername_label, 2, 0)
        self.setLayout(layout)
        self.resize(width, height)
        self.setWindowTitle("Dashboard")

    def set_buttons(self):
        self.create_group_button.setMinimumHeight(int(self.height / 10))
        self.view_groups_button.setMinimumHeight(int(self.height / 10))
        self.create_template_button.setMinimumHeight(int(self.height / 10))
        self.view_templates_button.setMinimumHeight(int(self.height / 10))
        self.exit_button.setMaximumHeight(int(self.height / 20))

        self.create_group_button.setMaximumWidth(int(self.width / 5))
        self.view_groups_button.setMaximumWidth(int(self.width / 5))
        self.create_template_button.setMaximumWidth(int(self.width / 5))
        self.view_templates_button.setMaximumWidth(int(self.width / 5))

        self.create_group_button.clicked.connect(self.create_group)
        self.create_template_button.clicked.connect(self.create_template)
        self.view_templates_button.clicked.connect(self.view_templates)
        self.view_groups_button.clicked.connect(self.view_groups)
        self.exit_button.clicked.connect(self.return_to_login)

    def create_group(self):
        cg = groups_gui.CreateGroupGUI(parent=self, santa_client=self.client)
        cg.show()

    def create_template(self):
        ct = templates_gui.CreateTemplateGUI(parent=self, client=self.client)
        ct.show()

    def view_templates(self):
        ret, templates = self.client.get_templates()
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return
        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self)
            self.return_to_login()
            return
        vt = templates_gui.ViewTemplates(templates_gui.JUST_VIEW, templates, parent=self, client=self.client)
        vt.show()

    def view_groups(self):
        ret, groups = self.client.get_groups()

        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return

        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.papa)
            self.return_to_login()
            return

        if ret == ReturnCodes.RELOGIN:
            alert(ERROR, ERROR, RELOGIN_ERR, parent=self.papa)
            self.return_to_login()
            return

        vg = groups_gui.ViewGroups(groups, parent=self, client=self.client)
        vg.show()

    def return_to_login(self):
        self.client.logout()
        self.papa.show()
        self.close()
