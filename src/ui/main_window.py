from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Main window component - the application's main interface."""

    # Default window geometry
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    DEFAULT_X = 100
    DEFAULT_Y = 100

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("Video Downloader")
        self.setGeometry(
            self.DEFAULT_X,
            self.DEFAULT_Y,
            self.DEFAULT_WIDTH,
            self.DEFAULT_HEIGHT,
        )
