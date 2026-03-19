# src/ui/main_window.py
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStatusBar, QMenuBar, QMenu, QToolBar, QStyle, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from src.ui.url_input_widget import UrlInputWidget
from src.ui.download_list import DownloadListWidget
from src.ui.settings_dialog import SettingsDialog
from src.models.download_task import DownloadTask, DownloadStatus
from src.services.yt_dlp_wrapper import YTDLPWrapper
from src.services.video_parser import VideoParser
from src.services.download_manager import DownloadManager
from src.services.config_manager import ConfigManager


class MainWindow(QMainWindow):
    """主窗口组件"""

    def __init__(self):
        super().__init__()

        # 创建配置管理器
        self.config_manager = ConfigManager()

        # 创建服务层组件
        self.ytdlp_wrapper = YTDLPWrapper()
        self.video_parser = VideoParser(self.ytdlp_wrapper)
        self.download_manager = DownloadManager()

        # 从配置加载下载路径
        self._download_path = self.config_manager.get("download_path", os.path.join(os.path.expanduser("~"), "Downloads"))

        # 连接信号
        self.download_manager.task_started.connect(self.on_task_started)
        self.download_manager.task_progress.connect(self.on_task_progress)
        self.download_manager.task_completed.connect(self.on_task_completed)
        self.download_manager.task_failed.connect(self.on_task_failed)
        self.download_manager.task_paused.connect(self.on_task_paused)
        self.download_manager.task_cancelled.connect(self.on_task_cancelled)

        self.init_ui()

        # 应用保存的主题
        theme = self.config_manager.get("theme", "浅色")
        self.apply_theme(theme)

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

        history_action = QAction("下载记录...", self)
        history_action.triggered.connect(self.on_history_clicked)
        file_menu.addAction(history_action)

        file_menu.addSeparator()

        import_action = QAction("导入URL列表...", self)
        import_action.triggered.connect(self.on_import_urls_clicked)
        file_menu.addAction(import_action)

        export_action = QAction("导出下载记录...", self)
        export_action.triggered.connect(self.on_export_history_clicked)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        settings_action = QAction("下载设置...", self)
        settings_action.triggered.connect(self.on_settings_clicked)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")

        select_all_action = QAction("全选任务", self)
        select_all_action.triggered.connect(self.on_select_all)
        edit_menu.addAction(select_all_action)

        edit_menu.addSeparator()

        clear_completed_action = QAction("清除已完成任务", self)
        clear_completed_action.triggered.connect(self.on_clear_completed)
        edit_menu.addAction(clear_completed_action)

        clear_failed_action = QAction("清除失败任务", self)
        clear_failed_action.triggered.connect(self.on_clear_failed)
        edit_menu.addAction(clear_failed_action)

        edit_menu.addSeparator()

        copy_urls_action = QAction("复制所有链接", self)
        copy_urls_action.triggered.connect(self.on_copy_urls)
        edit_menu.addAction(copy_urls_action)

        # 视图菜单
        view_menu = menubar.addMenu("视图")

        theme_menu = view_menu.addMenu("主题")
        light_action = QAction("浅色", self)
        light_action.triggered.connect(lambda: self.apply_theme("浅色"))
        theme_menu.addAction(light_action)
        dark_action = QAction("深色", self)
        dark_action.triggered.connect(lambda: self.apply_theme("深色"))
        theme_menu.addAction(dark_action)

        view_menu.addSeparator()

        self.toolbar_action = QAction("显示工具栏", self)
        self.toolbar_action.setCheckable(True)
        self.toolbar_action.setChecked(True)
        self.toolbar_action.triggered.connect(self.on_toggle_toolbar)
        view_menu.addAction(self.toolbar_action)

        view_menu.addSeparator()

        filter_menu = view_menu.addMenu("筛选任务")
        for label, status in [("全部", None), ("下载中", "DOWNLOADING"), ("已完成", "COMPLETED"), ("已暂停", "PAUSED"), ("失败", "FAILED")]:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, s=status: self.on_filter_tasks(s))
            filter_menu.addAction(action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.on_about_clicked)
        help_menu.addAction(about_action)

        open_dir_action = QAction("打开下载目录", self)
        open_dir_action.triggered.connect(self.on_open_download_dir)
        help_menu.addAction(open_dir_action)

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
        # 更新UI状态
        for task in self.download_list_widget.tasks:
            if task.task_id == task_id:
                task.status = DownloadStatus.COMPLETED
                task.progress = 100
                self.download_list_widget._update_item_widget_status(task)
                break
        # 保存历史记录
        task = self.download_manager.get_task(task_id)
        if task:
            import datetime
            self.config_manager.add_history({
                'title': task.title,
                'url': task.url,
                'file_path': file_path,
                'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    def on_task_failed(self, task_id: str, error_message: str):
        """下载失败"""
        self.status_bar.showMessage(f"下载失败: {error_message}")

    def on_task_paused(self, task_id: str):
        """任务暂停"""
        self.status_bar.showMessage(f"任务已暂停: {task_id}")
        # 更新UI状态
        for task in self.download_list_widget.tasks:
            if task.task_id == task_id:
                task.status = DownloadStatus.PAUSED
                self.download_list_widget._update_item_widget_status(task)
                break

    def on_task_cancelled(self, task_id: str):
        """任务取消"""
        self.status_bar.showMessage(f"任务已取消: {task_id}")
        # 更新UI状态
        for task in self.download_list_widget.tasks:
            if task.task_id == task_id:
                task.status = DownloadStatus.CANCELLED
                self.download_list_widget._update_item_widget_status(task)
                break

    def on_about_clicked(self):
        """关于对话框"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于视频下载器",
            "<b>视频下载器 v1.0</b><br><br>"
            "基于 yt-dlp 的视频下载工具<br>"
            "支持 YouTube、Bilibili、优酷、爱奇艺等平台<br><br>"
            "GitHub: <a href='https://github.com/ZD0314/video-downloader'>video-downloader</a>"
        )

    def on_open_download_dir(self):
        """打开下载目录"""
        import subprocess
        path = self._download_path
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        subprocess.Popen(f'explorer "{path}"')

    def on_toggle_toolbar(self, checked: bool):
        """显示/隐藏工具栏"""
        from PyQt6.QtWidgets import QToolBar
        for tb in self.findChildren(QToolBar):
            tb.setVisible(checked)

    def on_filter_tasks(self, status_name):
        """按状态筛选任务列表"""
        from src.models.download_task import DownloadStatus
        for i in range(self.download_list_widget.content_layout.count()):
            item = self.download_list_widget.content_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                from src.ui.download_item_widget import DownloadItemWidget
                if isinstance(widget, DownloadItemWidget):
                    if status_name is None:
                        widget.setVisible(True)
                    else:
                        widget.setVisible(widget.task.status.name == status_name)

    def on_select_all(self):
        """全选任务"""
        tasks = self.download_list_widget.get_selected_tasks()
        self.status_bar.showMessage(f"已选中 {len(tasks)} 个任务")

    def on_clear_completed(self):
        """清除已完成任务"""
        count = self.download_list_widget.clear_completed()
        self.status_bar.showMessage(f"已清除 {count} 个已完成任务")

    def on_clear_failed(self):
        """清除失败任务"""
        count = self.download_list_widget.clear_failed()
        self.status_bar.showMessage(f"已清除 {count} 个失败任务")

    def on_copy_urls(self):
        """复制所有链接到剪贴板"""
        from PyQt6.QtWidgets import QApplication
        urls = self.download_list_widget.get_urls()
        if not urls:
            self.status_bar.showMessage("暂无任务链接")
            return
        QApplication.clipboard().setText('\n'.join(urls))
        self.status_bar.showMessage(f"已复制 {len(urls)} 个链接")

    def on_export_history_clicked(self):
        """导出下载记录为CSV"""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        import csv
        history = self.config_manager.get_history()
        if not history:
            QMessageBox.information(self, "提示", "暂无下载记录")
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出下载记录", "下载记录.csv", "CSV文件 (*.csv)"
        )
        if not file_path:
            return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'url', 'file_path', 'time'])
                writer.writeheader()
                writer.writerows(history)
            self.status_bar.showMessage(f"已导出 {len(history)} 条记录到: {file_path}")
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"导出失败: {e}")

    def on_import_urls_clicked(self):
        """导入URL列表批量下载"""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择URL列表文件", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            QMessageBox.warning(self, "读取失败", f"无法读取文件: {e}")
            return
        if not urls:
            QMessageBox.information(self, "提示", "文件中没有有效的URL")
            return
        for url in urls:
            task_id = self.download_manager.add_task(url, self._download_path)
            task = self.download_manager.get_task(task_id)
            if task:
                self.download_list_widget.add_task(task)
        self.status_bar.showMessage(f"已添加 {len(urls)} 个下载任务")

    def on_history_clicked(self):
        """打开下载记录对话框"""
        from PyQt6.QtWidgets import (
            QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
            QTableWidgetItem, QPushButton, QHeaderView
        )
        dialog = QDialog(self)
        dialog.setWindowTitle("下载记录")
        dialog.resize(700, 450)

        layout = QVBoxLayout(dialog)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["标题", "下载时间", "文件路径", "链接"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        history = self.config_manager.get_history()
        table.setRowCount(len(history))
        for row, record in enumerate(history):
            table.setItem(row, 0, QTableWidgetItem(record.get('title', '')))
            table.setItem(row, 1, QTableWidgetItem(record.get('time', '')))
            table.setItem(row, 2, QTableWidgetItem(record.get('file_path', '')))
            table.setItem(row, 3, QTableWidgetItem(record.get('url', '')))

        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("清空记录")
        close_btn = QPushButton("关闭")

        def on_clear():
            self.config_manager.clear_history()
            table.setRowCount(0)

        clear_btn.clicked.connect(on_clear)
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        dialog.exec()

    def on_settings_clicked(self):
        """处理设置菜单点击"""
        # 创建设置对话框
        dialog = SettingsDialog(self)

        # 设置当前配置
        current_settings = self.config_manager.get_all()
        dialog.set_settings(current_settings)

        # 连接信号
        dialog.settings_saved.connect(self.on_settings_saved)

        # 显示对话框
        dialog.exec()

    def on_settings_saved(self, settings: dict):
        """处理设置保存"""
        # 保存设置到配置管理器
        self.config_manager.update(settings)
        # 应用设置
        self.on_settings_changed(settings)

    def on_settings_changed(self, settings: dict):
        """处理设置变化"""
        # 更新下载路径
        if settings.get("download_path"):
            self._download_path = settings["download_path"]
            self.status_bar.showMessage(f"下载路径已更新: {self._download_path}")

        # 应用主题
        if settings.get("theme"):
            self.apply_theme(settings["theme"])

    def apply_theme(self, theme: str):
        """应用主题"""
        if theme == "深色":
            # 深色主题样式
            dark_style = """
                QMainWindow {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QWidget {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QGroupBox {
                    border: 1px solid #555;
                    border-radius: 5px;
                    margin-top: 1ex;
                    color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 5px;
                    color: #ffffff;
                }
                QLineEdit, QComboBox, QSpinBox {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #555;
                    border-radius: 3px;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #555;
                    border-radius: 3px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                }
                QProgressBar {
                    border: 1px solid #555;
                    border-radius: 3px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4caf50;
                }
            """
            self.setStyleSheet(dark_style)
        else:
            # 浅色主题（默认）
            self.setStyleSheet("")
        self.status_bar.showMessage(f"主题已切换为: {theme}")
