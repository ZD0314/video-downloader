"""设置对话框"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
from src.ui.settings_panel import SettingsPanel


class SettingsDialog(QDialog):
    """设置对话框"""

    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("下载设置")
        self.setGeometry(200, 200, 500, 400)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)

        # 设置面板
        self.settings_panel = SettingsPanel()
        self.settings_panel.settings_changed.connect(self.on_settings_changed)
        layout.addWidget(self.settings_panel)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def on_settings_changed(self, settings: dict):
        """处理设置变化"""
        self.settings_changed.emit(settings)

    def set_settings(self, settings: dict):
        """设置当前配置"""
        self.settings_panel.path_input.setText(settings.get("download_path", ""))
        self.settings_panel.quality_combo.setCurrentText(settings.get("default_quality", "原画"))
        self.settings_panel.format_combo.setCurrentText(settings.get("default_format", "MP4"))
        self.settings_panel.concurrent_spin.setValue(settings.get("concurrent_downloads", 3))
        self.settings_panel.theme_combo.setCurrentText(settings.get("theme", "浅色"))

    def get_settings(self) -> dict:
        """获取当前设置"""
        return {
            "download_path": self.settings_panel.path_input.text(),
            "default_quality": self.settings_panel.quality_combo.currentText(),
            "default_format": self.settings_panel.format_combo.currentText(),
            "concurrent_downloads": self.settings_panel.concurrent_spin.value(),
            "theme": self.settings_panel.theme_combo.currentText()
        }
