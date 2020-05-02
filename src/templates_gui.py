from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from alerts import *
from utils import ReturnCodes
import auth

TEMPLATE_LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230);" \
                             "background: none;"
TEMPLATE_CREATE_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,100);"
TEMPLATE_TEXT_EDIT_SS = "color:white; border: none; background: rgba(0,0,0,100);"
TEMPLATE_LIST_VIEW_SS = "color:white; border: none; font-size: 18px; background: rgba(0,0,0,100); "
TEMPLATE_TEXT_BROWSER_SS = "border-image: none; font-size: 14px; border: none; " \
                           "color: white; background: rgba(0,0,0,50);"
TEMPLATE_DIALOG_SS = 'border-image: url("style/form-background.jpg"); background-repeat: no-repeat;' \
                     ' background-position: center;'

JUST_VIEW = 'V'
SELECT_TEMPLATE = 'S'


class CreateTemplateGUI(QDialog):
    def __init__(self, parent=None, client=None):
        super(CreateTemplateGUI, self).__init__(parent)
        self.setModal(True)

        self.parent = parent
        self.client = client
        self.template_max_length = MAX_TEMPLATE_LENGTH

        self.edit_template_name = QLineEdit()
        self.edit_template_name.setStyleSheet(TEMPLATE_CREATE_LINEEDIT_SS)
        self.edit_template_name.setMinimumWidth(int(parent.width / 3))

        label_template_name = QLabel()
        label_template_name.setStyleSheet(TEMPLATE_LABEL_STYLE_SHEET)
        label_template_name.setText("Template Name: ")
        label_template_name.setBuddy(self.edit_template_name)

        self.edit_text = QTextEdit()
        self.edit_text.setStyleSheet(TEMPLATE_TEXT_EDIT_SS)

        ok_button = auth.TransparentButton(text="Create", font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.setMinimumHeight(int(parent.height / 15))
        ok_button.clicked.connect(self.create_template)

        cancel_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.setMinimumHeight(int(parent.height / 15))
        cancel_button.clicked.connect(self.cancel)

        layout = QGridLayout()
        layout.addWidget(label_template_name, 0, 0)
        layout.addWidget(self.edit_template_name, 0, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(self.edit_text, 2, 0, 1, 2)
        layout.addWidget(ok_button, 3, 0)
        layout.addWidget(cancel_button, 3, 1)

        self.setLayout(layout)
        self.resize(int(3 * parent.width / 4), int(3 * parent.height / 4))
        self.width = 3 * parent.width / 4
        self.height = 3 * parent.height / 4
        self.setWindowTitle("Create Template")

    def limit_text(self):
        text = self.edit_text.toPlainText()
        t_len = len(text)
        if t_len == 0:
            alert(WARNING, WARNING, TEMPLATE_TEXT_NULL, parent=self)
            self.edit_text.setFocus()
            return False
        if t_len > self.template_max_length:
            alert(WARNING, "Maximum size violation", "Your template is too large, "
                  + str(t_len) + " characters, keep a maximum of " + str(self.template_max_length) +
                  " characters", parent=self)
            return False
        return True

    def create_template(self):
        if self.edit_template_name.text() == "":
            alert(WARNING, WARNING, TEMPLATE_NAME_NULL, parent=self)
            self.edit_template_name.setFocus()
            return
        if self.limit_text():
            ret = self.client.create_template(self.edit_template_name.text(), self.edit_text.toPlainText())
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
            if ret == ReturnCodes.USED_TEMPLATE_NAME:
                alert(WARNING, WARNING, USED_NAME, parent=self)
            if ret == ReturnCodes.UNKNOWN_ERROR:
                alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            if ret == ReturnCodes.SUCCESS:
                alert(SUCCESS, SUCCESS, TEMPLATE_CREATE_SUCCESS, parent=self.parent)
                self.close()

    def cancel(self):
        self.close()


class EditTemplate(QDialog):
    def __init__(self, template_name, template, client=None, parent=None, group=None):
        super(EditTemplate, self).__init__(parent)
        self.setModal(True)

        self.selected_template = template
        self.selected_template_name = template_name
        self.group = group
        self.parent = parent
        self.client = client

        self.text_box = QTextEdit()
        self.text_box.setText(template)
        self.text_box.setFocus()
        self.text_box.setStyleSheet(TEMPLATE_TEXT_BROWSER_SS)

        cancel_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(self.parent.width / 10))
        cancel_button.setMinimumHeight(int(self.parent.height / 15))
        cancel_button.clicked.connect(self.close)

        send_button = auth.TransparentButton(text="Send emails", font_size=10, parent=self)
        send_button.setMaximumWidth(int(self.parent.width / 5))
        send_button.setMinimumHeight(int(self.parent.height / 15))
        send_button.clicked.connect(self.send_emails)

        layout = QGridLayout()
        layout.addWidget(self.text_box, 0, 0, 1, 3)
        layout.addWidget(send_button, 1, 0)
        layout.addWidget(cancel_button, 1, 1)
        self.setLayout(layout)
        self.width = int(3 * self.parent.width / 4)
        self.height = int(3 * self.parent.height / 4)
        self.resize(self.width, self.height)
        self.setWindowTitle("Template " + template_name)

    def send_emails(self):
        changed = self.text_box.toPlainText() != self.selected_template
        if changed:
            ret = self.client.send_emails(self.group, text_template=self.text_box.toPlainText(), flag=True)
        else:
            ret = self.client.send_emails(self.group, template_name=self.selected_template_name, flag=False)
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self)
            return
        if ret == ReturnCodes.WAIT:
            alert(WARNING, WARNING, EMAILS_ALREADY_SENT, parent=self.parent.parent)
            self.close()
            self.parent.close()
            return
        if ret == ReturnCodes.CONNECTION_ERROR:
            alert(ERROR, ERROR, CONNECTION_ERROR, parent=self.parent.parent)
            self.close()
            self.parent.close()
            return
        if ret == ReturnCodes.SUCCESS:
            alert(SUCCESS, SUCCESS, SUCCESSFUL_SEND_REQUEST, parent=self.parent.parent)
            self.close()
            self.parent.close()


class ViewTemplates(QDialog):
    def __init__(self, view_type, templates, client=None, parent=None, group=None):
        super(ViewTemplates, self).__init__(parent)
        self.setModal(True)

        self.parent = parent
        self.client = client
        self.width = parent.width
        self.height = parent.height
        self.type = view_type
        self.selected_template_name = ""
        self.selected_template = ""
        self.text_box = None
        self.group = group

        self.list_templates = QListView()
        self.list_templates.setStyleSheet(TEMPLATE_LIST_VIEW_SS)
        self.list_templates.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_templates.setMaximumWidth(int(2 * parent.width / 3))

        ok_button = auth.TransparentButton(text="View", font_size=10, parent=self)
        if self.type == SELECT_TEMPLATE:
            ok_button.setText("Select")
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.setMinimumHeight(int(parent.height / 15))

        if self.type == SELECT_TEMPLATE:
            ok_button.clicked.connect(self.edit_template)
            self.list_templates.doubleClicked.connect(self.edit_template)
        else:
            ok_button.clicked.connect(self.view_template)
            self.list_templates.doubleClicked.connect(self.view_template)

        cancel_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.setMinimumHeight(int(parent.height / 15))
        cancel_button.clicked.connect(self.cancel)

        layout = QGridLayout()

        layout.addWidget(self.list_templates, 0, 0, 4, 1)
        layout.addWidget(ok_button, 0, 1)
        layout.addWidget(cancel_button, 1, 1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_list)
        self.timer.start(REFRESH_INTERVAL)

        self.model = QStringListModel()
        self.model.setStringList(templates)
        self.list_templates.setModel(self.model)
        self.setLayout(layout)
        self.resize(self.width, self.height)
        self.setWindowTitle("View Templates")

    def refresh_list(self):
        ret, templates = self.client.get_templates()
        if ret == ReturnCodes.UNKNOWN_ERROR:
            alert(WARNING, MI_SCUZI, UNKNOWN_ERROR_TEXT, parent=self.parent)
            self.close()
            return
        if ret == ReturnCodes.NOT_AUTH:
            alert(ERROR, ERROR, NOT_AUTH, parent=self.parent.parent)
            self.close()
            self.parent.return_to_login()
            return
        self.model.setStringList(templates)

    def cancel(self):
        self.close()

    def edit_template(self):
        if not self.list_templates.selectedIndexes():
            alert(WARNING, WARNING, NO_INDEX_SELECTED, parent=self)
            return
        idx = self.list_templates.selectedIndexes()[0]
        data = self.model.itemData(idx)[0]
        ret, template = self.client.get_template(data)

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

        et = EditTemplate(data, template, self.client, self, self.group)
        et.show()

    def view_template(self):
        if not self.list_templates.selectedIndexes():
            alert(WARNING, WARNING, NO_INDEX_SELECTED, parent=self)
            return
        idx = self.list_templates.selectedIndexes()[0]
        data = self.model.itemData(idx)[0]
        ret, template = self.client.get_template(data)

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

        qd = QDialog(parent=self)
        qd.setStyleSheet(TEMPLATE_DIALOG_SS)

        tb = QTextBrowser()
        tb.setText(template)

        cancel_button = auth.TransparentButton(text="Back", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(self.width / 10))
        cancel_button.setMinimumHeight(int(self.parent.height / 15))
        cancel_button.clicked.connect(qd.close)

        tb.setStyleSheet(TEMPLATE_TEXT_BROWSER_SS)
        layout = QVBoxLayout()
        layout.addWidget(tb)
        layout.addWidget(cancel_button)
        qd.setLayout(layout)
        qd.resize(int(3 * self.width / 4), int(3 * self.height / 4))
        qd.setWindowTitle("Template " + data)
        qd.show()
        pass
