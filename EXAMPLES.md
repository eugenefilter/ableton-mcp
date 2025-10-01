# Быстрые примеры API

Готовые команды для тестирования AI Agent for Ableton Live.

## 🚀 Запуск системы

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Установить скрипт в Ableton
python setup.py

# 3. Запустить bridge (в отдельном терминале)
python bridge.py

# 4. Настроить MyAgent в Ableton Live:
# Preferences → Link/MIDI → Control Surface → MyAgent
```

## 📊 Проверка состояния

```bash
# Получить информацию о проекте
curl -X GET http://127.0.0.1:8787/state
```

## 🎵 Управление воспроизведением

```bash
# Запуск
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "play"}'

# Остановка
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "stop"}'

# Темп 140 BPM
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "set_tempo", "args": {"bpm": 140}}'
```

## 🎹 Создание треков и клипов

```bash
# Новый MIDI трек
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "create_midi_track", "args": {"name": "Bass", "arm": true}}'

# MIDI клип 8 баров
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "create_midi_clip", "args": {"track": "Bass", "slot": 0, "bars": 8, "loop": true}}'

# Запуск клипа
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "launch_clip", "args": {"track": "Bass", "slot": 0}}'
```

## 🥁 Готовые паттерны

```bash
# Автоматический Amen Break (используйте Python скрипт)
python create_amen_break.py

# Или создайте вручную клип и добавьте ноты
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{
    "action": "set_clip_notes",
    "args": {
      "track": "1 808",
      "slot": 0,
      "notes": [
        {"p": 36, "s": 0.0, "d": 0.25, "v": 127},
        {"p": 38, "s": 1.0, "d": 0.25, "v": 120},
        {"p": 42, "s": 0.0, "d": 0.125, "v": 90}
      ]
    }
  }'
```

## 🌿 Jungle Sound Processing

```bash
# Автоматическая jungle обработка Amen Break
python jungle_processor.py

# Анализ доступных устройств на треке
python device_analyzer.py

# АВТОНАСТРОЙКА ЭФФЕКТОВ для jungle звука
python jungle_auto_tuner.py

# Изменение pitch клипа
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "set_clip_pitch", "args": {"track": "1 808", "slot": 1, "pitch_coarse": 12}}'

# Установка jungle темпа (174 BPM)
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "set_tempo", "args": {"bpm": 174}}'

# Получение списка устройств на треке
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "get_track_devices", "args": {"track": "1 808"}}'

# Настройка параметра устройства (например, EQ)
curl -X POST http://127.0.0.1:8787/cmd \
  -H "Content-Type: application/json" \
  -d '{"action": "set_device_parameter", "args": {"track": "1 808", "device_index": 1, "param_index": 0, "value": 0.8}}'
```

## 🧪 Тестирование

```bash
# Комплексный тест всех функций
python test_api.py
```

## 🎼 Формат MIDI нот

```json
{
  "p": 36, // pitch (MIDI нота: 36=C1/Kick, 38=D1/Snare, 42=F#1/HiHat)
  "s": 0.0, // start (позиция в четвертях: 0.0=начало, 1.0=2й бит)
  "d": 0.25, // duration (длительность: 0.25=16я, 0.5=8я, 1.0=4я)
  "v": 127 // velocity (громкость: 0-127)
}
```

## 🎹 MIDI ноты для ударных

```
Kick (Bass Drum):     C1  = 36
Snare Drum:           D1  = 38
Closed Hi-Hat:        F#1 = 42
Open Hi-Hat:          A#1 = 46
Crash Cymbal:         C#2 = 49
Rim Shot:             C#1 = 37
Low Tom:              F1  = 41
Mid Tom:              A1  = 45
High Tom:             D2  = 50
```

## ⚡ Быстрые команды

```bash
# Остановить все
curl -X POST http://127.0.0.1:8787/cmd -H "Content-Type: application/json" -d '{"action": "stop"}'

# Темп 128
curl -X POST http://127.0.0.1:8787/cmd -H "Content-Type: application/json" -d '{"action": "set_tempo", "args": {"bpm": 128}}'

# Статус
curl -X GET http://127.0.0.1:8787/state | python -m json.tool
```
