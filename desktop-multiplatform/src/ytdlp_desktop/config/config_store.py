"""Desktop config store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ytdlp_core.domain.ports import IConfigStore


class DesktopConfigStore(IConfigStore):
    """JSON config store for desktop."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Any] = {}
        self._load()

    def _load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception:
                self._cache = {}

    def _save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._save()

    def get_all(self) -> dict[str, Any]:
        return self._cache.copy()