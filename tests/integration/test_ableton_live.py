"""Integration тесты с реальным Ableton Live.

Запуск: pytest tests/integration/ -m integration -v
Требует: запущенный Ableton Live с AbletonOSC.
"""

import pytest

from ableton_mcp.ableton.client import AbletonClient


@pytest.fixture
def ableton():
    """Клиент подключённый к реальному Ableton."""
    client = AbletonClient()
    client.connect()
    yield client
    client.disconnect()


@pytest.mark.integration
def test_ping(ableton):
    """Проверка связи с Ableton."""
    assert ableton.ping() is True


@pytest.mark.integration
def test_get_tempo(ableton):
    """Получение текущего темпа."""
    tempo = ableton.get_tempo()
    assert 20.0 <= tempo <= 999.0


@pytest.mark.integration
def test_set_and_get_tempo(ableton):
    """Установка и проверка темпа."""
    original = ableton.get_tempo()

    ableton.set_tempo(142.0)
    import time
    time.sleep(0.1)
    new_tempo = ableton.get_tempo()
    assert abs(new_tempo - 142.0) < 0.1

    # Вернуть оригинальный темп
    ableton.set_tempo(original)


@pytest.mark.integration
def test_is_playing(ableton):
    """Проверка статуса воспроизведения."""
    result = ableton.is_playing()
    assert isinstance(result, bool)
