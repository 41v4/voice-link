from io import BytesIO

from PySide6.QtCore import QObject, QSize, Signal
from PySide6.QtWidgets import (QComboBox, QLabel, QProgressBar, QPushButton,
                               QStyle, QVBoxLayout, QWidget)

from client.utils.audio_utils import AudioRecorder


class AudioTabSignals(QObject):
    recording = Signal(BytesIO)  # Signal emitting recording data as BytesIO object

class AudioTab(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = AudioTabSignals()
        self.layout = QVBoxLayout()

        self.recorder = AudioRecorder()
        self.is_recording = False

        # Audio source dropdown
        self.audio_source_dropdown = QComboBox()
        self.audio_source_dropdown.addItems(["Mic 1", "Mic 2", "Mic 3"])  # Placeholder values
        self.layout.addWidget(self.audio_source_dropdown)

        # Test audio button and status
        self.test_audio_button = QPushButton("Test Audio")
        self.test_audio_status = QLabel("Test Status: Not Tested")
        self.test_audio_button.clicked.connect(self.test_audio)
        
        test_audio_layout = QVBoxLayout()
        test_audio_layout.addWidget(self.test_audio_button)
        test_audio_layout.addWidget(self.test_audio_status)
        
        self.layout.addLayout(test_audio_layout)

        # Start/stop recording settings
        self.recording_settings_dropdown = QComboBox()
        self.recording_settings_dropdown.addItems(["Custom Hotkey", "External Option"])
        self.recording_settings_dropdown.currentIndexChanged.connect(self.recording_settings_changed)
        
        self.hotkey_dropdown_1 = QComboBox()
        self.hotkey_dropdown_1.addItems(["Ctrl", "Alt", "Shift"])  # Example keys
        self.hotkey_dropdown_2 = QComboBox()
        self.hotkey_dropdown_2.addItems(["A", "B", "C"])  # Example keys
        
        # Initially visible
        self.hotkey_dropdown_1.setVisible(True)
        self.hotkey_dropdown_2.setVisible(True)
        
        self.layout.addWidget(self.recording_settings_dropdown)
        self.layout.addWidget(self.hotkey_dropdown_1)
        self.layout.addWidget(self.hotkey_dropdown_2)

        # Status label
        self.record_audio_status_label = QLabel("Status: Idle")
        self.layout.addWidget(self.record_audio_status_label)

        self.media_play_icon = QStyle.SP_MediaPlay
        self.media_play_icon_style = self.style().standardIcon(self.media_play_icon)
        self.record_audio_button = QPushButton()
        self.record_audio_button.clicked.connect(self.press_recording_button)
        self.record_audio_button.setIcon(self.media_play_icon_style)
        self.record_audio_button.setIconSize(QSize(50, 50))
        self.layout.addWidget(self.record_audio_button)

        # Loading (Indeterminate) Progress Bar for Recording
        self.recording_progress = QProgressBar()
        self.recording_progress.setRange(0, 0)  # Set the progress bar to indeterminate mode
        self.recording_progress.setTextVisible(False)  # Hide the percentage text
        self.recording_progress.setVisible(False)  # Initially hidden, show when recording starts
        self.layout.addWidget(self.recording_progress)

        self.setLayout(self.layout)

    def test_audio(self):
        # Placeholder for testing audio logic
        # Update self.test_audio_status based on actual test result
        self.test_audio_status.setText("Test Status: Success")

    def recording_settings_changed(self):
        # Show/Hide hotkey dropdowns based on selection
        is_custom_hotkey = self.recording_settings_dropdown.currentText() == "Custom Hotkey"
        self.hotkey_dropdown_1.setVisible(is_custom_hotkey)
        self.hotkey_dropdown_2.setVisible(is_custom_hotkey)

    def handle_command(self, command_data):
        if command_data['command'] == 'update_recording_status':
            if command_data['data'] == "start_recording":
                self.update_start_recording_status(message="recording")
            elif command_data['data'] == "stop_recording":
                self.update_stop_recording_status(message="idle")

        elif command_data['command'] == 'another_command':
            # Update other parts of the GUI or perform other actions
            pass

    def press_recording_button(self):
        if self.is_recording: # we stop recording
            self.update_stop_recording_status(message="idle")
        else:
            self.update_start_recording_status(message="recording")

    def update_start_recording_status(self, message):
        self.recorder.start_recording()
        self.is_recording = True
        self.recording_progress.setVisible(True)  # Show the progress bar when recording starts
        self.record_audio_status_label.setText(f"Status: {message}")
        self.media_stop_icon = QStyle.SP_MediaStop
        self.media_stop_icon_style = self.style().standardIcon(self.media_stop_icon)
        self.record_audio_button.setIcon(self.media_stop_icon_style)
    
    def update_stop_recording_status(self, message):
        recording_data = self.recorder.stop_recording() # will need send this recording to transcription tab
        self.signals.recording.emit(recording_data)
        self.is_recording = False
        self.recording_progress.setVisible(False)  # Hide the progress bar when recording stops
        self.record_audio_status_label.setText(f"Status: {message}")
        self.media_play_icon = QStyle.SP_MediaPlay
        self.media_play_icon_style = self.style().standardIcon(self.media_play_icon)
        self.record_audio_button.setIcon(self.media_play_icon_style)
