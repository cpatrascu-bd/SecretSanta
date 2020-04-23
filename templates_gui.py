from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import auth

TEMPLATE_LABEL_STYLE_SHEET = " font-weight: bold; font-size: 14px; color: rgb(230,230,230);" \
                             "background: none;"
TEMPLATE_CREATE_LINEEDIT_SS = "color: white; font-weight: bold; background: rgba(0,0,0,100);"
TEMPLATE_TEXT_EDIT_SS = "color:white; border: none; background: rgba(0,0,0,100);"
TEMPLATE_LIST_VIEW_SS = "color:white; border: none; background: rgba(0,0,0,100);"
TEMPLATE_TEXT_BROWSER_SS = "border-image: none; border: none; color: white; background: rgba(0,0,0,50);";
TEMPLATE_DIALOG_SS = 'border-image: url("form-background.jpg"); background-repeat: no-repeat;' \
                                                                ' background-position: center;'


class CreateTemplateGUI(QDialog):
    def __init__(self, client=None, parent=None):
        super(CreateTemplateGUI, self).__init__(parent)

        self.parent = parent
        self.client = client
        self.template_max_length = 28

        self.edit_template_name = QLineEdit()
        self.edit_template_name.setStyleSheet(TEMPLATE_CREATE_LINEEDIT_SS)
        self.edit_template_name.setMinimumWidth(int(parent.width / 3))

        label_template_name = QLabel()
        label_template_name.setStyleSheet(TEMPLATE_LABEL_STYLE_SHEET)
        label_template_name.setText("Template Name: ")
        label_template_name.setBuddy(self.edit_template_name)

        self.edit_text = QTextEdit()
        self.setStyleSheet(TEMPLATE_TEXT_EDIT_SS)

        ok_button = Auth.TransparentButton(text="Create", font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.clicked.connect(self.create_template)

        cancel_button = Auth.TransparentButton(text="Cancel", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.clicked.connect(self.cancel)

        layout = QGridLayout()
        layout.addWidget(label_template_name, 0, 0)
        layout.addWidget(self.edit_template_name, 0, 1, alignment=Qt.AlignHCenter)
        layout.addWidget(self.edit_text, 2, 0, 1, 2)
        layout.addWidget(ok_button, 3, 0)
        layout.addWidget(cancel_button, 3, 1)

        self.setLayout(layout)
        self.resize(int(3 * parent.width / 4), int(3 * parent.height / 4))
        self.setWindowTitle("Create Template")

    def limit_text(self):
        text = self.edit_text.toPlainText()
        t_len = len(text)
        if t_len > self.template_max_length:
            Auth.alert(Auth.WARNING,"Maximum size violation", "Yout template is too large, "
                      +str(t_len)+" characters, keep a maximum of " + str(self.template_max_length) +
                          " characters")
            return False
        return True

    def create_template(self):
        if not self.limit_text():
            pass

    def cancel(self):
        self.close()

class ViewTemplates(QDialog):
    def __init__(self, client=None, parent=None):
        super(ViewTemplates, self).__init__(parent)

        self.parent = parent
        self.client = client
        self.width = parent.width
        self.height = parent.height

        self.list_templates = QListView()
        self.list_templates.setStyleSheet(TEMPLATE_LIST_VIEW_SS)
        self.list_templates.setEditTriggers(QAbstractItemView.NoEditTriggers)

        ok_button = Auth.TransparentButton(text="View", font_size=10, parent=self)
        ok_button.setMaximumWidth(int(parent.width / 10))
        ok_button.clicked.connect(self.view_template)

        cancel_button = Auth.TransparentButton(text="Cancel", font_size=10, parent=self)
        cancel_button.setMaximumWidth(int(parent.width / 10))
        cancel_button.clicked.connect(self.cancel)

        layout = QGridLayout()

        layout.addWidget(self.list_templates, 0, 0, 4, 1)
        layout.addWidget(ok_button,0,1)
        layout.addWidget(cancel_button,1,1)

        self.model = QStringListModel()
        self.model.setStringList(["hehe","hihi","huhu"])
        self.list_templates.setModel(self.model)
        self.setLayout(layout)
        self.resize(self.width, self.height)
        self.setWindowTitle("View Templates")


    def cancel(self):
        self.close()

    def view_template(self):
        idx = self.list_templates.selectedIndexes()[0]
        data = self.model.itemData(idx)[0]
        print(data)
        tb = QTextBrowser()
        tb.setText("fasdffdsfasdfdsfadsfdsfsdfds")

        qd = QDialog(parent=self)
        qd.setStyleSheet(TEMPLATE_DIALOG_SS)
        tb.setStyleSheet(TEMPLATE_TEXT_BROWSER_SS)
        layout = QVBoxLayout()
        layout.addWidget(tb)
        qd.setLayout(layout)
        qd.resize(int(3*self.width/4), int(3*self.height/4))
        qd.setWindowTitle("Template "+data)
        qd.show()

        pass
