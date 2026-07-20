"""Main entry point for desktop app."""

from __future__ import annotations

import sys
import threading
from pathlib import Path

import customtkinter as ctk

from ytdlp_desktop.ui.main_window import MainWindow
from ytdlp_desktop.config.config_store import DesktopConfigStore
from ytdlp_desktop.platform.desktop_platform import DesktopPlatformService
from ytdlp_desktop.di.container import Container


def setup_directories():
    """Create necessary directories."""
    data_dir = DesktopPlatformService().get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def main():
    """Application entry point."""
    # Setup
    data_dir = setup_directories()
    config_path = data_dir / "config.json"

    # Initialize DI container
    container = Container()
    container.config_store.override(DesktopConfigStore(config_path))
    container.platform_service.override(DesktopPlatformService())
    container.wire(modules=["ytdlp_desktop.ui.main_window"])

    # CustomTkinter setup
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create and run app
    app = MainWindow(container)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()