"""视频解析器"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
import time

from src.services.yt_dlp_wrapper import YTDLPWrapper, VideoInfo


@dataclass
class FormatInfo:
    """格式信息"""
    format_id: str
    ext: str
    resolution: str
    filesize: int
    fps: Optional[int]
    vcodec: str
    acodec: str


class VideoParser:
    """视频解析器"""

    CACHE_TTL = 300  # 缓存有效期：5分钟

    def __init__(self, ytdlp_wrapper: YTDLPWrapper):
        self._wrapper = ytdlp_wrapper
        self._cache: Dict[str, Tuple[VideoInfo, float]] = {}

    def parse(self, url: str, use_cache: bool = True) -> VideoInfo:
        """解析视频URL，获取视频信息"""
        if use_cache and self._is_cache_valid(url):
            info, _ = self._cache[url]
            return info

        info = self._wrapper.get_video_info(url)
        self._cache[url] = (info, time.time())
        return info

    def parse_playlist(self, url: str) -> List[VideoInfo]:
        """解析播放列表"""
        # TODO: 实现播放列表解析
        return [self.parse(url)]

    def get_formats(self, url: str) -> List[FormatInfo]:
        """获取可用格式列表"""
        info = self.parse(url)
        formats = []
        for fmt in info.formats:
            formats.append(FormatInfo(
                format_id=fmt.get('format_id', ''),
                ext=fmt.get('ext', ''),
                resolution=fmt.get('resolution', ''),
                filesize=fmt.get('filesize', 0) or 0,
                fps=fmt.get('fps'),
                vcodec=fmt.get('vcodec', ''),
                acodec=fmt.get('acodec', '')
            ))
        return formats

    def clear_cache(self) -> None:
        """清空缓存"""
        self._cache.clear()

    def _is_cache_valid(self, url: str) -> bool:
        """检查缓存是否有效"""
        if url not in self._cache:
            return False
        _, timestamp = self._cache[url]
        return time.time() - timestamp < self.CACHE_TTL
