# AI Agent for Ableton Live

![Version](https://img.shields.io/badge/version-2.0-blue.svg) ![Ableton Live](https://img.shields.io/badge/Ableton%20Live-11%20Suite-orange.svg) ![Python](https://img.shields.io/badge/python-3.7+-green.svg)

Link for API description: https://docs.cycling74.com/legacy/max8/vignettes/max_for_live_topic

**Полнофункциональный AI-агент для автоматизации Ableton Live 11** через кастомный Control Surface скрипт с HTTP API.

## 🎯 Возможности

### 🎛️ **Управление проектом**

- ▶️ **Воспроизведение и остановка**
- 🎵 **Изменение темпа** в реальном времени
- 📊 **Получение состояния проекта** (треки, темп, статус)

### 🎹 **Создание контента**

- 🎼 **Создание MIDI треков** с настройкой arm-статуса
- 📝 **Создание MIDI клипов** произвольной длительности
- 🥁 **Программирование ударных паттернов**
- 🎵 **Автоматическое создание Amen Break** (классический jungle/dnb паттерн)
- 🌿 **Jungle Sound Processing** - автоматическая настройка jungle звука
- 🎚️ **Pitch Variations** - создание вариаций с разным pitch'ем
- 🎛️ **Device Control** - управление эффектами и их параметрами

### 🔗 **Интеграция**

- 🌐 **HTTP REST API** для внешнего управления
- 🔌 **UDP связь** с минимальной задержкой
- 🤖 **AI-готовая архитектура** для интеграции с LLM

## Быстрый старт

Для установки, настройки и запуска всех компонентов достаточно выполнить одну команду в терминале:

```bash
./start.sh
```

Скрипт `start.sh` сделает следующее:

1.  **Установит зависимости**: Запустит `pip install -r requirements.txt`.
2.  **Скопирует скрипт**: Выполнит `python setup.py` для копирования папки `MyAgent` в директорию Ableton.
3.  **Запустит мост**: Запустит сервер `python bridge.py`, который необходим для связи с агентом.

## Что делать после запуска скрипта

1.  **Перезапустите Ableton Live**.
2.  Откройте `Preferences → Link/MIDI`.
3.  В одном из свободных слотов `Control Surface` выберите `MyAgent`.

После этого всё готово к работе. Агент сможет отправлять команды в Ableton Live.

## Ручная установка

Если вы предпочитаете делать всё вручную:

1.  **Установите зависимости**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Скопируйте скрипт**:
    Запустите `python setup.py` или скопируйте папку `MyAgent` вручную `/Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/`.
3.  **Запустите мост**:
    ```bash
    python bridge.py
    ```
4.  **Настройте Ableton Live**, как описано выше.

## 🚀 Примеры использования

### 📊 Получение состояния проекта

```bash
curl -X GET http://127.0.0.1:8787/state
```

### ▶️ Управление воспроизведением

```bash
# Запуск
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "play"}'

# Остановка
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "stop"}'
```

### 🎵 Изменение темпа

```bash
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "set_tempo", "args": {"bpm": 140}}'
```

### 🎹 Создание MIDI трека

```bash
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "create_midi_track", "args": {"name": "My Track", "arm": true}}'
```

### 🥁 Создание Amen Break

Для быстрого создания классического jungle/dnb паттерна:

```bash
# 1. Создать MIDI клип
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "create_midi_clip", "args": {"track": "1 808", "slot": 0, "bars": 4, "loop": true}}'

# 2. Использовать готовый скрипт
python create_amen_break.py

# 3. Применить jungle обработку
python jungle_processor.py
```

## 🛠️ API Endpoints

### `GET /state`

Возвращает текущее состояние проекта:

```json
{
  "ok": true,
  "state": {
    "tempo": 128.0,
    "is_playing": false,
    "tracks": [{ "name": "1 808", "is_armed": true }]
  }
}
```

### `POST /cmd`

Отправка команд в Ableton Live:

**Доступные команды:**

- `play` - запуск воспроизведения
- `stop` - остановка воспроизведения
- `set_tempo` - изменение темпа (`args.bpm`)
- `create_midi_track` - создание MIDI трека (`args.name`, `args.arm`)
- `create_midi_clip` - создание MIDI клипа (`args.track`, `args.slot`, `args.bars`, `args.loop`)
- `set_clip_notes` - программирование нот (`args.track`, `args.slot`, `args.notes`)
- `add_notes` - добавление нот (`args.track`, `args.slot`, `args.notes`)
- `launch_clip` - запуск клипа (`args.track`, `args.slot`)
- `get_track_devices` - получение списка устройств трека (`args.track`)
- `get_device_parameters` - получение параметров устройства (`args.track`, `args.device_index`)
- `set_device_parameter` - изменение параметра устройства (`args.track`, `args.device_index`, `args.param_index`, `args.value`)
- `set_clip_pitch` - изменение pitch клипа (`args.track`, `args.slot`, `args.pitch_coarse`, `args.pitch_fine`)## 🎼 Готовые инструменты

### 🥁 Amen Break Generator (`create_amen_break.py`)

Автоматически создает классический Amen Break паттерн:

- **2 бара** аутентичного ритма
- **49 нот** детального программирования
- **Kick, Snare, Hi-hat** с ghost notes
- **Готов для jungle/drum'n'bass**

### 🌿 Jungle Processor (`jungle_processor.py`)

Автоматическая настройка jungle/dnb звука:

- **174 BPM** - классический jungle темп
- **Pitch variations** - 5 вариаций Amen Break
- **Effects chain** - рекомендации по обработке
- **Jungle sound guide** - детальные настройки EQ, компрессора, реверба

### 🔍 Device Analyzer (`device_analyzer.py`)

Анализ доступных устройств и их параметров:

- **Сканирование устройств** на треке
- **Анализ параметров** каждого эффекта
- **Рекомендации** по порядку устройств для jungle

### 🎛️ Jungle Auto-Tuner (`jungle_auto_tuner.py`)

Автоматическая настройка эффектов для jungle звука:

- **EQ Eight** - high-pass, boost высоких, cut средних
- **Compressor** - punch настройки (-18dB, 4:1, 1ms attack)
- **Saturator** - analog warmth (5dB drive)
- **Reverb** - атмосферные настройки (20% room, 1.5s decay)

### 🧪 API Tester (`test_api.py`)

Комплексное тестирование всех функций:

- Проверка связи с Ableton
- Тестирование всех команд API
- Автоматическая валидация ответов

## 📁 Структура проекта```

├── MyAgent/ # Control Surface скрипт для Ableton
│ └── **init**.py # Основной код агента с device control API
├── bridge.py # HTTP-UDP мост
├── setup.py # Установщик скрипта в Ableton
├── test_api.py # Тестер API функций
├── create_amen_break.py # Генератор Amen Break паттерна
├── jungle_processor.py # Jungle sound processor с pitch variations
├── device_analyzer.py # Анализатор устройств и параметров
├── jungle_auto_tuner.py # Автонастройка эффектов для jungle
├── start.sh # Автоматический запуск
└── requirements.txt # Python зависимости

```

## 🏗️ Архитектура

```

Внешний мир → HTTP (8787) → bridge.py → UDP (8788) → MyAgent → Ableton Live
Внешний мир ← HTTP (8787) ← bridge.py ← UDP (8789) ← MyAgent ← Ableton Live

```

**Компоненты:**

- **MyAgent**: Control Surface скрипт внутри Ableton Live
- **bridge.py**: Flask HTTP сервер + UDP клиент/сервер
- **HTTP API**: Внешний интерфейс на порту 8787
- **UDP сокеты**: Быстрая связь с Ableton (8788/8789)

## 🔧 Технические детали

### Требования

- **Ableton Live 11 Suite** (macOS/Windows)
- **Python 3.7+** с Flask
- **Права доступа** для копирования в системную папку Ableton

### Установка скрипта

Скрипт устанавливается в системную папку Ableton:

```

/Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/MyAgent/

````

### Особенности реализации

- **"Ленивые" импорты**: Системные модули импортируются внутри функций для совместимости с Ableton
- **Undo steps**: Все изменения проекта оборачиваются в undo шаги
- **Error handling**: Полное логирование в Ableton Log.txt
- **Thread safety**: UDP сервер работает в отдельном потоке

## 🤖 Интеграция с AI

Проект готов для интеграции с Large Language Models (LLM):

### Примеры AI команд

```python
# AI может автоматически создавать музыкальные паттерны
def create_drum_pattern(style="jungle", bpm=174):
    if style == "jungle":
        return create_amen_break()
    elif style == "trap":
        return create_trap_pattern()
    # ... другие стили
````

### Расширение функционала

Добавьте новые команды в `MyAgent/__init__.py`:

```python
def _action_create_melody(self, notes, track, scale="C major"):
    """Создание мелодии по заданной гамме"""
    # Ваш код здесь
```

## 📈 Roadmap

- [ ] **Поддержка аудио клипов** (не только MIDI)
- [ ] **Управление эффектами** и параметрами инструментов
- [ ] **Автоматизация** (envelope automation)
- [ ] **Session view** управление (сцены, группы)
- [ ] **Экспорт проектов** и stems
- [ ] **Интеграция с внешними синтезаторами**
- [ ] **AI композиция** на основе музыкальной теории
- [ ] **Генерация вариаций** существующих паттернов

## 🤝 Участие в разработке

1. **Fork** репозиторий
2. Создайте **feature branch**
3. Добавьте **тесты** для новой функциональности
4. Отправьте **Pull Request**

### Добавление новых команд

```python
# В MyAgent/__init__.py
def _action_your_command(self, param1, param2):
    """Ваша новая команда"""
    try:
        self.song.begin_undo_step()
        # Логика команды
        log.info("MyAgent: Your command executed")
    except Exception as e:
        log.error("MyAgent: Error in your_command: %s", e)
    finally:
        self.song.end_undo_step()
```

## 🐛 Troubleshooting

### Проблемы с установкой

- Убедитесь, что у вас есть права на запись в папку Ableton
- Проверьте правильность пути к Ableton Live 11 Suite

### API не отвечает

- Убедитесь, что bridge.py запущен
- Проверьте, что MyAgent выбран в настройках Ableton
- Посмотрите логи в терминале bridge.py

### Команды не выполняются

- Проверьте Ableton Log.txt для ошибок MyAgent
- Убедитесь, что имена треков корректны
- Проверьте формат отправляемых команд

---

**Создано для музыкантов, продюсеров и AI-разработчиков** 🎵🤖
