from datetime import datetime

from PySide6.QtWidgets import (QComboBox, QLabel, QTextEdit, QVBoxLayout,
                               QWidget)

# Assuming Transcriber is correctly implemented in your utils
from client.utils.transcription_utils import Transcriber


class TranscriptionTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Transcription settings dropdowns
        self.model_selection_dropdown = QComboBox()
        self.model_selection_dropdown.addItems(["tiny.en", "base.en", "small.en", "medium.en", "large.en"])
        self.device = QComboBox()
        self.device.addItems(["CPU", "GPU"])

        # Add widgets to layout
        layout.addWidget(QLabel("Transcription Model:"))
        layout.addWidget(self.model_selection_dropdown)
        layout.addWidget(QLabel("Device:"))
        layout.addWidget(self.device)

        # Transcribed text display
        self.transcribed_text_display = QTextEdit()
        self.transcribed_text_display.setReadOnly(True)
        layout.addWidget(self.transcribed_text_display)

        self.transcriber = Transcriber()

        self.setLayout(layout)

    def handle_recording(self, result):
        if result:
            transcribed_text = self.transcriber.start_transcribing(audio=result)
            # Appending the new transcribed text with timestamp
            current_time = datetime.now().strftime("%H:%M:%S")
            self.transcribed_text_display.append(f"{current_time} - {transcribed_text}")
