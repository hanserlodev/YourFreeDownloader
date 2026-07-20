"""Desktop configuration management."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ytdlp_core.domain.ports import IConfigStore

from ytdlp_desktop.domain.models import AppConfig


class ConfigManager:
    """Manage application configuration."""

    DEFAULTS = {
        "window_width": 900,
        "window_height": 700,
        "window_maximized": False,
        "theme": "dark",
        "color_theme": "blue",
        "default_output_dir": "",
        "default_format": "bestvideo+bestaudio/best",
        "default_media_type": "video",
        "filename_template": "%(title)s.%(ext)s",
        "proxy": "",
        "rate_limit": "",
        "retries": 3,
        "timeout": 30,
        "ffmpeg_path": "",
        "write_thumbnail": False,
        "write_subtitles": False,
        "subtitle_langs": [],
        "embed_subtitles": False,
        "embed_thumbnail": False,
    }

    def __init__(self, store: IConfigStore):
        self._store = store

    def load(self) -> AppConfig:
        """Load configuration from store."""
        data = self._store.get_all()
        # Merge with defaults
        for key, default in self.DEFAULTS.items():
            if key not in data:
                data[key] = default
        return AppConfig(**data)

    def save(self, config: AppConfig) -> None:
        """Save configuration to store."""
        data = {
            "window_width": config.window_width,
            "window_height": config.window_height,
            "window_maximized": config.window_maximized,
            "theme": config.theme,
            "color_theme": config.color_theme,
            "default_output_dir": config.default_output_dir,
            "default_format": config.default_format,
            "default_media_type": config.default_media_type.value,
            "filename_template": config.filename_template,
            "proxy": config.proxy,
            "rate_limit": config.rate_limit,
            "retries": config.retries,
            "timeout": config.timeout,
            "ffmpeg_path": config.ffmpeg_path,
            "write_thumbnail": config.write_thumbnail,
            "write_subtitles": config.write_subtitles,
            "subtitle_langs": config.subtitle_langs,
            "embed_subtitles": config.embed_subtitles,
            "embed_thumbnail": config.embed_thumbnail,
        }
        for key, value in data.items():
            self._store.set(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get single config value."""
        return self._store.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set single config value."""
        self._store.set(key, value)

    def reset_to_defaults(self) -> AppConfig:
        """Reset all config to defaults."""
        for key, value in self.DEFAULTS.items():
            self._store.set(key, value)
        return AppConfig(**self.DEFAULTS)