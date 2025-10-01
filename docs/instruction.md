# Инструкция для ИИ‑агента управления Ableton Live 11 (через Python Control Surface)

Версия: 1.1 (для Live 11.x). Цель — безопасное управление Live через кастомный Remote Script.
Связь: локальный HTTP/WS/UDP «Бридж» ⇄ Remote Script в Live (Python, API `ableton.v2.*`).

---

## 0) Отличия Live 11 от Live 12

- В кастомных скриптах используйте API **`ableton.v2.control_surface`** (в 12 распространён `ableton.v3`).
- Перезагрузка скриптов: в стабильном Live 11 нет меню Tools→Reload… → перезагружайте, **пере‑выбирая** скрипт в Preferences→Link/MIDI или перезапуская Live. (В некоторых beta‑сборках 11/12 доступен пункт Reload.)
- Python в Live 11 — **Python 3** (не совместим с Python 2‑скриптами из Live 10).

## 1) Роль и цели агента

- Понимать команды пользователя (NLU) и превращать их в атомарные действия Live.
- Работать **только** в пределах помеченных сущностей (`[AGENT]`).
- Запрашивать подтверждение перед «разрушающими» действиями. Вести лог и поддерживать откаты.

## 2) Предпосылки/окружение

- Ableton Live **11.x**. Включён кастомный Control Surface `MyAgent`.
- «Бридж» (локальный сервис) с API:
  - `POST /cmd` — выполнить действие
  - `GET /state` — получить снимок состояния
  - WS `/events` — события и подтверждения
- Соединение локальное (пример): `http://127.0.0.1:8787`.
- В Live подготовлен шаблон сета с треками/рэйками/макросами под агентом.

## 3) Принципы/безопасность

1. **Scope `[AGENT]`**: изменять только треки/клипы/устройства с таким маркером.
   - _Примечание_: Текущая реализация скрипта позволяет выбирать дорожку по любому точному имени, но в целях безопасности агент должен в первую очередь работать с дорожками, помеченными `[AGENT]`.
2. **Dry‑run по умолчанию**: сначала симуляция и дифф, затем — применение.
3. **Guard‑rails**: не трогать Master Gain; темп в разумных пределах; проверять доступность цели.
4. **Атомарность**: сложные задачи → на шаги с валидациями между ними.
5. **Логи/откат**: журнал команд; перед крупными операциями — `Save As`.

## 3.1) Важное замечание по реализации скрипта

Критически важно, чтобы Control Surface скрипт использовал **"ленивые импорты" (lazy imports)**. Системные модули Python, такие как `socket`, `threading`, `json`, должны импортироваться внутри функций, где они используются, а не на верхнем уровне файла. Глобальный импорт этих модулей приводит к тому, что Ableton Live не сможет распознать и загрузить скрипт, и он не появится в списке Control Surfaces.

## 4) Формат команд

Запрос в `POST /cmd`:

```json
{
  "id": "uuid",
  "dry_run": true,
  "action": "<имя-действия>",
  "args": {
    /* параметры */
  },
  "scope": { "track_hint": null }
}
```

Ответ OK:

```json
{
  "id": "...",
  "ok": true,
  "result": {
    /* ... */
  }
}
```

Ответ ошибка:

```json
{
  "id": "...",
  "ok": false,
  "error": { "code": "VALIDATION", "message": "..." }
}
```

## 5) Каталог действий v1.1

В текущей версии `MyAgent` доступны:

### Transport

- `play()`, `stop()`, `locate({ "beats": 0.0 })`, `set_tempo({ "bpm": 160 })`

### Tracks & Scenes

- `select_track({ "name": "Drums [AGENT]" })`
- `arm_track({ "name": "Bass [AGENT]", "arm": true })`
- `launch_scene({ "index": 3 })`
- `create_scene({ "index": 5, "name": "Drop A [AGENT]" })`

### Clips

- `launch_clip({ "track": "Drums [AGENT]", "slot": 1 })`
- `stop_clip({ "track": "Drums [AGENT]", "slot": 1 })`
- `create_midi_clip({ "track": "Drums [AGENT]", "slot": 1, "bars": 8, "loop": true })`
- `set_clip_notes({ "track": "...", "slot": 1, "notes": [ { "p": 36, "s": 0.0, "d": 0.5, "v": 110 } ] })`
- `add_notes({ "track": "...", "slot": 1, "notes": [ { "p": 38, "s": 1.0, "d": 0.5, "v": 90 } ] })` _(добавляет ноты, не удаляя старые)_

- `quantize_clip({ "track": "...", "slot": 1, "grid": "1/16", "amount": 80 })` _(если реализовано в вашей сборке)_

### Tracks

- `create_midi_track({ "name": "3 Bass", "index": 2, "arm": true })` — создаёт MIDI‑дорожку по индексу (0‑based). Если `index` не задан — добавит в конец.

### Devices & Params

- `toggle_device({ "track": "Bass [AGENT]", "device": "Compressor", "on": true })`
- `set_macro({ "track": "Bass [AGENT]", "device": "Bass Rack", "macro": 1, "value": 0.35 })`
- `set_param({ "track": "Pad [AGENT]", "device": "Auto Filter", "param": "Frequency", "value": 3200 })`
- `set_param_by_index({ "track": "...", "device_index": 1, "param_index": 5, "value": 0.5 })` — установка по индексам (надёжно при различии локализаций/имён).

**🎯 КРИТИЧЕСКИ ВАЖНО: Правильные значения параметров (Live Object Model)**

Согласно [LOM документации](https://docs.cycling74.com/apiref/lom/deviceparameter/), параметры устройств принимают **реальные значения**, а не normalized (0.0-1.0):

- **dB параметры**: используйте прямые dB значения (`-5.0`, `3.0`, `-18.0`)
- **Частоты**: используйте Hz значения (`2000`, `10000`, `80`)
- **Проценты**: используйте % значения (`50`, `100`, `15`)
- **Времена**: используйте ms/s значения (`50`, `1.5`, `250`)

**Примеры правильных значений:**

```json
// Saturator
{"param": 1, "value": 5.0}     // Drive: 5dB
{"param": 5, "value": -5.0}    // Base: -5dB
{"param": 3, "value": 2000}    // Frequency: 2000Hz
{"param": 4, "value": 100}     // Width: 100%

// Compressor
{"param": 1, "value": -18.0}   // Threshold: -18dB
{"param": 2, "value": 4.0}     // Ratio: 4:1
{"param": 3, "value": 1.0}     // Attack: 1ms
{"param": 4, "value": 50.0}    // Release: 50ms

// Reverb
{"param": 1, "value": 20}      // Room Size: 20%
{"param": 2, "value": 10}      // Dry/Wet: 10%
```

Примечания по адресации параметров:

- В `set_param`/`toggle_device` можно указывать `device` по имени или `device_index` (0‑based). Если указаны оба — приоритет у `device_index`.
- Для стабильности рекомендуется `set_param_by_index` (`param_index` — 0‑based, см. выдачу `/state`).
- **ВАЖНО**: Используйте реальные значения параметров, а не normalized! Система Live автоматически ограничивает значения диапазоном (min/max).

### Project Utilities

- `save_as({ "suffix": "agent-session" })`, `set_metronome({ "on": true })`, `set_quantization({ "value": "1/16" })`

> Загрузка новых девайсов из Browser — **запрещена**. Используйте преднастроенные рэки/макросы.

## 6) Состояние и события

- `GET /state` возвращает `tempo`, `is_playing`, `tracks[]` и (в v1.1) список устройств и их параметров.

Структура ответа (сокр.):

```jsonc
{
  "ok": true,
  "state": {
    "tempo": 160.0,
    "is_playing": false,
    "tracks": [
      {
        "name": "2 808",
        "is_armed": true,
        "devices": [
          {
            "index": 0,
            "name": "Drum Buss",
            "parameters": [{ "index": 5, "name": "Drive", "value": 30.0 }]
          },
          {
            "index": 1,
            "name": "Saturator",
            "parameters": [{ "index": 2, "name": "Drive", "value": 3.0 }]
          },
          {
            "index": 2,
            "name": "EQ Eight",
            "parameters": [{ "index": 0, "name": "1 Frequency", "value": 35.0 }]
          }
        ]
      }
    ]
  }
}
```

- WS `/events`: `clip_started`, `clip_stopped`, `tempo_changed`, `param_changed`, `error` и др.

## 7) Процедуры (шаблоны)

### 7.1 Старт безопасной сессии

1. `GET /state` → проверка наличия `[AGENT]` треков.
2. `set_tempo` (dry_run) → подтверждение.
3. `save_as` → защищённая копия.
4. Выполнить остальные шаги.

### 7.2 DnB драм‑луп 8 тактов (160 BPM)

1. `set_tempo(160)` (dry_run)
2. `create_midi_clip("Drums [AGENT]", 1, 8, loop=true)`
3. `set_clip_notes(...)` — скелет паттерна (kick/snare/hats)
4. `quantize_clip("1/16", 80)`
5. `launch_clip(...)` или `launch_scene(...)`

### 7.3 Сайдчейн

1. `toggle_device("Bass [AGENT]", "Compressor", true)`
2. `set_param("Bass [AGENT]", "Compressor", "Sidechain", 1)`
3. `set_macro("Bass [AGENT]", "Bass Rack", 2, 0.3)`

### 7.4 DnB‑ударные: шейпинг

1. Добавить на барабанную дорожку: `Drum Buss` → `Saturator` → `EQ Eight`.
2. `set_param_by_index`/`set_param` выставить: Drum Buss (Drive 30, Transients 20, Boom 0), Saturator (Drive +3 dB, Soft Clip On, Dry/Wet 30%).
3. EQ Eight: HP 35 Hz; −3 dB @ 280 Hz; +2 dB @ 9.5 kHz.

## 8) Валидация перед действием

- Синхронизировать `state`.
- Точно матчить имена по `[AGENT]`.
- Проверять диапазоны значений.

Адресация параметров и локализация:

- Имена параметров/устройств зависят от языка интерфейса Live. Для кросс‑локализации используйте индексы (`device_index`, `param_index`).

## 9) Ошибки/ретраи

- Ретраи до 2 раз: 100ms, 300ms.
- Коды: `VALIDATION`, `NOT_FOUND`, `BUSY`, `TIMEOUT`, `LOM_UNAVAILABLE`.

Диагностика TIMEOUT `/state`:

- Проверьте, что Control Surface `MyAgent` выбран (Preferences → Link/MIDI).
- Перезагрузите: снимите/поставьте `MyAgent` или перезапустите Live.
- Смотрите `Log.txt` на строки `MyAgent:` — ошибки в `_action_request_state`/старте UDP.

## 10) Логи и телеметрия

```
ts=2025-08-31T12:00:00Z action=set_tempo bpm=160 ok=true latency_ms=24
```

## 11) Установка/пути (Mac)

- Скрипт: `/Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/MyAgent`
- Включение: Live → Preferences → Link/MIDI → Control Surface: **MyAgent**
- Логи Live: `~/Library/Preferences/Ableton/Live xx.x.x/Log.txt`
- Перезагрузка скрипта: снять/поставить `MyAgent` в Preferences или перезапустить Live.

После обновления скрипта (копирование файлов) перезагрузка обязательна, иначе новые действия не будут доступны.

## 12) Примеры команд

```jsonc
{ "id": "1", "dry_run": false, "action": "set_tempo", "args": { "bpm": 160 } }
{ "id": "2", "dry_run": false, "action": "create_midi_clip", "args": { "track": "Drums [AGENT]", "slot": 1, "bars": 8, "loop": true } }
{ "id": "3", "dry_run": false, "action": "set_clip_notes", "args": { "track": "Drums [AGENT]", "slot": 1, "notes": [ { "p": 36, "s": 0.0, "d": 0.5, "v": 120 } ] } }
{ "id": "4", "dry_run": false, "action": "launch_scene", "args": { "index": 3 } }
{ "id": "5", "dry_run": false, "action": "toggle_device", "args": { "track": "Bass [AGENT]", "device": "Compressor", "on": true } }
{ "id": "6", "dry_run": false, "action": "create_midi_track", "args": { "name": "3 Bass", "index": 2, "arm": true } }
{ "id": "7", "dry_run": false, "action": "set_param_by_index", "args": { "track": "2 808", "device_index": 0, "param_index": 5, "value": 30 } }
```

---

**TL;DR:** Агент отправляет JSON‑команды локальному Бриджу. Бридж транслирует их в Python‑скрипт Control Surface на API `ableton.v2`, который управляет Live 11 через LOM. Работа — только в `[AGENT]`‑скоупе, с dry‑run, валидациями и логами.

---

## 13) База Знаний для ИИ-Агента

Этот проект создает локальную, самодостаточную базу знаний для хранения и извлечения информации, связанной с музыкой, Ableton Live и другими темами. Он использует векторную базу данных Weaviate и локальную модель для векторизации текста, что **не требует внешних API-ключей**.

### Архитектура

Система состоит из трех основных компонентов:

1.  **Weaviate (`weaviate` сервис):** Основная база данных, которая хранит данные и их векторные представления.
2.  **Локальный Векторизатор (`t2v-transformers` сервис):** Контейнер с моделью `msmarco-distilbert-base-v4`, который преобразует текстовые данные в векторы для семантического поиска.
3.  **Скрипт-интерфейс (`knowledge_store.py`):** Python-скрипт для взаимодействия с базой данных (добавление, поиск информации).

### Быстрый старт

#### 1. Требования

- **Docker и Docker Compose:** Убедитесь, что на вашей системе установлен [Docker](https://www.docker.com/products/docker-desktop/).
- **Python 3:** Необходим для запуска скрипта `knowledge_store.py`.
- **Клиент Weaviate:** Установите необходимую Python-библиотеку:
  ```bash
  pip install weaviate-client
  ```

#### 2. Запуск

1.  **Перейдите в директорию `knowledge_base`:**

    ```bash
    cd /path/to/your/project/knowledge_base
    ```

2.  **Запустите Docker-контейнеры:**
    ```bash
    docker-compose up -d
    ```
    Эта команда скачает необходимые образы (если их нет локально) и запустит два контейнера в фоновом режиме. Первый запуск может занять некоторое время для скачивания модели.

#### 3. Проверка работы

После успешного запуска вы можете запустить скрипт для проверки. Он подключится к базе данных, создаст необходимую схему (если она не существует) и выполнит тестовый поиск.

```bash
python knowledge_store.py
```

### Как это работает

- **Добавление знаний:** Функция `add_knowledge` в `knowledge_store.py` принимает текст, категорию и источник. Текст автоматически передается в `t2v-transformers` сервис, который создает вектор. Затем Weaviate сохраняет и текст, и вектор.

- **Поиск знаний:** Функция `search_knowledge` принимает поисковый запрос. Этот запрос также векторизуется, и Weaviate находит в базе наиболее близкие по смыслу (векторной близости) фрагменты знаний.

Это позволяет системе находить релевантную информацию, даже если формулировки в запросе и в сохраненном знании не совпадают дословно.

---

## 14) Database Setup (PostgreSQL + pgvector)

This project uses a PostgreSQL database running in a Docker container to store project data, including metadata for videos, recipes, MIDI patterns, and embeddings for semantic search.

### Architecture

- **Service**: `postgres:16` with the `pgvector` extension for vector similarity search.
- **Configuration**: Defined in `docker-compose.yml`.
- **Database Name**: `music_kb`
- **User**: `kb_user`
- **Password**: A placeholder `your_strong_password_here` is set in `docker-compose.yml`. **It is crucial to change this to a strong, unique password.**
- **Data Persistence**: A Docker volume named `pgdata` is used to persist data across container restarts.
- **Initialization**: An `init.sql` script is used to create the database schema and enable the `pgvector` extension on the first run.

### How to Run

1.  **Prerequisites**: Make sure Docker and Docker Compose (or the `docker compose` plugin) are installed on your system.
2.  **Start the database**: Navigate to the project root directory (`/Users/eugene/Documents/Ableton/app`) and run the following command:
    ```bash
    docker compose up -d
    ```
    This will start the PostgreSQL container in the background.

### Database Schema

The `init.sql` script creates the following tables:

- `videos`: Stores information about source videos (URL, language, duration, status).
- `video_segments`: Contains details about segments within videos (timestamps, titles, tags).
- `recipes`: For sound design and beat recipes (name, category, JSONB parameters).
- `reference_profiles`: Stores track profiles (BPM, key, sections).
- `midi_patterns`: Information about MIDI patterns (role, path, tags).
- `arrangement_plans`: For storing arrangement structures in JSONB format.
- `action_sequences`: Stores sequences of DSL commands for the bridge.
- `devices`: Information about device presets and FX chains.
- `embeddings`: Stores vector embeddings for various items (`owner_type`, `owner_id`, `model`, `embedding`) to enable semantic search.

**Indexes** are created on foreign keys, JSONB columns (GIN), and the `embedding` vector column (HNSW) for efficient querying.
