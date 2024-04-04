from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TranscriptionTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Transcription Settings"))
        self.setLayout(layout)