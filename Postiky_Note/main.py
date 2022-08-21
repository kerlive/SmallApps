# PyQt5 PostIt Notes
#code by kevin

__author__ = "_Kevin Chan_"
__copyright__ = "Copyright (C) 2022 Kevin"
__license__ = "GPL-3.0"
__version__ = "0.0.3"


import os, sys, time, hashlib, gzip, struct

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
        self.setWindowIcon(QtGui.QIcon(':/icon/Posit.ico'))
        self.setFixedSize(580, 380)

        # stacked layout
        self.stackedLayout = QStackedLayout()
        self.perviewWidget.setLayout(self.stackedLayout)

        self.page0 = QWidget()
        self.icon = QLabel()
        self.icon.setStyleSheet("background-image : url(':/icon/Posit.ico'); background-repeat: no repeat; background-position: center;")
        self.iconlayout = QGridLayout()
        self.iconlayout.addWidget(self.icon)
        self.page0.setLayout(self.iconlayout)
        self.stackedLayout.addWidget(self.page0)

        self.page1 = QWidget()
        self.draftEditor = QTextEdit()
        self.page1Layout = QFormLayout()
        self.page1Layout.addWidget(self.draftEditor)
        self.page1.setLayout(self.page1Layout)
        self.stackedLayout.addWidget(self.page1)


        

        # Layout setting
        self.draftWidget.setLayout(self.listLayout)
        self.draftWidget.setFixedWidth(181)
        self.perviewWidget.setMinimumWidth(341)
        self.perviewWidget.setMinimumHeight(311)
        # set a number for open a mutiple widget
        self.skNum = 1
        self.noteSheet = {}

        # list draft files
        self.list_Draft()

        # Button
        self.addButton.clicked.connect(self.newNotes)
        self.listView.itemClicked.connect(self.open_draft)
        #self.listView.itemDoubleClicked.connect(self.openDraftNotes)

    def open_draft(self):
        self.stackedLayout.setCurrentIndex(1)
        name = str(self.listView.currentItem().text())
        dn  = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Draft/"+name)
        print(dn)
        with open(dn, 'rb') as file:
                data = file.read()

        def remove_bytes(buffer, start, end):
            fmt = '%ds %dx %ds' % (start, end-start, len(buffer)-end) 
            return b''.join(struct.unpack(fmt, buffer))



        rCmpd = remove_bytes(data, len(data)-8, len(data))

        rEC = remove_bytes(data, 0 , len(data)-8)

        rSentence =  gzip.decompress(rCmpd).decode("utf-8")

        rHash = hashlib.sha256(rCmpd).hexdigest()

        print("read Error Check:" + rEC.decode("ASCII") +"---- rHash for check:" + rHash)

        print("decode data from file:" + rSentence)

        self.draftEditor.setText(rSentence)

    def list_Draft(self):
        self.listView.clear()
        draft_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Draft")
        if not os.path.exists(draft_path):
            os.makedirs(draft_path)
        
        for d in os.listdir(draft_path):
            if d.endswith(".bin"):
                self.listView.addItem(d)
        
    def openDraftNotes(self):
        self.noteSheet[self.skNum] = Notes()
        #self.noteSheet[self.skNum].textInput(self.open_draft)
        self.skNum = self.skNum + 1

    def newNotes(self):
        self.noteSheet[self.skNum] = Notes()
        self.skNum = self.skNum + 1
        
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

    def save_draft(self, draft):
        
        fileName = time.strftime("%Y-%b-%d_%Hh-%Mm-%Ss_",time.localtime())+ 'Nmb' +str(time.time()).split('.')[1] +'.bin'
        sentence = draft.encode('utf-8')
        cmpd = gzip.compress(sentence)

        hash = hashlib.sha256(cmpd).hexdigest()

        EC = [*hash][0] + [*hash][7] + [*hash][15] + [*hash][35] + hash[len(hash) - 4:]

        draft_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Draft")
        if not os.path.exists(draft_path):
            os.makedirs(draft_path)

        with open(os.path.join(draft_path,fileName), 'wb') as file:
            file.write(cmpd)
            file.write(EC.encode('ASCII'))

    def noteClose(self):
        text = self.textEdit.toPlainText()
        if text != '':
            self.save_draft(text)
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