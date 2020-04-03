from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit("Type an expression and press Enter")
        self.lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.lineedit.returnPressed.connect(self.updateUi)
        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = self.lineedit.text()
            self.browser.append("%s = <b>%s</b>" % (text, eval(text)))
        except:
            self.browser.append("<font color=red>%s is invalid!</font>" % text)

app = QApplication([])
form = Form()
form.show()
app.exec_()

"""
def on_click():
    alert = QMessageBox()
    alert.setText('You fucked up,boi!')
    alert.exec_()

app = QApplication([])
app.setStyle('Fusion')

h = QDesktopWidget.screenGeometry(app.desktop()).height()
w = QDesktopWidget.screenGeometry(app.desktop()).width()

window = QMainWindow()
window.resize(w / 2, h / 2)

form = FormWidget

layout = QVBoxLayout()
button_top = QPushButton('Top')
button_top.clicked.connect(on_click)
layout.addWidget(button_top)
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec_()
"""
