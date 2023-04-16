import sys
from PyQt5.QtCore import QRect,Qt,QSize
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QLineEdit,QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qtwidgets import AnimatedToggle

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        label = QLabel("ASDASD")
        b = QPushButton("asda")
        layout.addWidget(b)
        layout.addWidget(label)
        self.setLayout(layout)
        
        self.show()


        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())