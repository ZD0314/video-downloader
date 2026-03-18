from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal


class UrlInputWidget(QWidget):
    """URL输入组件"""

    # 信号
    download_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)

        # URL标签
        url_label = QLabel("视频URL:")
        layout.addWidget(url_label)

        # URL输入框
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入视频URL，支持YouTube、Bilibili等")
        layout.addWidget(self.url_input, stretch=1)

        # 下载按钮
        self.download_btn = QPushButton("下载")
        self.download_btn.clicked.connect(self.on_download_clicked)
        layout.addWidget(self.download_btn)

    def on_download_clicked(self):
        """下载按钮点击事件"""
        url = self.url_input.text().strip()
        if url:
            self.download_requested.emit(url)

    def get_url(self) -> str:
        """获取URL"""
        return self.url_input.text().strip()

    def set_url(self, url: str):
        """设置URL"""
        self.url_input.setText(url)

    def clear(self):
        """清空输入"""
        self.url_input.clear()
