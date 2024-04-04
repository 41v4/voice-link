from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AutomationTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Automation Settings"))
        self.setLayout(layout)