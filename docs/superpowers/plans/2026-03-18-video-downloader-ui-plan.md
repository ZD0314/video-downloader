# 视频下载器UI页面实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建视频下载器应用的UI页面，包括主窗口、下载列表、设置面板等组件

**Architecture:** 使用PyQt6构建桌面应用，采用MVC模式分离界面和业务逻辑，每个UI组件独立封装

**Tech Stack:** Python, PyQt6, pytest-qt

---

## 文件结构映射

### 将要创建的文件
- `src/ui/main_window.py` - 主窗口组件
- `src/ui/download_list.py` - 下载列表组件
- `src/ui/settings_panel.py` - 设置面板组件
- `src/ui/url_input_widget.py` - URL输入组件
- `src/ui/download_item_widget.py` - 单个下载项组件
- `tests/ui/test_main_window.py` - 主窗口测试
- `tests/ui/test_download_list.py` - 下载列表测试

### 将要修改的文件
- `src/main.py` - 应用入口，创建主窗口并启动

---

### Task 1: 创建项目基础结构

**Files:**
- Create: `src/__init__.py`
- Create: `src/ui/__init__.py`
- Create: `src/services/__init__.py`
- Create: `src/models/__init__.py`
- Create: `src/utils/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/ui/__init__.py`

- [ ] **Step 1: 创建包初始化文件**

创建 `src/__init__.py`:
```python
# src/__init__.py
"""视频下载器应用包"""
```

创建 `src/ui/__init__.py`:
```python
# src/ui/__init__.py
"""用户界面组件"""
```

创建其他包初始化文件...

- [ ] **Step 2: 创建主应用入口**

创建 `src/main.py`:
```python
# src/main.py
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 提交基础结构**

Run:
```bash
git add src/__init__.py src/ui/__init__.py src/services/__init__.py src/models/__init__.py src/utils/__init__.py tests/__init__.py tests/ui/__init__.py src/main.py
git commit -m "feat: 创建项目基础结构"
```

---

### Task 2: 创建主窗口组件

**Files:**
- Create: `src/ui/main_window.py`
- Test: `tests/ui/test_main_window.py`

- [ ] **Step 1: 写失败测试**

创建 `tests/ui/test_main_window.py`:
```python
# tests/ui/test_main_window.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

@pytest.fixture
def app():
    return QApplication([])

def test_main_window_creation(app):
    """测试主窗口创建"""
    window = MainWindow()
    assert window is not None
    assert window.windowTitle() == "视频下载器"

def test_main_window_initial_size(app):
    """测试主窗口初始大小"""
    window = MainWindow()
    assert window.width() >= 800
    assert window.height() >= 600
```

- [ ] **Step 2: 运行测试验证失败**

Run:
```bash
pytest tests/ui/test_main_window.py -v
```
Expected: FAIL - MainWindow not defined

- [ ] **Step 3: 创建主窗口实现**

创建 `src/ui/main_window.py`:
```python
# src/ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QStatusBar, QMenuBar, QMenu, QToolBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    """主窗口组件"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("视频下载器")
        self.setGeometry(100, 100, 900, 700)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        layout = QVBoxLayout(central_widget)

        # URL输入区域
        url_layout = QHBoxLayout()
        url_label = QLabel("视频URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入视频URL，支持YouTube、Bilibili等")
        self.download_btn = QPushButton("下载")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.download_btn)
        layout.addLayout(url_layout)

        # 下载列表区域
        self.download_list = QTextEdit()
        self.download_list.setReadOnly(True)
        self.download_list.setPlaceholderText("下载列表将显示在这里...")
        layout.addWidget(self.download_list)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 菜单栏
        self.init_menu_bar()

        # 工具栏
        self.init_tool_bar()

    def init_menu_bar(self):
        """初始化菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")

        # 视图菜单
        view_menu = menubar.addMenu("视图")

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)

    def init_tool_bar(self):
        """初始化工具栏"""
        toolbar = QToolBar("工具栏")
        self.addToolBar(toolbar)

        # 添加工具栏按钮
        download_action = QAction("下载", self)
        toolbar.addAction(download_action)

        pause_action = QAction("暂停", self)
        toolbar.addAction(pause_action)

        cancel_action = QAction("取消", self)
        toolbar.addAction(cancel_action)
```

- [ ] **Step 4: 运行测试验证通过**

Run:
```bash
pytest tests/ui/test_main_window.py -v
```
Expected: PASS

- [ ] **Step 5: 提交主窗口组件**

Run:
```bash
git add src/ui/main_window.py tests/ui/test_main_window.py
git commit -m "feat: 创建主窗口组件"
```

---

### Task 3: 创建URL输入组件

**Files:**
- Create: `src/ui/url_input_widget.py`
- Test: `tests/ui/test_url_input_widget.py`

- [ ] **Step 1: 写失败测试**

创建 `tests/ui/test_url_input_widget.py`:
```python
# tests/ui/test_url_input_widget.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.url_input_widget import UrlInputWidget

@pytest.fixture
def app():
    return QApplication([])

def test_url_input_widget_creation(app):
    """测试URL输入组件创建"""
    widget = UrlInputWidget()
    assert widget is not None

def test_url_input_widget_url_property(app):
    """测试URL属性"""
    widget = UrlInputWidget()
    widget.set_url("https://www.youtube.com/watch?v=test")
    assert widget.get_url() == "https://www.youtube.com/watch?v=test"
```

- [ ] **Step 2: 运行测试验证失败**

Run:
```bash
pytest tests/ui/test_url_input_widget.py -v
```
Expected: FAIL - UrlInputWidget not defined

- [ ] **Step 3: 创建URL输入组件**

创建 `src/ui/url_input_widget.py`:
```python
# src/ui/url_input_widget.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal


class UrlInputWidget(QWidget):
    """URL输入组件"""

    # 信号
    download_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)

        # URL标签
        url_label = QLabel("视频URL:")
        layout.addWidget(url_label)

        # URL输入框
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入视频URL，支持YouTube、Bilibili等")
        layout.addWidget(self.url_input, stretch=1)

        # 下载按钮
        self.download_btn = QPushButton("下载")
        self.download_btn.clicked.connect(self.on_download_clicked)
        layout.addWidget(self.download_btn)

    def on_download_clicked(self):
        """下载按钮点击事件"""
        url = self.url_input.text().strip()
        if url:
            self.download_requested.emit(url)

    def get_url(self) -> str:
        """获取URL"""
        return self.url_input.text().strip()

    def set_url(self, url: str):
        """设置URL"""
        self.url_input.setText(url)

    def clear(self):
        """清空输入"""
        self.url_input.clear()
```

- [ ] **Step 4: 运行测试验证通过**

Run:
```bash
pytest tests/ui/test_url_input_widget.py -v
```
Expected: PASS

- [ ] **Step 5: 提交URL输入组件**

Run:
```bash
git add src/ui/url_input_widget.py tests/ui/test_url_input_widget.py
git commit -m "feat: 创建URL输入组件"
```

---

### Task 4: 创建下载项组件

**Files:**
- Create: `src/ui/download_item_widget.py`
- Test: `tests/ui/test_download_item_widget.py`

- [ ] **Step 1: 写失败测试**

创建 `tests/ui/test_download_item_widget.py`:
```python
# tests/ui/test_download_item_widget.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.download_item_widget import DownloadItemWidget
from src.models.download_task import DownloadTask

@pytest.fixture
def app():
    return QApplication([])

def test_download_item_widget_creation(app):
    """测试下载项组件创建"""
    task = DownloadTask(url="https://example.com/video.mp4", title="测试视频")
    widget = DownloadItemWidget(task)
    assert widget is not None

def test_download_item_widget_update_progress(app):
    """测试进度更新"""
    task = DownloadTask(url="https://example.com/video.mp4", title="测试视频")
    widget = DownloadItemWidget(task)
    widget.update_progress(50, 100)
    assert widget.progress_bar.value() == 50
```

- [ ] **Step 2: 运行测试验证失败**

Run:
```bash
pytest tests/ui/test_download_item_widget.py -v
```
Expected: FAIL - DownloadItemWidget or DownloadTask not defined

- [ ] **Step 3: 创建下载任务模型**

创建 `src/models/download_task.py`:
```python
# src/models/download_task.py
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
```

- [ ] **Step 4: 创建下载项组件**

创建 `src/ui/download_item_widget.py`:
```python
# src/ui/download_item_widget.py
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QProgressBar, QPushButton, QFrame
)
from PyQt6.QtCore import pyqtSignal
from src.models.download_task import DownloadTask, DownloadStatus


class DownloadItemWidget(QWidget):
    """下载项组件"""

    # 信号
    pause_requested = pyqtSignal(object)
    resume_requested = pyqtSignal(object)
    cancel_requested = pyqtSignal(object)

    def __init__(self, task: DownloadTask, parent=None):
        super().__init__(parent)
        self.task = task
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 主容器
        container = QFrame()
        container.setFrameStyle(QFrame.StyledPanel)
        container_layout = QHBoxLayout(container)

        # 标题和进度信息
        info_layout = QVBoxLayout()
        title_label = QLabel(self.task.title or "正在解析...")
        title_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(title_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(self.task.progress)
        info_layout.addWidget(self.progress_bar)

        # 状态信息
        self.status_label = QLabel(self.get_status_text())
        info_layout.addWidget(self.status_label)

        container_layout.addLayout(info_layout, stretch=1)

        # 操作按钮
        btn_layout = QVBoxLayout()
        self.pause_btn = QPushButton("暂停")
        self.cancel_btn = QPushButton("取消")
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.cancel_btn)
        container_layout.addLayout(btn_layout)

        layout.addWidget(container)

        # 连接信号
        self.pause_btn.clicked.connect(self.on_pause_clicked)
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)

    def get_status_text(self) -> str:
        """获取状态文本"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            return f"下载中... {self.task.progress}% | {self.task.speed}"
        elif self.task.status == DownloadStatus.PAUSED:
            return f"已暂停 {self.task.progress}%"
        elif self.task.status == DownloadStatus.COMPLETED:
            return "下载完成"
        elif self.task.status == DownloadStatus.FAILED:
            return f"下载失败: {self.task.error_message}"
        else:
            return "等待中..."

    def update_progress(self, progress: int, total: int):
        """更新进度"""
        self.task.progress = progress
        self.task.total_size = total
        self.progress_bar.setValue(progress)
        self.status_label.setText(self.get_status_text())

    def on_pause_clicked(self):
        """暂停按钮点击"""
        if self.task.status == DownloadStatus.DOWNLOADING:
            self.pause_requested.emit(self.task)
        else:
            self.resume_requested.emit(self.task)

    def on_cancel_clicked(self):
        """取消按钮点击"""
        self.cancel_requested.emit(self.task)
```

- [ ] **Step 5: 运行测试验证通过**

Run:
```bash
pytest tests/ui/test_download_item_widget.py -v
```
Expected: PASS

- [ ] **Step 6: 提交下载项组件**

Run:
```bash
git add src/models/download_task.py src/ui/download_item_widget.py tests/ui/test_download_item_widget.py
git commit -m "feat: 创建下载项组件和下载任务模型"
```

---

### Task 5: 创建下载列表组件

**Files:**
- Create: `src/ui/download_list.py`
- Test: `tests/ui/test_download_list.py`

- [ ] **Step 1: 写失败测试**

创建 `tests/ui/test_download_list.py`:
```python
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
    task = DownloadTask(url="https://example.com/video.mp4", title="测试视频")
    widget.add_task(task)
    assert widget.count() == 1
```

- [ ] **Step 2: 运行测试验证失败**

Run:
```bash
pytest tests/ui/test_download_list.py -v
```
Expected: FAIL - DownloadListWidget not defined

- [ ] **Step 3: 创建下载列表组件**

创建 `src/ui/download_list.py`:
```python
# src/ui/download_list.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt6.QtCore import pyqtSignal
from src.ui.download_item_widget import DownloadItemWidget
from src.models.download_task import DownloadTask


class DownloadListWidget(QWidget):
    """下载列表组件"""

    # 信号
    task_pause_requested = pyqtSignal(object)
    task_resume_requested = pyqtSignal(object)
    task_cancel_requested = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.tasks = []

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # 内容容器
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(5)

        # 空状态提示
        self.empty_label = QLabel("暂无下载任务")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.empty_label)

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

    def add_task(self, task: DownloadTask):
        """添加下载任务"""
        self.tasks.append(task)

        # 隐藏空状态提示
        self.empty_label.hide()

        # 创建下载项组件
        item_widget = DownloadItemWidget(task)
        item_widget.pause_requested.connect(self.on_task_pause)
        item_widget.resume_requested.connect(self.on_task_resume)
        item_widget.cancel_requested.connect(self.on_task_cancel)

        self.content_layout.insertWidget(self.content_layout.count() - 1, item_widget)

    def count(self) -> int:
        """获取任务数量"""
        return len(self.tasks)

    def on_task_pause(self, task: DownloadTask):
        """处理任务暂停请求"""
        self.task_pause_requested.emit(task)

    def on_task_resume(self, task: DownloadTask):
        """处理任务恢复请求"""
        self.task_resume_requested.emit(task)

    def on_task_cancel(self, task: DownloadTask):
        """处理任务取消请求"""
        self.task_cancel_requested.emit(task)
```

- [ ] **Step 4: 运行测试验证通过**

Run:
```bash
pytest tests/ui/test_download_list.py -v
Expected: PASS
```

- [ ] **Step 5: 提交下载列表组件**

Run:
```bash
git add src/ui/download_list.py tests/ui/test_download_list.py
git commit -m "feat: 创建下载列表组件"
```

---

### Task 6: 集成UI组件到主窗口

**Files:**
- Modify: `src/ui/main_window.py`

- [ ] **Step 1: 修改主窗口集成组件**

修改 `src/ui/main_window.py`:
```python
# src/ui/main_window.py (修改部分)
from src.ui.url_input_widget import UrlInputWidget
from src.ui.download_list import DownloadListWidget

class MainWindow(QMainWindow):
    def init_ui(self):
        # ... 其他代码 ...

        # URL输入区域 (替换原来的简单实现)
        self.url_input_widget = UrlInputWidget()
        layout.addWidget(self.url_input_widget)

        # 下载列表区域 (替换原来的QTextEdit)
        self.download_list_widget = DownloadListWidget()
        layout.addWidget(self.download_list_widget)

        # 连接信号
        self.url_input_widget.download_requested.connect(self.on_download_requested)
        self.download_list_widget.task_pause_requested.connect(self.on_task_pause)
        self.download_list_widget.task_resume_requested.connect(self.on_task_resume)
        self.download_list_widget.task_cancel_requested.connect(self.on_task_cancel)

    def on_download_requested(self, url: str):
        """处理下载请求"""
        self.status_bar.showMessage(f"开始下载: {url}")
        # TODO: 调用下载管理器

    def on_task_pause(self, task):
        """处理任务暂停"""
        pass

    def on_task_resume(self, task):
        """处理任务恢复"""
        pass

    def on_task_cancel(self, task):
        """处理任务取消"""
        pass
```

- [ ] **Step 2: 运行应用验证**

Run:
```bash
python src/main.py
```
Expected: 应用窗口正常显示，包含URL输入和下载列表

- [ ] **Step 3: 提交集成代码**

Run:
```bash
git add src/ui/main_window.py
git commit -m "feat: 集成UI组件到主窗口"
```

---

### Task 7: 创建设置面板组件

**Files:**
- Create: `src/ui/settings_panel.py`
- Test: `tests/ui/test_settings_panel.py`

- [ ] **Step 1: 写失败测试**

创建 `tests/ui/test_settings_panel.py`:
```python
# tests/ui/test_settings_panel.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.settings_panel import SettingsPanel

@pytest.fixture
def app():
    return QApplication([])

def test_settings_panel_creation(app):
    """测试设置面板组件创建"""
    panel = SettingsPanel()
    assert panel is not None
```

- [ ] **Step 2: 运行测试验证失败**

Run:
```bash
pytest tests/ui/test_settings_panel.py -v
```
Expected: FAIL - SettingsPanel not defined

- [ ] **Step 3: 创建设置面板组件**

创建 `src/ui/settings_panel.py`:
```python
# src/ui/settings_panel.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSpinBox, QComboBox, QCheckBox,
    QPushButton, QGroupBox, QFileDialog
)
from PyQt6.QtCore import pyqtSignal


class SettingsPanel(QWidget):
    """设置面板组件"""

    # 信号
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)

        # 下载设置
        download_group = QGroupBox("下载设置")
        download_layout = QVBoxLayout(download_group)

        # 下载路径
        path_layout = QHBoxLayout()
        path_label = QLabel("下载路径:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("选择下载保存位置")
        self.path_btn = QPushButton("浏览...")
        self.path_btn.clicked.connect(self.on_browse_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_btn)
        download_layout.addLayout(path_layout)

        # 默认画质
        quality_layout = QHBoxLayout()
        quality_label = QLabel("默认画质:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["原画", "1080p", "720p", "480p", "360p"])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        download_layout.addLayout(quality_layout)

        # 默认格式
        format_layout = QHBoxLayout()
        format_label = QLabel("默认格式:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP4", "MKV", "AVI", "MP3"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        download_layout.addLayout(format_layout)

        # 并发下载数
        concurrent_layout = QHBoxLayout()
        concurrent_label = QLabel("并发下载数:")
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 10)
        self.concurrent_spin.setValue(3)
        concurrent_layout.addWidget(concurrent_label)
        concurrent_layout.addWidget(self.concurrent_spin)
        download_layout.addLayout(concurrent_layout)

        layout.addWidget(download_group)

        # 界面设置
        ui_group = QGroupBox("界面设置")
        ui_layout = QVBoxLayout(ui_group)

        # 主题选择
        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["浅色", "深色"])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        ui_layout.addLayout(theme_layout)

        layout.addWidget(ui_group)

        # 保存按钮
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        self.save_btn = QPushButton("保存设置")
        self.save_btn.clicked.connect(self.on_save_settings)
        save_layout.addWidget(self.save_btn)
        layout.addLayout(save_layout)

    def on_browse_path(self):
        """浏览下载路径"""
        path = QFileDialog.getExistingDirectory(self, "选择下载路径")
        if path:
            self.path_input.setText(path)

    def on_save_settings(self):
        """保存设置"""
        settings = {
            "download_path": self.path_input.text(),
            "default_quality": self.quality_combo.currentText(),
            "default_format": self.format_combo.currentText(),
            "concurrent_downloads": self.concurrent_spin.value(),
            "theme": self.theme_combo.currentText()
        }
        self.settings_changed.emit(settings)
```

- [ ] **Step 4: 运行测试验证通过**

Run:
```bash
pytest tests/ui/test_settings_panel.py -v
```
Expected: PASS

- [ ] **Step 5: 提交设置面板组件**

Run:
```bash
git add src/ui/settings_panel.py tests/ui/test_settings_panel.py
git commit -m "feat: 创建设置面板组件"
```

---

### Task 8: 创建应用图标和资源

**Files:**
- Create: `resources/icon.ico`
- Create: `resources/icon.png`
- Create: `resources/__init__.py`

- [ ] **Step 1: 创建资源目录和文件**

创建 `resources/__init__.py`:
```python
# resources/__init__.py
"""应用资源文件"""
```

创建简单的应用图标（使用Qt内置图标或创建占位符）...

- [ ] **Step 2: 更新主窗口使用图标**

修改 `src/ui/main_window.py`:
```python
from PyQt6.QtGui import QIcon

def init_ui(self):
    # 设置应用图标
    self.setWindowIcon(QIcon("resources/icon.ico"))
    # ...
```

- [ ] **Step 3: 提交资源文件**

Run:
```bash
git add resources/
git commit -m "feat: 添加应用图标和资源"
```

---

### Task 9: 完整UI测试

**Files:**
- Create: `tests/ui/test_ui_integration.py`

- [ ] **Step 1: 创建集成测试**

创建 `tests/ui/test_ui_integration.py`:
```python
# tests/ui/test_ui_integration.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.url_input_widget import UrlInputWidget
from src.ui.download_list import DownloadListWidget
from src.ui.settings_panel import SettingsPanel

@pytest.fixture
def app():
    return QApplication([])

def test_ui_components_integration(app):
    """测试UI组件集成"""
    # 测试主窗口
    window = MainWindow()
    assert window is not None

    # 测试URL输入组件
    url_widget = UrlInputWidget()
    assert url_widget is not None

    # 测试下载列表组件
    list_widget = DownloadListWidget()
    assert list_widget is not None

    # 测试设置面板组件
    settings_panel = SettingsPanel()
    assert settings_panel is not None
```

- [ ] **Step 2: 运行集成测试**

Run:
```bash
pytest tests/ui/test_ui_integration.py -v
```
Expected: PASS

- [ ] **Step 3: 提交集成测试**

Run:
```bash
git add tests/ui/test_ui_integration.py
git commit -m "test: 添加UI集成测试"
```

---

### Task 10: 运行完整测试并提交

**Files:**
- All UI test files

- [ ] **Step 1: 运行所有UI测试**

Run:
```bash
pytest tests/ui/ -v
```
Expected: 所有测试通过

- [ ] **Step 2: 运行应用验证**

Run:
```bash
python src/main.py
```
Expected: 应用正常启动，UI显示正常

- [ ] **Step 3: 提交所有更改**

Run:
```bash
git add .
git commit -m "feat: 完成UI页面创建

- 创建主窗口组件
- 创建URL输入组件
- 创建下载列表组件
- 创建下载项组件
- 创建设置面板组件
- 添加应用图标和资源
- 添加完整UI测试"
```

---

## Plan Review

请审查此实现计划，确认是否批准进入执行阶段。
