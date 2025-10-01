#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Precise Base Calibrator - Точная калибровка Base параметра для -5dB
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

def test_base_values_precise():
    """Точное тестирование значений для Base = -5dB"""
    
    print(f"🎯 ТОЧНАЯ КАЛИБРОВКА BASE = -5dB")
    print("=" * 40)
    print("Сейчас Base показывает 0.5, а нужно -5dB")
    
    # Пробуем различные значения вокруг области где может быть -5dB
    test_values = [
        0.0,    # Минимум
        0.1,    # 10%
        0.15,   # 15% 
        0.2,    # 20%
        0.25,   # 25%
        0.3,    # 30%
        0.35,   # 35%
        0.4,    # 40%
        0.45,   # 45%
        0.5,    # 50% (текущее)
    ]
    
    print(f"\n🔬 ТЕСТИРУЕМ ДИАПАЗОН ЗНАЧЕНИЙ:")
    print("   После каждого значения проверяйте Base в Saturator")
    
    for test_value in test_values:
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": "1 808",
                    "device_index": 3,
                    "param_index": 2,
                    "value": test_value
                },
                "id": f"calibrate_{test_value}"
            }
            
            print(f"\n🎛️ Устанавливаю Base = {test_value:.3f}")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"   ✅ Установлено: {test_value:.3f}")
                    
                    # Показываем что ожидать
                    expected_db = estimate_db_from_normalized(test_value)
                    print(f"   📊 Ожидаемый Base: ~{expected_db:.1f}dB")
                    
                    actual = input(f"   ❓ Какой Base показывает в Saturator? (или 'skip'): ")
                    
                    if actual != 'skip':
                        try:
                            actual_db = float(actual)
                            if abs(actual_db - (-5.0)) < 0.1:  # Близко к -5dB
                                print(f"   🎉 НАЙДЕНО! Для -5dB используйте: {test_value:.3f}")
                                return test_value
                            else:
                                print(f"   📝 {test_value:.3f} -> {actual_db}dB")
                        except ValueError:
                            print(f"   📝 {test_value:.3f} -> {actual}")
                else:
                    print(f"   ❌ API ошибка")
            else:
                print(f"   ❌ HTTP ошибка")
                
            time.sleep(1)  # Пауза между тестами
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return None

def estimate_db_from_normalized(normalized_value):
    """Оценка dB значения из normalized (предположение)"""
    # Если Base идет от -30 до +30 (60dB диапазон)
    if normalized_value == 0.5:
        return 0.0  # Середина
    elif normalized_value < 0.5:
        return -30 + (normalized_value * 60)  # От -30 до 0
    else:
        return (normalized_value - 0.5) * 60  # От 0 до +30

def binary_search_base():
    """Бинарный поиск точного значения для -5dB"""
    
    print(f"\n🔍 БИНАРНЫЙ ПОИСК -5dB")
    print("=" * 30)
    
    # Начинаем с диапазона где может быть -5dB
    min_val = 0.0   # Предполагаемый минимум (-30dB?)
    max_val = 0.5   # Середина (0dB?)
    target_db = -5.0
    
    for iteration in range(10):  # Максимум 10 итераций
        test_value = (min_val + max_val) / 2
        
        try:
            payload = {
                "action": "set_device_parameter", 
                "args": {
                    "track": "1 808",
                    "device_index": 3,
                    "param_index": 2,
                    "value": test_value
                },
                "id": f"binary_{iteration}"
            }
            
            print(f"\n🎯 Итерация {iteration + 1}: тестирую {test_value:.4f}")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    actual = input(f"   Какой Base показывает? (число или 'q' для выхода): ")
                    
                    if actual == 'q':
                        break
                    
                    try:
                        actual_db = float(actual)
                        print(f"   📊 {test_value:.4f} -> {actual_db}dB")
                        
                        if abs(actual_db - target_db) < 0.2:  # Достаточно близко
                            print(f"   🎉 НАЙДЕНО! Для -5dB: {test_value:.4f}")
                            return test_value
                        elif actual_db > target_db:
                            # Слишком высоко, уменьшаем верхнюю границу
                            max_val = test_value
                        else:
                            # Слишком низко, увеличиваем нижнюю границу  
                            min_val = test_value
                            
                    except ValueError:
                        print(f"   ⚠️ Введите число")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            break
    
    return None

def quick_test_common_values():
    """Быстрый тест часто встречающихся значений"""
    
    print(f"⚡ БЫСТРЫЙ ТЕСТ ПОПУЛЯРНЫХ ЗНАЧЕНИЙ")
    print("=" * 40)
    
    # Основываясь на том что 0.083 дало 0.5, а нужно меньше
    common_values = [
        (0.4, "Попытка 1"),
        (0.3, "Попытка 2"), 
        (0.35, "Попытка 3"),
        (0.33, "Попытка 4 (1/3)"),
        (0.25, "Попытка 5 (1/4)"),
        (0.16, "Попытка 6"),
        (0.42, "Попытка 7")
    ]
    
    for test_value, description in common_values:
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": "1 808",
                    "device_index": 3, 
                    "param_index": 2,
                    "value": test_value
                },
                "id": f"quick_{test_value}"
            }
            
            print(f"\n🎯 {description}: {test_value:.3f}")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    check = input(f"   Base показывает -5.00? (y/n/число): ")
                    
                    if check.lower() == 'y':
                        print(f"   🎉 НАЙДЕНО! Используйте: {test_value:.3f}")
                        return test_value
                    elif check.lower() != 'n':
                        try:
                            actual_db = float(check)
                            print(f"   📝 {test_value:.3f} -> {actual_db}dB")
                        except:
                            pass
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return None

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
    print("📋 Base сейчас показывает 0.5, а нужно -5dB")
    
    # Сначала быстрый тест
    result = quick_test_common_values()
    
    if not result:
        print(f"\n🔬 Переходим к детальному тестированию...")
        result = test_base_values_precise()
    
    if result:
        print(f"\n✅ КАЛИБРОВКА ЗАВЕРШЕНА!")
        print(f"   Для Base = -5dB используйте: {result:.4f}")
    else:
        print(f"\n🤔 Попробуйте бинарный поиск...")
        binary_search_base()