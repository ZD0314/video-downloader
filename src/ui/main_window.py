# src/ui/main_window.py
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QToolBar, QStyle
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from src.ui.url_input_widget import UrlInputWidget
from src.ui.download_list import DownloadListWidget
from src.ui.settings_panel import SettingsPanel
from src.models.download_task import DownloadTask
from src.services.yt_dlp_wrapper import YTDLPWrapper
from src.services.video_parser import VideoParser
from src.services.download_manager import DownloadManager


class MainWindow(QMainWindow):
    """主窗口组件"""

    def __init__(self):
        super().__init__()

        # 创建服务层组件
        self.ytdlp_wrapper = YTDLPWrapper()
        self.video_parser = VideoParser(self.ytdlp_wrapper)
        self.download_manager = DownloadManager()

        # 默认下载路径
        self._download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # 连接信号
        self.download_manager.task_started.connect(self.on_task_started)
        self.download_manager.task_progress.connect(self.on_task_progress)
        self.download_manager.task_completed.connect(self.on_task_completed)
        self.download_manager.task_failed.connect(self.on_task_failed)

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

        # 设置面板
        self.settings_panel = SettingsPanel()
        self.settings_panel.settings_changed.connect(self.on_settings_changed)
        layout.addWidget(self.settings_panel)

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

        # 调用下载管理器开始下载，返回任务ID
        task_id = self.download_manager.add_task(url, self._download_path)

        # 获取下载管理器创建的任务对象
        task = self.download_manager.get_task(task_id)
        if task:
            # 添加到UI列表
            self.download_list_widget.add_task(task)

    def on_task_pause(self, task):
        """处理任务暂停"""
        self.download_manager.pause_task(task.task_id)

    def on_task_resume(self, task):
        """处理任务恢复"""
        self.download_manager.resume_task(task.task_id)

    def on_task_cancel(self, task):
        """处理任务取消"""
        self.download_manager.cancel_task(task.task_id)

    def on_task_started(self, task_id: str):
        """任务开始"""
        self.status_bar.showMessage(f"下载中: {task_id}")

    def on_task_progress(self, task_id: str, downloaded: int, total: int, speed: str):
        """进度更新"""
        self.download_list_widget.update_progress(task_id, downloaded, total, speed)

    def on_task_completed(self, task_id: str, file_path: str):
        """下载完成"""
        self.status_bar.showMessage(f"下载完成: {file_path}")

    def on_task_failed(self, task_id: str, error_message: str):
        """下载失败"""
        self.status_bar.showMessage(f"下载失败: {error_message}")

    def on_settings_changed(self, settings: dict):
        """处理设置变化"""
        # 更新下载路径
        if settings.get("download_path"):
            self._download_path = settings["download_path"]
            self.status_bar.showMessage(f"下载路径已更新: {self._download_path}")
