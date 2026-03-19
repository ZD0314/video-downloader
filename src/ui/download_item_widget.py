from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QProgressBar, QPushButton, QFrame
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
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
        container.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 5px;
                border: 1px solid #e0e0e0;
            }
        """)
        container_layout = QHBoxLayout(container)

        # 标题和进度信息
        info_layout = QVBoxLayout()

        # 标题行
        title_layout = QHBoxLayout()
        self.title_label = QLabel(self.task.title or "正在解析...")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        # 状态标签
        self.status_badge = QLabel(self.get_status_text())
        self.status_badge.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                color: #1976d2;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 11px;
            }
        """)
        title_layout.addWidget(self.status_badge)
        info_layout.addLayout(title_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(self.task.progress)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 3px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 2px;
            }
        """)
        info_layout.addWidget(self.progress_bar)

        # 详细信息
        self.detail_label = QLabel(self.get_detail_text())
        self.detail_label.setStyleSheet("font-size: 11px; color: #666;")
        info_layout.addWidget(self.detail_label)

        container_layout.addLayout(info_layout, stretch=1)

        # 操作按钮
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(3)

        self.pause_btn = QPushButton("暂停")
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
        """)

        self.resume_btn = QPushButton("继续下载")
        self.resume_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        self.resume_btn.setVisible(False)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)

        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.resume_btn)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addStretch()
        container_layout.addLayout(btn_layout)

        layout.addWidget(container)

        # 连接信号
        self.pause_btn.clicked.connect(self.on_pause_clicked)
        self.resume_btn.clicked.connect(self.on_resume_clicked)
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)

        # 更新按钮状态和颜色
        self.update_button_states()
        self.update_status_color()

    def update_button_states(self):
        """根据任务状态更新按钮可见性"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            self.pause_btn.setVisible(True)
            self.resume_btn.setVisible(False)
        elif self.task.status == DownloadStatus.PAUSED:
            self.pause_btn.setVisible(False)
            self.resume_btn.setVisible(True)
        else:
            self.pause_btn.setVisible(False)
            self.resume_btn.setVisible(False)

    def update_status_color(self):
        """根据任务状态更新状态标签颜色"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            self.status_badge.setStyleSheet("""
                QLabel {
                    background-color: #e3f2fd;
                    color: #1976d2;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 11px;
                }
            """)
        elif self.task.status == DownloadStatus.PAUSED:
            self.status_badge.setStyleSheet("""
                QLabel {
                    background-color: #fff3e0;
                    color: #f57c00;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 11px;
                }
            """)
        elif self.task.status == DownloadStatus.COMPLETED:
            self.status_badge.setStyleSheet("""
                QLabel {
                    background-color: #e8f5e9;
                    color: #388e3c;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 11px;
                }
            """)
        elif self.task.status == DownloadStatus.FAILED:
            self.status_badge.setStyleSheet("""
                QLabel {
                    background-color: #ffebee;
                    color: #d32f2f;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 11px;
                }
            """)
        elif self.task.status == DownloadStatus.CANCELLED:
            self.status_badge.setStyleSheet("""
                QLabel {
                    background-color: #f5f5f5;
                    color: #616161;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 11px;
                }
            """)
        else:  # WAITING
            self.status_badge.setStyleSheet("""
                QLabel {
                    background-color: #f3e5f5;
                    color: #7b1fa2;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 11px;
                }
            """)

    def get_status_text(self) -> str:
        """获取状态文本"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            return "下载中"
        elif self.task.status == DownloadStatus.PAUSED:
            return "已暂停"
        elif self.task.status == DownloadStatus.COMPLETED:
            return "已完成"
        elif self.task.status == DownloadStatus.FAILED:
            return "失败"
        elif self.task.status == DownloadStatus.CANCELLED:
            return "已取消"
        else:
            return "等待中"

    def get_detail_text(self) -> str:
        """获取详细信息文本"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            return f"{self.task.progress}% | {self.task.speed}"
        elif self.task.status == DownloadStatus.PAUSED:
            return f"已暂停 {self.task.progress}%"
        elif self.task.status == DownloadStatus.COMPLETED:
            return f"完成 - {self._format_size(self.task.total_size)}"
        elif self.task.status == DownloadStatus.FAILED:
            return f"错误: {self.task.error_message}"
        else:
            return "等待开始下载..."

    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def update_progress(self, progress: int, total: int):
        """更新进度"""
        # 只有在下载中状态时才更新进度和进度条
        if self.task.status == DownloadStatus.DOWNLOADING:
            self.task.progress = progress
            self.task.total_size = total
            self.progress_bar.setValue(progress)

        # 总是更新状态标签和详细信息（包括暂停状态）
        self.status_badge.setText(self.get_status_text())
        self.detail_label.setText(self.get_detail_text())
        self.update_button_states()
        self.update_status_color()

    def update_status_only(self):
        """只更新状态（用于暂停/恢复后）"""
        self.status_badge.setText(self.get_status_text())
        self.detail_label.setText(self.get_detail_text())
        self.update_button_states()
        self.update_status_color()

    def on_pause_clicked(self):
        """暂停按钮点击"""
        self.pause_requested.emit(self.task)

    def on_resume_clicked(self):
        """恢复按钮点击"""
        self.resume_requested.emit(self.task)

    def on_cancel_clicked(self):
        """取消按钮点击：先暂停，弹确认框，确认后取消并删除"""
        from PyQt6.QtWidgets import QMessageBox
        # 如果正在下载，先暂停
        was_downloading = self.task.status == DownloadStatus.DOWNLOADING
        if was_downloading:
            self.pause_requested.emit(self.task)
        # 弹确认框
        reply = QMessageBox.question(
            self,
            "确认取消",
            f"确定要取消下载并删除任务吗？\n{self.task.title}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.cancel_requested.emit(self.task)
        elif was_downloading:
            # 用户选择不取消，恢复下载
            self.resume_requested.emit(self.task)
