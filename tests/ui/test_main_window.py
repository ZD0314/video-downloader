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

def test_main_window_has_services(app):
    """测试主窗口包含服务层组件"""
    window = MainWindow()
    assert hasattr(window, 'ytdlp_wrapper')
    assert hasattr(window, 'video_parser')
    assert hasattr(window, 'download_manager')
    assert hasattr(window, '_download_path')

def test_main_window_signals_connected(app):
    """测试信号连接"""
    window = MainWindow()
    # 验证信号已连接
    assert window.download_manager.receivers(window.download_manager.task_started) > 0
    assert window.download_manager.receivers(window.download_manager.task_completed) > 0
