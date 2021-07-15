from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, qApp, QMenuBar, QProgressBar, QFileDialog, QPlainTextEdit, QWidget, QLabel, QPushButton, QAction, QMessageBox, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QPixmap
from PyQt5.QtCore import pyqtSlot, QRect, Qt, QObject, pyqtSignal

import qrcode

import pyautogui
import sys

width, height= pyautogui.size()

class myLabel(QLabel): # For clickable label widget
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if(QMouseEvent.button() == Qt.LeftButton):
            self.clicked.emit()

class Window(QWidget):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.title = 'QR Code Generator'
        self.left = 0
        self.top = 0
        self.width = int(width/4)
        self.height = int(height/2)
        self.completed = 0
        self.isFullScreen = False
        self.initUI()

    # Widget creation
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('icon.png'))

        self.lay = QVBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)

        self.text = QLineEdit()
        self.text.setFixedHeight(115)
        self.text.setFont(QFont('Times', 15))
        self.text.textChanged.connect(self.generate)

        self.qrcode = myLabel()
        self.qrcode.clicked.connect(self.saveImg)
        self.clicked.connect(self.saveImg)

        self.lay.addWidget(self.text, 1 )
        self.lay.addWidget(self.qrcode, alignment=Qt.AlignCenter)

        self.setLayout(self.lay)
        self.show()

        self.generate() # empty qr code

    # Generate qr code base on the text in the LineEdit widget
    def generate(self):
        data = self.text.text()
        img = qrcode.make(data)
        img.save("tmp.png")

        pixmap = QPixmap('tmp.png')
        pixmap = pixmap.scaled(int(width/4), int(width/4), Qt.KeepAspectRatio)
        self.qrcode.setPixmap(pixmap)
        return img

    # Save image if click on image
    def saveImg(self):
        savepath, _ = QFileDialog.getSaveFileName(self, "Save image", "C:\\", ".png")
        if(savepath != ""):
            img = self.generate()
            img.save(savepath+".png")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(200, 50, 20)) # Rouge normalement
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(218, 218, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(palette)
    window = Window()
    window.show()
    sys.exit(app.exec_())
