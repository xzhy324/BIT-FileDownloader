from PyQt6 import QtCore


class MyOutputStream(QtCore.QObject):
    text_signal = QtCore.pyqtSignal(str)

    def __init__(self, func):
        super().__init__()
        self.text_signal.connect(func)

    def write(self, text):
        self.text_signal.emit(str(text))

    def flush(self):
        pass
