import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.download_item_widget import DownloadItemWidget
from src.models.download_task import DownloadTask

@pytest.fixture
def app():
    return QApplication([])

def test_download_item_widget_creation(app):
    """测试下载项组件创建"""
    task = DownloadTask(url="https://example.com/video.mp4", title="测试视频")
    widget = DownloadItemWidget(task)
    assert widget is not None

def test_download_item_widget_update_progress(app):
    """测试进度更新"""
    task = DownloadTask(url="https://example.com/video.mp4", title="测试视频")
    widget = DownloadItemWidget(task)
    widget.update_progress(50, 100)
    assert widget.progress_bar.value() == 50
