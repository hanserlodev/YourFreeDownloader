"""Infrastructure - platform-specific implementations."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Any, Optional

from ytdlp_core.domain.ports import IConfigStore, IFFmpegLocator, IPlatformService


class FFmpegLocator(IFFmpegLocator):
    """Locate ffmpeg executable."""

    def find_ffmpeg(self) -> Optional[str]:
        # 1. Check bundled with PyInstaller
        if getattr(sys, "frozen", False):
            base = Path(sys.executable).parent
            for path in [
                base / "ffmpeg" / "bin" / "ffmpeg.exe",
                base / "ffmpeg" / "ffmpeg.exe",
                base / "bin" / "ffmpeg.exe",
                base / "ffmpeg.exe",
            ]:
                if path.exists():
                    return str(path)

            if hasattr(sys, "_MEIPASS"):
                meipass_path = Path(sys._MEIPASS) / "ffmpeg" / "ffmpeg.exe"
                if meipass_path.exists():
                    return str(meipass_path)

        # 2. Check project-relative (dev mode)
        base = Path(__file__).parent.parent.parent.parent
        for path in [
            base / "ffmpeg" / "bin" / "ffmpeg.exe",
            base / "ffmpeg" / "ffmpeg.exe",
            base / "bin" / "ffmpeg.exe",
        ]:
            if path.exists():
                return str(path)

        # 3. Check PATH
        if ffmpeg := shutil.which("ffmpeg"):
            return ffmpeg

        # 4. Common system locations
        for path in [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",
        ]:
            if Path(path).exists():
                return path

        return None


class JsonConfigStore(IConfigStore):
    """JSON file-based config store."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        import json
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception:
                self._cache = {}

    def _save(self) -> None:
        import json
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._save()

    def get_all(self) -> dict[str, Any]:
        return self._cache.copy()


class MemoryCacheStore:
    """In-memory cache for video info."""

    def __init__(self):
        self._cache: dict[str, Any] = {}

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def clear(self) -> None:
        self._cache.clear()


class DesktopPlatformService(IPlatformService):
    """Platform service for desktop (Windows/Linux)."""

    def get_data_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent / "YouTubeDownloader_Data"
        return Path(__file__).parent.parent.parent.parent / "YouTubeDownloader_Data"

    def get_download_dir(self) -> Path:
        # Use user's Downloads folder
        if os.name == "nt":  # Windows
            import winreg
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
                    downloads = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
                    return Path(downloads)
            except Exception:
                pass
        # Linux/macOS fallback
        downloads = Path.home() / "Downloads"
        if downloads.exists():
            return downloads
        return Path.home()

    def open_folder(self, path: Path) -> bool:
        import subprocess
        try:
            if sys.platform == "win32":
                os.startfile(path)  # type: ignore
            elif sys.platform == "darwin":
                subprocess.run(["open", path], check=True)
            else:
                subprocess.run(["xdg-open", path], check=True)
            return True
        except Exception:
            return False

    def show_notification(self, title: str, message: str) -> None:
        # Could use plyer or platform-specific notifications
        print(f"[NOTIFICATION] {title}: {message}")