from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import Auth
import Groups_GUI
import Templates_GUI


class Dashboard(QDialog):
    def __init__(self, width=480, height=540, parent=None):
        super(Dashboard, self).__init__(parent)
        self.width = width
        self.height = height

        self.create_group_button = Auth.TransparentButton("Create Group")
        self.view_groups_button = Auth.TransparentButton("View Groups")
        self.create_template_button = Auth.TransparentButton("Create Template")
        self.view_templates_button = Auth.TransparentButton("View Templates")
        self.exit_button = Auth.TransparentButton("Exit")
        self.set_buttons()

        layout = QGridLayout()
        layout.addWidget(self.create_group_button, 0, 0)
        layout.addWidget(self.create_template_button, 0, 1)
        layout.addWidget(self.view_groups_button, 1, 0)
        layout.addWidget(self.view_templates_button, 1, 1)
        layout.addWidget(self.exit_button, 2, 1, alignment=Qt.AlignRight)
        self.setLayout(layout)
        self.resize(width, height)
        self.setWindowTitle("Dashboard")

    def set_buttons(self):
        self.create_group_button.setMinimumHeight(int(self.height / 10))
        self.view_groups_button.setMinimumHeight(int(self.height / 10))
        self.create_template_button.setMinimumHeight(int(self.height / 10))
        self.view_templates_button.setMinimumHeight(int(self.height / 10))
        self.exit_button.setMaximumHeight(int(self.height / 30))

        self.create_group_button.setMaximumWidth(int(self.width / 5))
        self.view_groups_button.setMaximumWidth(int(self.width / 5))
        self.create_template_button.setMaximumWidth(int(self.width / 5))
        self.view_templates_button.setMaximumWidth(int(self.width / 5))

        self.create_group_button.clicked.connect(self.create_group)
        self.create_template_button.clicked.connect(self.create_template)
        self.view_templates_button.clicked.connect(self.view_templates)
        self.exit_button.clicked.connect(self.exit)

    def create_group(self):
        cg = Groups_GUI.CreateGroupGUI(parent=self)
        cg.show()

    def create_template(self):
        ct = Templates_GUI.CreateTemplateGUI(parent=self)
        ct.show()

    def view_templates(self):
        vt = Templates_GUI.ViewTemplates(parent=self)
        vt.show()

    def exit(self):
        self.close()