"""Кастомные исключения для Ableton MCP."""


class AbletonMCPError(Exception):
    """Базовое исключение для всех ошибок MCP сервера."""

    pass


class AbletonConnectionError(AbletonMCPError):
    """Ошибка подключения к Ableton Live."""

    pass


class GenerationError(AbletonMCPError):
    """Ошибка генерации музыкального контента."""

    pass


class MusicValidationError(AbletonMCPError):
    """Ошибка валидации музыкальных параметров."""

    pass
