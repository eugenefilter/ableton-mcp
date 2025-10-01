#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования API моста с Ableton Live
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

def test_state():
    """Тестирует получение состояния проекта"""
    print("🔍 Тестируем получение состояния проекта...")
    try:
        response = requests.get(f"{BASE_URL}/state", timeout=5)
        print(f"Статус ответа: {response.status_code}")
        print(f"Содержимое: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка при получении состояния: {e}")
        return False

def test_play():
    """Тестирует команду воспроизведения"""
    print("\n▶️ Тестируем команду PLAY...")
    try:
        payload = {"action": "play", "id": "test_play"}
        response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
        print(f"Статус ответа: {response.status_code}")
        print(f"Содержимое: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка при отправке команды play: {e}")
        return False

def test_stop():
    """Тестирует команду остановки"""
    print("\n⏹️ Тестируем команду STOP...")
    try:
        payload = {"action": "stop", "id": "test_stop"}
        response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
        print(f"Статус ответа: {response.status_code}")
        print(f"Содержимое: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка при отправке команды stop: {e}")
        return False

def test_set_tempo():
    """Тестирует изменение темпа"""
    print("\n🎵 Тестируем изменение темпа на 128 BPM...")
    try:
        payload = {"action": "set_tempo", "args": {"bpm": 128}, "id": "test_tempo"}
        response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
        print(f"Статус ответа: {response.status_code}")
        print(f"Содержимое: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка при изменении темпа: {e}")
        return False

def test_create_midi_track():
    """Тестирует создание MIDI трека"""
    print("\n🎹 Тестируем создание MIDI трека...")
    try:
        payload = {
            "action": "create_midi_track", 
            "args": {"name": "Test Track", "arm": True}, 
            "id": "test_create_track"
        }
        response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
        print(f"Статус ответа: {response.status_code}")
        print(f"Содержимое: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ошибка при создании трека: {e}")
        return False

def main():
    print("🚀 Начинаем тестирование API для Ableton Live...")
    print("=" * 50)
    
    # Проверяем доступность сервера
    try:
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        print("✅ Bridge сервер доступен")
    except:
        print("❌ Bridge сервер недоступен. Проверьте, что он запущен!")
        return
    
    # Запускаем тесты
    tests = [
        test_state,
        test_set_tempo,
        test_play,
        test_stop,
        test_create_midi_track,
        test_state,  # Повторно проверяем состояние
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Небольшая пауза между тестами
    
    print("\n" + "=" * 50)
    print(f"📊 Результат: {passed}/{len(tests)} тестов прошли успешно")
    
    if passed == len(tests):
        print("🎉 Все тесты прошли! API работает корректно!")
    else:
        print("⚠️ Некоторые тесты не прошли. Проверьте настройки MyAgent в Ableton.")

if __name__ == "__main__":
    main()