import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

class SniffingThread(QThread):
    packet_sniffed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        from sniffing.sniffer import start_sniffing
        start_sniffing(self.packet_sniffed.emit)

class PacketViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('OctoFus - Packet Viewer')
        self.setGeometry(150, 150, 600, 400)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.packet_display = QTextEdit()
        self.packet_display.setReadOnly(True)
        layout.addWidget(self.packet_display)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.start_sniffing()

    def start_sniffing(self):
        self.sniffing_thread = SniffingThread()
        self.sniffing_thread.packet_sniffed.connect(self.display_packet)
        self.sniffing_thread.start()

    def display_packet(self, packet):
        self.packet_display.append(packet)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    packetWin = PacketViewer()
    packetWin.show()
    sys.exit(app.exec_())
