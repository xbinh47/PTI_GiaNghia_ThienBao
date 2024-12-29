import pytest
from PyQt6.QtWidgets import QMessageBox
from program import MessageBox

@pytest.fixture
def message_box():
    """Fixture to create a MessageBox instance."""
    return MessageBox()

@pytest.mark.describe("MessageBox.error_box")
class TestErrorBox:
    
    @pytest.mark.happy_path
    def test_error_box_shows_critical_icon(qtbot, message_box):
        """Test that the error_box method sets the icon to Critical."""
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            message_box.error_box("Test Error Message")
            assert blocker.signal_triggered
            assert blocker.args[0] == QMessageBox.StandardButton.Ok

    @pytest.mark.happy_path
    def test_error_box_shows_correct_message(qtbot, message_box):
        """Test that the error_box method displays the correct message."""
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            message_box.error_box("Test Error Message")
            assert blocker.signal_triggered
            assert QMessageBox().text() == "Test Error Message"

    @pytest.mark.edge_case
    def test_error_box_with_empty_message(qtbot, message_box):
        """Test that the error_box method handles an empty message."""
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            message_box.error_box("")
            assert blocker.signal_triggered
            assert QMessageBox().text() == ""

    @pytest.mark.edge_case
    def test_error_box_with_long_message(qtbot, message_box):
        """Test that the error_box method handles a very long message."""
        long_message = "A" * 1000  # A long message of 1000 characters
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            message_box.error_box(long_message)
            assert blocker.signal_triggered
            assert QMessageBox().text() == long_message

    @pytest.mark.edge_case
    def test_error_box_with_special_characters(qtbot, message_box):
        """Test that the error_box method handles special characters."""
        special_message = "!@#$%^&*()_+-=[]{}|;':,.<>/?"
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            message_box.error_box(special_message)
            assert blocker.signal_triggered
            assert QMessageBox().text() == special_message