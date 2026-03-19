# src/ui/download_list.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from src.ui.download_item_widget import DownloadItemWidget
from src.models.download_task import DownloadTask


class DownloadListWidget(QWidget):
    """下载列表组件"""

    # 信号
    task_pause_requested = pyqtSignal(object)
    task_resume_requested = pyqtSignal(object)
    task_cancel_requested = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.tasks = []

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # 内容容器
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(5)

        # 空状态提示
        self.empty_label = QLabel("暂无下载任务")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.empty_label)

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

    def add_task(self, task: DownloadTask):
        """添加下载任务"""
        self.tasks.append(task)

        # 隐藏空状态提示
        self.empty_label.hide()

        # 创建下载项组件
        item_widget = DownloadItemWidget(task)
        item_widget.pause_requested.connect(self.on_task_pause)
        item_widget.resume_requested.connect(self.on_task_resume)
        item_widget.cancel_requested.connect(self.on_task_cancel)

        self.content_layout.insertWidget(self.content_layout.count() - 1, item_widget)

    def count(self) -> int:
        """获取任务数量"""
        return len(self.tasks)

    def on_task_pause(self, task: DownloadTask):
        """处理任务暂停请求"""
        self.task_pause_requested.emit(task)

    def on_task_resume(self, task: DownloadTask):
        """处理任务恢复请求"""
        self.task_resume_requested.emit(task)

    def on_task_cancel(self, task: DownloadTask):
        """处理任务取消请求"""
        self.task_cancel_requested.emit(task)

    def update_progress(self, task_id: str, downloaded: int, total: int, speed: str):
        """更新任务进度"""
        for task in self.tasks:
            if task.url == task_id:
                task.downloaded_size = downloaded
                task.total_size = total
                task.speed = speed
                if total > 0:
                    task.progress = int(downloaded * 100 / total)
                self._update_item_widget(task)
                break

    def _update_item_widget(self, task: DownloadTask):
        """更新下载项组件"""
        for i in range(self.content_layout.count()):
            item = self.content_layout.itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, DownloadItemWidget) and widget.task == task:
                    widget.update_progress(task.progress, task.total_size)
                    break
