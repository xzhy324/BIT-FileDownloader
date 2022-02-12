import sys
import os
import logging
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow

import downloader
from GUI import UIForm
from GUI.my_output_stream import MyOutputStream


class MainForm(QMainWindow):

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = UIForm.Ui_MainWindow()
        self.ui.setupUi(self)  # ui对象初始化的时候，须将自身指针传给ui类，以供其中控件对象初始化

        # 初始化剪切板
        self.clipboard = QApplication.clipboard()

        self.http_downloader = downloader.HttpDownloader()

        # 由于logger初始化需要使用downloader的配置信息，因此downloader需要先实例化
        self.logger = self._setupLogger()  # 改变日志的输出位置

    # 增加日志的输出位置到qt的文本浏览器(textbrowser)控件中
    def _setupLogger(self):
        """
        为此需要实现一个文件流式的对象，其中需要重写write方法。
        这里我的实现是在该文件流的write方法中发射一个信号，并由调用该文件流对象的MainForm中的函数槽来接收该信号
        这样就实现了基于logger输出流的handler的添加以及显示
        """

        logger = logging.getLogger()

        # 自己重写的类文件输出流中的信号挂钩到父窗体的内部方法，该内部方法能够修改qt的控件内容，从而实现了日志文件输出的重定向
        streamToTextbrowser = MyOutputStream(self._writeConsoleToTextEdit)

        # 用重写的输出流来初始化logger的一个新的handler
        handler = logging.StreamHandler(streamToTextbrowser)
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s:%(lineno)s - [%(levelname)s] %(message)s')  # 规定输出格式
        handler.setFormatter(formatter)  # 将输出格式指定到handler上
        logger.addHandler(handler)

        logger.setLevel(level=self.http_downloader.settings.get('logging.level'))

        # 重定向输出
        # sys.stdout = EmittingConsole(text_signal=self.writeConsoleToTextEdit)
        # sys.stderr = EmittingConsole(text_signal=self.writeConsoleToTextEdit)
        return logger

    # 点击打开输入文件按钮的槽函数
    def inputFileClicked(self):
        f_name = QFileDialog.getOpenFileName(self, '打开文件', './')
        if f_name[0]:
            with open(f_name[0], 'r', encoding='utf-8', errors='ignore') as fp:
                self.ui.textEdit.setText(fp.read())

    # 点击http下载按钮的槽函数
    def downloadFileClicked(self):
        # 从控件中获取下载的url
        urls = self.ui.textEdit.document().toPlainText().split()
        # 每次点击下载按钮，都从磁盘重新加载配置文件
        self.http_downloader.update_settings()
        for url in urls:
            self.http_downloader.start_default_task(url)  # 从配置文件得到存放地址和线程数

    # 日志重定向的槽函数
    def _writeConsoleToTextEdit(self, text):
        self.ui.textBrowser.append(text)

    # 点击打开设置按钮的槽函数
    def OpenSettingsFile(self):
        # 注意每次下载时，会自动读取一遍磁盘的设置信息
        try:
            os.startfile("./settings.txt")
        except OSError as e:
            logging.error("error opening settings.txt,reason: %s" % e)
        else:
            self.http_downloader.update_settings()

    # 检测到剪切板变化的槽函数
    def clipboardChanged(self):
        # TODO
        pass

    # 点击ftp下载按钮的槽函数
    def ftpClicked(self):
        # TODO
        pass


if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    my_window = MainForm()
    my_window.show()
    sys.exit(my_app.exec())
