# PyQt5 PostIt Notes
#code by kevin

__author__ = "_My_Software_"
__copyright__ = "Copyright (C) 2022-year Kevin"
__license__ = "MIT or GPL-3.0"
__version__ = "0.0.2"


import os, sys


from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import UIresource_rc

ui_dir = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(ui_dir,"UI")

form_0, base_0 = uic.loadUiType(os.path.join(ui_path,"Postiky_Note.ui"))
form_1, base_1 = uic.loadUiType(os.path.join(ui_path,"Note.ui"))

class Postiky_Note(base_0, form_0):
    def __init__(self):
        super(base_0, self).__init__()
        self.setupUi(self)


        self.setWindowTitle('PostList')
        self.setWindowIcon(QtGui.QIcon('./Posit.ico'))

        self.skNum = 1
        self.noteSheet = {}

        self.addButton.clicked.connect(self.newNotes)


        self.listWidget.setFixedWidth(181)
        self.perviewWidget.setMinimumWidth(341)
        self.perviewWidget.setMinimumHeight(311)



    def newNotes(self):
        self.noteSheet[self.skNum] = Notes()
        self.skNum = self.skNum + 1
        print (self.skNum)
        
"""     self.newOne = Notes()
        self.new2 = Notes()
        self.skNum[0] = Notes()
        
        for n in range(1,3):
            self.skNum[n] = Notes()"""




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

        self.closeButton.clicked.connect(self.noteClose)
        self.colorButton.clicked.connect(self.changeColor)

        self.controlTools.setVisible(False)
        self.invisiableArea.installEventFilter(self)
        self.controlTools.installEventFilter(self)

        self.show()

        # effect a blur filler for shadow

        b_blur = QGraphicsBlurEffect()
        b_blur.setBlurRadius(15)
        b_blur.setBlurHints(QGraphicsBlurEffect.QualityHint)

        self.label_2.setGraphicsEffect(b_blur)

        
        # switch
        self.bold = False
        self.italic = False
        self.underline = False
        self.strikeout = False

        # font format
        self.boldButton.clicked.connect(self.setBold)
        self.italicButton.clicked.connect(self.setItalic)
        self.underlineButton.clicked.connect(self.setUnderline)
        self.strikethroughButton.clicked.connect(self.setStrikeout)
        self.togglebulletButton.clicked.connect(self.setBulletpoint)


    def noteClose(self):
        text = self.textEdit.toPlainText()
        if text != '':
            print (text)
            self.close()
        else:
            self.close()

    def setBold(self):
        if self.bold == False:
            self.textEdit.setFontWeight(QtGui.QFont.Bold)
            self.bold = True
            print(self.textEdit.currentCharFormat())
        else:
            self.textEdit.setFontWeight(QtGui.QFont.Normal)
            self.bold = False

    def setItalic(self):
        if self.italic == False:
            self.textEdit.setFontItalic(True)
            self.italic = True
        else:
            self.textEdit.setFontItalic(False)
            self.italic = False

    def setUnderline(self):
        if self.underline == False:
            self.textEdit.setFontUnderline(True)
            self.underline = True
        else:
            self.textEdit.setFontUnderline(False)
            self.underline = False

    def setStrikeout(self):
        if self.strikeout == False:
            format = self.textEdit.currentCharFormat()
            format.setFontStrikeOut(True)
            self.textEdit.setCurrentCharFormat(format)
            self.strikeout = True
        else:
            format = self.textEdit.currentCharFormat()
            format.setFontStrikeOut(False)
            self.textEdit.setCurrentCharFormat(format)
            self.strikeout = False

    def setBulletpoint(self):
        print(".")




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