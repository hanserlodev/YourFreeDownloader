"""Domain layer - interfaces and exceptions."""

from ytdlp_core.domain.exceptions import (
    CancellationError,
    ConfigurationError,
    DomainError,
    DownloadError,
    ExtractionError,
    FFmpegNotFoundError,
    ValidationError,
)
from ytdlp_core.domain.ports import (
    ICacheStore,
    IConfigStore,
    IDownloader,
    IFFmpegLocator,
    IPlatformService,
    IVideoInfoExtractor,
)

__all__ = [
    "DomainError",
    "ValidationError",
    "ExtractionError",
    "DownloadError",
    "FFmpegNotFoundError",
    "CancellationError",
    "ConfigurationError",
    "IVideoInfoExtractor",
    "IDownloader",
    "IFFmpegLocator",
    "IConfigStore",
    "ICacheStore",
    "IPlatformService",
]