# tests/ui/test_download_list.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.download_list import DownloadListWidget
from src.models.download_task import DownloadTask

@pytest.fixture
def app():
    return QApplication([])

def test_download_list_widget_creation(app):
    """测试下载列表组件创建"""
    widget = DownloadListWidget()
    assert widget is not None

def test_download_list_add_task(app):
    """测试添加下载任务"""
    widget = DownloadListWidget()
    task = DownloadTask(task_id="test123", url="https://example.com/video.mp4", title="测试视频")
    widget.add_task(task)
    assert widget.count() == 1

def test_update_progress(app):
    """测试更新进度"""
    widget = DownloadListWidget()
    task = DownloadTask(task_id="test456", url="https://test.com/video", title="Test")
    widget.add_task(task)

    widget.update_progress("test456", 1024, 2048, "1.0 KB/s")

    assert task.downloaded_size == 1024
    assert task.total_size == 2048
    assert task.speed == "1.0 KB/s"
    assert task.progress == 50
