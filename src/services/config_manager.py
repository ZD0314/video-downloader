"""配置管理器"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from PyQt6.QtCore import QObject, pyqtSignal


class ConfigManager(QObject):
    """配置管理器 - 负责配置的持久化存储"""

    config_changed = pyqtSignal(dict)

    def __init__(self, config_dir: Optional[str] = None):
        super().__init__()
        if config_dir is None:
            config_dir = os.path.join(os.path.expanduser("~"), ".video-downloader")
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.json"
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            else:
                # 默认配置
                self._config = {
                    "download_path": os.path.join(os.path.expanduser("~"), "Downloads"),
                    "default_quality": "原画",
                    "default_format": "MP4",
                    "concurrent_downloads": 3,
                    "theme": "浅色"
                }
                self._save_config()
        except Exception as e:
            print(f"加载配置失败: {e}")
            # 使用默认配置
            self._config = {
                "download_path": os.path.join(os.path.expanduser("~"), "Downloads"),
                "default_quality": "原画",
                "default_format": "MP4",
                "concurrent_downloads": 3,
                "theme": "浅色"
            }

    def _save_config(self):
        """保存配置文件"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """设置配置值"""
        if self._config.get(key) != value:
            self._config[key] = value
            self._save_config()
            self.config_changed.emit(self._config.copy())

    def update(self, settings: Dict[str, Any]):
        """更新多个配置"""
        changed = False
        for key, value in settings.items():
            if self._config.get(key) != value:
                self._config[key] = value
                changed = True
        if changed:
            self._save_config()
            self.config_changed.emit(self._config.copy())

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()

    def add_history(self, record: Dict[str, Any]):
        """添加下载历史记录"""
        history = self.get_history()
        history.insert(0, record)
        # 最多保留500条
        history = history[:500]
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            history_file = self.config_dir / "history.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def get_history(self) -> List[Dict[str, Any]]:
        """获取下载历史记录"""
        history_file = self.config_dir / "history.json"
        try:
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"读取历史记录失败: {e}")
        return []

    def clear_history(self):
        """清空历史记录"""
        history_file = self.config_dir / "history.json"
        try:
            if history_file.exists():
                history_file.unlink()
        except Exception as e:
            print(f"清空历史记录失败: {e}")
