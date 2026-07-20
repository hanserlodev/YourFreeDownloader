"""Core domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class MediaType(Enum):
    """Type of media to download."""

    VIDEO = "video"
    AUDIO_ONLY = "audio_only"


class DownloadStatus(Enum):
    """Download status."""

    PENDING = "pending"
    DOWNLOADING = "downloading"
    FINISHED = "finished"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class VideoFormat:
    """Video/audio format info."""

    format_id: str
    ext: str
    resolution: Optional[str] = None
    fps: Optional[float] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    bitrate: Optional[float] = None  # total bitrate
    audio_bitrate: Optional[int] = None  # audio bitrate in kbps
    video_bitrate: Optional[float] = None
    filesize: Optional[int] = None
    protocol: Optional[str] = None
    format_note: Optional[str] = None

    @property
    def is_video(self) -> bool:
        return self.vcodec is not None and self.vcodec != "none"

    @property
    def is_audio(self) -> bool:
        return self.acodec is not None and self.acodec != "none"

    @property
    def is_video_only(self) -> bool:
        return self.is_video and not self.is_audio

    @property
    def is_audio_only(self) -> bool:
        return self.is_audio and not self.is_video

    @property
    def display_name(self) -> str:
        parts = []
        if self.resolution:
            parts.append(self.resolution)
        if self.fps:
            parts.append(f"{self.fps}fps")
        if self.is_video:
            parts.append(f"v:{self.vcodec or 'unknown'}")
        if self.is_audio:
            parts.append(f"a:{self.acodec or 'unknown'}")
        if self.audio_bitrate:
            parts.append(f"{self.audio_bitrate}kbps")
        if self.filesize:
            parts.append(f"{self.filesize / (1024*1024):.1f}MB")
        elif self.bitrate:
            parts.append(f"{self.bitrate}kbps")
        return " | ".join(parts) if parts else self.format_id


@dataclass(frozen=True)
class VideoInfo:
    """Video metadata."""

    id: str
    title: str
    description: Optional[str] = None
    uploader: Optional[str] = None
    uploader_id: Optional[str] = None
    upload_date: Optional[str] = None
    duration: Optional[int] = None  # seconds
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    thumbnail: Optional[str] = None
    thumbnails: list[dict] = field(default_factory=list)
    formats: list[VideoFormat] = field(default_factory=list)
    webpage_url: Optional[str] = None
    original_url: Optional[str] = None
    is_live: bool = False
    availability: Optional[str] = None
    age_limit: Optional[int] = None
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def video_formats(self) -> list[VideoFormat]:
        return [f for f in self.formats if f.is_video]

    @property
    def audio_formats(self) -> list[VideoFormat]:
        return [f for f in self.formats if f.is_audio_only]

    @property
    def combined_formats(self) -> list[VideoFormat]:
        return [f for f in self.formats if f.is_video and f.is_audio]

    def get_best_video(self, prefer_mp4: bool = True) -> Optional[VideoFormat]:
        """Get highest quality video format."""
        candidates = self.video_formats
        if prefer_mp4:
            candidates = [f for f in candidates if f.ext == "mp4"]
        if not candidates:
            return None
        return max(candidates, key=lambda f: int(f.resolution.replace("p", "")) if f.resolution and f.resolution.endswith("p") else 0)

    def get_best_audio(self) -> Optional[VideoFormat]:
        """Get highest quality audio format."""
        if not self.audio_formats:
            return None
        return max(self.audio_formats, key=lambda f: f.audio_bitrate or 0)


@dataclass(frozen=True)
class DownloadOptions:
    """Download configuration."""

    url: str
    output_path: Path
    format_id: str
    media_type: MediaType = MediaType.VIDEO
    filename_template: str = "%(title)s.%(ext)s"
    ffmpeg_path: Optional[str] = None
    proxy: Optional[str] = None
    rate_limit: Optional[str] = None
    retries: int = 3
    timeout: int = 30
    write_thumbnail: bool = False
    write_subtitles: bool = False
    subtitle_langs: list[str] = field(default_factory=list)

    def to_ydl_opts(self) -> dict[str, Any]:
        """Convert to yt-dlp options dict."""
        opts = {
            "format": self.format_id,
            "outtmpl": str(self.output_path / self.filename_template),
            "noplaylist": True,
            "retries": self.retries,
            "socket_timeout": self.timeout,
        }

        if self.proxy:
            opts["proxy"] = self.proxy

        if self.rate_limit:
            opts["ratelimit"] = self._parse_rate_limit(self.rate_limit)

        if self.ffmpeg_path:
            opts["ffmpeg_location"] = self.ffmpeg_path

        if self.media_type == MediaType.AUDIO_ONLY:
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        if self.write_thumbnail:
            opts["writethumbnail"] = True

        if self.write_subtitles:
            opts["writesubtitles"] = True
            opts["subtitleslangs"] = self.subtitle_langs

        return opts

    def _parse_rate_limit(self, limit: str) -> int:
        """Parse rate limit string to bytes/s."""
        limit = limit.upper()
        if limit.endswith("K"):
            return int(float(limit[:-1]) * 1024)
        elif limit.endswith("M"):
            return int(float(limit[:-1]) * 1024 * 1024)
        elif limit.endswith("G"):
            return int(float(limit[:-1]) * 1024 * 1024 * 1024)
        return int(limit)


@dataclass(frozen=True)
class DownloadProgress:
    """Download progress info."""

    status: DownloadStatus
    downloaded_bytes: int = 0
    total_bytes: Optional[int] = None
    speed: Optional[float] = None  # bytes/s
    eta: Optional[int] = None  # seconds
    filename: Optional[str] = None
    percent: float = 0.0
    error: Optional[str] = None


@dataclass(frozen=True)
class DownloadResult:
    """Download operation result."""

    success: bool
    output_path: Optional[Path] = None
    video_info: Optional[VideoInfo] = None
    error: Optional[str] = None