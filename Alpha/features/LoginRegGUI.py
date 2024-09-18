import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Login/Regester')

        layout = QVBoxLayout()

        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText('Enter your Email Id')
        layout.addWidget(self.emailInput)

        self.operationInput = QComboBox()
        self.operationInput.addItem('Login')
        self.operationInput.addItem('Regester')
        layout.addWidget(self.operationInput)

        self.loginButton = QPushButton('Submit')
        self.loginButton.clicked.connect(self.submitOperation)
        layout.addWidget(self.loginButton)

        self.setLayout(layout)

    def submitOperation(self):
        email = self.emailInput.text()
        operation = self.operationInput.currentText()

        if operation == 'Login':
            # Call your login function here
            print(f'Login with email: {email}')
        elif operation == 'Regester':
            # Call your regester function here
            print(f'Regester with email: {email}')

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()