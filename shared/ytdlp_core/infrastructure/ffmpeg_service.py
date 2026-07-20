"""Infrastructure - ffmpeg service implementation."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

from ytdlp_core.domain.ports import IFFmpegService
from ytdlp_core.domain.exceptions import FFmpegError


class FFmpegService(IFFmpegService):
    """FFmpeg service for audio/video processing."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self._ffmpeg_path = ffmpeg_path or self._find_ffmpeg()

    def _find_ffmpeg(self) -> str:
        """Find ffmpeg executable."""
        # Check common locations
        paths = [
            shutil.which("ffmpeg"),
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "C:/ffmpeg/bin/ffmpeg.exe",
            "C:/Program Files/ffmpeg/bin/ffmpeg.exe",
        ]
        for p in paths:
            if p and Path(p).exists():
                return p
        return "ffmpeg"  # fallback to PATH

    @property
    def ffmpeg_path(self) -> str:
        return self._ffmpeg_path

    def is_available(self) -> bool:
        """Check if ffmpeg is available."""
        try:
            result = subprocess.run(
                [self._ffmpeg_path, "-version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_version(self) -> str:
        """Get ffmpeg version string."""
        try:
            result = subprocess.run(
                [self._ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            lines = result.stdout.split("\n")
            return lines[0] if lines else "unknown"
        except Exception:
            return "unknown"

    def convert_to_mp3(
        self,
        input_path: Path,
        output_path: Path,
        bitrate: int = 192,
        progress_callback: Optional[callable] = None,
    ) -> Path:
        """Convert video/audio to MP3."""
        cmd = [
            self._ffmpeg_path,
            "-y",  # overwrite
            "-i", str(input_path),
            "-vn",  # no video
            "-acodec", "libmp3lame",
            "-ab", f"{bitrate}k",
            str(output_path),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            return output_path
        except subprocess.CalledProcessError as e:
            raise FFmpegError(f"MP3 conversion failed: {e.stderr.decode()}", original=e)
        except Exception as e:
            raise FFmpegError(f"MP3 conversion failed: {e}", original=e)

    def merge_video_audio(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
        progress_callback: Optional[callable] = None,
    ) -> Path:
        """Merge separate video and audio streams."""
        cmd = [
            self._ffmpeg_path,
            "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            str(output_path),
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            return output_path
        except subprocess.CalledProcessError as e:
            raise FFmpegError(f"Merge failed: {e.stderr.decode()}", original=e)
        except Exception as e:
            raise FFmpegError(f"Merge failed: {e}", original=e)

    def extract_audio(
        self,
        input_path: Path,
        output_path: Path,
        format: str = "mp3",
        bitrate: int = 192,
    ) -> Path:
        """Extract audio from video file."""
        if format == "mp3":
            return self.convert_to_mp3(input_path, output_path, bitrate)
        else:
            cmd = [
                self._ffmpeg_path,
                "-y",
                "-i", str(input_path),
                "-vn",
                "-acodec", "copy" if format == "m4a" else "libmp3lame",
                "-ab", f"{bitrate}k" if format != "m4a" else "",
                str(output_path),
            ]
            cmd = [c for c in cmd if c]  # remove empty strings
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=300)
                return output_path
            except subprocess.CalledProcessError as e:
                raise FFmpegError(f"Audio extraction failed: {e.stderr.decode()}", original=e)