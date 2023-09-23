from PySide6.QtWidgets import QApplication,QPushButton,QWidget
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,1024,768)
        # 初始化窗口大小
        btn = QPushButton('开始游戏',self)
