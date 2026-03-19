"""格式转换器（基于 FFmpeg）"""
import os
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FormatConverterError(Exception):
    pass


class FFmpegNotFoundError(FormatConverterError):
    pass


class FormatConverter:
    """使用 FFmpeg 进行格式转换"""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self._ffmpeg = ffmpeg_path
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """检查 FFmpeg 是否可用"""
        try:
            subprocess.run(
                [self._ffmpeg, "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            raise FFmpegNotFoundError("未找到 FFmpeg，请先安装 FFmpeg 并确保其在 PATH 中")

    def convert(self, input_path: str, output_format: str, output_path: Optional[str] = None) -> str:
        """转换文件格式

        Args:
            input_path: 输入文件路径
            output_format: 目标格式，如 'mp4', 'mp3', 'mkv'
            output_path: 输出文件路径，不指定则与输入同目录

        Returns:
            输出文件路径
        """
        if not os.path.exists(input_path):
            raise FormatConverterError(f"输入文件不存在: {input_path}")

        if output_path is None:
            base = os.path.splitext(input_path)[0]
            output_path = f"{base}.{output_format}"

        cmd = [
            self._ffmpeg, "-i", input_path,
            "-y",  # 覆盖已存在文件
            output_path
        ]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise FormatConverterError(f"FFmpeg 转换失败: {result.stderr[-500:]}")
        except FileNotFoundError:
            raise FFmpegNotFoundError("未找到 FFmpeg")

        logger.info(f"转换完成: {input_path} -> {output_path}")
        return output_path

    def extract_audio(self, input_path: str, output_format: str = "mp3", output_path: Optional[str] = None) -> str:
        """提取音频

        Args:
            input_path: 输入视频文件路径
            output_format: 音频格式，如 'mp3', 'aac', 'm4a'
            output_path: 输出文件路径

        Returns:
            输出文件路径
        """
        if not os.path.exists(input_path):
            raise FormatConverterError(f"输入文件不存在: {input_path}")

        if output_path is None:
            base = os.path.splitext(input_path)[0]
            output_path = f"{base}.{output_format}"

        cmd = [
            self._ffmpeg, "-i", input_path,
            "-vn",           # 不包含视频
            "-y",
            output_path
        ]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise FormatConverterError(f"音频提取失败: {result.stderr[-500:]}")
        except FileNotFoundError:
            raise FFmpegNotFoundError("未找到 FFmpeg")

        logger.info(f"音频提取完成: {input_path} -> {output_path}")
        return output_path

    @staticmethod
    def is_ffmpeg_available(ffmpeg_path: str = "ffmpeg") -> bool:
        """检查 FFmpeg 是否可用"""
        try:
            subprocess.run(
                [ffmpeg_path, "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
