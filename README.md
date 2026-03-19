# 视频下载器

基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 和 PyQt6 开发的桌面视频下载工具，支持 YouTube、Bilibili、优酷、爱奇艺、腾讯视频等主流平台。

## 功能特性

- 支持主流视频平台下载（YouTube、Bilibili、优酷、爱奇艺等）
- 支持 m3u8/HLS 流媒体下载（并发分片加速）
- 多任务并发下载
- 暂停 / 恢复 / 取消下载
- 下载进度实时显示
- 下载历史记录（支持导出 CSV）
- 批量导入 URL 列表
- 深色 / 浅色主题切换
- 按状态筛选任务列表

## 截图

> 运行 `python src/main.py` 查看效果

## 安装

### 方式一：直接运行 exe（Windows）

从 [Releases](https://github.com/ZD0314/video-downloader/releases) 下载最新的 `视频下载器.exe`，双击运行。

### 方式二：源码运行

**环境要求：** Python 3.11+

```bash
# 克隆项目
git clone https://github.com/ZD0314/video-downloader.git
cd video-downloader

# 安装依赖
pip install -r requirements.txt

# 运行
python src/main.py
```

## 依赖

```
PyQt6
yt-dlp
```

完整依赖见 [requirements.txt](requirements.txt)

## 打包为 exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "视频下载器" --add-data "src;src" src/main.py
```

打包完成后 exe 在 `dist/` 目录。

## 项目结构

```
video-downloader/
├── src/
│   ├── main.py                    # 入口
│   ├── ui/                        # UI 层
│   │   ├── main_window.py         # 主窗口
│   │   ├── download_list.py       # 下载列表
│   │   ├── download_item_widget.py# 下载项组件
│   │   ├── url_input_widget.py    # URL 输入
│   │   └── settings_dialog.py     # 设置对话框
│   ├── services/                  # 服务层
│   │   ├── download_manager.py    # 下载管理器
│   │   ├── yt_dlp_wrapper.py      # yt-dlp 封装
│   │   ├── video_parser.py        # 视频解析器
│   │   ├── format_converter.py    # 格式转换（FFmpeg）
│   │   └── config_manager.py      # 配置管理
│   └── models/
│       └── download_task.py       # 下载任务模型
├── tests/                         # 测试
├── docs/                          # 文档
└── requirements.txt
```

## 使用说明

1. 在输入框粘贴视频 URL，点击下载
2. 批量下载：文件 → 导入 URL 列表（每行一个 URL 的 .txt 文件）
3. 修改下载路径：文件 → 下载设置
4. 查看历史：文件 → 下载记录
5. 导出记录：文件 → 导出下载记录

## License

MIT
