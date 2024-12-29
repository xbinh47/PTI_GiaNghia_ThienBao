import pytest
from PyQt6.QtWidgets import QMessageBox
from program import MessageBox

@pytest.mark.describe("MessageBox.success_box")
class TestSuccessBox:
    
    @pytest.mark.happy_path
    def test_success_box_shows_correct_message(self, qtbot):
        """
        Test that the success_box method displays a message box with the correct message.
        """
        message = "Operation completed successfully!"
        msg_box = MessageBox()
        
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            msg_box.success_box(message)
        
        assert blocker.signal_triggered
        assert blocker.args[0] == QMessageBox.StandardButton.Ok

    @pytest.mark.happy_path
    def test_success_box_has_correct_title_and_icon(self, qtbot):
        """
        Test that the success_box method sets the correct title and icon for the message box.
        """
        message = "Operation completed successfully!"
        msg_box = MessageBox()
        
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            msg_box.success_box(message)
        
        assert blocker.signal_triggered
        assert QMessageBox().windowTitle() == "Success"
        assert QMessageBox().icon() == QMessageBox.Icon.Information

    @pytest.mark.edge_case
    def test_success_box_with_empty_message(self, qtbot):
        """
        Test that the success_box method handles an empty message string gracefully.
        """
        message = ""
        msg_box = MessageBox()
        
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            msg_box.success_box(message)
        
        assert blocker.signal_triggered
        assert blocker.args[0] == QMessageBox.StandardButton.Ok

    @pytest.mark.edge_case
    def test_success_box_with_long_message(self, qtbot):
        """
        Test that the success_box method handles a very long message string.
        """
        message = "A" * 1000  # Very long message
        msg_box = MessageBox()
        
        with qtbot.waitSignal(QMessageBox.finished, timeout=1000) as blocker:
            msg_box.success_box(message)
        
        assert blocker.signal_triggered
        assert blocker.args[0] == QMessageBox.StandardButton.Ok