from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QProgressBar, QPushButton, QFrame
)
from PyQt6.QtCore import pyqtSignal
from src.models.download_task import DownloadTask, DownloadStatus


class DownloadItemWidget(QWidget):
    """下载项组件"""

    # 信号
    pause_requested = pyqtSignal(object)
    resume_requested = pyqtSignal(object)
    cancel_requested = pyqtSignal(object)

    def __init__(self, task: DownloadTask, parent=None):
        super().__init__(parent)
        self.task = task
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 主容器
        container = QFrame()
        container.setFrameStyle(QFrame.Shape.StyledPanel)
        container_layout = QHBoxLayout(container)

        # 标题和进度信息
        info_layout = QVBoxLayout()
        title_label = QLabel(self.task.title or "正在解析...")
        title_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(title_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(self.task.progress)
        info_layout.addWidget(self.progress_bar)

        # 状态信息
        self.status_label = QLabel(self.get_status_text())
        info_layout.addWidget(self.status_label)

        container_layout.addLayout(info_layout, stretch=1)

        # 操作按钮
        btn_layout = QVBoxLayout()
        self.pause_btn = QPushButton("暂停")
        self.cancel_btn = QPushButton("取消")
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.cancel_btn)
        container_layout.addLayout(btn_layout)

        layout.addWidget(container)

        # 连接信号
        self.pause_btn.clicked.connect(self.on_pause_clicked)
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)

    def get_status_text(self) -> str:
        """获取状态文本"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            return f"下载中... {self.task.progress}% | {self.task.speed}"
        elif self.task.status == DownloadStatus.PAUSED:
            return f"已暂停 {self.task.progress}%"
        elif self.task.status == DownloadStatus.COMPLETED:
            return "下载完成"
        elif self.task.status == DownloadStatus.FAILED:
            return f"下载失败: {self.task.error_message}"
        else:
            return "等待中..."

    def update_progress(self, progress: int, total: int):
        """更新进度"""
        self.task.progress = progress
        self.task.total_size = total
        self.progress_bar.setValue(progress)
        self.status_label.setText(self.get_status_text())

    def on_pause_clicked(self):
        """暂停按钮点击"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            self.pause_requested.emit(self.task)
        else:
            self.resume_requested.emit(self.task)

    def on_cancel_clicked(self):
        """取消按钮点击"""
        self.cancel_requested.emit(self.task)
