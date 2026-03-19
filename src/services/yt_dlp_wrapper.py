"""yt-dlp 封装器"""
from typing import Callable, Optional, Dict, Any, List
from dataclasses import dataclass
import time
import yt_dlp


# 异常定义
class YTDLPError(Exception):
    """yt-dlp基础异常"""
    pass

class VideoNotFoundError(YTDLPError):
    """视频不存在或已删除"""
    pass

class NetworkError(YTDLPError):
    """网络错误"""
    pass

class NetworkTimeoutError(NetworkError):
    """连接超时"""
    pass

class NetworkConnectionError(NetworkError):
    """连接失败"""
    pass

class FormatNotAvailableError(YTDLPError):
    """请求的格式不可用"""
    pass

class DiskFullError(YTDLPError):
    """磁盘空间不足"""
    pass

class PermissionDeniedError(YTDLPError):
    """权限错误"""
    pass


@dataclass
class VideoInfo:
    """视频信息"""
    id: str
    title: str
    duration: int  # 秒
    thumbnail: str
    description: str
    uploader: str
    formats: List[Dict[str, Any]]


class YTDLPWrapper:
    """yt-dlp封装器"""

    def __init__(self):
        self._retry_count = 3
        self._retry_delay = 1.0

    def get_video_info(self, url: str) -> VideoInfo:
        """获取视频信息（不下载）"""
        def _extract():
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return VideoInfo(
                    id=info.get('id', ''),
                    title=info.get('title', ''),
                    duration=info.get('duration', 0),
                    thumbnail=info.get('thumbnail', ''),
                    description=info.get('description', ''),
                    uploader=info.get('uploader', ''),
                    formats=info.get('formats', [])
                )

        try:
            return self._retry_with_backoff(_extract)
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            if 'not found' in error_msg or 'unavailable' in error_msg:
                raise VideoNotFoundError(f"视频不存在: {e}")
            raise YTDLPError(f"解析失败: {e}")

    def download(
        self,
        url: str,
        output_path: str,
        format_id: Optional[str] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> str:
        """下载视频"""
        def progress_hook(d):
            if progress_callback:
                # 在所有状态下都提供文件名信息
                progress_callback({
                    'downloaded_bytes': d.get('downloaded_bytes', 0),
                    'total_bytes': d.get('total_bytes', 0),
                    'speed': d.get('speed', 0),
                    'eta': d.get('eta', 0),
                    'filename': d.get('filename', ''),
                    'status': d.get('status', '')
                })

        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }

        if format_id:
            ydl_opts['format'] = format_id

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        except yt_dlp.utils.DownloadError as e:
            self._handle_download_error(e)
            raise YTDLPError(f"下载失败: {e}")

    def _handle_download_error(self, error: Exception) -> None:
        """处理下载错误"""
        error_msg = str(error).lower()
        if 'not found' in error_msg:
            raise VideoNotFoundError(str(error))
        if 'timeout' in error_msg:
            raise NetworkTimeoutError(str(error))
        if 'connection' in error_msg:
            raise NetworkConnectionError(str(error))
        if 'no space' in error_msg:
            raise DiskFullError(str(error))
        if 'permission' in error_msg:
            raise PermissionDeniedError(str(error))
        raise YTDLPError(str(error))

    def _retry_with_backoff(self, func, *args, **kwargs):
        """指数退避重试"""
        last_exception = None
        for attempt in range(self._retry_count + 1):
            try:
                return func(*args, **kwargs)
            except (NetworkTimeoutError, NetworkConnectionError) as e:
                last_exception = e
                if attempt < self._retry_count:
                    delay = self._retry_delay * (2 ** attempt)
                    time.sleep(delay)
            except YTDLPError:
                raise
        raise last_exception
