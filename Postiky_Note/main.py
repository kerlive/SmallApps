# PyQt5 PostIt Notes
#code by kevin

__author__ = "_My_Software_"
__copyright__ = "Copyright (C) 2022-year Kevin"
__license__ = "MIT or GPL-3.0"
__version__ = "0.0.1"


import os, sys

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import UIresource_rc

ui_dir = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(ui_dir,"UI")

form_0, base_0 = uic.loadUiType(os.path.join(ui_path,"Postiky_Note.ui"))
form_1, base_1 = uic.loadUiType(os.path.join(ui_path,"Note.ui"))

class Postiky_Note(base_0, form_0):
    def __init__(self):
        super(base_0, self).__init__()
        self.setupUi(self)
        #self.setFixedSize(280, 400)
        self.setWindowTitle('PostList')

        self.skNum = 0
        

        self.addButton.clicked.connect(self.dupWidget)

    
    def dupWidget(self):
        self.dup = {self.skNum: self.newNotes()}


    def newNotes(self):
        self.newOne = Notes()
        self.newOne.show()




class moveWidget(base_1):
    def __init__(self):
        super(moveWidget, self).__init__()
    def mousePressEvent(self, event):
        self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


class Notes(moveWidget, form_1):
    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)

        self.colorNum = 0

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.closeButton.clicked.connect(self.close)
        self.colorButton.clicked.connect(self.changeColor)

        self.controlTools.setVisible(False)
        self.invisiableArea.installEventFilter(self)
        self.controlTools.installEventFilter(self)

    def changeColor(self):
        match self.colorNum:
            case 0:
                self.colorNum = 1
                self.label.setStyleSheet('background-color: rgb(228, 249, 224);')
            case 1:
                self.colorNum = 2
                self.label.setStyleSheet('background-color: rgb(255, 228, 241);')
            case 2:
                self.colorNum = 3
                self.label.setStyleSheet('background-color: rgb(242, 230, 255);')
            case 3:
                self.colorNum = 4
                self.label.setStyleSheet('background-color: rgb(226, 241, 255);')
            case 4:
                self.colorNum = 5
                self.label.setStyleSheet('background-color: rgb(243, 242, 241);')
            case 5:
                self.colorNum = 0
                self.label.setStyleSheet('background-color: rgb(255, 247, 209);')
            

            
        

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter:
            self.controlTools.setVisible(True)
            return True
        elif object == self.controlTools and event.type() == QtCore.QEvent.Leave:
            self.controlTools.setVisible(False)
        return False

if __name__ == '__main__':

    app = QApplication(sys.argv)
    demo = Postiky_Note()
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window ...")