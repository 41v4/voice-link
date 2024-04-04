import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QTabWidget

from client.tabs.audio_tab import AudioTab
from client.tabs.automation_tab import AutomationTab
from client.tabs.logging_tab import LoggingTab
from client.tabs.transcription_tab import TranscriptionTab


class MainWindow(QMainWindow):
    def __init__(self, shared_queue):
        super().__init__()
        self.shared_queue = shared_queue
        self.setWindowTitle("Audio Transcription Application")
        self.resize(370, 600)

        # Create the tab widget
        tabs = QTabWidget()
        self.audio_tab = AudioTab()  # Keep a reference to update it
        tabs.addTab(self.audio_tab, "Audio")
        tabs.addTab(TranscriptionTab(), "Transcription")
        tabs.addTab(AutomationTab(), "Automation")
        tabs.addTab(LoggingTab(), "Logging")

        self.setCentralWidget(tabs)

        # Polling timer
        self.timer = QTimer()
        self.timer.setInterval(100)  # Check every 0.1 second
        self.timer.timeout.connect(self.check_queue)
        self.timer.start()

    def check_queue(self):
        while not self.shared_queue.empty():
            command_data = self.shared_queue.get()
            print(command_data)
            if command_data['command'] == 'update_recording_status':
                self.audio_tab.handle_command(command_data)