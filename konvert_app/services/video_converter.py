import subprocess
import tempfile
from pathlib import Path

def get_video_duration(video_bytes: bytes) -> float:
    with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
        tmp.write(video_bytes)
        tmp.flush()

        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            tmp.name
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        return float(result.stdout.strip())


def convert_video_to_mp3(video_bytes: bytes) -> bytes:
    """
    Converts video bytes to MP3 bytes using ffmpeg
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = Path(tmpdir) / "input_video"
        audio_path = Path(tmpdir) / "output.mp3"

        video_path.write_bytes(video_bytes)

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(video_path),
            "-vn",
            "-acodec", "libmp3lame",
            str(audio_path)
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        return audio_path.read_bytes()
