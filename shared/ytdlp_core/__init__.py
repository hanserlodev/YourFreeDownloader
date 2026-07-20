"""ytdlp-core: Shared core library for YouTube downloading."""

from ytdlp_core.core.models import (
    DownloadOptions,
    DownloadProgress,
    DownloadResult,
    DownloadStatus,
    MediaType,
    VideoFormat,
    VideoInfo,
)
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
from ytdlp_core.application.use_cases import (
    DownloadVideoUseCase,
    GetDefaultOptionsUseCase,
    GetVideoInfoUseCase,
    SaveDefaultOptionsUseCase,
)

__version__ = "1.0.0"

__all__ = [
    # Core models
    "VideoInfo",
    "VideoFormat",
    "DownloadOptions",
    "DownloadProgress",
    "DownloadResult",
    "DownloadStatus",
    "MediaType",
    # Exceptions
    "DomainError",
    "ValidationError",
    "ExtractionError",
    "DownloadError",
    "FFmpegNotFoundError",
    "CancellationError",
    "ConfigurationError",
    # Ports
    "IVideoInfoExtractor",
    "IDownloader",
    "IFFmpegLocator",
    "IConfigStore",
    "ICacheStore",
    "IPlatformService",
    # Use cases
    "GetVideoInfoUseCase",
    "DownloadVideoUseCase",
    "GetDefaultOptionsUseCase",
    "SaveDefaultOptionsUseCase",
]