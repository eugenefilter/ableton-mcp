"""Тесты OSC клиента (mock, без реального Ableton)."""

from unittest.mock import MagicMock, patch

import pytest

from ableton_mcp.ableton.client import AbletonClient
from ableton_mcp.exceptions import AbletonConnectionError


@pytest.fixture
def client():
    """Клиент с замоканным OSC."""
    c = AbletonClient(host="127.0.0.1", port_out=11000, port_in=11001, timeout=0.5)
    c._client = MagicMock()
    c._connected = True
    return c


class TestConnection:
    def test_not_connected_by_default(self):
        c = AbletonClient()
        assert c.connected is False

    def test_send_without_connect_raises(self):
        c = AbletonClient()
        with pytest.raises(AbletonConnectionError):
            c.send("/live/test")

    def test_query_without_connect_raises(self):
        c = AbletonClient()
        with pytest.raises(AbletonConnectionError):
            c.query("/live/test")

    def test_disconnect(self, client):
        client.disconnect()
        assert client.connected is False


class TestSend:
    def test_send_message(self, client):
        client.send("/live/song/start_playing")
        client._client.send_message.assert_called_once_with("/live/song/start_playing", [])

    def test_send_with_args(self, client):
        client.send("/live/song/set/tempo", 140.0)
        client._client.send_message.assert_called_once_with(
            "/live/song/set/tempo", [140.0]
        )


class TestQuery:
    def test_query_timeout(self, client):
        """Таймаут если Ableton не отвечает."""
        with pytest.raises(AbletonConnectionError, match="Таймаут"):
            client.query("/live/song/get/tempo")

    def test_query_with_response(self, client):
        """Успешный запрос с ответом."""

        def fake_send(address, args):
            # Симулируем ответ от Ableton
            client._handle_response(address, 140.0)

        client._client.send_message.side_effect = fake_send
        result = client.query("/live/song/get/tempo")
        assert result == [140.0]


class TestTransport:
    def test_set_tempo(self, client):
        client.set_tempo(145.0)
        client._client.send_message.assert_called_once_with(
            "/live/song/set/tempo", [145.0]
        )

    def test_get_tempo(self, client):
        def fake_send(address, args):
            client._handle_response(address, 140.0)

        client._client.send_message.side_effect = fake_send
        assert client.get_tempo() == 140.0

    def test_is_playing(self, client):
        def fake_send(address, args):
            client._handle_response(address, True)

        client._client.send_message.side_effect = fake_send
        assert client.is_playing() is True

    def test_start_playing(self, client):
        client.start_playing()
        client._client.send_message.assert_called_once_with(
            "/live/song/start_playing", []
        )

    def test_stop_playing(self, client):
        client.stop_playing()
        client._client.send_message.assert_called_once_with(
            "/live/song/stop_playing", []
        )

    def test_ping_success(self, client):
        def fake_send(address, args):
            client._handle_response(address, "ok")

        client._client.send_message.side_effect = fake_send
        assert client.ping() is True

    def test_ping_timeout(self, client):
        """Ping возвращает False при таймауте."""
        assert client.ping() is False
