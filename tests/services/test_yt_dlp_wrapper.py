# tests/services/test_yt_dlp_wrapper.py
import pytest
from unittest.mock import patch, MagicMock
from src.services.yt_dlp_wrapper import (
    YTDLPWrapper, VideoInfo,
    YTDLPError, VideoNotFoundError, NetworkError,
    NetworkTimeoutError, NetworkConnectionError, FormatNotAvailableError,
    DiskFullError, PermissionDeniedError
)

class TestYTDLPWrapper:
    def test_video_info_dataclass(self):
        """测试 VideoInfo 数据类"""
        info = VideoInfo(
            id="test123",
            title="Test Video",
            duration=120,
            thumbnail="https://example.com/thumb.jpg",
            description="Test description",
            uploader="Test User",
            formats=[]
        )
        assert info.id == "test123"
        assert info.title == "Test Video"
        assert info.duration == 120

    def test_exception_hierarchy(self):
        """测试异常继承关系"""
        assert issubclass(VideoNotFoundError, YTDLPError)
        assert issubclass(NetworkError, YTDLPError)
        assert issubclass(NetworkTimeoutError, NetworkError)
        assert issubclass(NetworkConnectionError, NetworkError)
        assert issubclass(FormatNotAvailableError, YTDLPError)
        assert issubclass(DiskFullError, YTDLPError)
        assert issubclass(PermissionDeniedError, YTDLPError)

    @patch('yt_dlp.YoutubeDL')
    def test_get_video_info_success(self, mock_ydl):
        """测试成功获取视频信息"""
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance
        mock_instance.extract_info.return_value = {
            'id': 'test123',
            'title': 'Test Video',
            'duration': 120,
            'thumbnail': 'https://example.com/thumb.jpg',
            'description': 'Test description',
            'uploader': 'Test User',
            'formats': [{'format_id': 'best'}]
        }

        wrapper = YTDLPWrapper()
        info = wrapper.get_video_info("https://www.youtube.com/watch?v=test123")

        assert isinstance(info, VideoInfo)
        assert info.title == "Test Video"
        assert info.duration == 120

    @patch('yt_dlp.YoutubeDL')
    def test_get_video_info_not_found(self, mock_ydl):
        """测试视频不存在"""
        import yt_dlp
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance
        mock_instance.extract_info.side_effect = yt_dlp.utils.DownloadError("Video not found")

        wrapper = YTDLPWrapper()
        with pytest.raises(VideoNotFoundError):
            wrapper.get_video_info("https://www.youtube.com/watch?v=invalid")

    @patch('yt_dlp.YoutubeDL')
    def test_download_with_progress_callback(self, mock_ydl):
        """测试下载进度回调"""
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance
        mock_instance.download.return_value = None

        progress_data = []
        def on_progress(data):
            progress_data.append(data)

        wrapper = YTDLPWrapper()
        wrapper.download(
            "https://test.com/video",
            "/tmp/downloads",
            progress_callback=on_progress
        )

        # 验证 yt-dlp 配置包含 progress_hooks
        mock_ydl.assert_called_once()
        call_args = mock_ydl.call_args[0][0]
        assert 'progress_hooks' in call_args

    def test_retry_with_backoff(self):
        """测试指数退避重试"""
        wrapper = YTDLPWrapper()
        wrapper._retry_count = 2
        wrapper._retry_delay = 0.01  # 短延迟用于测试

        call_count = 0
        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise NetworkTimeoutError("Timeout")
            return "success"

        result = wrapper._retry_with_backoff(failing_func)
        assert result == "success"
        assert call_count == 3

    def test_handle_download_error_timeout(self):
        """测试下载错误处理 - 超时"""
        wrapper = YTDLPWrapper()
        with pytest.raises(NetworkTimeoutError):
            wrapper._handle_download_error(Exception("Read timeout"))

    def test_handle_download_error_connection(self):
        """测试下载错误处理 - 连接失败"""
        wrapper = YTDLPWrapper()
        with pytest.raises(NetworkConnectionError):
            wrapper._handle_download_error(Exception("Connection refused"))

    def test_handle_download_error_disk_full(self):
        """测试下载错误处理 - 磁盘空间不足"""
        wrapper = YTDLPWrapper()
        with pytest.raises(DiskFullError):
            wrapper._handle_download_error(Exception("No space left on device"))

    def test_handle_download_error_permission(self):
        """测试下载错误处理 - 权限错误"""
        wrapper = YTDLPWrapper()
        with pytest.raises(PermissionDeniedError):
            wrapper._handle_download_error(Exception("Permission denied"))

    def test_handle_download_error_generic(self):
        """测试下载错误处理 - 通用错误"""
        wrapper = YTDLPWrapper()
        with pytest.raises(YTDLPError):
            wrapper._handle_download_error(Exception("Something went wrong"))

    def test_handle_download_error_video_not_found(self):
        """测试下载错误处理 - 视频不存在"""
        wrapper = YTDLPWrapper()
        with pytest.raises(VideoNotFoundError):
            wrapper._handle_download_error(Exception("Video not found"))

    @patch('yt_dlp.YoutubeDL')
    def test_download_with_format_id(self, mock_ydl):
        """测试下载时指定 format_id"""
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance
        mock_instance.extract_info.return_value = {
            'id': 'test123',
            'title': 'Test Video',
            'ext': 'mp4'
        }
        mock_instance.prepare_filename.return_value = '/tmp/downloads/Test Video.mp4'

        wrapper = YTDLPWrapper()
        result = wrapper.download(
            "https://test.com/video",
            "/tmp/downloads",
            format_id="best[ext=mp4]"
        )

        assert result == '/tmp/downloads/Test Video.mp4'
        call_args = mock_ydl.call_args[0][0]
        assert call_args['format'] == "best[ext=mp4]"

    def test_retry_with_backoff_all_exhausted(self):
        """测试指数退避重试全部耗尽"""
        wrapper = YTDLPWrapper()
        wrapper._retry_count = 2
        wrapper._retry_delay = 0.01

        call_count = 0
        def always_failing():
            nonlocal call_count
            call_count += 1
            raise NetworkTimeoutError("Timeout")

        with pytest.raises(NetworkTimeoutError):
            wrapper._retry_with_backoff(always_failing)

        assert call_count == 3  # _retry_count + 1
