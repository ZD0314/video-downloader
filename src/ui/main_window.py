# src/ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QStatusBar, QMenuBar, QMenu, QToolBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    """主窗口组件"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("视频下载器")
        self.setGeometry(100, 100, 900, 700)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        layout = QVBoxLayout(central_widget)

        # URL输入区域
        url_layout = QHBoxLayout()
        url_label = QLabel("视频URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入视频URL，支持YouTube、Bilibili等")
        self.download_btn = QPushButton("下载")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.download_btn)
        layout.addLayout(url_layout)

        # 下载列表区域
        self.download_list = QTextEdit()
        self.download_list.setReadOnly(True)
        self.download_list.setPlaceholderText("下载列表将显示在这里...")
        layout.addWidget(self.download_list)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 菜单栏
        self.init_menu_bar()

        # 工具栏
        self.init_tool_bar()

    def init_menu_bar(self):
        """初始化菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")

        # 视图菜单
        view_menu = menubar.addMenu("视图")

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)

    def init_tool_bar(self):
        """初始化工具栏"""
        toolbar = QToolBar("工具栏")
        self.addToolBar(toolbar)

        # 添加工具栏按钮
        download_action = QAction("下载", self)
        toolbar.addAction(download_action)

        pause_action = QAction("暂停", self)
        toolbar.addAction(pause_action)

        cancel_action = QAction("取消", self)
        toolbar.addAction(cancel_action)
