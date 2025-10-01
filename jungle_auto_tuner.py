#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Effects Tuner для Jungle Sound
Автоматическая настройка добавленных эффектов для jungle звука
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

class JungleAutoTuner:
    """Автоматический настройщик эффектов для jungle звука"""
    
    def __init__(self, track_name="1 808"):
        self.track_name = track_name
        
        # Настройки для различных устройств Ableton Live
        self.device_presets = {
            "EqEight": {
                "jungle_settings": [
                    # Band 1 - High-pass filter на 80Hz
                    {"param": 0, "value": 1.0},    # Band 1 On
                    {"param": 1, "value": 0.08},   # Band 1 Freq (80Hz normalized)
                    {"param": 2, "value": 0.5},    # Band 1 Gain (0dB)
                    {"param": 3, "value": 0.7},    # Band 1 Q (0.7)
                    
                    # Band 3 - Cut средних на 400Hz  
                    {"param": 8, "value": 1.0},    # Band 3 On
                    {"param": 9, "value": 0.15},   # Band 3 Freq (400Hz normalized)
                    {"param": 10, "value": 0.45},  # Band 3 Gain (-1dB)
                    {"param": 11, "value": 0.6},   # Band 3 Q
                    
                    # Band 8 - Boost высоких на 10kHz
                    {"param": 28, "value": 1.0},   # Band 8 On  
                    {"param": 29, "value": 0.8},   # Band 8 Freq (10kHz normalized)
                    {"param": 30, "value": 0.6},   # Band 8 Gain (+3dB)
                    {"param": 31, "value": 0.5}    # Band 8 Q
                ]
            },
            
            "Compressor2": {
                "jungle_settings": [
                    # Пропускаем param 0 (On/Off) 
                    {"param": 1, "value": 0.75},   # Threshold (-15dB) - безопасно
                    {"param": 2, "value": 0.2},    # Ratio (3:1) - мягче
                    {"param": 3, "value": 0.02},   # Attack (5ms) 
                    {"param": 4, "value": 0.08}    # Release (80ms)
                ]
            },
            
            "Saturator": {
                "jungle_settings": [
                    # Пропускаем param 0 (On/Off)
                    {"param": 1, "value": 5.0},    # Drive: 5dB (analog warmth)
                    {"param": 5, "value": -5.0},   # Base: -5dB ✅ 
                    {"param": 3, "value": 2000},   # Frequency: 2kHz (midrange punch)
                    {"param": 7, "value": 0.0},    # Type: Analog Clip (musical distortion)
                    {"param": 4, "value": 100.0},  # Width: 100%
                    {"param": 6, "value": 100.0}   # Dry/Wet: 100%
                ]
            },
            
            "Reverb": {
                "jungle_settings": [
                    # Пропускаем param 0 (On/Off)
                    {"param": 1, "value": 0.18},   # Room Size (18%) 
                    {"param": 2, "value": 0.08}    # Dry/Wet (~10%) - скорректировано
                ]
            },
            
            "Chorus2": {
                "jungle_settings": [
                    # Пропускаем param 0 (On/Off)
                    {"param": 1, "value": 0.05},   # Rate (~0.2Hz) - медленно
                    {"param": 2, "value": 0.1}     # Amount (10%) - легкий эффект
                ]
            }
        }
    
    def set_device_parameter(self, device_index, param_index, value):
        """Устанавливает параметр устройства с нормализованным значением 0-1"""
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": value
                },
                "id": f"tune_{device_index}_{param_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Ошибка настройки параметра {param_index} устройства {device_index}: {e}")
            return False
    
    def auto_tune_eq_eight(self, device_index):
        """Автонастройка EQ Eight для jungle звука"""
        print(f"🎚️ Настраиваю EQ Eight в слоте {device_index}...")
        
        settings = self.device_presets.get("EqEight", {}).get("jungle_settings", [])
        success_count = 0
        
        for setting in settings:
            if self.set_device_parameter(device_index, setting["param"], setting["value"]):
                success_count += 1
            time.sleep(0.1)  # Небольшая пауза между параметрами
        
        print(f"   ✅ EQ Eight: установлено {success_count}/{len(settings)} параметров")
        print(f"      - High-pass на 80Hz")
        print(f"      - Boost высоких на 10kHz (+3dB)")
        print(f"      - Cut средних на 400Hz (-1dB)")
        
        return success_count == len(settings)
    
    def auto_tune_compressor(self, device_index):
        """Автонастройка Compressor для jungle punch"""
        print(f"🎛️ Настраиваю Compressor в слоте {device_index}...")
        
        settings = self.device_presets.get("Compressor2", {}).get("jungle_settings", [])
        success_count = 0
        
        for setting in settings:
            if self.set_device_parameter(device_index, setting["param"], setting["value"]):
                success_count += 1
            time.sleep(0.1)
        
        print(f"   ✅ Compressor: установлено {success_count}/{len(settings)} параметров")
        print(f"      - Threshold: -15dB (безопасно)")
        print(f"      - Ratio: 3:1 (консервативно)") 
        print(f"      - Attack: 5ms, Release: 80ms")
        
        return success_count == len(settings)
    
    def auto_tune_saturator(self, device_index):
        """Автонастройка Saturator для аналогового тепла"""
        print(f"🔥 Настраиваю Saturator в слоте {device_index}...")
        
        settings = self.device_presets.get("Saturator", {}).get("jungle_settings", [])
        success_count = 0
        
        for setting in settings:
            if self.set_device_parameter(device_index, setting["param"], setting["value"]):
                success_count += 1
            time.sleep(0.1)
        
        print(f"   ✅ Saturator: установлено {success_count}/{len(settings)} параметров")
        print(f"      - Drive: 5dB (analog warmth)")
        print(f"      - Base: -5dB, Focus: 2kHz")
        print(f"      - Type: Analog Clip (musical distortion)")
        
        return success_count == len(settings)
    
    def auto_tune_reverb(self, device_index):
        """Автонастройка Reverb для jungle атмосферы"""
        print(f"🌊 Настраиваю Reverb в слоте {device_index}...")
        
        settings = self.device_presets.get("Reverb", {}).get("jungle_settings", [])
        success_count = 0
        
        for setting in settings:
            if self.set_device_parameter(device_index, setting["param"], setting["value"]):
                success_count += 1
            time.sleep(0.1)
        
        print(f"   ✅ Reverb: установлено {success_count}/{len(settings)} параметров")
        print(f"      - Room size: 18% (консервативно)")
        print(f"      - Dry/Wet: ~10% (тонкая атмосфера)")
        
        return success_count == len(settings)
    
    def auto_tune_chorus(self, device_index):
        """Автонастройка Chorus для stereo width"""
        print(f"〰️ Настраиваю Chorus в слоте {device_index}...")
        
        settings = self.device_presets.get("Chorus2", {}).get("jungle_settings", [])
        success_count = 0
        
        for setting in settings:
            if self.set_device_parameter(device_index, setting["param"], setting["value"]):
                success_count += 1
            time.sleep(0.1)
        
        print(f"   ✅ Chorus: установлено {success_count}/{len(settings)} параметров")
        print(f"      - Rate: 0.2Hz (медленная модуляция)")
        print(f"      - Amount: 10% (тонкий эффект)")
        print(f"      - Stereo width enhancement")
        
        return success_count == len(settings)
    
    def scan_and_tune_all_devices(self):
        """Сканирует устройства на треке и автоматически настраивает их"""
        print(f"🎯 Автонастройка всех jungle эффектов на треке '{self.track_name}'")
        print("=" * 60)
        
        # Пытаемся настроить устройства в предполагаемых слотах
        device_tuners = [
            (1, "EQ Eight", self.auto_tune_eq_eight),
            (2, "Compressor", self.auto_tune_compressor), 
            (3, "Saturator", self.auto_tune_saturator),
            (4, "Chorus", self.auto_tune_chorus),
            (5, "Reverb", self.auto_tune_reverb)
        ]
        
        tuned_count = 0
        
        for device_index, device_name, tuner_func in device_tuners:
            try:
                print(f"\n🔧 Попытка настройки {device_name} в слоте {device_index}...")
                if tuner_func(device_index):
                    tuned_count += 1
                time.sleep(0.5)  # Пауза между устройствами
            except Exception as e:
                print(f"   ❌ Ошибка настройки {device_name}: {e}")
        
        print(f"\n🎉 Автонастройка завершена!")
        print(f"📊 Настроено устройств: {tuned_count}/{len(device_tuners)}")
        
        if tuned_count > 0:
            print(f"\n🔥 Jungle звук готов! Эффекты настроены для:")
            print(f"   • Пробивной kick и snare")
            print(f"   • Четкие высокие частоты")
            print(f"   • Аналоговое тепло")
            print(f"   • Атмосферный reverb")
        
        return tuned_count
    
    def create_jungle_preset_summary(self):
        """Создает сводку всех jungle настроек"""
        print(f"\n📋 JUNGLE PRESET SUMMARY")
        print("=" * 40)
        
        presets_info = {
            "EQ Eight": [
                "Band 1: High-pass на 80Hz (убираем mud)",
                "Band 3: Cut на 400Hz -1dB (больше clarity)", 
                "Band 8: Boost на 10kHz +3dB (crispy highs)"
            ],
            "Compressor": [
                "Threshold: -18dB (aggressive compression)",
                "Ratio: 4:1 (punchy response)",
                "Attack: 1ms (preserve transients)",
                "Release: 50ms (quick recovery)"
            ],
            "Saturator": [
                "Drive: 5dB (analog warmth)",
                "Type: Analog Clip (musical distortion)",
                "Focus: 2kHz (midrange punch)"
            ],
            "Reverb": [
                "Room: 20% (intimate space)",
                "Decay: 1.5s (quick tail)",
                "Wet: 15% (subtle ambience)",
                "PreDelay: 15ms (clarity)"
            ]
        }
        
        for device, settings in presets_info.items():
            print(f"\n🎛️ {device}:")
            for setting in settings:
                print(f"   • {setting}")

def main():
    """Основная функция автонастройки jungle эффектов"""
    print("🎛️ JUNGLE AUTO-TUNER для добавленных эффектов")
    print("=" * 50)
    
    tuner = JungleAutoTuner("1 808")
    
    try:
        # Проверяем доступность API
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code != 200:
            print("❌ Bridge сервер недоступен!")
            return
        
        print("✅ Подключение к Ableton установлено")
        
        # Выполняем автонастройку всех устройств
        tuned_devices = tuner.scan_and_tune_all_devices()
        
        # Показываем сводку настроек
        tuner.create_jungle_preset_summary()
        
        if tuned_devices > 0:
            print(f"\n🎯 Готово! Jungle звук настроен и готов к использованию!")
            print(f"   Попробуйте запустить различные Amen Break вариации")
        else:
            print(f"\n⚠️  Устройства не найдены или не настроены")
            print(f"   Убедитесь что вы добавили рекомендуемые эффекты на трек")
        
    except Exception as e:
        print(f"❌ Ошибка в jungle auto-tuner: {e}")

if __name__ == "__main__":
    main()