import os
import sounddevice as sd
import soundfile as sf

from .audio_driver import AudioDriver


class MicAudioDriver(AudioDriver):
    """
    The MicAudioDriver class
    Responsible for the audio extraction and saving from microphone input
    """

    def __init__(self, **kwargs):
        """
        Initialize the MicAudioDriver class
        """
        super().__init__(**kwargs)

    def list_driver_sources(self) -> list[str]:
        """
        Get the list of available audio sources for the microphone driver
        :return: List of audio sources
        """
        devices = sd.query_devices()
        input_devices = [
            dev["name"] for dev in devices if dev["max_input_channels"] > 0
        ]
        return input_devices

    def extract_single(self, tmp_file_path: str, frame_length_s: int) -> str:
        """
        Extract a single audio file from microphone input
        :param tmp_file_path: Path to the temporary file
        :param frame_length_s: Length of each audio frame in seconds
        """
        file_name = os.path.join(tmp_file_path, self._generate_tmp_name())
        samplerate = self.sample_rate
        channels = self.channels

        # Find device index by name
        device_index = None
        if self.driver_source:
            devices = sd.query_devices()
            for idx, dev in enumerate(devices):
                if dev["name"] == self.driver_source and dev["max_input_channels"] > 0:
                    device_index = idx
                    break

        # Record audio
        audio = sd.rec(
            int(frame_length_s * samplerate),
            # samplerate=samplerate,
            channels=channels,
            dtype="int16",
            device=device_index,
        )
        sd.wait()

        # Save to file
        sf.write(file_name, audio, samplerate)

        return file_name
