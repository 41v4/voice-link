from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class LoggingTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Logging Settings"))
        self.setLayout(layout)