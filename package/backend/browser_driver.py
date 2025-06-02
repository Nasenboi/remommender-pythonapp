import os
import subprocess
import pyaudio
import soundfile as sf

from .audio_driver import AudioDriver


class BrowserAudioDriver(AudioDriver):
    """
    Audio driver for capturing audio from browser windows.
    On Linux, uses wmctrl to list browser windows.
    Note: This captures system output audio, not per-window audio.
    """

    def list_driver_sources(self) -> list[str]:
        """
        List currently open browser windows (Chrome, Firefox) using wmctrl.
        """
        return []

    def extract_single(self, tmp_file_path: str, frame_length_s: int) -> str:
        """
        Record system audio for a given duration.
        """
        file_name = os.path.join(tmp_file_path, self._generate_tmp_name())
        samplerate = self.sample_rate
        channels = self.channels

        # Find PulseAudio monitor source
        try:
            pactl_out = subprocess.check_output(["pactl", "list", "sources"], text=True)
            monitor_sources = [
                line.split(":")[1].strip()
                for line in pactl_out.splitlines()
                if "Name: " in line and ".monitor" in line
            ]
            if not monitor_sources:
                raise RuntimeError("No monitor sources found. Is PulseAudio running?")
            monitor_source = monitor_sources[0]  # Use the first monitor source
        except Exception as e:
            raise RuntimeError(f"Could not find monitor source: {e}")

        # Use parec to record system audio, then convert to wav with ffmpeg
        raw_file = file_name + ".raw"
        try:
            # Record raw audio with parec
            subprocess.run(
                [
                    "parec",
                    "--format=s16le",
                    f"--rate={samplerate}",
                    f"--channels={channels}",
                    f"--device={monitor_source}",
                    "--latency-msec=10",
                ],
                stdout=open(raw_file, "wb"),
                timeout=frame_length_s,
            )
        except subprocess.TimeoutExpired:
            pass  # Expected: parec will be killed after timeout

        # Convert raw to wav using ffmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "s16le",
                "-ar",
                str(samplerate),
                "-ac",
                str(channels),
                "-i",
                raw_file,
                file_name,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Remove raw file
        if os.path.exists(raw_file):
            os.remove(raw_file)

        return file_name
