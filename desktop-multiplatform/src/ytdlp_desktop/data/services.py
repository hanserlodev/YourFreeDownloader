"""Desktop data layer - repositories and services."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import customtkinter as ctk

from ytdlp_core.application.use_cases import (
    DownloadVideoUseCase,
    GetDefaultOptionsUseCase,
    GetVideoInfoUseCase,
    SaveDefaultOptionsUseCase,
)
from ytdlp_core.core.models import DownloadOptions, DownloadProgress, DownloadResult, MediaType, VideoInfo
from ytdlp_core.domain.ports import (
    ICacheStore,
    IConfigStore,
    IDownloader,
    IFFmpegLocator,
    IPlatformService,
    IVideoInfoExtractor,
)
from ytdlp_core.domain.exceptions import CancellationError, DownloadError, ExtractionError
from ytdlp_core.infrastructure.platform import DesktopPlatformService, FFmpegLocator, JsonConfigStore, MemoryCacheStore
from ytdlp_core.infrastructure.yt_dlp_impl import YtDlpDownloader, YtDlpVideoInfoExtractor


class DesktopServiceContainer:
    """Dependency injection container for desktop app."""

    def __init__(self):
        self._config: IConfigStore | None = None
        self._cache: ICacheStore | None = None
        self._extractor: IVideoInfoExtractor | None = None
        self._downloader: IDownloader | None = None
        self._ffmpeg: IFFmpegLocator | None = None
        self._platform: IPlatformService | None = None

        self._get_video_info_use_case: GetVideoInfoUseCase | None = None
        self._download_video_use_case: DownloadVideoUseCase | None = None
        self._get_default_options_use_case: GetDefaultOptionsUseCase | None = None
        self._save_default_options_use_case: SaveDefaultOptionsUseCase | None = None

    @property
    def config(self) -> IConfigStore:
        if self._config is None:
            data_dir = self.platform.get_data_dir()
            self._config = JsonConfigStore(data_dir / "config.json")
        return self._config

    @property
    def cache(self) -> ICacheStore:
        if self._cache is None:
            self._cache = MemoryCacheStore()
        return self._cache

    @property
    def extractor(self) -> IVideoInfoExtractor:
        if self._extractor is None:
            self._extractor = YtDlpVideoInfoExtractor(
                timeout=self.config.get("timeout", 30),
                proxy=self.config.get("proxy") or None,
            )
        return self._extractor

    @property
    def downloader(self) -> IDownloader:
        if self._downloader is None:
            self._downloader = YtDlpDownloader()
        return self._downloader

    @property
    def ffmpeg(self) -> IFFmpegLocator:
        if self._ffmpeg is None:
            self._ffmpeg = FFmpegLocator()
        return self._ffmpeg

    @property
    def platform(self) -> IPlatformService:
        if self._platform is None:
            self._platform = DesktopPlatformService()
        return self._platform

    @property
    def get_video_info_use_case(self) -> GetVideoInfoUseCase:
        if self._get_video_info_use_case is None:
            self._get_video_info_use_case = GetVideoInfoUseCase(
                extractor=self.extractor,
                cache=self.cache,
            )
        return self._get_video_info_use_case

    @property
    def download_video_use_case(self) -> DownloadVideoUseCase:
        if self._download_video_use_case is None:
            self._download_video_use_case = DownloadVideoUseCase(
                downloader=self.downloader,
                ffmpeg_locator=self.ffmpeg,
                config=self.config,
                platform=self.platform,
            )
        return self._download_video_use_case

    @property
    def get_default_options_use_case(self) -> GetDefaultOptionsUseCase:
        if self._get_default_options_use_case is None:
            self._get_default_options_use_case = GetDefaultOptionsUseCase(
                config=self.config,
            )
        return self._get_default_options_use_case

    @property
    def save_default_options_use_case(self) -> SaveDefaultOptionsUseCase:
        if self._save_default_options_use_case is None:
            self._save_default_options_use_case = SaveDefaultOptionsUseCase(
                config=self.config,
            )
        return self._save_default_options_use_case


# Global container instance
container = DesktopServiceContainer()


def get_container() -> DesktopServiceContainer:
    """Get global service container."""
    return container


def setup_logging(config: IConfigStore) -> None:
    """Setup application logging."""
    data_dir = container.platform.get_data_dir()
    log_file = data_dir / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Reduce noise from libraries
    logging.getLogger("yt_dlp").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)