import pytest
from src.models.download_task import DownloadStatus


def test_download_status_has_cancelled():
    """测试 DownloadStatus 包含 CANCELLED 状态"""
    assert hasattr(DownloadStatus, 'CANCELLED')
    assert DownloadStatus.CANCELLED.value == "已取消"


def test_download_status_all_values():
    """测试所有状态值"""
    expected = {"等待中", "下载中", "已暂停", "已完成", "失败", "已取消"}
    actual = {s.value for s in DownloadStatus}
    assert actual == expected
