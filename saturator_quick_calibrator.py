#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saturator Quick Calibrator - Быстрая калибровка для нужных значений
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

def test_drive_values():
    """Тестируем разные способы установки Drive на 5dB"""
    
    print(f"🔧 КАЛИБРОВКА DRIVE НА 5dB")
    print("=" * 35)
    
    # Пробуем разные подходы
    drive_tests = [
        (1, 0.1, "Param 1: normalized 0.1"),
        (1, 0.05, "Param 1: normalized 0.05"),
        (2, 5.0, "Param 2: direct 5dB"),
        (2, 0.2, "Param 2: normalized 0.2"),
    ]
    
    for param_idx, value, description in drive_tests:
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": "1 808",
                    "device_index": 3,
                    "param_index": param_idx,
                    "value": value
                },
                "id": f"drive_test_{param_idx}_{value}"
            }
            
            print(f"\n🧪 {description}")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"   ✅ Установлено: {value}")
                    time.sleep(0.5)
                    
                    drive_result = input(f"   Какой Drive показывает? ")
                    
                    if '5' in drive_result:
                        print(f"   🎉 НАЙДЕНО! Для Drive 5dB: param {param_idx} = {value}")
                        return (param_idx, value)
                    else:
                        print(f"   📝 Drive: {drive_result}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return None

def test_frequency_values():
    """Тестируем разные способы установки Frequency на 2kHz"""
    
    print(f"\n🔧 КАЛИБРОВКА FREQUENCY НА 2kHz")
    print("=" * 40)
    
    freq_tests = [
        (2, 0.8, "Param 2: normalized 0.8"),
        (3, 0.7, "Param 3: normalized 0.7"), 
        (4, 0.6, "Param 4: normalized 0.6"),
        (2, 2000, "Param 2: direct 2000Hz"),
        (3, 2000, "Param 3: direct 2000Hz"),
    ]
    
    for param_idx, value, description in freq_tests:
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": "1 808",
                    "device_index": 3,
                    "param_index": param_idx,
                    "value": value
                },
                "id": f"freq_test_{param_idx}_{value}"
            }
            
            print(f"\n🧪 {description}")
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"   ✅ Установлено: {value}")
                    time.sleep(0.5)
                    
                    freq_result = input(f"   Какой Freq показывает? ")
                    
                    if '2' in freq_result and ('k' in freq_result.lower() or '000' in freq_result):
                        print(f"   🎉 НАЙДЕНО! Для Freq 2kHz: param {param_idx} = {value}")
                        return (param_idx, value)
                    else:
                        print(f"   📝 Freq: {freq_result}")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    return None

def main():
    print("🎛️ SATURATOR QUICK CALIBRATOR")
    print("Цель: Drive 5dB, Frequency 2kHz")
    print("=" * 40)
    
    # Проверяем подключение
    try:
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code != 200:
            print("❌ Bridge сервер недоступен!")
            return
    except:
        print("❌ Не могу подключиться к серверу!")
        return
    
    print("✅ Подключение установлено")
    
    # Калибруем Drive
    drive_result = test_drive_values()
    
    # Калибруем Frequency  
    freq_result = test_frequency_values()
    
    print(f"\n📊 РЕЗУЛЬТАТЫ КАЛИБРОВКИ:")
    print("=" * 30)
    
    if drive_result:
        print(f"Drive 5dB: param {drive_result[0]} = {drive_result[1]}")
    else:
        print(f"Drive 5dB: НЕ НАЙДЕНО")
    
    if freq_result:
        print(f"Freq 2kHz: param {freq_result[0]} = {freq_result[1]}")
    else:
        print(f"Freq 2kHz: НЕ НАЙДЕНО")
    
    if drive_result or freq_result:
        print(f"\n🔧 Обновите jungle_auto_tuner.py с этими значениями!")

if __name__ == "__main__":
    main()