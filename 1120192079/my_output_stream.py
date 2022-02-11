from PyQt6 import QtCore

class MyOutputStream(QtCore.QObject):
    text_signal = QtCore.pyqtSignal(str)

    def write(self, text):
        self.text_signal.emit(str(text))