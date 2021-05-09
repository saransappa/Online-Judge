from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
import sys
import socket


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def button_clicked(self):
        self.label.setText("you pressed the button")
        self.update()

    def initUI(self):
        self.setGeometry(20,50,800,950)
        self.setWindowTitle("Online Judge Code Submission")

        self.roll_label = QtWidgets.QLabel(self)
        self.roll_label.setText("Roll Number : ")
        self.roll_label.move(50,50)

        self.roll = QtWidgets.QTextEdit(self)
        self.roll.move(200,50)


        self.questions = QtWidgets.QComboBox(self)
        self.questions.setEditable(False)
        self.questions.adjustSize()
        self.questions.move(200,150)
        
        self.get_ques = QtWidgets.QPushButton(self)
        self.get_ques.move(400,150)
        self.get_ques.setText("Get Questions")
        self.obtained_questions = False # A boolean to check if GET Questions is pressed at least once
        self.get_ques.clicked.connect(self.get_questions)


        self.question_label = QtWidgets.QLabel(self)
        self.question_label.setText("Question : ")
        self.question_label.adjustSize()
        self.question_label.move(50,150)

        self.view = QtWidgets.QPushButton(self)
        self.view.move(200,175)
        self.view.setText("View Question")
        self.view.adjustSize()
        self.view.clicked.connect(self.view_question)

        self.show_question = QtWidgets.QPlainTextEdit(self)
        self.show_question.move(150,230)
        self.show_question.setVisible(False)

        self.prog_language = QtWidgets.QLabel(self)
        self.prog_language.setText("Programming Language : ")
        self.prog_language.adjustSize()
        self.prog_language.move(50,450)

        languages = ["","Python3","C++"]
        self.lang = QtWidgets.QComboBox(self)
        self.lang.setEditable(False)
        self.lang.addItems(languages)
        self.lang.adjustSize()
        self.lang.move(200,450)

        self.file_label = QtWidgets.QLabel(self)
        self.file_label.setText("Code File : ")
        self.file_label.adjustSize()
        self.file_label.move(50,550)

        self.file_name_label  = QtWidgets.QLabel(self)
        self.file_name_label.setText("No files chosen")
        self.file_name_label.move(200,550)

        self.file_chosen = ""
        self.browse = QtWidgets.QPushButton(self)
        self.browse.move(550,550)
        self.browse.setText("Browse...")
        self.browse.clicked.connect(self.open_file)

        self.submit = QtWidgets.QPushButton(self)
        self.submit.move(300,650)
        self.submit.setText("Submit Code")
        self.submit.clicked.connect(self.submit_file)

        self.status_label  = QtWidgets.QLabel(self)
        self.status_label.setText("Submission Status:")
        self.status_label.move(200,750)
        self.status_label.adjustSize()


        self.status = QtWidgets.QLabel(self)
        self.status.move(350,750)
        self.status.setText("")

        self.close = QtWidgets.QPushButton(self)
        self.close.move(300,850)
        self.close.setText("Close")
        self.close.clicked.connect(self.close_application)

    def open_file(self):
        self.status.setText("")
        self.file_name_label.setText("")
        self.status.adjustSize()
        self.file_chosen,_ = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                        'All Files (*.*)')
        if self.file_chosen:
            #print("File path : "+ self.file_chosen)
            self.file_name_label.setText(str(self.file_chosen))
            self.file_name_label.adjustSize() 

    def get_questions(self):
        s = socket.socket()
        s.connect(("localhost",9999))
        s.send("GET".encode('utf-8'))
        z = s.recv(2048).decode('utf-8')
        self.questions.clear()
        self.questions.addItems(z.split(","))
        self.questions.adjustSize()
        self.obtained_questions = True

    def view_question(self):
        s = socket.socket()
        s.connect(("localhost",9999))
        print(self.questions.currentText())
        s.send(f"VIEW{self.questions.currentText()}".encode('utf-8'))
        z = s.recv(2048).decode('utf-8')
        print(z)
        self.show_question.setPlainText(z)
        self.show_question.adjustSize()
        self.show_question.setVisible(True)

    def submit_file(self):
        if self.roll.toPlainText().replace(" ","")=="":
            self.status.setText("Please enter Roll Number.")
            self.status.adjustSize()
            return 
        if not self.obtained_questions:
            self.status.setText("Please select a question by clicking \"Get Questions\".")
            self.status.adjustSize()
            return
        print(self.roll.toPlainText())
        s = socket.socket()
        s.connect(("localhost",9999))
        print(self.roll.toPlainText())
       
        s.send(str(self.roll.toPlainText().replace(" ","")).encode('utf-8'))
        z = s.recv(12).decode('utf-8')
        print(z)
        
         
        s.send(str(self.questions.currentText()).encode('utf-8'))
        z = s.recv(20).decode('utf-8')
        print(z)
        print(self.lang.currentText())
        if self.lang.currentText().replace(" ","")=="":
            self.status.setText("Please select a Programming language.")
            self.status.adjustSize()
            return
        s.send(str(self.lang.currentText()).encode('utf-8'))
        z = s.recv(13).decode('utf-8') 
        print(z)
        print(self.file_chosen)
        try:
            f = open (self.file_chosen, "rb")
        except:
            self.status.setText("Please select a valid code file.")
            self.status.adjustSize()
            return
        l = f.read()
        while (l):
            s.send(l)
            l = f.read(10)
        s.shutdown(socket.SHUT_WR)
        z = s.recv(1024).decode('utf-8')
        print(z)
        z = s.recv(1024).decode('utf-8')
        print(z)
        s.close()
        self.status.setText(z.title())
        self.status.adjustSize()
    def update(self):
        self.label.adjustSize()

    def close_application(self):
        sys.exit(0)

def window():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
