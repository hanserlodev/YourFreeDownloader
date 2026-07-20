"""Domain ports (interfaces)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Optional, Protocol

from ytdlp_core.core.models import (
    DownloadOptions,
    DownloadProgress,
    DownloadResult,
    MediaType,
    VideoFormat,
    VideoInfo,
)


class IVideoInfoExtractor(ABC):
    """Port for extracting video info."""

    @abstractmethod
    def extract_info(self, url: str) -> VideoInfo:
        """Extract video info without downloading."""
        ...

    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """Check if URL is supported."""
        ...


class IDownloader(ABC):
    """Port for downloading media."""

    @abstractmethod
    def download(
        self,
        options: DownloadOptions,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
    ) -> DownloadResult:
        """Download media with progress updates."""
        ...

    @abstractmethod
    def cancel(self) -> None:
        """Cancel current download."""
        ...


class IFFmpegLocator(ABC):
    """Port for finding ffmpeg."""

    @abstractmethod
    def find_ffmpeg(self) -> Optional[str]:
        """Return ffmpeg path or None."""
        ...


class IConfigStore(ABC):
    """Port for persistent config."""

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    def get_all(self) -> dict[str, Any]:
        ...


class ICacheStore(ABC):
    """Port for caching video info."""

    @abstractmethod
    def get(self, key: str) -> Optional[VideoInfo]:
        ...

    @abstractmethod
    def set(self, key: str, value: VideoInfo) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...


class IPlatformService(ABC):
    """Port for platform-specific operations."""

    @abstractmethod
    def get_data_dir(self) -> Path:
        ...

    @abstractmethod
    def get_download_dir(self) -> Path:
        ...

    @abstractmethod
    def open_folder(self, path: Path) -> bool:
        ...

    @abstractmethod
    def show_notification(self, title: str, message: str) -> None:
        ...