# tests/ui/test_ui_integration.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.url_input_widget import UrlInputWidget
from src.ui.download_list import DownloadListWidget
from src.ui.settings_panel import SettingsPanel

@pytest.fixture
def app():
    return QApplication([])

def test_ui_components_integration(app):
    """测试UI组件集成"""
    # 测试主窗口
    window = MainWindow()
    assert window is not None

    # 测试URL输入组件
    url_widget = UrlInputWidget()
    assert url_widget is not None

    # 测试下载列表组件
    list_widget = DownloadListWidget()
    assert list_widget is not None

    # 测试设置面板组件
    settings_panel = SettingsPanel()
    assert settings_panel is not None
