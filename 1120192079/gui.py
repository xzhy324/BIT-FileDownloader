import sys
import myUIForm
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
import dev as coreDownloader
import os
import logging
from RedirectConsole import EmittingConsole


class MainForm(QWidget):
    _settings = {}

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.ui = myUIForm.Ui_Form()
        self.ui.setupUi(self)  # ui对象初始化的时候，须将自身指针传给ui类，以供其中控件对象初始化

        self.clipboard = QApplication.clipboard()

        coreDownloader.init_settings()
        self._settings = coreDownloader.settings

        # 重定向输出
        # sys.stdout = EmittingConsole(text_signal=self.writeConsoleToTextEdit)
        # sys.stderr = EmittingConsole(text_signal=self.writeConsoleToTextEdit)


        # 测试重定向
        # print("lalala")
        # logging.info("bababa")

    def inputFileClicked(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', './')
        if fname[0]:
            with open(fname[0], 'r', encoding='utf-8', errors='ignore') as fp:
                self.ui.textEdit.setText(fp.read())

    def downloadFileClicked(self):
        # 从设置中获取下载的基本信息
        output = self._settings['output']
        concurrency = int(self._settings['concurrency'])
        urls = self.ui.textEdit.document().toPlainText()
        urls = urls.split()
        for url in urls:
            self.ui.textBrowser.append("%s started!\n" % os.path.basename(url))
            coreDownloader.start_single_task(url, output, concurrency)
            self.ui.textBrowser.append("%s completed!\n" % os.path.basename(url))
            # TODO
            # 将logging的输出结果添加到textBrowser

    # 重定向的槽函数
    def writeConsoleToTextEdit(self, text):
        self.ui.textBrowser.append(text)

    def clipboardChanged(self):
        # TODO:剪切板的槽函数

        pass



if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    my_widget = MainForm()
    my_widget.show()
    sys.exit(my_app.exec())
