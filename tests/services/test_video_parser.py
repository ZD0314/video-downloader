import pytest
import time
from unittest.mock import MagicMock
from src.services.video_parser import VideoParser, FormatInfo
from src.services.yt_dlp_wrapper import VideoInfo


class TestVideoParser:
    def test_format_info_dataclass(self):
        """测试 FormatInfo 数据类"""
        fmt = FormatInfo(
            format_id="137",
            ext="mp4",
            resolution="1920x1080",
            filesize=1024000,
            fps=30,
            vcodec="avc1",
            acodec="mp4a"
        )
        assert fmt.format_id == "137"
        assert fmt.resolution == "1920x1080"

    def test_parse_caches_result(self):
        """测试解析结果缓存"""
        mock_wrapper = MagicMock()
        mock_wrapper.get_video_info.return_value = VideoInfo(
            id="test", title="Test", duration=100,
            thumbnail="", description="", uploader="", formats=[]
        )

        parser = VideoParser(mock_wrapper)
        info1 = parser.parse("https://test.com/video")
        info2 = parser.parse("https://test.com/video")

        assert info1 == info2
        mock_wrapper.get_video_info.assert_called_once()

    def test_cache_expires_after_ttl(self):
        """测试缓存过期"""
        mock_wrapper = MagicMock()
        mock_wrapper.get_video_info.return_value = VideoInfo(
            id="test", title="Test", duration=100,
            thumbnail="", description="", uploader="", formats=[]
        )

        parser = VideoParser(mock_wrapper)
        parser.CACHE_TTL = 0.1  # 100ms

        parser.parse("https://test.com/video")
        time.sleep(0.15)
        parser.parse("https://test.com/video")

        assert mock_wrapper.get_video_info.call_count == 2

    def test_parse_with_cache_disabled(self):
        """测试禁用缓存"""
        mock_wrapper = MagicMock()
        mock_wrapper.get_video_info.return_value = VideoInfo(
            id="test", title="Test", duration=100,
            thumbnail="", description="", uploader="", formats=[]
        )

        parser = VideoParser(mock_wrapper)
        parser.parse("https://test.com/video", use_cache=False)
        parser.parse("https://test.com/video", use_cache=False)

        assert mock_wrapper.get_video_info.call_count == 2

    def test_clear_cache(self):
        """测试清空缓存"""
        mock_wrapper = MagicMock()
        mock_wrapper.get_video_info.return_value = VideoInfo(
            id="test", title="Test", duration=100,
            thumbnail="", description="", uploader="", formats=[]
        )

        parser = VideoParser(mock_wrapper)
        parser.parse("https://test.com/video")
        parser.clear_cache()
        parser.parse("https://test.com/video")

        assert mock_wrapper.get_video_info.call_count == 2

    def test_is_cache_valid(self):
        """测试缓存有效性检查"""
        mock_wrapper = MagicMock()
        parser = VideoParser(mock_wrapper)
        parser.CACHE_TTL = 1

        assert parser._is_cache_valid("https://test.com/video") is False

        parser._cache["https://test.com/video"] = (
            VideoInfo(id="test", title="Test", duration=100,
                     thumbnail="", description="", uploader="", formats=[]),
            time.time()
        )
        assert parser._is_cache_valid("https://test.com/video") is True
