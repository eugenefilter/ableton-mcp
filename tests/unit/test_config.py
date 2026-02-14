"""Тесты конфигурации."""

from ableton_mcp.utils.config import AbletonMCPConfig


def test_config_defaults():
    """Проверяет значения по умолчанию."""
    config = AbletonMCPConfig()

    assert config.osc_host == "127.0.0.1"
    assert config.osc_port_out == 11000
    assert config.osc_port_in == 11001
    assert config.default_tempo == 140
    assert config.default_key == "A"
    assert config.default_scale == "harmonic_minor"
    assert config.log_level == "INFO"


def test_config_custom_values():
    """Проверяет установку кастомных значений."""
    config = AbletonMCPConfig(
        osc_host="192.168.1.100",
        osc_port_out=12000,
        default_tempo=145,
        default_key="C",
        default_scale="phrygian",
    )

    assert config.osc_host == "192.168.1.100"
    assert config.osc_port_out == 12000
    assert config.default_tempo == 145
    assert config.default_key == "C"
    assert config.default_scale == "phrygian"
