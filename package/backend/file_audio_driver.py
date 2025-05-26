import os
import librosa
import soundfile as sf

from .audio_driver import AudioDriver


class FileAudioDriver(AudioDriver):
    """
    The FileAudioDriver class
    Responsible for the audio extraction and saving from file input
    """

    def __init__(self, file_path: str = "tmp", **kwargs):
        """
        Initialize the MicAudioDriver class
        """
        self.file_path = file_path
        super().__init__(**kwargs)

    def list_driver_sources(self) -> list[str]:
        """
        Get the list of available audio files for the file driver
        :return: List of audio sources
        """
        return os.listdir(self.file_path)

    def extract_single(self, tmp_file_path: str, frame_length_s: int) -> str:
        """
        Extract a single audio file from microphone input
        :param tmp_file_path: Path to the temporary file
        :param frame_length_s: Length of each audio frame in seconds
        """
        file_name = os.path.join(tmp_file_path, self._generate_tmp_name())
        samplerate = self.sample_rate
        channels = self.channels

        y, sr = librosa.load(
            os.path.join(self.file_path, self.driver_source),
            sr=samplerate,
            mono=(channels == 1),
        )
        if len(y) > frame_length_s * sr:
            y = y[: frame_length_s * sr]

        sf.write(file_name, y, samplerate, subtype="PCM_16")

        return file_name
