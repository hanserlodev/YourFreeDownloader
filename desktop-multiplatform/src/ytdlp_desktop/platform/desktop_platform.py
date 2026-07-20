"""Desktop platform service."""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

from ytdlp_core.domain.ports import IPlatformService


class DesktopPlatformService(IPlatformService):
    """Platform service for desktop."""

    def get_data_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent / "YouTubeDownloader_Data"
        return Path(__file__).parent.parent.parent.parent / "YouTubeDownloader_Data"

    def get_download_dir(self) -> Path:
        if os.name == "nt":
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
                    downloads = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
                    return Path(downloads)
            except Exception:
                pass
        downloads = Path.home() / "Downloads"
        if downloads.exists():
            return downloads
        return Path.home()

    def open_folder(self, path: Path) -> bool:
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
        print(f"[NOTIFICATION] {title}: {message}")