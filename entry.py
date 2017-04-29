from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5 import QtGui, QtCore
import PyQt5.uic
from a_cat import Query
import sys

(class_ui, class_basic_class) = PyQt5.uic.loadUiType('widget.ui')
print(class_basic_class)


class MainFrame(class_basic_class, class_ui):
    def __init__(self):
        super(MainFrame, self).__init__()
        # 使用qt自带的监听系统剪贴板的功能
        self.clipboard = QtGui.QGuiApplication.clipboard()
        self.setupUi(self)
        self.connects()
        # 这里还没太理解，主要是解决了focusoutevent事件不响应的bug
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        # todo: 耦合性？？
        self.query = Query()

    def connects(self):
        """信号槽的连接"""
        # 当选中文字变化的时候，抓取释义
        self.clipboard.selectionChanged.connect(self.selection_changed)
        pass

    def refresh_window(self):
        """更新翻译的显示"""
        # 设置位置和大小
        self.setFixedSize(400, 300)
        cur = QtGui.QCursor.pos()
        x = cur.x() + 20
        y = cur.y() + 20
        # 如果超出了屏幕边界，便显示在里面
        window_h = QDesktopWidget().screenGeometry().height()
        window_w = QDesktopWidget().screenGeometry().width()
        if x + 400 > window_h or y + 300 > window_w:
            x -= 20 + 400
            y -= 20 + 300
        self.move(x, y)

        self.setWindowTitle("search for: %s" % self.clipboard.text(QtGui.QClipboard.Selection))
        # todo: 如果没有显示结果，需要提示
        voice_text = ''
        for x in self.query.word.voices:
            for key in x:
                voice_text += key + "\t"
        self.voice_label.setText(voice_text)

        base_info = ''
        for x in self.query.word.props:
            base_info += x + self.query.word.props[x] + '\n'
        self.base_infor_label.setText(base_info)

    def selection_changed(self):
        """剪切板的数据有变化"""
        # todo: 将
        print(self.clipboard.text(QtGui.QClipboard.Selection))
        if self.clipboard.text(QtGui.QClipboard.Selection):
            self.query.get(self.clipboard.text(QtGui.QClipboard.Selection))
            self.refresh_window()
            self.show()

    def focusOutEvent(self, event):
        self.hide()
        pass

    # 这种方法只适用于当前这个窗口内
    def mousePressEvent(self, event):
        pass

    def keyPressEvent(self, e):
        pass

    def closeEvent(self, e):
        """隐藏窗口到后台"""
        self.hide()
        e.ignore()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        widget = MainFrame()
        widget.hide()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit(app.exec_())