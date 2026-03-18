from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSpinBox, QComboBox, QCheckBox,
    QPushButton, QGroupBox, QFileDialog
)
from PyQt6.QtCore import pyqtSignal


class SettingsPanel(QWidget):
    """设置面板组件"""

    # 信号
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)

        # 下载设置
        download_group = QGroupBox("下载设置")
        download_layout = QVBoxLayout(download_group)

        # 下载路径
        path_layout = QHBoxLayout()
        path_label = QLabel("下载路径:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("选择下载保存位置")
        self.path_btn = QPushButton("浏览...")
        self.path_btn.clicked.connect(self.on_browse_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_btn)
        download_layout.addLayout(path_layout)

        # 默认画质
        quality_layout = QHBoxLayout()
        quality_label = QLabel("默认画质:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["原画", "1080p", "720p", "480p", "360p"])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        download_layout.addLayout(quality_layout)

        # 默认格式
        format_layout = QHBoxLayout()
        format_label = QLabel("默认格式:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP4", "MKV", "AVI", "MP3"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        download_layout.addLayout(format_layout)

        # 并发下载数
        concurrent_layout = QHBoxLayout()
        concurrent_label = QLabel("并发下载数:")
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 10)
        self.concurrent_spin.setValue(3)
        concurrent_layout.addWidget(concurrent_label)
        concurrent_layout.addWidget(self.concurrent_spin)
        download_layout.addLayout(concurrent_layout)

        layout.addWidget(download_group)

        # 界面设置
        ui_group = QGroupBox("界面设置")
        ui_layout = QVBoxLayout(ui_group)

        # 主题选择
        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["浅色", "深色"])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        ui_layout.addLayout(theme_layout)

        layout.addWidget(ui_group)

        # 保存按钮
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        self.save_btn = QPushButton("保存设置")
        self.save_btn.clicked.connect(self.on_save_settings)
        save_layout.addWidget(self.save_btn)
        layout.addLayout(save_layout)

    def on_browse_path(self):
        """浏览下载路径"""
        path = QFileDialog.getExistingDirectory(self, "选择下载路径")
        if path:
            self.path_input.setText(path)

    def on_save_settings(self):
        """保存设置"""
        settings = {
            "download_path": self.path_input.text(),
            "default_quality": self.quality_combo.currentText(),
            "default_format": self.format_combo.currentText(),
            "concurrent_downloads": self.concurrent_spin.value(),
            "theme": self.theme_combo.currentText()
        }
        self.settings_changed.emit(settings)
