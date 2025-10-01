#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saturator Parameter Scanner - Поиск правильного индекса Base параметра
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

class DeviceAnalyzer:
    """Анализатор устройств и их параметров в Ableton Live"""
    
    def __init__(self, track_name="1 808"):
        self.track_name = track_name
    
    def get_track_devices(self):
        """Получает список всех устройств на треке"""
        try:
            payload = {
                "action": "get_track_devices",
                "args": {"track": self.track_name},
                "id": "analyze_devices"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            if response.status_code == 200:
                print(f"📱 Ответ API для get_track_devices: {response.json()}")
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Ошибка получения устройств: {e}")
            return None
    
    def get_device_parameters(self, device_index):
        """Получает все параметры конкретного устройства"""
        try:
            payload = {
                "action": "get_device_parameters",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index
                },
                "id": f"analyze_device_{device_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"🎛️ Параметры устройства {device_index}: {result}")
                return result
            return None
        except Exception as e:
            print(f"❌ Ошибка получения параметров устройства {device_index}: {e}")
            return None
    
    def analyze_all_devices(self):
        """Полный анализ всех устройств на треке"""
        print(f"🔍 Анализирую все устройства на треке '{self.track_name}'...")
        print("=" * 60)
        
        # Получаем список устройств
        devices_response = self.get_track_devices()
        
        # Пока API возвращает только подтверждение, создадим тестовый анализ
        # для распространенных Ableton устройств
        
        print("\n🎯 Поскольку API пока возвращает только подтверждения отправки,")
        print("   создам анализ для типичных Ableton устройств:")
        
        # Тестируем получение параметров для первых нескольких слотов
        for device_idx in range(5):  # Проверим первые 5 слотов
            print(f"\n📊 Анализ устройства в слоте {device_idx}:")
            params = self.get_device_parameters(device_idx)
            time.sleep(0.5)  # Пауза между запросами
        
        print("\n💡 Рекомендуемый порядок устройств для jungle звука:")
        self.recommend_device_order()
    
    def recommend_device_order(self):
        """Рекомендует оптимальный порядок устройств для jungle звука"""
        recommendations = [
            {
                "position": 0,
                "device": "Drum Kit / Drum Rack",
                "purpose": "Основные звуки ударных",
                "settings": "Настроить kick, snare, hi-hat отдельно"
            },
            {
                "position": 1, 
                "device": "EQ Eight",
                "purpose": "Коррекция частот для jungle звука",
                "settings": "High-pass 80Hz, boost 8-12kHz, cut 400Hz"
            },
            {
                "position": 2,
                "device": "Compressor", 
                "purpose": "Punch и dynamics control",
                "settings": "Threshold -18dB, Ratio 4:1, Attack 1ms"
            },
            {
                "position": 3,
                "device": "Saturator",
                "purpose": "Аналоговое тепло и гармоники", 
                "settings": "Drive 3-5dB, Analog Clip mode"
            },
            {
                "position": 4,
                "device": "Chorus / Ensemble",
                "purpose": "Stereo width (опционально)",
                "settings": "Rate 0.5Hz, Amount 15%"
            },
            {
                "position": 5,
                "device": "Reverb",
                "purpose": "Пространство и атмосфера",
                "settings": "Room 20%, Decay 1.5s, Wet 15%"
            },
            {
                "position": 6,
                "device": "Limiter",
                "purpose": "Финальный контроль уровня",
                "settings": "Ceiling -0.3dB, gentle limiting"
            }
        ]
        
        for rec in recommendations:
            print(f"\n   {rec['position']}. 🎛️ {rec['device']}")
            print(f"      Цель: {rec['purpose']}")
            print(f"      Настройки: {rec['settings']}")
    
    def identify_common_ableton_devices(self):
        """Идентифицирует типичные устройства Ableton и их параметры"""
        
        common_devices = {
            "EQEight": {
                "parameters": [
                    {"name": "1 Freq A", "range": "20-20000 Hz", "jungle_value": "80"},
                    {"name": "1 Gain A", "range": "-15 to +15 dB", "jungle_value": "0"},
                    {"name": "1 Q A", "range": "0.1 to 40", "jungle_value": "0.7"},
                    {"name": "8 Freq H", "range": "20-20000 Hz", "jungle_value": "10000"},
                    {"name": "8 Gain H", "range": "-15 to +15 dB", "jungle_value": "+3"}
                ]
            },
            
            "Compressor": {
                "parameters": [
                    {"name": "Threshold", "range": "-60 to 0 dB", "jungle_value": "-18"},
                    {"name": "Ratio", "range": "1:1 to ∞:1", "jungle_value": "4.0"},
                    {"name": "Attack", "range": "0.01 to 800 ms", "jungle_value": "1"},
                    {"name": "Release", "range": "1 to 5000 ms", "jungle_value": "50"},
                    {"name": "Makeup", "range": "0 to 20 dB", "jungle_value": "auto"}
                ]
            },
            
            "Saturator": {
                "parameters": [
                    {"name": "Drive", "range": "0 to 36 dB", "jungle_value": "5"},
                    {"name": "Base", "range": "0 to 100", "jungle_value": "50"},
                    {"name": "Frequency", "range": "100 to 18000 Hz", "jungle_value": "2000"},
                    {"name": "Width", "range": "0 to 100", "jungle_value": "100"},
                    {"name": "Depth", "range": "0 to 100", "jungle_value": "50"}
                ]
            },
            
            "Reverb": {
                "parameters": [
                    {"name": "PreDelay", "range": "0 to 250 ms", "jungle_value": "15"},
                    {"name": "Room Size", "range": "0 to 100", "jungle_value": "20"},
                    {"name": "Decay Time", "range": "0.1 to 60 s", "jungle_value": "1.5"}, 
                    {"name": "Dry/Wet", "range": "0 to 100", "jungle_value": "15"},
                    {"name": "Freeze", "range": "0 to 1", "jungle_value": "0"}
                ]
            }
        }
        
        print("\n📋 Анализ параметров типичных Ableton устройств:")
        print("=" * 60)
        
        for device_name, device_info in common_devices.items():
            print(f"\n🎛️ {device_name}:")
            for param in device_info["parameters"]:
                print(f"   • {param['name']:<12} | {param['range']:<20} | Jungle: {param['jungle_value']}")

def main():
    """Основная функция анализа устройств"""
    print("🔍 DEVICE ANALYZER для AI Agent Ableton Live")
    print("=" * 50)
    
    analyzer = DeviceAnalyzer("1 808")
    
    try:
        # Проверяем доступность API
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code != 200:
            print("❌ Bridge сервер недоступен!")
            return
        
        print("✅ Подключение к Ableton установлено")
        
        # Анализируем устройства
        analyzer.analyze_all_devices()
        
        # Показываем информацию о типичных устройствах
        analyzer.identify_common_ableton_devices()
        
        print(f"\n🎯 Следующий шаг: создать автонастройку этих устройств")
        print(f"   Для этого нужно получить точные индексы параметров через live API")
        
    except Exception as e:
        print(f"❌ Ошибка в device analyzer: {e}")

if __name__ == "__main__":
    main()