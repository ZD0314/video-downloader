# src/ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QToolBar, QStyle
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from src.ui.url_input_widget import UrlInputWidget
from src.ui.download_list import DownloadListWidget


class MainWindow(QMainWindow):
    """主窗口组件"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("视频下载器")
        self.setGeometry(100, 100, 900, 700)

        # 设置应用图标（使用Qt内置图标）
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        layout = QVBoxLayout(central_widget)

        # URL输入区域 (替换原来的简单实现)
        self.url_input_widget = UrlInputWidget()
        layout.addWidget(self.url_input_widget)

        # 下载列表区域 (替换原来的QTextEdit)
        self.download_list_widget = DownloadListWidget()
        layout.addWidget(self.download_list_widget)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 连接信号
        self.url_input_widget.download_requested.connect(self.on_download_requested)
        self.download_list_widget.task_pause_requested.connect(self.on_task_pause)
        self.download_list_widget.task_resume_requested.connect(self.on_task_resume)
        self.download_list_widget.task_cancel_requested.connect(self.on_task_cancel)

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

    def on_download_requested(self, url: str):
        """处理下载请求"""
        self.status_bar.showMessage(f"开始下载: {url}")
        # TODO: 调用下载管理器

    def on_task_pause(self, task):
        """处理任务暂停"""
        pass

    def on_task_resume(self, task):
        """处理任务恢复"""
        pass

    def on_task_cancel(self, task):
        """处理任务取消"""
        pass
