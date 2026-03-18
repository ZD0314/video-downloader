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
