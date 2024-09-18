from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import time
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Alpha")
        MainWindow.resize(810, 582)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 810, 582))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("live_wallpaper.gif"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(500, 430, 101, 51))
        self.pushButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 75 18pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("RunButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 430, 101, 51))
        self.pushButton_2.setStyleSheet("background-color:rgb(255, 0, 0);\n"
"font: 75 18pt \"MS Shell Dlg 2\";")
        self.pushButton_2.setObjectName("ExitButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 401, 91))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("initiating.gif"))
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 120, 791, 291))
        self.textBrowser.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";\n"
"background-color:transparent;\ncolor:white;"
"border-radius:none;")
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 420, 481, 61))
        self.lineEdit.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";\n"
"background-color:transparent;\ncolor:white;"
"border-radius:none;")
        self.lineEdit.setObjectName("lineEdit")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(500, 420, 101, 61))
        self.sendButton.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 75 18pt \"MS Shell Dlg 2\";")
        self.sendButton.setObjectName("sendButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.startChat)
        self.sendButton.clicked.connect(self.sendMessage)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Run"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.sendButton.setText(_translate("MainWindow", "Send"))

    def startChat(self):
        self.pushButton.setEnabled(False)
        self.sendButton.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.textBrowser.append("Chat started. Type 'exit' to quit.")

    def sendMessage(self):
        message = self.lineEdit.text()
        if message.lower() == 'exit':
            self.textBrowser.append("Chat ended.")
            self.sendButton.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(True)
        else:
            self.textBrowser.append("You: " + message)
            self.lineEdit.clear()
            # Here you can add your chatbot's response
            response = self.get_response(message)
            self.textBrowser.append("Bot: " + response)

    def get_response(self, message):
        # This is a very basic response system. You can improve it by using machine learning models or more complex logic.
        responses = {
            "hello": "Hi, how are you?",
            "hi": "Hello, how can I assist you?",
            "how are you": "I'm good, thanks. How about you?",
            "what is your name": "My name is Alpha, I'm a chatbot.",
            "default": "I didn't understand that. Can you please rephrase?"
        }
        message = message.lower()
        for key in responses:
            if key in message:
                return responses[key]
        return responses["default"]

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())