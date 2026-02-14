# Ableton MCP Server

MCP (Model Context Protocol) сервер для управления Ableton Live через AbletonOSC.
AI агент (Claude) может создавать треки, генерировать мелодии, управлять микшером — всё через промпты.

## Архитектура

```
Claude (AI) → MCP Protocol → ableton-mcp (Python) → OSC → AbletonOSC → Ableton Live
```

- **MCP** — протокол для подключения AI инструментов к Claude
- **OSC** — протокол обмена сообщениями (UDP, порты 11000/11001)
- **AbletonOSC** — Remote Script внутри Ableton, принимает OSC команды

## Требования

- Python 3.10+
- Ableton Live 11+
- AbletonOSC (Remote Script для Ableton)

## Установка

### 1. Клонировать и установить проект

```bash
git clone git@github.com:eugenefilter/ableton-mcp.git
cd ableton-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Установить AbletonOSC в Ableton

Скачать с https://github.com/ideoforms/AbletonOSC

Скопировать папку `AbletonOSC` в Remote Scripts:
- **Mac:** `~/Music/Ableton/User Library/Remote Scripts/`
- **Windows:** `\Users\[username]\Documents\Ableton\User Library\Remote Scripts\`

Включить в Ableton:
`Preferences → Link, Tempo & MIDI → Control Surface` → выбрать **AbletonOSC**

В статус-баре Ableton появится сообщение что AbletonOSC запущен.

### 3. Конфигурация (опционально)

Скопировать `.env.example` в `.env` и изменить при необходимости:

```bash
cp .env.example .env
```

Значения по умолчанию:
| Параметр | Значение | Описание |
|----------|----------|----------|
| `ABLETON_OSC_HOST` | 127.0.0.1 | IP адрес Ableton |
| `ABLETON_OSC_PORT_OUT` | 11000 | Порт отправки (AbletonOSC слушает) |
| `ABLETON_OSC_PORT_IN` | 11001 | Порт приёма ответов |
| `LOG_LEVEL` | INFO | Уровень логирования |

## Использование

### Проверка связи с Ableton

```python
from ableton_mcp.ableton.client import AbletonClient

client = AbletonClient()
client.connect()

client.ping()              # True — связь есть
client.get_tempo()         # 120.0
client.set_tempo(140)      # Установить 140 BPM
client.is_playing()        # False
client.start_playing()     # Запустить воспроизведение
client.stop_playing()      # Остановить

client.disconnect()
```

### Как работает OSC клиент

`AbletonClient` общается с Ableton через два типа сообщений:

**`send(address, *args)`** — отправить команду без ожидания ответа:
```python
client.send("/live/song/set/tempo", 140.0)
client.send("/live/song/start_playing")
```

**`query(address, *args)`** — отправить запрос и получить ответ (с таймаутом):
```python
result = client.query("/live/song/get/tempo")  # [140.0]
result = client.query("/live/song/get/is_playing")  # [True]
```

Полный список OSC адресов: https://github.com/ideoforms/AbletonOSC

### Основные OSC адреса

#### Transport
| Адрес | Описание |
|-------|----------|
| `/live/song/start_playing` | Начать воспроизведение |
| `/live/song/stop_playing` | Остановить |
| `/live/song/get/tempo` | Получить темп |
| `/live/song/set/tempo <bpm>` | Установить темп |
| `/live/song/get/is_playing` | Играет ли |

#### Треки
| Адрес | Описание |
|-------|----------|
| `/live/song/create_midi_track <index>` | Создать MIDI трек (-1 = в конец) |
| `/live/song/create_audio_track <index>` | Создать Audio трек |
| `/live/song/create_return_track` | Создать Return трек |
| `/live/song/delete_track <index>` | Удалить трек |
| `/live/track/set/name <track_id> <name>` | Назвать трек |
| `/live/track/set/volume <track_id> <level>` | Громкость (0.0-1.0) |
| `/live/track/set/panning <track_id> <pan>` | Панорама (-1.0 ... 1.0) |
| `/live/track/set/mute <track_id> <0\|1>` | Mute |
| `/live/track/set/solo <track_id> <0\|1>` | Solo |
| `/live/track/set/send <track_id> <send_id> <value>` | Send уровень |

#### Клипы
| Адрес | Описание |
|-------|----------|
| `/live/clip_slot/create_clip <track_id> <slot_id> <length>` | Создать MIDI клип (length в долях) |
| `/live/clip_slot/delete_clip <track_id> <slot_id>` | Удалить клип |
| `/live/clip_slot/fire <track_id> <slot_id>` | Запустить клип |
| `/live/clip/stop <track_id> <slot_id>` | Остановить клип |
| `/live/clip/get/name <track_id> <slot_id>` | Имя клипа |
| `/live/clip/set/name <track_id> <slot_id> <name>` | Назвать клип |
| `/live/clip/get/length <track_id> <slot_id>` | Длина клипа |

#### MIDI ноты
| Адрес | Описание |
|-------|----------|
| `/live/clip/add/notes <track_id> <slot_id> <pitch> <start> <duration> <velocity> <mute> ...` | Добавить ноты. Параметры повторяются для каждой ноты. pitch=0-127, start/duration в долях, velocity=0-127, mute=0/1 |
| `/live/clip/get/notes <track_id> <slot_id>` | Получить все ноты |
| `/live/clip/remove/notes <track_id> <slot_id>` | Удалить все ноты |

#### Устройства (Device)
| Адрес | Описание |
|-------|----------|
| `/live/device/get/name <track_id> <device_id>` | Имя устройства |
| `/live/device/get/num_parameters <track_id> <device_id>` | Количество параметров |
| `/live/device/get/parameters/name <track_id> <device_id>` | Имена всех параметров |
| `/live/device/get/parameters/value <track_id> <device_id>` | Значения параметров |
| `/live/device/set/parameter/value <track_id> <device_id> <param_id> <value>` | Установить параметр |

## Структура проекта

```
src/ableton_mcp/
├── __main__.py           # Entry point
├── exceptions.py         # Кастомные исключения
├── server/               # MCP сервер (tools, prompts)
├── ableton/              # OSC клиент и операции с Ableton
│   └── client.py         # AbletonClient — основной класс связи
├── generators/           # AI генераторы (мелодии, ритмы, басс)
├── music/                # Музыкальная теория (гаммы, аккорды)
├── styles/               # Жанровые плагины (goa trance, psytrance)
└── utils/
    ├── config.py         # Конфигурация (Pydantic Settings + .env)
    ├── logger.py         # Логирование
    └── validators.py     # Валидация MIDI/музыкальных параметров
```

## Тесты

```bash
# Все unit тесты (без Ableton)
pytest tests/unit/ -v

# Integration тесты (требуют запущенный Ableton + AbletonOSC)
pytest tests/integration/ -m integration -v

# С coverage
pytest tests/unit/ --cov=src/ableton_mcp --cov-report=term
```

## Текущий статус разработки

Подробный план: [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)

| Этап | Статус |
|------|--------|
| 1. Фундамент (структура, конфиг, утилиты) | ✅ |
| 2. Связь с Ableton (OSC клиент, операции, MCP) | 🔧 В работе |
| 3. Генерация музыки | ⬜ |
| 4. Стили и жанры | ⬜ |
| 5. Полировка | ⬜ |
