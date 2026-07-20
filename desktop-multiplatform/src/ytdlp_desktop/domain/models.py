"""Desktop-specific domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from ytdlp_core.core.models import MediaType


class ThemeMode(str, Enum):
    DARK = "dark"
    LIGHT = "light"
    SYSTEM = "system"


@dataclass
class AppConfig:
    """Application configuration."""

    # Window
    window_width: int = 900
    window_height: int = 700
    window_maximized: bool = False

    # Theme
    theme: str = "dark"
    color_theme: str = "blue"

    # Downloads
    default_output_dir: str = ""
    default_format: str = "bestvideo+bestaudio/best"
    default_media_type: MediaType = MediaType.VIDEO
    filename_template: str = "%(title)s.%(ext)s"

    # Network
    proxy: str = ""
    rate_limit: str = ""
    retries: int = 3
    timeout: int = 30

    # FFmpeg
    ffmpeg_path: str = ""

    # Advanced
    write_thumbnail: bool = False
    write_subtitles: bool = False
    subtitle_langs: list[str] = field(default_factory=list)
    embed_subtitles: bool = False
    embed_thumbnail: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_width": self.window_width,
            "window_height": self.window_height,
            "window_maximized": self.window_maximized,
            "theme": self.theme,
            "color_theme": self.color_theme,
            "default_output_dir": self.default_output_dir,
            "default_format": self.default_format,
            "default_media_type": self.default_media_type.value,
            "filename_template": self.filename_template,
            "proxy": self.proxy,
            "rate_limit": self.rate_limit,
            "retries": self.retries,
            "timeout": self.timeout,
            "ffmpeg_path": self.ffmpeg_path,
            "write_thumbnail": self.write_thumbnail,
            "write_subtitles": self.write_subtitles,
            "subtitle_langs": self.subtitle_langs,
            "embed_subtitles": self.embed_subtitles,
            "embed_thumbnail": self.embed_thumbnail,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AppConfig:
        return cls(
            window_width=data.get("window_width", 900),
            window_height=data.get("window_height", 700),
            window_maximized=data.get("window_maximized", False),
            theme=data.get("theme", "dark"),
            color_theme=data.get("color_theme", "blue"),
            default_output_dir=data.get("default_output_dir", ""),
            default_format=data.get("default_format", "bestvideo+bestaudio/best"),
            default_media_type=MediaType(data.get("default_media_type", "video")),
            filename_template=data.get("filename_template", "%(title)s.%(ext)s"),
            proxy=data.get("proxy", ""),
            rate_limit=data.get("rate_limit", ""),
            retries=data.get("retries", 3),
            timeout=data.get("timeout", 30),
            ffmpeg_path=data.get("ffmpeg_path", ""),
            write_thumbnail=data.get("write_thumbnail", False),
            write_subtitles=data.get("write_subtitles", False),
            subtitle_langs=data.get("subtitle_langs", []),
            embed_subtitles=data.get("embed_subtitles", False),
            embed_thumbnail=data.get("embed_thumbnail", False),
        )