"""OSC клиент для связи с Ableton Live через AbletonOSC."""

import threading
import time
from typing import Any, List, Optional

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from ableton_mcp.exceptions import AbletonConnectionError
from ableton_mcp.utils.config import get_config
from ableton_mcp.utils.logger import setup_logger

logger = setup_logger(__name__)


class AbletonClient:
    """OSC клиент для управления Ableton Live.

    Отправляет OSC сообщения на AbletonOSC (порт 11000)
    и принимает ответы (порт 11001).

    Args:
        host: IP адрес Ableton (по умолчанию из конфига).
        port_out: Порт отправки (AbletonOSC слушает).
        port_in: Порт приёма (наш сервер слушает).
        timeout: Таймаут ожидания ответа в секундах.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port_out: Optional[int] = None,
        port_in: Optional[int] = None,
        timeout: float = 2.0,
    ):
        config = get_config()
        self._host = host or config.osc_host
        self._port_out = port_out or config.osc_port_out
        self._port_in = port_in or config.osc_port_in
        self._timeout = timeout

        self._client: Optional[SimpleUDPClient] = None
        self._server: Optional[BlockingOSCUDPServer] = None
        self._server_thread: Optional[threading.Thread] = None

        self._response: Optional[List[Any]] = None
        self._response_event = threading.Event()
        self._response_address: Optional[str] = None
        self._lock = threading.Lock()

        self._connected = False

    @property
    def connected(self) -> bool:
        """Статус подключения."""
        return self._connected

    def connect(self) -> None:
        """Установить соединение с Ableton.

        Создаёт UDP клиент для отправки и OSC сервер для приёма ответов.

        Raises:
            AbletonConnectionError: Если не удалось подключиться.
        """
        try:
            self._client = SimpleUDPClient(self._host, self._port_out)

            dispatcher = Dispatcher()
            dispatcher.set_default_handler(self._handle_response)

            self._server = BlockingOSCUDPServer(
                (self._host, self._port_in), dispatcher
            )
            self._server_thread = threading.Thread(
                target=self._server.serve_forever, daemon=True
            )
            self._server_thread.start()

            self._connected = True
            logger.info(
                "Подключено к Ableton",
                extra={"host": self._host, "port_out": self._port_out, "port_in": self._port_in},
            )
        except Exception as e:
            self._connected = False
            raise AbletonConnectionError(f"Не удалось подключиться к Ableton: {e}") from e

    def disconnect(self) -> None:
        """Закрыть соединение."""
        if self._server:
            self._server.shutdown()
            self._server = None
        self._server_thread = None
        self._client = None
        self._connected = False
        logger.info("Отключено от Ableton")

    def send(self, address: str, *args: Any) -> None:
        """Отправить OSC сообщение без ожидания ответа.

        Args:
            address: OSC адрес (например, "/live/song/start_playing").
            *args: Аргументы сообщения.

        Raises:
            AbletonConnectionError: Если не подключен.
        """
        if not self._connected or not self._client:
            raise AbletonConnectionError("Не подключен к Ableton")

        logger.debug("OSC send: %s %s", address, args)
        self._client.send_message(address, list(args) if args else [])

    def query(self, address: str, *args: Any) -> List[Any]:
        """Отправить OSC запрос и дождаться ответа.

        Args:
            address: OSC адрес запроса (например, "/live/song/get/tempo").
            *args: Аргументы запроса.

        Returns:
            Список значений из ответа.

        Raises:
            AbletonConnectionError: Если не подключен или таймаут ответа.
        """
        if not self._connected or not self._client:
            raise AbletonConnectionError("Не подключен к Ableton")

        with self._lock:
            self._response = None
            self._response_event.clear()
            self._response_address = address

            self._client.send_message(address, list(args) if args else [])
            logger.debug("OSC query: %s %s", address, args)

            if not self._response_event.wait(timeout=self._timeout):
                raise AbletonConnectionError(
                    f"Таймаут ожидания ответа от Ableton: {address} ({self._timeout}s)"
                )

            result = self._response if self._response is not None else []
            self._response = None
            return result

    def _handle_response(self, address: str, *args: Any) -> None:
        """Обработчик входящих OSC сообщений.

        Args:
            address: OSC адрес ответа.
            *args: Данные ответа.
        """
        logger.debug("OSC recv: %s %s", address, args)
        self._response = list(args)
        self._response_event.set()

    # --- Transport ---

    def ping(self) -> bool:
        """Проверить связь с Ableton.

        Returns:
            True если Ableton отвечает.
        """
        try:
            self.query("/live/test")
            return True
        except AbletonConnectionError:
            return False

    def get_tempo(self) -> float:
        """Получить текущий темп.

        Returns:
            Темп в BPM.
        """
        result = self.query("/live/song/get/tempo")
        return float(result[0])

    def set_tempo(self, bpm: float) -> None:
        """Установить темп.

        Args:
            bpm: Темп в BPM (60-200).
        """
        self.send("/live/song/set/tempo", float(bpm))

    def is_playing(self) -> bool:
        """Проверить играет ли Ableton.

        Returns:
            True если воспроизведение активно.
        """
        result = self.query("/live/song/get/is_playing")
        return bool(result[0])

    def start_playing(self) -> None:
        """Начать воспроизведение."""
        self.send("/live/song/start_playing")

    def stop_playing(self) -> None:
        """Остановить воспроизведение."""
        self.send("/live/song/stop_playing")
