"""Dependency injection container."""

from ytdlp_desktop.config.manager import ConfigManager
from ytdlp_desktop.data.services import container


class AppContainer:
    """Application container."""

    def __init__(self):
        self._config_manager: ConfigManager | None = None

    @property
    def config_manager(self) -> ConfigManager:
        if self._config_manager is None:
            self._config_manager = ConfigManager(container.config)
        return self._config_manager

    @property
    def services(self):
        return container


app_container = AppContainer()