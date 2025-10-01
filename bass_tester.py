#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Saturator Bass Tester - Прямое тестирование Bass параметра в Saturator
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8787"

def test_saturator_bass(bass_db=-5):
    """Тест настройки Bass в Saturator на конкретное значение в dB"""
    
    print(f"🔥 ТЕСТ SATURATOR BASS = {bass_db}dB")
    print("=" * 40)
    
    # Saturator Bass обычно имеет диапазон от -30dB до +30dB
    # Конвертируем dB в normalized значение (0.0 - 1.0)
    min_db = -30.0
    max_db = 30.0
    normalized_value = (bass_db - min_db) / (max_db - min_db)
    
    print(f"📊 Конвертация:")
    print(f"   Bass: {bass_db}dB")
    print(f"   Диапазон: {min_db}dB - {max_db}dB") 
    print(f"   Normalized: {normalized_value:.3f}")
    
    # Пробуем разные индексы параметров для Bass
    test_params = [
        (0, "Device On/Off"),
        (1, "Drive"),
        (2, "Base/Bass"), 
        (3, "Frequency"),
        (4, "Color"),
        (5, "Output")
    ]
    
    track_name = "1 808"
    device_index = 3  # Saturator в слоте 3
    
    print(f"\n🧪 Тестирую параметры Saturator (слот {device_index}):")
    
    for param_index, param_name in test_params:
        try:
            # Пропускаем параметр 0 (On/Off)
            if param_index == 0:
                continue
                
            # Для Bass параметра используем наше значение
            if "bass" in param_name.lower() or "base" in param_name.lower():
                test_value = normalized_value
                description = f"{param_name} = {bass_db}dB"
            else:
                continue  # Пропускаем другие параметры в этом тесте
            
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": track_name,
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": test_value
                },
                "id": f"test_saturator_{param_index}"
            }
            
            print(f"\n   🎛️ Параметр {param_index} ({param_name}):")
            print(f"      Значение: {test_value:.3f} ({description})")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"      ✅ Установлено успешно!")
                    return True
                else:
                    print(f"      ❌ Ошибка API: {result}")
            else:
                print(f"      ❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Исключение: {e}")
    
    # Если не нашли Bass, пробуем все подряд
    print(f"\n🔍 Bass параметр не найден. Пробуем все индексы 1-8:")
    
    for param_index in range(1, 9):
        try:
            payload = {
                "action": "set_device_parameter", 
                "args": {
                    "track": track_name,
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": normalized_value
                },
                "id": f"test_bass_{param_index}"
            }
            
            print(f"   Индекс {param_index}: ", end="")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=3)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"✅ OK")
                else:
                    print(f"❌ API error")
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

def quick_bass_test():
    """Быстрый тест наиболее вероятных индексов для Bass"""
    
    print(f"⚡ БЫСТРЫЙ ТЕСТ BASS ПАРАМЕТРА")
    print("=" * 30)
    
    # Bass в Saturator чаще всего находится в индексе 2
    most_likely_indices = [2, 3, 1, 4]
    bass_db = -5
    normalized_value = (bass_db + 30) / 60  # -5dB -> normalized
    
    for param_idx in most_likely_indices:
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": "1 808",
                    "device_index": 3,
                    "param_index": param_idx, 
                    "value": normalized_value
                },
                "id": f"quick_bass_{param_idx}"
            }
            
            print(f"🎯 Тестирую индекс {param_idx} (Bass = -5dB)...")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"   ✅ Параметр {param_idx} установлен успешно!")
                    print(f"   🎵 Проверьте Saturator в Ableton - Bass должен быть -5dB")
                    return True
                    
        except Exception as e:
            print(f"   ❌ Ошибка на индексе {param_idx}: {e}")
    
    print(f"❌ Не удалось установить Bass параметр")
    return False

if __name__ == "__main__":
    # Проверяем подключение
    try:
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code == 200:
            print("✅ Bridge сервер доступен")
        else:
            print("❌ Bridge сервер недоступен!")
            exit(1)
    except:
        print("❌ Не могу подключиться к серверу!")
        exit(1)
    
    # Запускаем быстрый тест
    success = quick_bass_test()
    
    if success:
        print(f"\n🎉 ТЕСТ ПРОЙДЕН!")
        print(f"   Saturator Bass настроен на -5dB")
    else:
        print(f"\n📋 Запускаю полное тестирование...")
        test_saturator_bass(-5)