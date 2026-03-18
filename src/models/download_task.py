from enum import Enum
from dataclasses import dataclass


class DownloadStatus(Enum):
    """下载状态"""
    WAITING = "等待中"
    DOWNLOADING = "下载中"
    PAUSED = "已暂停"
    COMPLETED = "已完成"
    FAILED = "失败"


@dataclass
class DownloadTask:
    """下载任务"""
    url: str
    title: str = ""
    status: DownloadStatus = DownloadStatus.WAITING
    progress: int = 0
    total_size: int = 0
    downloaded_size: int = 0
    speed: str = ""
    error_message: str = ""
