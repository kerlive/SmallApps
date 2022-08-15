# PyQt5 Demo
#code by kevin

import os, sys

import random
import UIResource_rc

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic, QtCore

ui_path = os.path.dirname(os.path.abspath(__file__))
form_1, base_1 = uic.loadUiType(os.path.join(ui_path,"Reg.ui"))

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


class Main(moveWidget, form_1):
    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)
        
        self.setWindowIcon(QtGui.QIcon(':/icon/UIelement/key.ico'))
        #QtCore set FramelessWindow
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #QtCore set alpha background
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # A sample algorithm

        self.lineEdit.setText("aSlKFJdaL0123")
        self.lineEdit.setInputMask('aaa-aaa-aaa-000')
        self.pushButton.clicked.connect(self.register)      
        self.closeButton.clicked.connect(self.exit)


    def register(self):

        alp0 = chr(random.randint(ord('a'), ord('z'))) + chr(random.randint(ord('o'), ord('x'))) + chr(random.randint(ord('c'), ord('y')))
        alp1 = chr(random.randint(ord('A'), ord('K'))) + chr(random.randint(ord('O'), ord('X'))) + chr(random.randint(ord('c'), ord('y')))
        alp2 = chr(random.randint(ord('Y'), ord('Z'))) + chr(random.randint(ord('o'), ord('x'))) + chr(random.randint(ord('c'), ord('y')))
        
        nmb = int(random.uniform(100,999))
        
        
        self.lineEdit.setText(str(alp0) + str(alp1) + str(alp2) + str(nmb))

    def exit(self):
        sys.exit(1)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    demo = Main()
    demo.show()
    
    sys.exit(app.exec_())
