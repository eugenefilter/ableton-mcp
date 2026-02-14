"""Тесты исключений."""

from ableton_mcp.exceptions import (
    AbletonConnectionError,
    AbletonMCPError,
    GenerationError,
    MusicValidationError,
)


def test_exception_hierarchy():
    """Все исключения наследуются от AbletonMCPError."""
    assert issubclass(AbletonConnectionError, AbletonMCPError)
    assert issubclass(GenerationError, AbletonMCPError)
    assert issubclass(MusicValidationError, AbletonMCPError)


def test_exception_message():
    """Исключения сохраняют сообщение."""
    err = AbletonConnectionError("Cannot connect to Ableton")
    assert str(err) == "Cannot connect to Ableton"
