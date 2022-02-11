import sys
import UIForm as UIForm
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
import downloader
import os
import logging
from my_output_stream import MyOutputStream


class MainForm(QMainWindow):

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = UIForm.Ui_MainWindow()
        self.ui.setupUi(self)  # ui对象初始化的时候，须将自身指针传给ui类，以供其中控件对象初始化

        # 初始化剪切板
        self.clipboard = QApplication.clipboard()
        # 改变日志的输出位置
        self.logger = self.setupLogger()

    # 增加日志的输出位置到qt的文本浏览器(textbrowser)控件中
    def setupLogger(self):
        """
        为此需要实现一个文件流式的对象，其中需要重写write方法。
        这里我的实现是在该文件流的write方法中发射一个信号，并由调用该文件流对象的MainForm中的函数槽来接收该信号
        这样就实现了基于logger输出流的handler的添加以及显示
        """

        logger = logging.getLogger()
        # 用重写的输出流来初始化logger的一个新的handler
        StreamToTextBrowser = MyOutputStream(text_signal=self._writeConsoleToTextEdit)
        logger.addHandler(logging.StreamHandler(StreamToTextBrowser))
        # 重定向输出
        # sys.stdout = EmittingConsole(text_signal=self.writeConsoleToTextEdit)
        # sys.stderr = EmittingConsole(text_signal=self.writeConsoleToTextEdit)

        # 测试重定向
        # print("lalala")
        # logging.info("bababa")
        return logger

    # 点击打开输入文件按钮的槽函数
    def inputFileClicked(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', './')
        if fname[0]:
            with open(fname[0], 'r', encoding='utf-8', errors='ignore') as fp:
                self.ui.textEdit.setText(fp.read())

    # 点击http下载按钮的槽函数
    def downloadFileClicked(self):
        # 从设置中获取下载的基本信息
        urls = self.ui.textEdit.document().toPlainText().split()
        # 每次点击下载按钮，都初始化一个downloader对象
        http_downloader = downloader.HttpDownloader()  # 注意初始化对象时，会从磁盘重新加载配置文件
        for url in urls:
            self.ui.textBrowser.append("%s started!\n" % os.path.basename(url))
            http_downloader.start_default_task(url)  # 从配置文件得到存放地址和线程数
            self.ui.textBrowser.append("%s completed!\n" % os.path.basename(url))
            # TODO
            # 将logging的输出结果添加到textBrowser

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

    # 检测到剪切板变化的槽函数
    def clipboardChanged(self):
        pass

    # 点击ftp下载按钮的槽函数
    def ftpClicked(self):
        pass


if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    my_widget = MainForm()
    my_widget.show()
    sys.exit(my_app.exec())
