"""Infrastructure - yt-dlp implementation."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Callable, Optional

import yt_dlp

from ytdlp_core.core.models import (
    DownloadOptions,
    DownloadProgress,
    DownloadResult,
    DownloadStatus,
    MediaType,
    VideoFormat,
    VideoInfo,
)
from ytdlp_core.domain.ports import IDownloader, IVideoInfoExtractor
from ytdlp_core.domain.exceptions import DownloadError, ExtractionError, ValidationError


class YtDlpVideoInfoExtractor(IVideoInfoExtractor):
    """Video info extractor using yt-dlp."""

    YOUTUBE_PATTERNS = [
        r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/embed/[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/v/[\w-]+",
        r"^(https?://)?youtu\.be/[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/shorts/[\w-]+",
    ]

    def __init__(self, timeout: int = 10, proxy: Optional[str] = None):
        self.timeout = timeout
        self.proxy = proxy

    def validate_url(self, url: str) -> bool:
        import re
        return any(re.match(pattern, url) for pattern in self.YOUTUBE_PATTERNS)

    def extract_info(self, url: str) -> VideoInfo:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": self.timeout,
        }
        if self.proxy:
            ydl_opts["proxy"] = self.proxy

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                raw_info = ydl.extract_info(url, download=False)
        except yt_dlp.DownloadError as e:
            raise ExtractionError(str(e), url=url, original=e)
        except Exception as e:
            raise ExtractionError(f"Unexpected error: {e}", url=url, original=e)

        if not raw_info:
            raise ExtractionError("No info returned", url=url)

        formats = []
        for f in raw_info.get("formats", []):
            if f.get("vcodec") != "none" or f.get("acodec") != "none":
                formats.append(VideoFormat(
                    format_id=f.get("format_id", ""),
                    ext=f.get("ext", ""),
                    resolution=f.get("height"),
                    fps=f.get("fps"),
                    vcodec=f.get("vcodec"),
                    acodec=f.get("acodec"),
                    abr=f.get("abr"),
                    filesize=f.get("filesize"),
                    filesize_approx=f.get("filesize_approx"),
                    protocol=f.get("protocol"),
                    format_note=f.get("format_note"),
                    is_video_only=f.get("vcodec") != "none" and f.get("acodec") == "none",
                    is_audio_only=f.get("acodec") != "none" and f.get("vcodec") == "none",
                ))

        return VideoInfo(
            id=raw_info.get("id", ""),
            title=raw_info.get("title", ""),
            duration=raw_info.get("duration"),
            duration_string=raw_info.get("duration_string"),
            uploader=raw_info.get("uploader"),
            uploader_id=raw_info.get("uploader_id"),
            upload_date=raw_info.get("upload_date"),
            view_count=raw_info.get("view_count"),
            like_count=raw_info.get("like_count"),
            description=raw_info.get("description"),
            thumbnail=raw_info.get("thumbnail"),
            webpage_url=raw_info.get("webpage_url"),
            formats=tuple(formats),
            is_live=raw_info.get("is_live", False),
            age_limit=raw_info.get("age_limit", 0),
            categories=tuple(raw_info.get("categories", [])),
            tags=tuple(raw_info.get("tags", [])),
        )


class YtDlpDownloader(IDownloader):
    """Downloader using yt-dlp."""

    def __init__(self):
        self._cancel_event = threading.Event()
        self._current_ydl: Optional[yt_dlp.YoutubeDL] = None

    def cancel(self) -> None:
        """Cancel current download."""
        self._cancel_event.set()
        if self._current_ydl:
            # yt-dlp doesn't have a clean cancel, but we can try
            pass

    def download(
        self,
        options: DownloadOptions,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
    ) -> DownloadResult:
        self._cancel_event.clear()

        def progress_hook(d: dict[str, Any]) -> None:
            if self._cancel_event.is_set():
                raise CancellationError("Download cancelled by user")

            if progress_callback:
                if d["status"] == "downloading":
                    downloaded = d.get("downloaded_bytes", 0)
                    total = d.get("total_bytes") or d.get("total_bytes_estimate")
                    percent = (downloaded / total * 100) if total else 0

                    progress = DownloadProgress(
                        status=DownloadStatus.DOWNLOADING,
                        downloaded_bytes=downloaded,
                        total_bytes=total,
                        speed=d.get("speed"),
                        eta=d.get("eta"),
                        filename=d.get("filename"),
                        percent=percent,
                    )
                elif d["status"] == "finished":
                    progress = DownloadProgress(
                        status=DownloadStatus.COMPLETED,
                        downloaded_bytes=d.get("downloaded_bytes", 0),
                        total_bytes=d.get("total_bytes"),
                        filename=d.get("filename"),
                        percent=100.0,
                    )
                elif d["status"] == "error":
                    progress = DownloadProgress(
                        status=DownloadStatus.FAILED,
                        error=d.get("error", "Unknown error"),
                    )
                else:
                    return
                progress_callback(progress)

        ydl_opts = options.to_ydl_opts()
        ydl_opts["progress_hooks"] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self._current_ydl = ydl
                ydl.download([options.url])

            # Find output file
            output_files = list(options.output_path.glob(f"*{options.format_id}*"))
            if not output_files:
                # Try with template
                from string import Formatter
                # Simple fallback
                output_files = list(options.output_path.glob("*.mp4")) + \
                              list(options.output_path.glob("*.mp3")) + \
                              list(options.output_path.glob("*.webm")) + \
                              list(options.output_path.glob("*.mkv"))

            output_file = output_files[0] if output_files else None

            return DownloadResult(
                success=True,
                output_path=output_file,
            )

        except CancellationError:
            return DownloadResult(success=False, error="Cancelled")
        except yt_dlp.DownloadError as e:
            return DownloadResult(success=False, error=str(e))
        except Exception as e:
            return DownloadResult(success=False, error=f"Unexpected error: {e}")
        finally:
            self._current_ydl = None