"""Main application window."""

from __future__ import annotations

import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk

from ytdlp_desktop.config.manager import ConfigManager
from ytdlp_desktop.data.services import DesktopServiceContainer
from ytdlp_core.core.models import DownloadProgress, DownloadStatus, MediaType
from ytdlp_core.application.use_cases import GetVideoInfoUseCase, DownloadVideoUseCase
from ytdlp_core.domain.exceptions import ExtractionError, ValidationError


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self, config_manager: ConfigManager, container: DesktopServiceContainer):
        super().__init__()
        self.config_manager = config_manager
        self.container = container

        self.title("YourFreeDownloader")
        self.minsize(800, 600)

        # State
        self._video_info = None
        self._selected_format_id: Optional[str] = None
        self._download_thread: Optional[threading.Thread] = None
        self._is_downloading = False

        # UI Components
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()

        # Load last used directory
        last_dir = self.config_manager.get("default_output_dir")
        if last_dir and Path(last_dir).exists():
            self.output_dir_var.set(last_dir)

    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # URL Section
        self.url_frame = ctk.CTkFrame(self.main_frame)
        self.url_label = ctk.CTkLabel(self.url_frame, text="YouTube URL:", font=ctk.CTkFont(size=14, weight="bold"))
        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="https://www.youtube.com/watch?v=...", height=40)
        self.get_info_btn = ctk.CTkButton(self.url_frame, text="Get Info", command=self._on_get_info, width=120, height=40)
        self.theme_btn = ctk.CTkButton(self.url_frame, text="🌓", command=self._toggle_theme, width=40, height=40)

        # Video Info Section
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_label = ctk.CTkLabel(self.info_frame, text="", justify="left", anchor="w", font=ctk.CTkFont(size=12))

        # Options Section
        self.options_frame = ctk.CTkFrame(self.main_frame)

        # Media type
        self.media_type_var = ctk.StringVar(value="video")
        self.media_type_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.video_radio = ctk.CTkRadioButton(
            self.media_type_frame, text="Video", variable=self.media_type_var, value="video",
            command=self._on_media_type_change
        )
        self.audio_radio = ctk.CTkRadioButton(
            self.media_type_frame, text="Audio Only (MP3)", variable=self.media_type_var, value="audio",
            command=self._on_media_type_change
        )

        # Quality selection
        self.quality_label = ctk.CTkLabel(self.options_frame, text="Quality:", font=ctk.CTkFont(weight="bold"))
        self.quality_combo = ctk.CTkComboBox(
            self.options_frame,
            values=["Select video info first"],
            state="readonly",
            command=self._on_quality_select,
        )
        self.quality_combo.set("Select video info first")

        # Output directory
        self.output_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.output_label = ctk.CTkLabel(self.output_frame, text="Output Folder:", font=ctk.CTkFont(weight="bold"))
        self.output_dir_var = ctk.StringVar()
        self.output_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_dir_var, height=35)
        self.browse_btn = ctk.CTkButton(self.output_frame, text="Browse", command=self._browse_output, width=100, height=35)

        # Download button
        self.download_btn = ctk.CTkButton(
            self.main_frame,
            text="🚀 Download",
            command=self._on_download,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled",
        )

        # Progress Section
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Progress:", font=ctk.CTkFont(weight="bold"))
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=20)
        self.progress_bar.set(0)

        # Progress details
        self.progress_details_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.speed_var = ctk.StringVar(value="Speed: --")
        self.eta_var = ctk.StringVar(value="ETA: --:--")
        self.downloaded_var = ctk.StringVar(value="Downloaded: 0 / 0 MB")
        self.speed_label = ctk.CTkLabel(self.progress_details_frame, textvariable=self.speed_var)
        self.eta_label = ctk.CTkLabel(self.progress_details_frame, textvariable=self.eta_var)
        self.downloaded_label = ctk.CTkLabel(self.progress_details_frame, textvariable=self.downloaded_var)

        # Log Section
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_header_frame = ctk.CTkFrame(self.log_frame, fg_color="transparent")
        self.log_label = ctk.CTkLabel(self.log_header_frame, text="Activity Log:", font=ctk.CTkFont(weight="bold"))
        self.clear_log_btn = ctk.CTkButton(self.log_header_frame, text="Clear", command=self._clear_log, width=60, height=25)
        self.log_text = ctk.CTkTextbox(self.log_frame, height=150, font=("Consolas", 11))

    def _layout_widgets(self):
        """Layout all widgets."""
        # URL Section
        self.url_frame.pack(fill=tk.X, pady=(0, 10))
        self.url_label.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        self.get_info_btn.pack(side=tk.LEFT, padx=5, pady=10)
        self.theme_btn.pack(side=tk.LEFT, padx=(5, 10), pady=10)

        # Video Info
        self.info_frame.pack(fill=tk.X, pady=(0, 10))
        self.info_label.pack(fill=tk.X, padx=15, pady=10)

        # Options
        self.options_frame.pack(fill=tk.X, pady=(0, 10))

        # Media type
        self.media_type_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        ctk.CTkLabel(self.media_type_frame, text="Type:", font=ctk.CTkFont(weight="bold")).pack(side=tk.LEFT)
        self.video_radio.pack(side=tk.LEFT, padx=(10, 20))
        self.audio_radio.pack(side=tk.LEFT)

        # Quality
        self.quality_label.pack(anchor=tk.W, padx=15, pady=(10, 0))
        self.quality_combo.pack(fill=tk.X, padx=15, pady=(5, 10))

        # Output directory
        self.output_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.output_label.pack(anchor=tk.W)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=(5, 10))
        self.browse_btn.pack(side=tk.LEFT, pady=(5, 10))

        # Download button
        self.download_btn.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Progress
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        self.progress_label.pack(anchor=tk.W, padx=15, pady=(10, 0))
        self.progress_bar.pack(fill=tk.X, padx=15, pady=(5, 5))

        self.progress_details_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        self.speed_label.pack(side=tk.LEFT, padx=(0, 20))
        self.eta_label.pack(side=tk.LEFT, padx=(0, 20))
        self.downloaded_label.pack(side=tk.LEFT)

        # Log
        self.log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_header_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
        self.log_label.pack(side=tk.LEFT)
        self.clear_log_btn.pack(side=tk.RIGHT)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 10))

    def _bind_events(self):
        """Bind events."""
        self.url_entry.bind("<Return>", lambda e: self._on_get_info())

    def _toggle_theme(self):
        """Toggle theme."""
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self.config_manager.set("theme", new_mode)

    def _browse_output(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get() or str(Path.home()))
        if directory:
            self.output_dir_var.set(directory)
            self.config_manager.set("default_output_dir", directory)

    def _on_get_info(self):
        """Handle get info button click."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("URL Required", "Please enter a YouTube URL.")
            return

        self._log(f"Fetching info for: {url}")
        self.get_info_btn.configure(state="disabled", text="Loading...")
        self.info_label.configure(text="Fetching video info...")

        def fetch():
            try:
                use_case: GetVideoInfoUseCase = self.container.get_video_info_use_case
                info = use_case.execute(url)
                self.after(0, lambda: self._on_info_loaded(info))
            except ValidationError as e:
                self.after(0, lambda: self._on_info_error(str(e)))
            except ExtractionError as e:
                self.after(0, lambda: self._on_info_error(f"Failed to extract info: {e}"))
            except Exception as e:
                self.after(0, lambda: self._on_info_error(f"Unexpected error: {e}"))

        threading.Thread(target=fetch, daemon=True).start()

    def _on_info_loaded(self, info):
        """Handle loaded video info."""
        self._video_info = info
        self.get_info_btn.configure(state="normal", text="Get Info")

        # Format video info for display
        duration_str = "Unknown"
        if info.duration:
            h, rem = divmod(info.duration, 3600)
            m, s = divmod(rem, 60)
            duration_str = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

        views_str = f"{info.view_count:,}" if info.view_count else "Unknown"

        display_text = f"📹 {info.title}\n⏱️ {duration_str} | 👤 {info.uploader or 'Unknown'} | 👁️ {views_str} views"
        self.info_label.configure(text=display_text)

        # Populate quality combo
        self._update_quality_options()
        self.download_btn.configure(state="normal")
        self._log(f"Loaded: {info.title} ({len(info.formats)} formats)")

    def _on_info_error(self, error: str):
        """Handle info loading error."""
        self.get_info_btn.configure(state="normal", text="Get Info")
        self.info_label.configure(text="")
        messagebox.showerror("Error", error)
        self._log(f"Error: {error}")

    def _update_quality_options(self):
        """Update quality combo based on media type."""
        if not self._video_info:
            return

        media_type = MediaType(self.media_type_var.get())
        formats = self._video_info.video_formats if media_type == MediaType.VIDEO else self._video_info.audio_formats

        if not formats:
            self.quality_combo.configure(values=["No formats available"])
            self.quality_combo.set("No formats available")
            return

        options = [f.display_name for f in formats]
        self.quality_combo.configure(values=options)
        self.quality_combo.set(options[0])
        self._selected_format_id = formats[0].format_id

    def _on_media_type_change(self):
        """Handle media type change."""
        self._update_quality_options()

    def _on_quality_select(self, value: str):
        """Handle quality selection."""
        if not self._video_info:
            return

        media_type = MediaType(self.media_type_var.get())
        formats = self._video_info.video_formats if media_type == MediaType.VIDEO else self._video_info.audio_formats

        for fmt in formats:
            if fmt.display_name == value:
                self._selected_format_id = fmt.format_id
                break

    def _on_download(self):
        """Handle download button click."""
        if not self._video_info or not self._selected_format_id:
            return

        url = self.url_entry.get().strip()
        output_dir = Path(self.output_dir_var.get()) if self.output_dir_var.get() else None
        media_type = MediaType(self.media_type_var.get())

        self._is_downloading = True
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.progress_bar.set(0)
        self._log(f"Starting download: {self._video_info.title}")

        def download():
            try:
                use_case: DownloadVideoUseCase = self.container.download_video_use_case
                result = use_case.execute(
                    url=url,
                    format_id=self._selected_format_id,
                    media_type=media_type,
                    output_dir=output_dir,
                    progress_callback=self._on_progress,
                )
                self.after(0, lambda: self._on_download_complete(result))
            except Exception as e:
                self.after(0, lambda: self._on_download_error(str(e)))

        self._download_thread = threading.Thread(target=download, daemon=True)
        self._download_thread.start()

    def _on_progress(self, progress: DownloadProgress):
        """Handle download progress."""
        def update():
            if progress.status == DownloadStatus.DOWNLOADING:
                if progress.total_bytes:
                    self.progress_bar.set(progress.percent / 100)
                self.speed_var.set(f"Speed: {progress.speed / (1024*1024):.2f} MB/s" if progress.speed else "Speed: --")
                self.eta_var.set(f"ETA: {progress.eta}s" if progress.eta else "ETA: --:--")
                self.downloaded_var.set(
                    f"Downloaded: {progress.downloaded_bytes / (1024*1024):.1f} / "
                    f"{progress.total_bytes / (1024*1024):.1f} MB" if progress.total_bytes else
                    f"Downloaded: {progress.downloaded_bytes / (1024*1024):.1f} MB"
                )
            elif progress.status == DownloadStatus.COMPLETED:
                self.progress_bar.set(1)
                self.speed_var.set("Speed: Done")
                self.eta_var.set("ETA: 0s")
        self.after(0, update)

    def _on_download_complete(self, result):
        """Handle download completion."""
        self._is_downloading = False
        self.download_btn.configure(state="normal", text="🚀 Download")

        if result.success:
            self._log(f"✅ Download completed: {result.output_path}")
            messagebox.showinfo("Success", f"Download completed!\nSaved to: {result.output_path}")
        else:
            self._log(f"❌ Download failed: {result.error}")
            messagebox.showerror("Error", f"Download failed: {result.error}")

    def _on_download_error(self, error: str):
        """Handle download error."""
        self._is_downloading = False
        self.download_btn.configure(state="normal", text="🚀 Download")
        self._log(f"❌ Error: {error}")
        messagebox.showerror("Error", f"Download error: {error}")

    def _log(self, message: str):
        """Add message to log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")

    def _clear_log(self):
        """Clear log."""
        self.log_text.delete("1.0", "end")