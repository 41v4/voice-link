import wave
from io import BytesIO

import pyaudio
from loguru import logger


class AudioRecorder:
    def __init__(self):
        self.output_filename = "output.wav"
        self.is_recording = False
        self.frames = []
        self.stream = None
        self.p = pyaudio.PyAudio()

    def start_recording(self):
        logger.debug("Start recording")
        self.is_recording = True
        self.frames = []

        # Define audio settings based on your device information
        device_index = 5  # Device index found earlier
        chunk = 1024
        format = pyaudio.paInt16  # 16 bits per sample
        channels = 2  # Stereo
        rate = 48000  # Sample rate

        # Open stream with callback
        self.stream = self.p.open(format=format, channels=channels, rate=rate,
                                  input=True, frames_per_buffer=chunk, input_device_index=device_index,
                                  stream_callback=self.callback)


    def callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            self.frames.append(in_data)
            return (None, pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def stop_recording(self):
        logger.debug("Stop recording")
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        # self.save_recording_as_file()
        recording = self.save_recording_to_memory()
        return recording

    def save_recording_as_file(self):
        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(48000)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def save_recording_to_memory(self):
        self.audio_data = BytesIO()
        wf = wave.open(self.audio_data, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(48000)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        # Reset the buffer's cursor to the beginning
        self.audio_data.seek(0)
        return self.audio_data

