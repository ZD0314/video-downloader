"""下载管理器"""
import logging
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool, QMutex, QMutexLocker, QMetaObject, Qt, Q_ARG
from typing import Dict, Optional
import uuid

logger = logging.getLogger(__name__)

from src.services.yt_dlp_wrapper import YTDLPWrapper, YTDLPError
from src.models.download_task import DownloadTask, DownloadStatus


class DownloadManager(QObject):
    """下载管理器"""

    # 信号定义
    task_added = pyqtSignal(str)
    task_started = pyqtSignal(str)
    task_progress = pyqtSignal(str, int, int, str)  # task_id, downloaded, total, speed
    task_completed = pyqtSignal(str, str)  # task_id, file_path
    task_failed = pyqtSignal(str, str)  # task_id, error_message
    task_paused = pyqtSignal(str)
    task_cancelled = pyqtSignal(str)

    def __init__(self, max_concurrent: int = 3):
        super().__init__()
        self._max_concurrent = max_concurrent
        self._thread_pool = QThreadPool()
        self._thread_pool.setMaxThreadCount(max_concurrent)
        self._tasks: Dict[str, DownloadTask] = {}
        self._workers: Dict[str, DownloadWorker] = {}
        self._task_params: Dict[str, Dict] = {}
        self._mutex = QMutex()

    def add_task(
        self,
        url: str,
        output_path: str,
        format_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> str:
        """添加下载任务"""
        task_id = str(uuid.uuid4())[:8]

        with QMutexLocker(self._mutex):
            task = DownloadTask(
                task_id=task_id,
                url=url,
                title=title or url,
                status=DownloadStatus.WAITING
            )
            self._tasks[task_id] = task
            self._task_params[task_id] = {
                'url': url,
                'output_path': output_path,
                'format_id': format_id
            }

        self.task_added.emit(task_id)

        worker = DownloadWorker(
            task_id=task_id,
            url=url,
            output_path=output_path,
            format_id=format_id,
            wrapper=YTDLPWrapper(),
            manager=self
        )

        with QMutexLocker(self._mutex):
            self._workers[task_id] = worker

        self._thread_pool.start(worker)
        return task_id

    def pause_task(self, task_id: str) -> bool:
        """暂停任务"""
        with QMutexLocker(self._mutex):
            if task_id not in self._workers:
                return False
            worker = self._workers[task_id]
            worker.cancel()
            # 从工作线程字典中移除
            del self._workers[task_id]
            if task_id in self._tasks:
                self._tasks[task_id].status = DownloadStatus.PAUSED

        self.task_paused.emit(task_id)
        return True

    def resume_task(self, task_id: str) -> bool:
        """恢复任务"""
        with QMutexLocker(self._mutex):
            if task_id not in self._tasks:
                return False
            task = self._tasks[task_id]
            if task.status != DownloadStatus.PAUSED:
                return False
            if task_id not in self._task_params:
                return False

            params = self._task_params[task_id]
            task.status = DownloadStatus.WAITING

        worker = DownloadWorker(
            task_id=task_id,
            url=params['url'],
            output_path=params['output_path'],
            format_id=params.get('format_id'),
            wrapper=YTDLPWrapper(),
            manager=self
        )

        with QMutexLocker(self._mutex):
            self._workers[task_id] = worker

        self._thread_pool.start(worker)
        self.task_started.emit(task_id)
        return True

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with QMutexLocker(self._mutex):
            if task_id not in self._workers:
                return False
            worker = self._workers[task_id]
            worker.cancel()
            # 从工作线程字典中移除
            del self._workers[task_id]
            if task_id in self._tasks:
                self._tasks[task_id].status = DownloadStatus.CANCELLED

        self.task_cancelled.emit(task_id)
        return True

    def get_task(self, task_id: str) -> Optional[DownloadTask]:
        """获取任务信息"""
        with QMutexLocker(self._mutex):
            return self._tasks.get(task_id)

    def get_all_tasks(self) -> Dict[str, DownloadTask]:
        """获取所有任务"""
        with QMutexLocker(self._mutex):
            return self._tasks.copy()

    @pyqtSlot(str, int, int, str)
    def _on_progress(self, task_id: str, downloaded: int, total: int, speed: str):
        """进度回调"""
        with QMutexLocker(self._mutex):
            if task_id in self._tasks:
                task = self._tasks[task_id]
                task.downloaded_size = downloaded
                task.total_size = total
                task.speed = speed
                if total > 0:
                    task.progress = int(downloaded * 100 / total)

        self.task_progress.emit(task_id, downloaded, total, speed)

    @pyqtSlot(str, str)
    def _on_completed(self, task_id: str, file_path: str):
        """完成回调"""
        with QMutexLocker(self._mutex):
            if task_id in self._tasks:
                self._tasks[task_id].status = DownloadStatus.COMPLETED

        self.task_completed.emit(task_id, file_path)

    @pyqtSlot(str, str)
    def _on_failed(self, task_id: str, error_message: str):
        """失败回调"""
        with QMutexLocker(self._mutex):
            if task_id in self._tasks:
                self._tasks[task_id].status = DownloadStatus.FAILED
                self._tasks[task_id].error_message = error_message

        self.task_failed.emit(task_id, error_message)

    @pyqtSlot(str)
    def _on_started(self, task_id: str):
        """开始回调"""
        with QMutexLocker(self._mutex):
            if task_id in self._tasks:
                self._tasks[task_id].status = DownloadStatus.DOWNLOADING


class DownloadWorker(QRunnable):
    """下载工作线程"""

    def __init__(
        self,
        task_id: str,
        url: str,
        output_path: str,
        format_id: Optional[str],
        wrapper: YTDLPWrapper,
        manager: DownloadManager
    ):
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.output_path = output_path
        self.format_id = format_id
        self.wrapper = wrapper
        self.manager = manager
        self._cancelled = False
        self.setAutoDelete(True)

    def run(self):
        """执行下载"""
        try:
            # 更新任务状态为下载中
            QMetaObject.invokeMethod(
                self.manager, "_on_started",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, self.task_id)
            )
            # 发射任务开始信号
            QMetaObject.invokeMethod(
                self.manager, "task_started",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, self.task_id)
            )

            def on_progress(data):
                if self._cancelled:
                    raise YTDLPError("下载已取消")

                downloaded = data.get('downloaded_bytes', 0)
                total = data.get('total_bytes', 0)
                speed = self._format_speed(data.get('speed', 0))

                QMetaObject.invokeMethod(
                    self.manager, "_on_progress",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, self.task_id),
                    Q_ARG(int, downloaded),
                    Q_ARG(int, total),
                    Q_ARG(str, speed)
                )

            file_path = self.wrapper.download(
                url=self.url,
                output_path=self.output_path,
                format_id=self.format_id,
                progress_callback=on_progress
            )

            QMetaObject.invokeMethod(
                self.manager, "_on_completed",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, self.task_id),
                Q_ARG(str, file_path)
            )

        except YTDLPError as e:
            if not self._cancelled:
                QMetaObject.invokeMethod(
                    self.manager, "_on_failed",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, self.task_id),
                    Q_ARG(str, str(e))
                )
        except Exception as e:
            logger.exception("下载任务 %s 发生未预期错误", self.task_id)
            if not self._cancelled:
                QMetaObject.invokeMethod(
                    self.manager, "_on_failed",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, self.task_id),
                    Q_ARG(str, str(e))
                )

    def cancel(self):
        """标记取消"""
        self._cancelled = True

    def _format_speed(self, speed_bytes: float) -> str:
        """格式化下载速度"""
        if speed_bytes < 1024:
            return f"{speed_bytes:.0f} B/s"
        elif speed_bytes < 1024 * 1024:
            return f"{speed_bytes / 1024:.1f} KB/s"
        else:
            return f"{speed_bytes / (1024 * 1024):.1f} MB/s"
