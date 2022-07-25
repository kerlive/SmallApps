from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os

path = os.getcwd()
lsd = list(filter(os.path.isdir, os.listdir(path)))
iniTxt = os.path.join(path,"工事中.txt")

cpn = 'NONE'
cid = 0

class main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.scaning()
        self.comboBox.currentIndexChanged.connect(self.tobeWorking)


    def initUI(self):

        self.setGeometry(1200, 600, 0, 0)
        self.setFixedSize(280, 100)
        self.setWindowTitle('PojectStatus')


        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QRect(40, 20, 201, 41))

        self.show()
    
    def scaning(self):
        for f in lsd:
            self.comboBox.addItem(f)
        self.tobeWorking()
    
    def tobeWorking(self):
        global cpn, cid
        cpn = self.comboBox.currentText()
        cid = self.comboBox.currentIndex()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        if os.path.exists(os.path.join(os.getcwd(),"工事中.txt")):
            os.remove(os.path.join(os.getcwd(),"工事中.txt"))
        f = open("工事中.txt",'x')
        f.write('——————to be in working order.....\n')
        f.write('1. '+cpn+'\n\n')
        
        f.write('______to be in worked pausing.....\n')
        if cpn != '':
            lsd.pop(cid)
        for n,d in enumerate(lsd):
            i=n+2
            f.write(str(i) + '. ' + d + '\n')
        f.close()

        print("save to file")