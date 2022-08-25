# PyQt5 PostIt Notes
#code by kevin

__author__ = "_Kevin Chan_"
__copyright__ = "Copyright (C) 2022 Kevin"
__license__ = "GPL-3.0"
__version__ = "0.1.0"

import os, sys, time, hashlib, gzip, struct, random
from pickle import NONE

from multiprocessing import shared_memory
key = "Postiky_Note"
instance = 1
try:
    single = shared_memory.SharedMemory(key, create=False)
    single.buf[0] = 0
except:
    instance = 0
if instance == 0:
    single = shared_memory.SharedMemory(key, create=True,size=1)
    single.buf[0] = 1
else:
    sys.exit("App is runing")

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import UIresource_rc

import weakness_data_encryption as wde

ui_dir = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(ui_dir,"UI")

form_0, base_0 = uic.loadUiType(os.path.join(ui_path,"Postiky_Note.ui"))
form_1, base_1 = uic.loadUiType(os.path.join(ui_path,"Note.ui"))

class File_packaged():
    def save_draft(draft, fileName):
        
        sentence = draft.encode('utf-8')
        cmpd = gzip.compress(sentence)

        hash = hashlib.sha256(cmpd).hexdigest()

        EC = [*hash][0] + [*hash][7] + [*hash][15] + [*hash][35] + hash[len(hash) - 4:]

        draft_path = os.path.join(os.path.dirname(os.path.abspath(__name__)),"Draft")
        if not os.path.exists(draft_path):
            os.makedirs(draft_path)

        with open(os.path.join(draft_path,fileName), 'wb') as file:
            file.write(cmpd)
            file.write(EC.encode('ASCII'))

    def open_draft(fileName):
        
        dn  = os.path.join(os.path.dirname(os.path.abspath(__name__)),"Draft/"+fileName)
    
        with open(dn, 'rb') as file:
                data = file.read()

        def remove_bytes(buffer, start, end):
            fmt = '%ds %dx %ds' % (start, end-start, len(buffer)-end) 
            return b''.join(struct.unpack(fmt, buffer))

        rCmpd = remove_bytes(data, len(data)-8, len(data))
        rEC = (remove_bytes(data, 0 , len(data)-8)).decode("ASCII")

        rHash = hashlib.sha256(rCmpd).hexdigest()
        checkHash = [*rHash][0] + [*rHash][7] + [*rHash][15] + [*rHash][35] + rHash[len(rHash) - 4:]
        if rEC == checkHash:
            rSentence =  gzip.decompress(rCmpd).decode("utf-8")
            return rSentence
            #self.draftBrowser.setText(rSentence)
        else:
            return ("<span style=\"color:red;\">***** some issuse happened, data can not be read!!! *****</span>")
            #self.draftBrowser.setText("<span style=\"color:red;\">***** some issuse happened, data can not be read!!! *****</span>")



class Postiky_Note(base_0, form_0):
    def __init__(self):
        super(base_0, self).__init__()
        self.setupUi(self)

        wde.forincludetesting()

        self.setWindowTitle('Notes_List')
        self.setWindowIcon(QtGui.QIcon(':/icon/Posit.ico'))
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint)
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
        self.draftBrowser = QTextBrowser()
        self.draftBrowser.setStyleSheet("font: 12pt 'Times New Roman';")
        self.page1Layout = QFormLayout()
        self.page1Layout.addWidget(self.draftBrowser)
        self.page1.setLayout(self.page1Layout)
        self.stackedLayout.addWidget(self.page1)

        self.page2 = QWidget()
        self.pw_e = QLineEdit()
        self.cpw_e = QLineEdit()
        self.rmbk_e = QLineEdit()
        self.rmbk_e.setPlaceholderText("write some thing here about password.")
        self.pw_e.setEchoMode(QLineEdit.Password)
        self.cpw_e.setEchoMode(QLineEdit.Password)
        self.encpto = QFormLayout()
        self.encpto.addRow("Remember-key:", self.rmbk_e)
        self.encpto.addRow("Password:", self.pw_e)
        self.encpto.addRow("Conform Password:", self.cpw_e)
        dlgLayout = QVBoxLayout()
        # Add a button box
        self.btnBox = QDialogButtonBox()
        self.btnBox.setStandardButtons(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        # Set the layout on the dialog
        dlgLayout.addLayout(self.encpto)
        dlgLayout.addWidget(self.btnBox)
        self.page2.setLayout(dlgLayout)
        self.stackedLayout.addWidget(self.page2)

        self.page3 = QWidget()
        self.rmbk_d = QLabel()
        self.pw_d = QLineEdit()
        self.cpw_d = QLineEdit()
        self.pw_d.setEchoMode(QLineEdit.Password)
        self.cpw_d.setEchoMode(QLineEdit.Password)
        self.maskButton = QPushButton()
        self.maskButton.setText("Masked")
        self.Mask = True
        self.decpto = QFormLayout()
        self.decryptButton = QPushButton('Accepted')
        self.decpto.addRow("Remember-key:", self.rmbk_d)
        self.decpto.addRow("Password:", self.pw_d)
        self.decpto.addRow("Conform Password:",self.cpw_d)
        self.decpto.addRow(self.maskButton, self.decryptButton)
        self.page3.setLayout(self.decpto)
        self.stackedLayout.addWidget(self.page3)


        # Layout setting
        self.draftWidget.setLayout(self.listLayout)
        self.draftWidget.setFixedWidth(181)
        self.perviewWidget.setMinimumWidth(341)
        self.perviewWidget.setMinimumHeight(311)
        self.addButton.setMaximumWidth(41)
        # set a number for open a mutiple widget
        self.skNum = 1
        self.noteSheet = {}

        # list draft files
        self.list_Draft()
        self.listView.setWordWrap(True)

        # Button
        self.addButton.clicked.connect(self.newNotes)
        self.cryptoButton.clicked.connect(self.crypto_page)
        self.deleteButton.clicked.connect(self.draftDel)
        self.listView.itemClicked.connect(self.print_to_Browser)
        self.listView.itemDoubleClicked.connect(self.openDraftNotes)
        self.btnBox.accepted.connect(self.save_crypto)
        self.btnBox.rejected.connect(self.crypto_page_reset)
        self.decryptButton.clicked.connect(self.view_crypto)
        self.maskButton.clicked.connect(self.echoMask)

        # Button Icon
        self.addButton.setIcon(QtGui.QIcon(":/Button/UI/Element/plus.png"))
        self.cryptoButton.setIcon(QtGui.QIcon(":/Button/UI/Element/locked.png"))
        self.deleteButton.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))

        # TrayIcon
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(QtGui.QIcon(":/icon/Posit.ico"))
        self.trayIcon.setVisible(True)

        self.trayIcon.activated.connect(self.onTrayIconActivated)

        menu = QMenu()

        info = QAction("About",self)
        info.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        info.triggered.connect(self.about)
        menu.addAction(info)

        quit = QAction("Quit",self)
        quit.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        quit.triggered.connect(app.quit)
        menu.addAction(quit)

        self.trayIcon.setContextMenu(menu)

    def about(self):
        About = QMessageBox.information(
            self,
            "About Postiky Note",
            "Postiky Note is a free opensource software \n programmed in Python3, based on PyQt5.\n Copyright (c) 2022 Kevin\n Author: Kevin Chan(E) 陈 作乾（中） ケン・チェン（日） https://github.com/kerlive/\n License: GPL-3.0\n Version: 0.1.0\n",
            buttons=QMessageBox.Yes ,
            defaultButton=QMessageBox.Yes,
        )

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
        if reason == QSystemTrayIcon.Trigger:
            self.hide()

    def anotherCall(self):
        cTimer = QtCore.QTimer(self)
        cTimer.start(1000)
        cTimer.timeout.connect(self.checkNew)
    def checkNew(self):
        if single.buf[0] == 0:
            self.show()
            single.buf[0] = 1

    def echoMask(self):
        if self.Mask == True:
            self.Mask = False
            self.pw_d.setEchoMode(QLineEdit.Normal)
            self.cpw_d.setEchoMode(QLineEdit.Normal)
            self.maskButton.setText("Masking")
        else:
            self.Mask = True
            self.pw_d.setEchoMode(QLineEdit.Password)
            self.cpw_d.setEchoMode(QLineEdit.Password)
            self.maskButton.setText("Masked")

    def crypto_page(self):
        if  self.listView.currentRow() != -1 :
            if str(self.listView.currentItem().text())[:6] != '_ECPD_':
                self.stackedLayout.setCurrentIndex(2)  

    def crypto_page_reset(self):
            self.stackedLayout.setCurrentIndex(0)
            self.listView.setCurrentRow(-1)
            self.rmbk_e.clear()
            self.pw_e.clear()
            self.cpw_e.clear()

    def save_crypto(self):
        password = self.pw_e.text()
        comform = self.cpw_e.text()
        if password != '' and comform != '' :
            if len(password) > 5:
                if password == comform :
                    data = File_packaged.open_draft(self.listView.currentItem().text())
                    crypted_data = wde.data_encryption(password, data) + '.' + self.rmbk_e.text()
                    print("data:")
                    print(data)
                    print("crypted data:")
                    print(crypted_data)
                    print("password:")
                    print(password)
                    fileName = time.strftime("_ECPD_%Y-%b-%d %Hh-%Mm-%Ss_",time.localtime())+ '.N' +str(time.time()).split('.')[1] +'.bin'
                    File_packaged.save_draft(crypted_data, fileName)
                    self.draftDel()
                    self.crypto_page_reset()

                else:
                    self.showErrorDialog("password comform failed.")
            else:
                self.showErrorDialog("password width less than 6.")
        else:
            self.showErrorDialog("please fill out password format: \n you need over 6 Number,Alpha or Sign.\n exp:'123abc+-*'\n if you want you can use Number only!\n exp:'123456'")

    def read_crypto(self, password, comform):
        data = File_packaged.open_draft(self.listView.currentItem().text())
        crypto = data.split('.')[0]
        if password != '' and comform != '' :
            if len(password) > 5:
                if password == comform :
                    dcpd = wde.data_conversion(password, crypto)
                    if dcpd != '':
                        return dcpd
                    else:
                        self.showErrorDialog("password incorrect.")
                else:
                    self.showErrorDialog("password comform failed.")
            else:
                self.showErrorDialog("password width less than 6.")
        else:
            self.showErrorDialog("password format is incomplete.")
    def view_crypto(self):
        view = self.read_crypto(self.pw_d.text(), self.cpw_d.text())
        if view != None:
            self.draftBrowser.setText(view)
            self.stackedLayout.setCurrentIndex(1)

    def open_crypto(self):

        self.pw_d_tn = QLineEdit()
        self.cpw_d_tn = QLineEdit()
        self.pw_d_tn.setEchoMode(QLineEdit.Password)
        self.cpw_d_tn.setEchoMode(QLineEdit.Password)
        self.toNote = QFormLayout()
        self.deToNoteButton = QPushButton('Accepted')
        self.toNote.addRow("Password:", self.pw_d_tn)
        self.toNote.addRow("Conform Password:",self.cpw_d_tn)
        self.toNote.addRow('', self.deToNoteButton)
        self.decp = QDialog()
        self.decp.setLayout(self.toNote)
        self.decp.show()

        self.deToNoteButton.clicked.connect(self.decryptToNotes)


    def showErrorDialog(self, argv):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
   
        msg.setText("ERROR REQUEST")
        msg.setWindowTitle("ERROR!")
        msg.setInformativeText(argv)
        msg.setStandardButtons(QMessageBox.Ok)
        
        retval = msg.exec_()
        
    def print_to_Browser(self):
        if str(self.listView.currentItem().text())[:6] != '_ECPD_':
            text = File_packaged.open_draft(self.listView.currentItem().text())
            self.draftBrowser.setText(text)
            self.stackedLayout.setCurrentIndex(1)
        else:
            self.stackedLayout.setCurrentIndex(3)
            self.rmbk_d.setText(File_packaged.open_draft(self.listView.currentItem().text()).split('.')[1])
            self.pw_d.setText('')
            self.cpw_d.setText('')

    def draftDel(self):
        if self.listView.currentRow() != -1:
            name = str(self.listView.currentItem().text())
            dn  = os.path.join(os.path.dirname(os.path.abspath(__name__)),"Draft/"+name)
            if os.path.exists(dn):
                os.remove(dn)
            self.list_Draft()
            self.stackedLayout.setCurrentIndex(0)

    def list_Draft(self):
        self.listView.clear()
        draft_path = os.path.join(os.path.dirname(os.path.abspath(__name__)),"Draft")
        if not os.path.exists(draft_path):
            os.makedirs(draft_path)
        
        for d in os.listdir(draft_path):
            if d.endswith(".bin"):
                self.listView.addItem(d)
        
    def openDraftNotes(self):
        if str(self.listView.currentItem().text())[:6] != '_ECPD_':
            self.noteSheet[self.skNum] = Notes()
            text = File_packaged.open_draft(self.listView.currentItem().text())
            self.noteSheet[self.skNum].textEdit.setText(text)
            self.skNum = self.skNum + 1
            self.draftDel()
        else:
            self.open_crypto()
            self.stackedLayout.setCurrentIndex(0)

    def decryptToNotes(self):
            data = self.read_crypto(self.pw_d_tn.text(), self.cpw_d_tn.text())
            if data != None:
                self.decp.close()
                self.noteSheet[self.skNum] = Notes()
                self.noteSheet[self.skNum].textEdit.setText(data)
                self.skNum = self.skNum + 1

    def newNotes(self):
        self.noteSheet[self.skNum] = Notes()
        self.skNum += 1
        
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

        self.setWindowTitle('PostIt')
        self.setWindowIcon(QtGui.QIcon(':/icon/Posit.ico'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.textEdit.setPlaceholderText("Take a note..")
        # background color
        self.colorNum = random.randrange(6)
        self.changeColor()

        # Button
        self.addButton.clicked.connect(demo.newNotes)
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
        self.lock = False

        # font format
        self.boldButton.clicked.connect(self.setBold)
        self.italicButton.clicked.connect(self.setItalic)
        self.underlineButton.clicked.connect(self.setUnderline)
        self.strikethroughButton.clicked.connect(self.setStrikeout)
        self.togglebulletButton.clicked.connect(self.setBulletpoint)
        self.cryptoButton.clicked.connect(self.crypto)
    

    def noteClose(self):
        text = self.textEdit.toPlainText()
        if text != '':
            fileName = time.strftime("%Y-%b-%d %Hh-%Mm-%Ss_",time.localtime())+ '.N' +str(time.time()).split('.')[1] +'.bin'
            File_packaged.save_draft(text, fileName)
            demo.list_Draft()
            if self.lock == True:
                demo.listView.setCurrentItem(demo.listView.findItems(fileName, QtCore.Qt.MatchContains)[0])
                demo.crypto_page()
            self.close()
        else:
            self.close()

    
    def crypto(self):
        if self.lock == False:
            self.lock = True
            self.cryptoButton.setStyleSheet("background-image: url(:/Button/UI/Element/locked.png);	background-position: center; background-repeat: no-repeat; border: 0;")
        else:
            self.lock =False
            self.cryptoButton.setStyleSheet("background-image: url(:/Button/UI/Element/unlocked.png); background-position: center; background-repeat: no-repeat; border: 0;")

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
        color = self.colorNum
        if color == 0:
                self.colorNum = 1
                self.label.setStyleSheet('background-color: rgb(228, 249, 224);')
                self.textEdit.setStyleSheet('background-color: rgb(228, 249, 224);  border: 0; font: 12pt "Times New Roman";')
        if color == 1:
                self.colorNum = 2
                self.label.setStyleSheet('background-color: rgb(255, 228, 241);')
                self.textEdit.setStyleSheet('background-color: rgb(255, 228, 241);  border: 0;  font: 12pt "Times New Roman";')
        if color == 2:
                self.colorNum = 3
                self.label.setStyleSheet('background-color: rgb(242, 230, 255);')
                self.textEdit.setStyleSheet('background-color: rgb(242, 230, 255);  border: 0;  font: 12pt "Times New Roman";')
        if color == 3:
                self.colorNum = 4
                self.label.setStyleSheet('background-color: rgb(226, 241, 255);')
                self.textEdit.setStyleSheet('background-color: rgb(226, 241, 255);  border: 0;  font: 12pt "Times New Roman";')
        if color == 4:
                self.colorNum = 5
                self.label.setStyleSheet('background-color: rgb(243, 242, 241);')
                self.textEdit.setStyleSheet('background-color: rgb(243, 242, 241);  border: 0;  font: 12pt "Times New Roman";')
        if color == 5:
                self.colorNum = 0
                self.label.setStyleSheet('background-color: rgb(255, 247, 209);')
                self.textEdit.setStyleSheet('background-color: rgb(255, 247, 209);  border: 0;  font: 12pt "Times New Roman";')
            

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