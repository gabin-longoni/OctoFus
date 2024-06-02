import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('OctoFus - Main Window')
        self.setGeometry(100, 100, 800, 600)

        # Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        viewPacketAction = QAction('View Packets', self)
        viewPacketAction.triggered.connect(self.openPacketViewer)
        fileMenu.addAction(viewPacketAction)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Main widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Welcome to OctoFus'))
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def openPacketViewer(self):
        from .packet_viewer import PacketViewer
        self.packet_viewer = PacketViewer()
        self.packet_viewer.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
