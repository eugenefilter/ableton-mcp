"""Конфигурация MCP сервера."""

from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class AbletonMCPConfig(BaseSettings):
    """Конфигурация Ableton MCP сервера.

    Читает из .env файла или environment variables.
    """

    # Ableton OSC
    osc_host: str = Field(default="127.0.0.1", alias="ABLETON_OSC_HOST")
    osc_port_out: int = Field(default=11000, alias="ABLETON_OSC_PORT_OUT")
    osc_port_in: int = Field(default=11001, alias="ABLETON_OSC_PORT_IN")

    # MCP Server
    mcp_name: str = Field(default="ableton-mcp")
    mcp_version: str = Field(default="0.1.0")

    # Music Generation
    default_tempo: int = Field(default=140, ge=60, le=200)
    default_key: str = Field(default="A")
    default_scale: str = Field(default="harmonic_minor")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, alias="LOG_FILE")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "populate_by_name": True,
    }


# Singleton конфиг
_config: Optional[AbletonMCPConfig] = None


def get_config() -> AbletonMCPConfig:
    """Получить конфигурацию (singleton)."""
    global _config
    if _config is None:
        _config = AbletonMCPConfig()
    return _config
