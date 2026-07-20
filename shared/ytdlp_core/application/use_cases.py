"""Application layer - use cases."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from ytdlp_core.core.models import (
    DownloadOptions,
    DownloadProgress,
    DownloadResult,
    MediaType,
    VideoFormat,
    VideoInfo,
)
from ytdlp_core.domain.ports import (
    ICacheStore,
    IConfigStore,
    IDownloader,
    IFFmpegLocator,
    IVideoInfoExtractor,
    IPlatformService,
)
from ytdlp_core.domain.exceptions import (
    CancellationError,
    DownloadError,
    ExtractionError,
    FFmpegError,
    ValidationError,
)


@dataclass
class GetVideoInfoUseCase:
    """Use case for fetching video info."""

    extractor: IVideoInfoExtractor
    cache: ICacheStore

    def execute(self, url: str, use_cache: bool = True) -> VideoInfo:
        """Get video info, using cache if available."""
        if not self.extractor.validate_url(url):
            raise ValidationError(f"Invalid YouTube URL: {url}")

        if use_cache:
            cached = self.cache.get(url)
            if cached:
                return cached

        info = self.extractor.extract_info(url)
        self.cache.set(url, info)
        return info


@dataclass
class DownloadVideoUseCase:
    """Use case for downloading video/audio."""

    downloader: IDownloader
    ffmpeg_locator: IFFmpegLocator
    config: IConfigStore
    platform: IPlatformService

    def execute(
        self,
        url: str,
        format_id: str,
        media_type: MediaType,
        output_dir: Optional[Path] = None,
        filename_template: str = "%(title)s.%(ext)s",
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
    ) -> DownloadResult:
        """Download video or audio."""
        if output_dir is None:
            output_dir = self.platform.get_download_dir()

        output_dir.mkdir(parents=True, exist_ok=True)

        ffmpeg_path = self.ffmpeg_locator.find_ffmpeg()
        if media_type == MediaType.AUDIO_ONLY and not ffmpeg_path:
            raise FFmpegError("FFmpeg required for audio-only downloads")

        options = DownloadOptions(
            url=url,
            format_id=format_id,
            media_type=media_type,
            output_path=output_dir,
            filename_template=filename_template,
            ffmpeg_path=ffmpeg_path,
            proxy=self.config.get("proxy"),
            rate_limit=self.config.get("rate_limit"),
            retries=self.config.get("download_retries", 3),
            timeout=self.config.get("download_timeout", 30),
            write_thumbnail=self.config.get("write_thumbnail", False),
            write_subtitles=self.config.get("write_subtitles", False),
            subtitle_langs=tuple(self.config.get("subtitle_langs", [])),
            embed_subtitles=self.config.get("embed_subtitles", False),
            embed_thumbnail=self.config.get("embed_thumbnail", False),
            post_processors=tuple(self.config.get("post_processors", [])),
        )

        return self.downloader.download(options, progress_callback)

    def cancel(self) -> None:
        """Cancel ongoing download."""
        self.downloader.cancel()


@dataclass
class GetDefaultOptionsUseCase:
    """Get default download options from config."""

    config: IConfigStore

    def execute(self) -> dict[str, Any]:
        return {
            "default_quality": self.config.get("default_quality", "best"),
            "default_media_type": self.config.get("default_media_type", MediaType.VIDEO.value),
            "output_dir": self.config.get("last_output_dir"),
            "filename_template": self.config.get("filename_template", "%(title)s.%(ext)s"),
        }


@dataclass
class SaveDefaultOptionsUseCase:
    """Save default download options to config."""

    config: IConfigStore

    def execute(
        self,
        default_quality: Optional[str] = None,
        default_media_type: Optional[MediaType] = None,
        output_dir: Optional[Path] = None,
        filename_template: Optional[str] = None,
    ) -> None:
        if default_quality is not None:
            self.config.set("default_quality", default_quality)
        if default_media_type is not None:
            self.config.set("default_media_type", default_media_type.value)
        if output_dir is not None:
            self.config.set("last_output_dir", str(output_dir))
        if filename_template is not None:
            self.config.set("filename_template", filename_template)