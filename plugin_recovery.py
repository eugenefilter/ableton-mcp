#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plugin Recovery Tool
Восстановление и диагностика отключенных плагинов
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

class PluginRecovery:
    """Инструмент для восстановления и диагностики плагинов"""
    
    def __init__(self, track_name="1 808"):
        self.track_name = track_name
    
    def enable_device(self, device_index):
        """Включает устройство (обычно параметр 0 - On/Off)"""
        try:
            # Пытаемся включить устройство через параметр 0 (обычно On/Off)
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index,
                    "param_index": 0,
                    "value": 1.0  # Включить
                },
                "id": f"enable_device_{device_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Ошибка включения устройства {device_index}: {e}")
            return False
    
    def safe_set_parameter(self, device_index, param_index, value, param_name=""):
        """Безопасная установка параметра с проверкой"""
        try:
            payload = {
                "action": "set_device_parameter", 
                "args": {
                    "track": self.track_name,
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": value
                },
                "id": f"safe_set_{device_index}_{param_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            success = response.status_code == 200
            
            if success:
                print(f"   ✅ {param_name} (param {param_index}) = {value}")
            else:
                print(f"   ❌ Ошибка установки {param_name}")
                
            return success
        except Exception as e:
            print(f"   ❌ Ошибка установки параметра: {e}")
            return False
    
    def recover_compressor(self, device_index):
        """Восстановление и безопасная настройка компрессора"""
        print(f"🔧 Восстанавливаю Compressor в слоте {device_index}...")
        
        # Сначала включаем устройство
        self.enable_device(device_index)
        time.sleep(0.2)
        
        # Консервативные настройки компрессора 
        # Используем параметры которые точно есть в стандартном Compressor
        settings = [
            # Основные параметры (осторожные значения)
            (1, 0.7, "Threshold"),      # Threshold -18dB
            (2, 0.25, "Ratio"),         # Ratio 4:1
            (3, 0.001, "Attack"),       # Attack 1ms 
            (4, 0.05, "Release"),       # Release 50ms
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name):
                success_count += 1
            time.sleep(0.2)
        
        print(f"   📊 Compressor: восстановлено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def recover_saturator(self, device_index):
        """Восстановление и безопасная настройка сатуратора"""
        print(f"🔥 Восстанавливаю Saturator в слоте {device_index}...")
        
        self.enable_device(device_index) 
        time.sleep(0.2)
        
        # Консервативные настройки сатуратора
        settings = [
            (1, 0.1, "Drive"),          # Небольшой drive
            (2, 0.5, "Base"),           # Base 50%
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name):
                success_count += 1
            time.sleep(0.2)
        
        print(f"   📊 Saturator: восстановлено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def recover_reverb(self, device_index):
        """Восстановление и безопасная настройка реверба"""
        print(f"🌊 Восстанавливаю Reverb в слоте {device_index}...")
        
        self.enable_device(device_index)
        time.sleep(0.2)
        
        # Консервативные настройки реверба
        settings = [
            (1, 0.2, "Room Size"),      # Room Size 20%
            (2, 0.15, "Dry/Wet"),       # Dry/Wet 15%
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name):
                success_count += 1
            time.sleep(0.2)
        
        print(f"   📊 Reverb: восстановлено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def recover_chorus(self, device_index):
        """Восстановление и безопасная настройка хоруса"""
        print(f"〰️ Восстанавливаю Chorus в слоте {device_index}...")
        
        self.enable_device(device_index)
        time.sleep(0.2)
        
        # Консервативные настройки хоруса
        settings = [
            (1, 0.1, "Rate"),           # Rate 0.5Hz
            (2, 0.15, "Amount"),        # Amount 15%
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name):
                success_count += 1
            time.sleep(0.2)
        
        print(f"   📊 Chorus: восстановлено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def recover_eq_eight(self, device_index):
        """Восстановление EQ Eight (если он тоже пострадал)"""
        print(f"🎚️ Восстанавливаю EQ Eight в слоте {device_index}...")
        
        self.enable_device(device_index)
        time.sleep(0.2)
        
        # Только основные параметры EQ
        settings = [
            (1, 1.0, "EQ On"),          # Включить EQ
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name):
                success_count += 1
            time.sleep(0.2)
        
        print(f"   📊 EQ Eight: восстановлено {success_count}/{len(settings)} параметров") 
        return success_count > 0
    
    def full_recovery(self):
        """Полное восстановление всех отключенных эффектов"""
        print("🚨 ВОССТАНОВЛЕНИЕ ОТКЛЮЧЕННЫХ ПЛАГИНОВ")
        print("=" * 50)
        
        # Пытаемся восстановить устройства в предполагаемых слотах
        recovery_tasks = [
            (1, "EQ Eight", self.recover_eq_eight),
            (2, "Compressor", self.recover_compressor),
            (3, "Saturator", self.recover_saturator), 
            (4, "Chorus", self.recover_chorus),
            (5, "Reverb", self.recover_reverb)
        ]
        
        recovered = 0
        
        for device_index, device_name, recovery_func in recovery_tasks:
            try:
                print(f"\n🔧 Попытка восстановления {device_name} в слоте {device_index}...")
                if recovery_func(device_index):
                    recovered += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"   ❌ Ошибка восстановления {device_name}: {e}")
        
        print(f"\n📊 ИТОГ ВОССТАНОВЛЕНИЯ:")
        print(f"   Восстановлено: {recovered}/{len(recovery_tasks)} устройств")
        
        if recovered > 0:
            print(f"\n✅ Плагины должны быть снова включены!")
            print(f"   Проверьте их состояние в Ableton")
        else:
            print(f"\n⚠️  Возможно потребуется ручное включение")
            print(f"   Включите плагины в Ableton и попробуйте еще раз")
            
        return recovered
    
    def create_safe_jungle_settings(self):
        """Создает безопасные jungle настройки без отключения"""
        print(f"\n🎯 БЕЗОПАСНЫЕ JUNGLE НАСТРОЙКИ")
        print("=" * 40)
        
        print("Вместо автоматической настройки, рекомендуем:")
        print("\n🎚️ EQ Eight (слот 1):")
        print("   • Band 1: High-pass на 80-100Hz")
        print("   • Band 8: Gentle boost на 8-12kHz (+2dB)")
        
        print("\n🎛️ Compressor (слот 2):")
        print("   • Threshold: -20 до -15dB")
        print("   • Ratio: 3:1 до 4:1") 
        print("   • Attack: 1-3ms")
        print("   • Release: 30-100ms")
        
        print("\n🔥 Saturator (слот 3):")
        print("   • Drive: 2-5dB")
        print("   • Type: Analog Clip")
        
        print("\n🌊 Reverb (слот 5):")
        print("   • Room Size: 15-25%")
        print("   • Dry/Wet: 10-20%")
        print("   • Decay: 1-2 seconds")

def main():
    """Основная функция восстановления"""
    print("🛠️  PLUGIN RECOVERY TOOL")
    print("=" * 30)
    
    recovery = PluginRecovery("1 808")
    
    try:
        # Проверяем доступность API
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code != 200:
            print("❌ Bridge сервер недоступен!")
            return
        
        print("✅ Подключение к Ableton установлено")
        
        # Восстанавливаем плагины
        recovered = recovery.full_recovery()
        
        # Показываем безопасные рекомендации
        recovery.create_safe_jungle_settings()
        
        print(f"\n💡 Следующие шаги:")
        print(f"1. Проверьте что плагины включены в Ableton")
        print(f"2. Настройте их вручную по рекомендациям выше")
        print(f"3. Избегайте автонастройки до улучшения системы")
        
    except Exception as e:
        print(f"❌ Ошибка восстановления: {e}")

if __name__ == "__main__":
    main()