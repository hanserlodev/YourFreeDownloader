"""Infrastructure - yt-dlp implementation of downloader."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Callable, Optional

import yt_dlp

from ytdlp_core.core.models import DownloadOptions, DownloadProgress, DownloadResult, DownloadStatus
from ytdlp_core.domain.ports import IDownloader
from ytdlp_core.domain.exceptions import CancellationError, DownloadError


class YtDlpDownloader(IDownloader):
    """Video downloader using yt-dlp."""

    def __init__(self):
        self._cancel_event = threading.Event()
        self._current_ydl: Optional[yt_dlp.YoutubeDL] = None

    def download(
        self,
        options: DownloadOptions,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
    ) -> DownloadResult:
        """Download video using yt-dlp."""
        self._cancel_event.clear()

        def progress_hook(d: dict[str, Any]) -> None:
            if self._cancel_event.is_set():
                raise CancellationError("Download cancelled by user")

            if progress_callback:
                progress = self._parse_progress(d)
                progress_callback(progress)

        ydl_opts = options.to_ydl_opts()
        ydl_opts["progress_hooks"] = [progress_hook]

        try:
            self._current_ydl = yt_dlp.YoutubeDL(ydl_opts)
            self._current_ydl.download([options.url])

            # Find downloaded file
            output_path = self._find_downloaded_file(options)

            return DownloadResult(
                success=True,
                output_path=output_path,
                video_info=None,  # Could extract info again if needed
            )

        except yt_dlp.DownloadError as e:
            if "cancelled" in str(e).lower():
                raise CancellationError("Download cancelled")
            raise DownloadError(str(e), original=e)
        except CancellationError:
            raise
        except Exception as e:
            raise DownloadError(f"Download failed: {e}", original=e)
        finally:
            self._current_ydl = None

    def cancel(self) -> None:
        """Cancel ongoing download."""
        self._cancel_event.set()
        if self._current_ydl:
            # yt-dlp doesn't have a clean cancel, but we can try
            pass

    def _parse_progress(self, d: dict[str, Any]) -> DownloadProgress:
        """Parse yt-dlp progress dict to DownloadProgress."""
        status = d.get("status", "downloading")

        if status == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            speed = d.get("speed")
            eta = d.get("eta")
            filename = d.get("filename")

            percent = 0.0
            if total and total > 0:
                percent = (downloaded / total) * 100

            return DownloadProgress(
                status=DownloadStatus.DOWNLOADING,
                downloaded_bytes=downloaded,
                total_bytes=total,
                speed=speed,
                eta=eta,
                filename=filename,
                percent=percent,
            )

        elif status == "finished":
            return DownloadProgress(
                status=DownloadStatus.FINISHED,
                downloaded_bytes=d.get("total_bytes", 0),
                total_bytes=d.get("total_bytes"),
                filename=d.get("filename"),
                percent=100.0,
            )

        elif status == "error":
            return DownloadProgress(
                status=DownloadStatus.ERROR,
                error=d.get("error", "Unknown error"),
                percent=0.0,
            )

        return DownloadProgress(status=DownloadStatus.PENDING)

    def _find_downloaded_file(self, options: DownloadOptions) -> Optional[Path]:
        """Find the downloaded file based on output template."""
        import glob

        # The template might have %(title)s etc, so we glob the directory
        pattern = str(options.output_path / "*")
        files = glob.glob(pattern)

        # Filter by modification time (recent files)
        if files:
            # Return the most recently modified file
            return max(files, key=lambda f: Path(f).stat().st_mtime)

        return None