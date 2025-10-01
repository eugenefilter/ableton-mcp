#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание классического Amen Break паттерна для Ableton Live
Основано на оригинальном брейкбите "Amen, Brother" by The Winstons
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8787"

def create_amen_break():
    """
    Создает классический Amen Break паттерн
    
    MIDI ноты для ударных (General MIDI Standard):
    - Kick (Bass Drum): C1 (36)  
    - Snare Drum: D1 (38)
    - Closed Hi-Hat: F#1 (42)
    - Open Hi-Hat: A#1 (46)
    - Crash: C#2 (49)
    
    Временная сетка: 16-я ноты в 4/4 (16 позиций на бар)
    Длительность: 2 бара (32 позиции всего)
    """
    
    # Классический Amen Break паттерн (2 бара)
    # Позиции указаны в четвертных нотах (1.0 = четверть, 0.25 = шестнадцатая)
    amen_pattern = [
        # БАР 1
        # Бит 1
        {"p": 36, "s": 0.0, "d": 0.25, "v": 127},    # Kick на 1
        {"p": 42, "s": 0.0, "d": 0.125, "v": 90},    # Hi-hat на 1
        
        {"p": 42, "s": 0.25, "d": 0.125, "v": 70},   # Hi-hat на 1e
        
        {"p": 42, "s": 0.5, "d": 0.125, "v": 90},    # Hi-hat на &
        
        {"p": 42, "s": 0.75, "d": 0.125, "v": 70},   # Hi-hat на 1a
        
        # Бит 2
        {"p": 38, "s": 1.0, "d": 0.25, "v": 120},    # Snare на 2
        {"p": 42, "s": 1.0, "d": 0.125, "v": 90},    # Hi-hat на 2
        
        {"p": 42, "s": 1.25, "d": 0.125, "v": 70},   # Hi-hat на 2e
        
        {"p": 36, "s": 1.5, "d": 0.25, "v": 110},    # Kick на &2
        {"p": 42, "s": 1.5, "d": 0.125, "v": 90},    # Hi-hat на &2
        
        {"p": 42, "s": 1.75, "d": 0.125, "v": 70},   # Hi-hat на 2a
        
        # Бит 3
        {"p": 36, "s": 2.0, "d": 0.25, "v": 127},    # Kick на 3
        {"p": 42, "s": 2.0, "d": 0.125, "v": 90},    # Hi-hat на 3
        
        {"p": 42, "s": 2.25, "d": 0.125, "v": 70},   # Hi-hat на 3e
        
        {"p": 42, "s": 2.5, "d": 0.125, "v": 90},    # Hi-hat на &3
        
        {"p": 42, "s": 2.75, "d": 0.125, "v": 70},   # Hi-hat на 3a
        
        # Бит 4
        {"p": 38, "s": 3.0, "d": 0.25, "v": 120},    # Snare на 4
        {"p": 42, "s": 3.0, "d": 0.125, "v": 90},    # Hi-hat на 4
        
        {"p": 36, "s": 3.25, "d": 0.25, "v": 100},   # Kick на 4e (ghost)
        {"p": 42, "s": 3.25, "d": 0.125, "v": 70},   # Hi-hat на 4e
        
        {"p": 42, "s": 3.5, "d": 0.125, "v": 90},    # Hi-hat на &4
        
        {"p": 38, "s": 3.75, "d": 0.25, "v": 100},   # Snare (ghost) на 4a
        {"p": 42, "s": 3.75, "d": 0.125, "v": 70},   # Hi-hat на 4a
        
        # БАР 2 (Вариация)
        # Бит 1
        {"p": 36, "s": 4.0, "d": 0.25, "v": 127},    # Kick на 1
        {"p": 42, "s": 4.0, "d": 0.125, "v": 90},    # Hi-hat на 1
        
        {"p": 42, "s": 4.25, "d": 0.125, "v": 70},   # Hi-hat на 1e
        
        {"p": 42, "s": 4.5, "d": 0.125, "v": 90},    # Hi-hat на &1
        
        {"p": 36, "s": 4.75, "d": 0.25, "v": 100},   # Kick (ghost) на 1a
        {"p": 42, "s": 4.75, "d": 0.125, "v": 70},   # Hi-hat на 1a
        
        # Бит 2
        {"p": 38, "s": 5.0, "d": 0.25, "v": 120},    # Snare на 2
        {"p": 42, "s": 5.0, "d": 0.125, "v": 90},    # Hi-hat на 2
        
        {"p": 38, "s": 5.25, "d": 0.125, "v": 90},   # Snare на 2e
        {"p": 42, "s": 5.25, "d": 0.125, "v": 70},   # Hi-hat на 2e
        
        {"p": 36, "s": 5.5, "d": 0.25, "v": 110},    # Kick на &2
        {"p": 42, "s": 5.5, "d": 0.125, "v": 90},    # Hi-hat на &2
        
        {"p": 38, "s": 5.75, "d": 0.125, "v": 85},   # Snare на 2a
        {"p": 42, "s": 5.75, "d": 0.125, "v": 70},   # Hi-hat на 2a
        
        # Бит 3
        {"p": 36, "s": 6.0, "d": 0.25, "v": 127},    # Kick на 3
        {"p": 46, "s": 6.0, "d": 0.5, "v": 100},     # Open Hi-hat на 3
        
        {"p": 36, "s": 6.5, "d": 0.25, "v": 100},    # Kick на &3
        {"p": 42, "s": 6.5, "d": 0.125, "v": 90},    # Hi-hat на &3
        
        {"p": 42, "s": 6.75, "d": 0.125, "v": 70},   # Hi-hat на 3a
        
        # Бит 4
        {"p": 38, "s": 7.0, "d": 0.25, "v": 120},    # Snare на 4
        {"p": 42, "s": 7.0, "d": 0.125, "v": 90},    # Hi-hat на 4
        
        {"p": 38, "s": 7.25, "d": 0.125, "v": 95},   # Snare на 4e
        {"p": 42, "s": 7.25, "d": 0.125, "v": 70},   # Hi-hat на 4e
        
        {"p": 36, "s": 7.5, "d": 0.25, "v": 110},    # Kick на &4
        {"p": 42, "s": 7.5, "d": 0.125, "v": 90},    # Hi-hat на &4
        
        {"p": 42, "s": 7.75, "d": 0.125, "v": 70},   # Hi-hat на 4a
    ]
    
    print("🥁 Создаю классический Amen Break паттерн...")
    print(f"📋 Всего нот: {len(amen_pattern)}")
    
    # Отправляем ноты в Ableton
    try:
        payload = {
            "action": "set_clip_notes", 
            "args": {
                "track": "1 808", 
                "slot": 0, 
                "notes": amen_pattern
            }, 
            "id": "amen_break_notes"
        }
        
        response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Amen Break паттерн успешно создан!")
            print("🎵 Паттерн включает:")
            print("   - Kick drum (басовый барабан)")
            print("   - Snare drum (малый барабан)")  
            print("   - Hi-hat (хай-хэт)")
            print("   - Классические ghost notes")
            print("   - 2 бара в петле")
            return True
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании паттерна: {e}")
        return False

def launch_clip():
    """Запускает созданный клип"""
    print("\n▶️ Запускаю Amen Break клип...")
    try:
        payload = {
            "action": "launch_clip", 
            "args": {
                "track": "1 808", 
                "slot": 0
            }, 
            "id": "launch_amen"
        }
        
        response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
        
        if response.status_code == 200:
            print("✅ Клип запущен!")
            return True
        else:
            print(f"❌ Ошибка запуска: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        return False

if __name__ == "__main__":
    print("🎼 Создание Amen Break в Ableton Live")
    print("=" * 40)
    
    if create_amen_break():
        print("\n🎯 Готово! Теперь можно:")
        print("1. Запустить клип в Ableton")
        print("2. Настроить звуки ударных в Drum Kit")
        print("3. Добавить эффекты")
        
        # Автоматически запускаем клип
        launch_clip()
    else:
        print("\n❌ Не удалось создать паттерн")