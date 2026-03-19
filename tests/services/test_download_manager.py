import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMutexLocker
from unittest.mock import MagicMock, patch
from src.services.download_manager import DownloadManager, DownloadWorker
from src.services.yt_dlp_wrapper import YTDLPWrapper
from src.models.download_task import DownloadStatus


@pytest.fixture(scope="session")
def app():
    application = QApplication([])
    yield application


@pytest.fixture
def manager(app):
    """创建 DownloadManager 实例并确保线程池在测试后正确清理"""
    mgr = DownloadManager()
    yield mgr
    # 终止所有线程，避免影响后续测试
    mgr._thread_pool.clear()
    mgr._thread_pool.waitForDone(3000)


class TestDownloadManager:
    def test_add_task(self, manager):
        """测试添加任务"""
        task_id = manager.add_task("https://test.com/video", "/tmp/downloads")
        assert task_id is not None
        assert task_id in manager.get_all_tasks()

    def test_get_task(self, manager):
        """测试获取任务"""
        task_id = manager.add_task("https://test.com/video", "/tmp/downloads")
        task = manager.get_task(task_id)
        assert task is not None
        assert task.url == "https://test.com/video"

    def test_concurrent_limit(self, app):
        """测试并发限制"""
        manager = DownloadManager(max_concurrent=2)
        assert manager._thread_pool.maxThreadCount() == 2

    def test_pause_task(self, manager):
        """测试暂停任务"""
        task_id = manager.add_task("https://test.com/video", "/tmp/downloads")
        result = manager.pause_task(task_id)
        assert result is True
        assert manager.get_task(task_id).status == DownloadStatus.PAUSED

    def test_cancel_task(self, manager):
        """测试取消任务"""
        task_id = manager.add_task("https://test.com/video", "/tmp/downloads")
        result = manager.cancel_task(task_id)
        assert result is True
        assert manager.get_task(task_id).status == DownloadStatus.CANCELLED

    def test_resume_task(self, manager):
        """测试恢复任务"""
        task_id = manager.add_task("https://test.com/video", "/tmp/downloads")

        # 保存任务参数
        manager._task_params[task_id] = {
            'url': "https://test.com/video",
            'output_path': "/tmp/downloads",
            'format_id': None
        }

        # 先暂停
        manager.pause_task(task_id)

        # 恢复
        result = manager.resume_task(task_id)
        assert result is True

    def test_on_progress(self, manager):
        """测试进度更新"""
        task_id = "test-task-1"

        progress_data = []
        def on_progress(tid, downloaded, total, speed):
            progress_data.append((tid, downloaded, total, speed))

        manager.task_progress.connect(on_progress)
        manager._on_progress(task_id, 1024, 2048, "1.0 KB/s")

        assert len(progress_data) == 1
        assert progress_data[0] == (task_id, 1024, 2048, "1.0 KB/s")

    def test_mutex_protection(self, manager):
        """测试互斥锁保护"""
        # 验证 mutex 存在且可使用
        with QMutexLocker(manager._mutex):
            manager._tasks["test"] = MagicMock()
        assert "test" in manager._tasks


class TestDownloadWorker:
    def test_worker_creation(self, app):
        """测试工作线程创建"""
        manager = DownloadManager()
        wrapper = YTDLPWrapper()

        worker = DownloadWorker(
            task_id="test-1",
            url="https://test.com/video",
            output_path="/tmp",
            format_id=None,
            wrapper=wrapper,
            manager=manager
        )

        assert worker.task_id == "test-1"
        assert worker.url == "https://test.com/video"
        assert worker._cancelled is False

    def test_worker_cancel(self, app):
        """测试工作线程取消"""
        manager = DownloadManager()
        wrapper = YTDLPWrapper()

        worker = DownloadWorker(
            task_id="test-1",
            url="https://test.com/video",
            output_path="/tmp",
            format_id=None,
            wrapper=wrapper,
            manager=manager
        )

        worker.cancel()
        assert worker._cancelled is True

    def test_format_speed(self, app):
        """测试速度格式化"""
        manager = DownloadManager()
        wrapper = YTDLPWrapper()

        worker = DownloadWorker(
            task_id="test-1",
            url="https://test.com/video",
            output_path="/tmp",
            format_id=None,
            wrapper=wrapper,
            manager=manager
        )

        assert worker._format_speed(500) == "500 B/s"
        assert worker._format_speed(1536) == "1.5 KB/s"
        assert worker._format_speed(1572864) == "1.5 MB/s"
