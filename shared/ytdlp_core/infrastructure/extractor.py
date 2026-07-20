"""Infrastructure - yt-dlp implementation of video info extractor."""

from __future__ import annotations

from typing import Any, Optional

import yt_dlp

from ytdlp_core.core.models import VideoFormat, VideoInfo
from ytdlp_core.domain.ports import IVideoInfoExtractor
from ytdlp_core.domain.exceptions import ExtractionError, ValidationError


class YtDlpVideoInfoExtractor(IVideoInfoExtractor):
    """Video info extractor using yt-dlp."""

    YOUTUBE_PATTERNS = [
        r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/embed/[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/v/[\w-]+",
        r"^(https?://)?youtu\.be/[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/shorts/[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/playlist\?list=[\w-]+",
        r"^(https?://)?(www\.)?youtube\.com/@[\w-]+",
    ]

    def __init__(self, timeout: int = 10, proxy: Optional[str] = None):
        self.timeout = timeout
        self.proxy = proxy

    def validate_url(self, url: str) -> bool:
        """Validate if URL matches YouTube patterns."""
        import re

        return any(re.match(pattern, url) for pattern in self.YOUTUBE_PATTERNS)

    def extract_info(self, url: str) -> VideoInfo:
        """Extract video info using yt-dlp."""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
            "socket_timeout": self.timeout,
        }

        if self.proxy:
            ydl_opts["proxy"] = self.proxy

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise ExtractionError("No video info returned", url=url)

                return self._parse_video_info(info, url)

        except yt_dlp.DownloadError as e:
            raise ExtractionError(str(e), url=url, original=e)
        except Exception as e:
            raise ExtractionError(f"Unexpected error: {e}", url=url, original=e)

    def _parse_video_info(self, info: dict[str, Any], url: str) -> VideoInfo:
        """Parse yt-dlp info dict to VideoInfo model."""
        formats = []
        for f in info.get("formats", []):
            if f.get("vcodec") == "none" and f.get("acodec") == "none":
                continue

            format_id = f.get("format_id", "")
            ext = f.get("ext", "unknown")
            vcodec = f.get("vcodec", "none")
            acodec = f.get("acodec", "none")
            height = f.get("height")
            width = f.get("width")
            fps = f.get("fps")
            tbr = f.get("tbr")  # total bitrate
            abr = f.get("abr")  # audio bitrate
            vbr = f.get("vbr")  # video bitrate
            filesize = f.get("filesize") or f.get("filesize_approx")
            protocol = f.get("protocol", "")
            format_note = f.get("format_note", "")

            resolution = None
            if height and width:
                resolution = f"{width}x{height}"
            elif height:
                resolution = f"{height}p"

            formats.append(
                VideoFormat(
                    format_id=format_id,
                    ext=ext,
                    resolution=resolution,
                    fps=fps,
                    vcodec=vcodec if vcodec != "none" else None,
                    acodec=acodec if acodec != "none" else None,
                    bitrate=tbr,
                    audio_bitrate=abr,
                    video_bitrate=vbr,
                    filesize=filesize,
                    protocol=protocol,
                    format_note=format_note,
                )
            )

        return VideoInfo(
            id=info.get("id", ""),
            title=info.get("title", "Unknown"),
            description=info.get("description"),
            uploader=info.get("uploader"),
            uploader_id=info.get("uploader_id"),
            upload_date=info.get("upload_date"),
            duration=info.get("duration"),
            view_count=info.get("view_count"),
            like_count=info.get("like_count"),
            thumbnail=info.get("thumbnail"),
            thumbnails=info.get("thumbnails", []),
            formats=formats,
            webpage_url=info.get("webpage_url", url),
            original_url=url,
            is_live=info.get("is_live", False),
            availability=info.get("availability"),
            age_limit=info.get("age_limit"),
            categories=info.get("categories", []),
            tags=info.get("tags", []),
        )