from faster_whisper import WhisperModel
from loguru import logger


class Transcriber:
    model_size = "base.en"
    def __init__(self):
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")

    def start_transcribing(self, audio):
        all_text = []
        segments, info = self.model.transcribe(audio, beam_size=5)

        logger.debug("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        for segment in segments:
            logger.debug("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            all_text.append(segment.text)

        return " ".join(all_text).strip()