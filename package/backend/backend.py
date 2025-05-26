import os
from typing import Literal
import requests

from .audio_driver import AudioDriver
from .mic_audio_driver import MicAudioDriver
from .file_audio_driver import FileAudioDriver

audio_driver_types = Literal["mic", "file"]


class Backend:
    """
    The backend class
    """

    def __init__(
        self,
        tmp_file_path: str = "tmp",
        frame_length_s: int = 5,
        hop_length_s: int = 3,
        audio_driver_type: audio_driver_types = "mic",
        api_root: str = "http://localhost:8000/",
    ):
        """
        Initialize the Backend class
        :param tmp_file_path: Path to the temporary file
        :param frame_length_s: Length of each audio frame in seconds
        :param hop_length_s: Hop length in seconds
        """
        self.tmp_file_path = tmp_file_path
        self.tmp_file = None
        self.frame_length_s = frame_length_s
        self.hop_length_s = hop_length_s
        self.audio_driver: AudioDriver = None
        self.api_root = api_root

        self._set_audio_driver(audio_driver_type)

    def list_audio_sources(self) -> list[str]:
        """
        List the available audio sources
        :return: List of audio sources
        """
        return self.audio_driver.list_driver_sources()

    def set_audio_source(self, driver_source: str):
        """
        Set the audio source for the audio driver
        :param driver_source: Name of the audio source
        """
        self.audio_driver.driver_source = driver_source

    def extract_single(self) -> str:
        """
        Extract a single audio file
        :return: Path to the extracted audio file
        """
        if not os.path.exists(self.tmp_file_path):
            os.makedirs(self.tmp_file_path)

        self.tmp_file = self.audio_driver.extract_single(
            tmp_file_path=self.tmp_file_path,
            frame_length_s=self.frame_length_s,
        )
        return self.tmp_file

    def send_single_request(self, tmp_file_path: str) -> str:
        """
        Send a single audio file to the backend API server and return the response.
        :param tmp_file_path: Path to the audio file to send
        :return: Response from the backend as a string
        """
        api_path = f"{self.api_root}recommend/from-speech/"
        api_url = f"{api_path}{os.path.basename(tmp_file_path)}"

        with open(tmp_file_path, "rb") as f:
            data = f.read()
            headers = {"Content-Type": "audio/wav"}
            response = requests.post(api_url, data=data, headers=headers)

        print(response.status_code, response.text)

        return response.text

    def _set_audio_driver(self, audio_driver_type: audio_driver_types):
        """
        Set the audio driver based on the type
        :param audio_driver_type: Type of the audio driver
        """
        if audio_driver_type == "mic":
            self.audio_driver = MicAudioDriver()
        elif audio_driver_type == "file":
            self.audio_driver = FileAudioDriver(file_path=self.tmp_file_path)
        else:
            raise ValueError(f"Unsupported audio driver type: {audio_driver_type}")
