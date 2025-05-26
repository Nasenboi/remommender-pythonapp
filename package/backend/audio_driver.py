import os
from datetime import datetime


class AudioDriver:
    """
    The AudioDriver class
    Responsible for the audio extraction and saving
    """

    def __init__(
        self, driver_source: str = None, sample_rate: int = 16_000, channels: int = 1
    ):
        """
        Initialize the AudioDriver class
        """
        self.driver_source = driver_source
        self.sample_rate = sample_rate
        self.channels = channels

    def list_driver_sources(self) -> list[str]:
        """
        Get the list of available audio sources for the audio driver
        :return: List of audio sources
        """
        raise NotImplementedError("This method should be implemented in a subclass")

    def extract_single(self, tmp_file_path: str, frame_length_s: int) -> str:
        """
        Extract a single audio file
        :param tmp_file_path: Path to the temporary file
        :param frame_length_s: Length of each audio frame in seconds
        """
        raise NotImplementedError("This method should be implemented in a subclass")

    def _generate_tmp_name(self) -> str:
        """
        Generate a temporary file name
        :return: Temporary file name
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"tmp_{timestamp}.wav"
