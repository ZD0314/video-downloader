# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a video downloader desktop application built with PyQt6 and yt-dlp. The application supports downloading videos from mainstream platforms (YouTube, Bilibili) and domestic Chinese platforms (Youku, iQiyi, Tencent Video, etc.).

## Project Structure

```
video-downloader/
├── src/
│   ├── ui/                    # User interface components
│   │   ├── main_window.py     # Main application window
│   │   ├── url_input_widget.py # URL input component
│   │   ├── download_list.py   # Download list component
│   │   ├── download_item_widget.py # Individual download item
│   │   └── settings_panel.py  # Settings panel component
│   ├── models/                # Data models
│   │   └── download_task.py   # Download task model
│   ├── services/              # Business logic (not yet implemented)
│   ├── utils/                 # Utility classes
│   └── main.py                # Application entry point
├── tests/
│   └── ui/                    # UI tests
│       ├── test_main_window.py
│       ├── test_url_input_widget.py
│       ├── test_download_item_widget.py
│       ├── test_download_list.py
│       ├── test_settings_panel.py
│       └── test_ui_integration.py
├── docs/                      # Documentation
├── resources/                 # Application resources (icons, etc.)
└── .gitignore
```

## Architecture

The application follows a layered architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    UI Layer (PyQt6)                         │
│  MainWindow → UrlInputWidget → DownloadList → SettingsPanel │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Service Layer (Business Logic)              │
│  DownloadManager, VideoParser, FormatConverter, etc.        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer (External Tools)                │
│  yt-dlp, FFmpeg, JSON config files                          │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Principles:**
- **MVC Pattern**: Model-View-Controller separation for maintainability
- **Signal-Slot Mechanism**: PyQt6 signals for component communication
- **Thread Safety**: Background threads for download operations
- **TDD Approach**: Tests written before implementation

## Common Commands

### Running the Application
```bash
# Run the video downloader application
python src/main.py
```

### Running Tests
```bash
# Run all UI tests
pytest tests/ui/ -v

# Run specific test file
pytest tests/ui/test_main_window.py -v

# Run with coverage
pytest tests/ui/ --cov=src --cov-report=html
```

### Installing Dependencies
```bash
# Install PyQt6 and testing dependencies
pip install PyQt6 pytest pytest-qt

# Install from Tsinghua mirror (faster in China)
pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple PyQt6 pytest pytest-qt
```

## Key Components

### MainWindow (`src/ui/main_window.py`)
- Application main window with menu bar, tool bar, and status bar
- Coordinates between URL input, download list, and settings
- Handles user actions and signals from child components

### UrlInputWidget (`src/ui/url_input_widget.py`)
- URL input field with download button
- Emits `download_requested(url)` signal when download is triggered

### DownloadListWidget (`src/ui/download_list.py`)
- Scrollable list of download tasks
- Manages DownloadItemWidget components
- Emits task control signals (pause, resume, cancel)

### DownloadItemWidget (`src/ui/download_item_widget.py`)
- Individual download task display with progress bar
- Shows title, progress, status, and control buttons

### SettingsPanel (`src/ui/settings_panel.py`)
- Configuration UI for download path, quality, format, etc.
- Emits `settings_changed(settings)` signal

### DownloadTask Model (`src/models/download_task.py`)
- Data class representing a download task
- Contains URL, title, status, progress, speed, etc.
- Uses `DownloadStatus` enum for task states

## Testing Strategy

### UI Tests (pytest-qt)
- Test component creation and rendering
- Test user interactions (button clicks, input)
- Test signal emissions and connections

### Test Fixtures
```python
@pytest.fixture
def app():
    return QApplication([])
```

### Example Test
```python
def test_main_window_creation(app):
    window = MainWindow()
    assert window is not None
    assert window.windowTitle() == "视频下载器"
```

## Development Notes

### Import Path
The application uses `src/` as the root package. Imports should use the full path:
```python
from src.ui.main_window import MainWindow
from src.models.download_task import DownloadTask
```

### PyQt6 Signals
Components communicate using PyQt6 signals:
```python
# Define signal
download_requested = pyqtSignal(str)

# Connect signal
widget.download_requested.connect(handler_function)

# Emit signal
self.download_requested.emit(url)
```

### Thread Safety
- UI operations must run on the main thread
- Download operations run in background threads
- Use signals to communicate between threads

## Next Steps (Incomplete Tasks)

The following components are planned but not yet implemented:
- `src/services/download_manager.py` - Download task management
- `src/services/video_parser.py` - Video URL parsing
- `src/services/yt_dlp_wrapper.py` - yt-dlp wrapper
- `src/services/format_converter.py` - FFmpeg format conversion
- `src/services/config_manager.py` - Configuration management

## Resources

- Design Document: `docs/superpowers/specs/2026-03-18-video-downloader-design.md`
- UI Implementation Plan: `docs/superpowers/plans/2026-03-18-video-downloader-ui-plan.md`
- GitHub Repository: https://github.com/ZD0314/video-downloader.git
