# ИНСТРУКЦИЯ ДЛЯ AI АГЕНТА: РАЗРАБОТКА ABLETON MCP СЕРВЕРА

## 📋 ОБЗОР ПРОЕКТА

Создать MCP (Model Context Protocol) сервер для управления Ableton Live через AbletonOSC,
с фокусом на автоматическую генерацию музыкальных треков (особенно goa trance / psytrance / DNB / Braeks).

---

## 📚 1. ДОКУМЕНТАЦИЯ И РЕСУРСЫ

### 1.1 MCP Protocol

- **Официальная спецификация MCP:** https://spec.modelcontextprotocol.io/
- **MCP SDK Python:** https://github.com/modelcontextprotocol/python-sdk
- **Примеры MCP серверов:** https://github.com/modelcontextprotocol/servers
- **MCP документация:** https://modelcontextprotocol.io/docs

### 1.2 Ableton Live API

- **Live Object Model (LOM):** https://docs.cycling74.com/max8/vignettes/live_object_model
- **Live API Overview:** https://docs.cycling74.com/max8/vignettes/live_api_overview
- **Unofficial API docs:** https://nsuspray.github.io/Live_API_Doc/
- **Max for Live API:** https://help.ableton.com/hc/en-us/articles/5402681764242-Controlling-Live-using-Max-for-Live

### 1.3 AbletonOSC

- **AbletonOSC GitHub:** https://github.com/ideoforms/AbletonOSC
- **AbletonOSC API Reference:** https://github.com/ideoforms/AbletonOSC#api-reference
- **AbletonOSC Paper (NIME 2023):** https://nime.org/proceedings/2023/nime2023_60.pdf
- **PyLive (Python wrapper):** https://github.com/ideoforms/pylive

### 1.4 Существующие решения для изучения

- **AbletonMCP (reference):** https://lobehub.com/mcp/fabian-tinkl-abletonmcp
- **Controlling Ableton with Python:** https://sangarshanan.com/2025/02/25/connecting-python-with-ableton/

### 1.5 Музыкальная теория и генерация

- **Music21 (theory library):** https://web.mit.edu/music21/
- **Magenta (Google AI music):** https://magenta.tensorflow.org/
- **Mido (MIDI library):** https://mido.readthedocs.io/

---

## 🏗️ 2. АРХИТЕКТУРНЫЕ ПРИНЦИПЫ

### 2.1 SOLID принципы

- **S - Single Responsibility:** Каждый класс/модуль отвечает за одну задачу
- **O - Open/Closed:** Открыт для расширения, закрыт для модификации
- **L - Liskov Substitution:** Подтипы должны быть заменяемы базовыми типами
- **I - Interface Segregation:** Множество специфичных интерфейсов лучше одного общего
- **D - Dependency Inversion:** Зависимость от абстракций, а не конкретных реализаций

### 2.2 KISS (Keep It Simple, Stupid)

- Избегать излишней сложности
- Простые решения предпочтительнее сложных
- Код должен быть понятен без глубокого анализа
- Одна функция = одна задача

### 2.3 DRY (Don't Repeat Yourself)

- Никакого дублирования кода
- Переиспользуемые утилиты и хелперы
- Общая логика вынесена в базовые классы/функции
- Конфигурация в одном месте

---

## 📦 3. МОДУЛЬНАЯ СТРУКТУРА

### 3.1 Требуемая структура проекта

```
ableton-mcp/
├── README.md                      # Документация проекта
├── pyproject.toml                 # Python dependencies (Poetry)
├── requirements.txt               # Альтернативно pip
├── .env.example                   # Пример конфигурации
├── .gitignore
│
├── src/
│   └── ableton_mcp/
│       ├── __init__.py
│       ├── __main__.py           # Entry point
│       │
│       ├── server/               # MCP Server
│       │   ├── __init__.py
│       │   ├── mcp_server.py    # Главный MCP сервер
│       │   ├── tools.py         # MCP tools definitions
│       │   └── prompts.py       # MCP prompts
│       │
│       ├── ableton/              # Ableton интеграция
│       │   ├── __init__.py
│       │   ├── client.py        # OSC client для AbletonOSC
│       │   ├── track.py         # Track management
│       │   ├── clip.py          # Clip management
│       │   ├── device.py        # Device/plugin control
│       │   ├── mixer.py         # Mixing (volume, pan, sends)
│       │   └── transport.py     # Transport controls
│       │
│       ├── generators/           # AI генераторы
│       │   ├── __init__.py
│       │   ├── base.py          # Базовый генератор
│       │   ├── melody.py        # Генерация мелодий
│       │   ├── harmony.py       # Генерация аккордов
│       │   ├── rhythm.py        # Генерация ритмов
│       │   ├── bass.py          # Генерация басслайнов
│       │   └── arrangement.py   # Структура трека
│       │
│       ├── music/                # Музыкальная теория
│       │   ├── __init__.py
│       │   ├── scales.py        # Гаммы и лады
│       │   ├── chords.py        # Аккорды
│       │   ├── patterns.py      # Ритмические паттерны
│       │   └── theory.py        # Музыкальная теория
│       │
│       ├── styles/               # Жанровые шаблоны
│       │   ├── __init__.py
│       │   ├── base.py          # Базовый стиль
│       │   ├── goa_trance.py    # Goa Trance
│       │   ├── psytrance.py     # Psytrance
│       │   └── techno.py        # Techno (опционально)
│       │
│       ├── utils/                # Утилиты
│       │   ├── __init__.py
│       │   ├── config.py        # Конфигурация
│       │   ├── logger.py        # Логирование
│       │   ├── midi.py          # MIDI утилиты
│       │   └── validators.py    # Валидация данных
│       │
│       └── exceptions.py         # Кастомные исключения
│
├── tests/                        # Тесты
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   │
│   ├── unit/                    # Unit тесты
│   │   ├── test_generators.py
│   │   ├── test_music_theory.py
│   │   ├── test_ableton_client.py
│   │   └── test_utils.py
│   │
│   ├── integration/             # Integration тесты
│   │   ├── test_mcp_server.py
│   │   └── test_ableton_integration.py
│   │
│   └── fixtures/                # Тестовые данные
│       ├── midi_samples/
│       └── mock_responses/
│
├── docs/                         # Документация
│   ├── architecture.md          # Архитектура
│   ├── api_reference.md         # API референс
│   ├── user_guide.md           # Руководство пользователя
│   ├── development.md          # Для разработчиков
│   └── examples/               # Примеры использования
│
└── scripts/                     # Вспомогательные скрипты
    ├── install_abletonosc.sh   # Установка AbletonOSC
    └── setup_dev.sh            # Dev окружение
```

### 3.2 Модульность: Ключевые требования

- Каждый модуль должен быть **независим** и **тестируем отдельно**
- Четкие **интерфейсы** между модулями
- Возможность **легко заменить** любой модуль (например, OSC client на MIDI)
- **Плагин-архитектура** для жанровых стилей
- **Dependency Injection** для конфигурации

---

## 📝 4. ДОКУМЕНТАЦИЯ

### 4.1 Документация кода (обязательно!)

#### Python Docstrings (Google Style)

```python
def generate_melody(
    key: str,
    scale: str,
    bars: int,
    style: str = "goa_trance"
) -> List[Note]:
    """
    Генерирует мелодию в заданной тональности и стиле.

    Args:
        key: Тональность (например, "A", "C#", "Bb")
        scale: Лад (например, "minor", "harmonic_minor", "phrygian")
        bars: Количество тактов (обычно 4, 8, 16)
        style: Музыкальный стиль для генерации

    Returns:
        Список MIDI нот с параметрами pitch, start_time, duration, velocity

    Raises:
        ValueError: Если key или scale невалидны
        GenerationError: Если генерация не удалась

    Examples:
        >>> notes = generate_melody("A", "harmonic_minor", 8, "goa_trance")
        >>> len(notes)
        128  # 8 bars * 16 notes per bar

    Note:
        Для goa trance используется быстрая арпеджированная структура
        с характерными скачками октав и психоделическими паттернами.
    """
```

#### Комментарии в коде

```python
# ✅ ХОРОШО: Объясняет ПОЧЕМУ, а не ЧТО
# Используем harmonic minor вместо natural minor для более
# психоделического звучания характерного для goa trance
scale_notes = get_harmonic_minor_scale(root_note)

# ❌ ПЛОХО: Объясняет очевидное
# Получаем ноты гаммы
scale_notes = get_scale_notes(root_note, scale_type)
```

### 4.2 README.md структура

- **Описание проекта**
- **Быстрый старт** (установка за 5 минут)
- **Требования** (Ableton Live 11+, Python 3.10+, AbletonOSC)
- **Примеры использования**
- **Конфигурация**
- **Troubleshooting**
- **Contributing**
- **License**

### 4.3 API Documentation (docs/)

- **Архитектура системы** (диаграммы)
- **Референс всех MCP tools**
- **Примеры промптов** для пользователей
- **Музыкальная теория** (какие алгоритмы используются)
- **Расширение системы** (как добавить новый стиль)

### 4.4 Inline комментарии

```python
# TODO: Добавить поддержку полиритмии для progressive psytrance
# FIXME: Баг с генерацией нот вне диапазона MIDI (0-127)
# NOTE: Этот алгоритм основан на исследовании гармонии в goa trance
# WARNING: Не использовать более 16 bars - может быть медленно
# HACK: Временное решение, нужен рефакторинг
```

---

## 🧪 5. ТЕСТИРОВАНИЕ

### 5.1 Обязательные тесты

#### Unit тесты (pytest)

```python
# tests/unit/test_melody_generator.py

def test_generate_melody_returns_correct_number_of_notes():
    """Проверяет что генератор возвращает правильное количество нот."""
    generator = MelodyGenerator()
    notes = generator.generate(key="A", scale="minor", bars=4)

    # Для goa trance: 16 нот на такт
    assert len(notes) == 4 * 16

def test_generate_melody_notes_in_scale():
    """Проверяет что все ноты принадлежат заданной гамме."""
    generator = MelodyGenerator()
    notes = generator.generate(key="A", scale="minor", bars=2)

    valid_pitches = get_scale_pitches("A", "minor")
    for note in notes:
        assert note.pitch % 12 in valid_pitches

def test_generate_melody_with_invalid_key_raises_error():
    """Проверяет выброс исключения при невалидной тональности."""
    generator = MelodyGenerator()

    with pytest.raises(ValueError, match="Invalid key"):
        generator.generate(key="X", scale="minor", bars=4)
```

#### Integration тесты

```python
# tests/integration/test_ableton_integration.py

@pytest.mark.integration
def test_create_track_and_add_clip(ableton_client):
    """Тест создания трека и клипа в реальном Ableton."""
    # Создать MIDI трек
    track_id = ableton_client.create_midi_track(name="Test Track")

    # Создать клип
    clip_id = ableton_client.create_clip(track_id, slot=0, length=4)

    # Добавить ноты
    notes = [{"pitch": 60, "start": 0.0, "duration": 0.5, "velocity": 100}]
    ableton_client.add_notes_to_clip(track_id, clip_id, notes)

    # Проверить что клип существует
    clip_info = ableton_client.get_clip_info(track_id, clip_id)
    assert clip_info["length"] == 4.0
```

#### Mock тесты (для OSC без Ableton)

```python
# tests/unit/test_ableton_client_mock.py

@pytest.fixture
def mock_osc_client(mocker):
    """Mock OSC клиента для тестов без реального Ableton."""
    return mocker.patch('pythonosc.udp_client.SimpleUDPClient')

def test_set_tempo_sends_correct_osc_message(mock_osc_client):
    """Проверяет что set_tempo отправляет правильное OSC сообщение."""
    client = AbletonClient()
    client.set_tempo(140)

    mock_osc_client.send_message.assert_called_once_with(
        "/live/song/set/tempo",
        [140]
    )
```

### 5.2 Coverage требования

- **Минимум 80% coverage** для всего кода
- **90%+ coverage** для критичных модулей (generators, ableton client)
- Использовать `pytest-cov`:
  ```bash
  pytest --cov=src/ableton_mcp --cov-report=html --cov-report=term
  ```

### 5.3 CI/CD тесты

- Автоматический запуск тестов на каждый commit
- Pre-commit hooks для линтеров
- GitHub Actions / GitLab CI конфигурация

---

## 🎨 6. CODE QUALITY & STYLE

### 6.1 Линтеры и форматтеры (обязательно!)

#### Black (форматирование)

```bash
black src/ tests/ --line-length 100
```

#### isort (сортировка импортов)

```bash
isort src/ tests/ --profile black
```

#### flake8 (линтинг)

```bash
flake8 src/ tests/ --max-line-length 100
```

#### mypy (type checking)

```python
# Все функции должны иметь type hints!
def create_track(
    name: str,
    color: int = 0,
    position: int = -1
) -> TrackId:
    ...
```

#### pylint (дополнительный линтинг)

```bash
pylint src/ableton_mcp --rcfile=.pylintrc
```

### 6.2 Type Hints (строго обязательно!)

```python
from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class Note:
    """MIDI нота."""
    pitch: int          # 0-127
    start_time: float   # В долях такта
    duration: float     # В долях такта
    velocity: int       # 0-127

    def __post_init__(self):
        """Валидация после инициализации."""
        if not 0 <= self.pitch <= 127:
            raise ValueError(f"Invalid pitch: {self.pitch}")
        if not 0 <= self.velocity <= 127:
            raise ValueError(f"Invalid velocity: {self.velocity}")
```

### 6.3 Error Handling

```python
# Кастомные исключения
class AbletonMCPError(Exception):
    """Базовое исключение для всех ошибок MCP сервера."""
    pass

class AbletonConnectionError(AbletonMCPError):
    """Ошибка подключения к Ableton."""
    pass

class GenerationError(AbletonMCPError):
    """Ошибка генерации музыкального контента."""
    pass

# Использование
try:
    client.connect()
except AbletonConnectionError as e:
    logger.error(f"Failed to connect to Ableton: {e}")
    # Graceful degradation или retry logic
```

---

## ⚙️ 7. КОНФИГУРАЦИЯ И НАСТРОЙКИ

### 7.1 Конфигурационный файл

```python
# src/ableton_mcp/utils/config.py

from pydantic import BaseSettings, Field

class AbletonMCPConfig(BaseSettings):
    """Конфигурация MCP сервера."""

    # Ableton OSC
    osc_host: str = Field(default="127.0.0.1", env="ABLETON_OSC_HOST")
    osc_port_out: int = Field(default=11000, env="ABLETON_OSC_PORT_OUT")
    osc_port_in: int = Field(default=11001, env="ABLETON_OSC_PORT_IN")

    # MCP Server
    mcp_name: str = Field(default="ableton-mcp", env="MCP_NAME")
    mcp_version: str = Field(default="1.0.0", env="MCP_VERSION")

    # Music Generation
    default_tempo: int = Field(default=140, ge=60, le=200)
    default_key: str = Field(default="A")
    default_scale: str = Field(default="harmonic_minor")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

### 7.2 Environment Variables

```bash
# .env.example
ABLETON_OSC_HOST=127.0.0.1
ABLETON_OSC_PORT_OUT=11000
ABLETON_OSC_PORT_IN=11001
LOG_LEVEL=INFO
DEFAULT_TEMPO=140
```

---

## 📊 8. ЛОГИРОВАНИЕ

### 8.1 Structured Logging

```python
import logging
from pythonjsonlogger import jsonlogger

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Настройка структурированного логирования."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Использование
logger = setup_logger(__name__)
logger.info("Track created", extra={
    "track_id": 0,
    "track_name": "Kick",
    "tempo": 140
})
```

### 8.2 Уровни логирования

- **DEBUG:** Детальная отладочная информация
- **INFO:** Важные события (создание трека, генерация паттерна)
- **WARNING:** Неожиданные ситуации, но работа продолжается
- **ERROR:** Ошибки, которые нужно исправить
- **CRITICAL:** Критические ошибки, останавливающие работу

---

## 🔐 9. БЕЗОПАСНОСТЬ

### 9.1 Input Validation

```python
from pydantic import BaseModel, validator, Field

class CreateTrackRequest(BaseModel):
    """Запрос на создание трека."""
    name: str = Field(..., min_length=1, max_length=100)
    color: int = Field(default=0, ge=0, le=69)  # Ableton имеет 70 цветов

    @validator('name')
    def validate_name(cls, v):
        """Валидация имени трека."""
        if not v.strip():
            raise ValueError("Track name cannot be empty")
        # Запретить специальные символы которые могут вызвать проблемы
        forbidden_chars = ['/', '\\', '<', '>', '|', '*', '?']
        if any(char in v for char in forbidden_chars):
            raise ValueError(f"Track name contains forbidden characters")
        return v.strip()
```

### 9.2 Rate Limiting

```python
from functools import wraps
import time

def rate_limit(max_calls: int, time_window: int):
    """Декоратор для ограничения частоты вызовов."""
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Удалить старые вызовы
            calls[:] = [c for c in calls if c > now - time_window]

            if len(calls) >= max_calls:
                raise Exception(f"Rate limit exceeded: {max_calls} calls per {time_window}s")

            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Использование
@rate_limit(max_calls=10, time_window=1)
def generate_melody(...):
    ...
```

---

## 🚀 10. PERFORMANCE & OPTIMIZATION

### 10.1 Кэширование

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_scale_notes(root: str, scale_type: str) -> List[int]:
    """Получить ноты гаммы (с кэшированием)."""
    # Дорогая операция вычисления нот гаммы
    ...
```

### 10.2 Async где возможно

```python
import asyncio
from typing import List

async def generate_multiple_tracks(
    track_configs: List[Dict]
) -> List[Track]:
    """Параллельная генерация нескольких треков."""
    tasks = [
        generate_track_async(config)
        for config in track_configs
    ]
    return await asyncio.gather(*tasks)
```

### 10.3 Профилирование

```python
import cProfile
import pstats

def profile_function(func):
    """Декоратор для профилирования функции."""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Топ 10 медленных функций

        return result
    return wrapper
```

---

## 📋 11. ДОПОЛНИТЕЛЬНЫЕ ТРЕБОВАНИЯ

### 11.1 Versioning

- **Semantic Versioning:** MAJOR.MINOR.PATCH (1.0.0)
- **CHANGELOG.md:** Документировать все изменения
- **Git Tags:** Для каждой версии

### 11.2 Dependencies Management

```toml
# pyproject.toml (Poetry)
[tool.poetry.dependencies]
python = "^3.10"
mcp = "^1.0.0"
pythonosc = "^1.8.0"
pydantic = "^2.0.0"
music21 = "^9.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.0.0"
isort = "^5.12.0"
mypy = "^1.5.0"
```

### 11.3 Git Workflow

- **main/master:** Стабильная версия
- **develop:** Разработка
- **feature/\*:** Новые фичи
- **bugfix/\*:** Исправления
- **Conventional Commits:**
  ```
  feat: добавить генератор goa trance мелодий
  fix: исправить баг с MIDI нотами вне диапазона
  docs: обновить README с примерами
  test: добавить тесты для rhythm generator
  ```

### 11.4 Code Review Checklist

- [ ] Код следует SOLID, KISS, DRY
- [ ] Все функции имеют type hints
- [ ] Docstrings для всех публичных API
- [ ] Тесты написаны и проходят (coverage >80%)
- [ ] Линтеры пройдены (black, isort, flake8, mypy)
- [ ] Документация обновлена
- [ ] Нет TODO/FIXME в production коде
- [ ] Error handling реализован корректно
- [ ] Логирование добавлено для важных операций

### 11.5 Мониторинг и метрики

```python
from prometheus_client import Counter, Histogram
import time

# Метрики
tracks_created = Counter(
    'ableton_tracks_created_total',
    'Total number of tracks created'
)

generation_duration = Histogram(
    'generation_duration_seconds',
    'Time spent generating music'
)

# Использование
def generate_track(...):
    start_time = time.time()

    try:
        # Генерация
        ...
        tracks_created.inc()
    finally:
        duration = time.time() - start_time
        generation_duration.observe(duration)
```

### 11.6 Graceful Degradation

```python
class AbletonClient:
    def __init__(self):
        self._connected = False
        self._offline_mode = False

    def send_message(self, address: str, args):
        """Отправить OSC сообщение с graceful degradation."""
        if not self._connected:
            if self._offline_mode:
                logger.warning(
                    "Offline mode: skipping OSC message",
                    extra={"address": address}
                )
                return
            else:
                raise AbletonConnectionError("Not connected to Ableton")

        try:
            self.osc_client.send_message(address, args)
        except Exception as e:
            logger.error(f"Failed to send OSC: {e}")
            # Попытка переподключения
            self._reconnect()
```

### 11.7 Extensibility

```python
# Plugin система для жанров
from abc import ABC, abstractmethod

class StylePlugin(ABC):
    """Базовый класс для жанровых плагинов."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Имя стиля."""
        pass

    @property
    @abstractmethod
    def default_tempo(self) -> int:
        """Темп по умолчанию."""
        pass

    @abstractmethod
    def generate_melody(self, **kwargs) -> List[Note]:
        """Генерация мелодии в данном стиле."""
        pass

# Регистрация плагинов
class StyleRegistry:
    """Реестр жанровых плагинов."""

    _styles: Dict[str, StylePlugin] = {}

    @classmethod
    def register(cls, style: StylePlugin):
        """Регистрация нового стиля."""
        cls._styles[style.name] = style

    @classmethod
    def get(cls, name: str) -> StylePlugin:
        """Получить стиль по имени."""
        if name not in cls._styles:
            raise ValueError(f"Unknown style: {name}")
        return cls._styles[name]
```

---

## 🎯 12. КРИТЕРИИ УСПЕШНОЙ РАЗРАБОТКИ

### AI Агент должен создать систему, которая:

1. ✅ **Работает из коробки** - установка и запуск за 5 минут
2. ✅ **Хорошо документирована** - любой разработчик может разобраться
3. ✅ **Легко расширяется** - добавление нового жанра = 1 новый файл
4. ✅ **Надежна** - обработка всех ошибок, graceful degradation
5. ✅ **Тестируема** - >80% coverage, CI/CD настроен
6. ✅ **Поддерживаема** - чистый код, следование best practices
7. ✅ **Производительна** - генерация трека <5 секунд
8. ✅ **Безопасна** - валидация входных данных, rate limiting

---

## 📞 13. ФИНАЛЬНЫЙ ЧЕКЛИСТ ДЛЯ AI АГЕНТА

Перед завершением разработки, убедись что:

- [ ] Все модули следуют SOLID принципам
- [ ] Нет повторяющегося кода (DRY)
- [ ] Код простой и понятный (KISS)
- [ ] Все публичные API имеют docstrings
- [ ] Type hints везде где возможно
- [ ] Тесты написаны (unit + integration)
- [ ] Coverage >80%
- [ ] Все линтеры пройдены
- [ ] README.md содержит quick start
- [ ] docs/ содержит полную документацию
- [ ] Примеры использования работают
- [ ] Error handling реализован
- [ ] Логирование настроено
- [ ] Конфигурация через .env
- [ ] Git commits следуют Conventional Commits
- [ ] CHANGELOG.md актуален
- [ ] Код ревью пройден

---

## 🎵 14. СПЕЦИФИЧНЫЕ ТРЕБОВАНИЯ ДЛЯ GOA TRANCE ГЕНЕРАЦИИ

### 14.1 Музыкальные особенности Goa Trance

```python
# src/ableton_mcp/styles/goa_trance.py

class GoaTranceStyle(StylePlugin):
    """
    Goa Trance специфичные настройки и генераторы.

    Характеристики:
    - Темп: 138-145 BPM (обычно 140)
    - Тональность: Минор (часто harmonic minor, phrygian)
    - Структура: Длинные билды (16-32 bar), психоделические брейки
    - Мелодии: Быстрые арпеджио (16th notes), октавные скачки
    - Басс: Rolling 16th notes, резонансный фильтр
    - Ударные: 4-on-the-floor kick, offbeat bass, busy hi-hats
    """

    # Темповый диапазон
    MIN_TEMPO = 138
    MAX_TEMPO = 145
    DEFAULT_TEMPO = 140

    # Предпочитаемые гаммы
    PREFERRED_SCALES = [
        "harmonic_minor",
        "phrygian_dominant",
        "double_harmonic",
    ]

    # Ритмические паттерны
    KICK_PATTERN = "four_on_floor"
    BASS_PATTERN = "sixteenth_rolling"
    HATS_PATTERN = "sixteenth_offbeat"
```

### 14.2 Специфичные генераторы

- **Psychedelic Lead Generator** - характерные арпеджио
- **Rolling Bass Generator** - непрерывные 16-е
- **Acid Line Generator** - 303-style кислотные линии
- **Build-up Generator** - автоматические билды с фильтрами
- **Breakdown Generator** - атмосферные брейки

---

## 💬 15. ПРИМЕРЫ ПРОМПТОВ ДЛЯ КОНЕЧНЫХ ПОЛЬЗОВАТЕЛЕЙ

Система должна понимать такие промпты:

```
"Создай goa trance трек: kick, bass, lead, pads.
Тональность A minor, 140 BPM, 64 такта"

"Добавь психоделический lead на 5 трек с
арпеджио в harmonic minor"

"Сделай билд-ап с 32 по 48 такт:
открывай фильтр и добавляй энергию"

"Создай breakdown с 48 по 64: ambient pads,
остановить kick и bass"

"Настрой сведение: kick -6dB, bass -8dB,
lead -12dB, reverb на lead 30%"
```

---

## 🔗 16. ИНТЕГРАЦИИ (будущее развитие)

План для расширения:

- [ ] **Spotify API** - анализ референсных треков
- [ ] **Discogs API** - база данных goa trance артистов/альбомов
- [ ] **Freesound API** - загрузка семплов
- [ ] **LANDR/CloudBounce** - автоматический мастеринг
- [ ] **Export to DAW Project** - экспорт в другие DAW

---

ЭТО ПОЛНАЯ ИНСТРУКЦИЯ ДЛЯ AI АГЕНТА.
СЛЕДУЯ ЭТОМУ ДОКУМЕНТУ, АГЕНТ СОЗДАСТ ПРОФЕССИОНАЛЬНЫЙ,
ПОДДЕРЖИВАЕМЫЙ, ТЕСТИРУЕМЫЙ И РАСШИРЯЕМЫЙ MCP СЕРВЕР.
