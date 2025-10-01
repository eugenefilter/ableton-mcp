#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saturator Base Fixer - Исправление настройки Base параметра
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8787"

def test_base_values():
    """Тестируем разные значения для Base параметра"""
    
    print(f"🔧 ТЕСТ РАЗНЫХ ЗНАЧЕНИЙ ДЛЯ BASE")
    print("=" * 40)
    
    # На скриншоте видно что Base сейчас 0.00
    # Нужно найти правильное normalized значение для -5dB
    
    test_values = [
        # Пробуем разные подходы к конвертации
        (0.33, "Попытка 1: -5dB как 1/3"),
        (0.25, "Попытка 2: -5dB как 1/4"), 
        (0.2, "Попытка 3: -5dB как 1/5"),
        (0.15, "Попытка 4: -5dB как 15%"),
        (0.1, "Попытка 5: -5dB как 10%"),
        
        # Если Base имеет диапазон от -30 до +30
        (0.417, "Попытка 6: (-5+30)/60 = 0.417"),
        
        # Если Base имеет другой диапазон
        (0.3, "Попытка 7: Попробуем 30%"),
        (0.45, "Попытка 8: Попробуем 45%"),
    ]
    
    device_index = 3  # Saturator
    param_index = 2   # Base параметр (как мы выяснили)
    
    for test_value, description in test_values:
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": "1 808",
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": test_value
                },
                "id": f"test_base_{test_value}"
            }
            
            print(f"\n🎯 {description}")
            print(f"   Устанавливаю Base = {test_value:.3f}...")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"   ✅ Значение {test_value:.3f} установлено")
                    print(f"   👀 ПРОВЕРЬТЕ В ABLETON: Base должен измениться")
                    
                    # Пауза чтобы пользователь мог проверить
                    input(f"   ⏸️  Нажмите Enter после проверки в Ableton...")
                else:
                    print(f"   ❌ API ошибка: {result}")
            else:
                print(f"   ❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Исключение: {e}")

def try_specific_base_minus5():
    """Пробуем конкретные значения для -5dB"""
    
    print(f"\n🎯 СПЕЦИАЛЬНЫЙ ТЕСТ ДЛЯ BASE = -5dB")
    print("=" * 45)
    
    # Анализируем возможные диапазоны Base параметра:
    
    # Вариант 1: Base от -15 до +15 dB
    range1_value = (-5 + 15) / 30  # = 10/30 = 0.333
    
    # Вариант 2: Base от -20 до +20 dB  
    range2_value = (-5 + 20) / 40  # = 15/40 = 0.375
    
    # Вариант 3: Base от -10 до +10 dB
    range3_value = (-5 + 10) / 20  # = 5/20 = 0.25
    
    # Вариант 4: Base от -6 до +6 dB (часто в Saturator)
    range4_value = (-5 + 6) / 12   # = 1/12 = 0.083
    
    test_cases = [
        (range4_value, f"Base диапазон -6..+6dB: {range4_value:.3f}"),
        (range3_value, f"Base диапазон -10..+10dB: {range3_value:.3f}"),
        (range1_value, f"Base диапазон -15..+15dB: {range1_value:.3f}"), 
        (range2_value, f"Base диапазон -20..+20dB: {range2_value:.3f}"),
    ]
    
    for test_value, description in test_cases:
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": "1 808",
                    "device_index": 3,
                    "param_index": 2,
                    "value": test_value
                },
                "id": f"base_minus5_{test_value}"
            }
            
            print(f"\n🔬 {description}")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"   ✅ Установлено: {test_value:.3f}")
                    print(f"   🔍 Проверьте Base в Saturator")
                    
                    check = input(f"   ❓ Base показывает -5.00? (y/n): ")
                    if check.lower() == 'y':
                        print(f"   🎉 НАЙДЕНО ПРАВИЛЬНОЕ ЗНАЧЕНИЕ!")
                        print(f"   📝 Для Base = -5dB используйте: {test_value:.3f}")
                        return test_value
                else:
                    print(f"   ❌ API ошибка")
            else:
                print(f"   ❌ HTTP ошибка")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return None

def manual_base_test():
    """Ручной тест с пользовательским вводом"""
    
    print(f"\n🛠️  РУЧНОЙ ТЕСТ BASE ПАРАМЕТРА")
    print("=" * 35)
    
    try:
        test_value = float(input("Введите значение для Base (0.0 - 1.0): "))
        
        if not (0.0 <= test_value <= 1.0):
            print("❌ Значение должно быть от 0.0 до 1.0")
            return
        
        payload = {
            "action": "set_device_parameter",
            "args": {
                "track": "1 808", 
                "device_index": 3,
                "param_index": 2,
                "value": test_value
            },
            "id": f"manual_base_{test_value}"
        }
        
        response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("ok"):
                print(f"✅ Base установлен на {test_value:.3f}")
                print(f"🔍 Проверьте результат в Ableton")
            else:
                print(f"❌ Ошибка API")
        else:
            print(f"❌ HTTP ошибка")
            
    except ValueError:
        print("❌ Введите корректное число")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    # Проверяем подключение
    try:
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code != 200:
            print("❌ Bridge сервер недоступен!")
            exit(1)
    except:
        print("❌ Не могу подключиться к серверу!")
        exit(1)
    
    print("✅ Подключение установлено")
    print("📋 На скриншоте видно что Base = 0.00, а нужно -5dB")
    
    # Пробуем найти правильное значение
    correct_value = try_specific_base_minus5()
    
    if not correct_value:
        print(f"\n🤔 Автоматический поиск не помог")
        print(f"📝 Попробуем ручной тест...")
        manual_base_test()