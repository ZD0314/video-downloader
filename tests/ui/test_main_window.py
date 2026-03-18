# tests/ui/test_main_window.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

@pytest.fixture
def app():
    return QApplication([])

def test_main_window_creation(app):
    """测试主窗口创建"""
    window = MainWindow()
    assert window is not None
    assert window.windowTitle() == "视频下载器"

def test_main_window_initial_size(app):
    """测试主窗口初始大小"""
    window = MainWindow()
    assert window.width() >= 800
    assert window.height() >= 600
