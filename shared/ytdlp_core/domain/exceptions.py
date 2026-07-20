"""Domain exceptions."""

from __future__ import annotations

from typing import Optional


class YtdlpCoreError(Exception):
    """Base exception for ytdlp-core."""

    def __init__(self, message: str, original: Optional[Exception] = None):
        super().__init__(message)
        self.original = original


class ExtractionError(YtdlpCoreError):
    """Video info extraction failed."""

    def __init__(self, message: str, url: str = "", original: Optional[Exception] = None):
        super().__init__(message, original)
        self.url = url


class DownloadError(YtdlpCoreError):
    """Download operation failed."""

    pass


class CancellationError(YtdlpCoreError):
    """Operation was cancelled."""

    pass


class FFmpegError(YtdlpCoreError):
    """FFmpeg operation failed."""

    pass


class ValidationError(YtdlpCoreError):
    """Input validation failed."""

    pass


class ConfigurationError(YtdlpCoreError):
    """Configuration error."""

    pass