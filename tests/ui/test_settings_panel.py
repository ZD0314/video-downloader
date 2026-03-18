import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.settings_panel import SettingsPanel

@pytest.fixture
def app():
    return QApplication([])

def test_settings_panel_creation(app):
    """测试设置面板组件创建"""
    panel = SettingsPanel()
    assert panel is not None
