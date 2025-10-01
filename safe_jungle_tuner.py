#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Safe Jungle Auto-Tuner v2.0
Безопасная автонастройка jungle эффектов без отключения плагинов
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

class SafeJungleAutoTuner:
    """Безопасный автонастройщик jungle эффектов"""
    
    def __init__(self, track_name="1 808"):
        self.track_name = track_name
        
    def safe_set_parameter(self, device_index, param_index, value, param_name="", device_name=""):
        """Безопасная установка параметра с проверкой и логированием"""
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": value
                },
                "id": f"safe_tune_{device_index}_{param_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            success = response.status_code == 200
            
            if success:
                print(f"   ✅ {device_name} {param_name} = {value:.3f}")
            else:
                print(f"   ❌ Ошибка: {device_name} {param_name}")
                
            return success
        except Exception as e:
            print(f"   ❌ Ошибка установки параметра {param_name}: {e}")
            return False
    
    def gentle_eq_tuning(self, device_index):
        """Мягкая настройка EQ Eight для jungle"""
        print(f"🎚️ Настраиваю EQ Eight (слот {device_index}) - консервативно...")
        
        # Используем только основные параметры которые точно есть
        # Избегаем параметр 0 который может быть On/Off
        success_count = 0
        
        # Пропускаем первый параметр (0) - может быть On/Off
        # Настраиваем только основные частотные параметры
        
        print("   💡 Рекомендация: настройте EQ вручную:")
        print("      - Band 1: High-pass на 80Hz")
        print("      - Band 8: Slight boost на 8-12kHz (+2dB)")
        
        return True
    
    def gentle_compressor_tuning(self, device_index):
        """Мягкая настройка Compressor для jungle"""
        print(f"🎛️ Настраиваю Compressor (слот {device_index}) - осторожно...")
        
        # Используем консервативные значения
        settings = [
            # Избегаем param 0 (может быть On/Off)
            (1, 0.75, "Threshold (~-15dB)"),    # Более мягкий threshold
            (2, 0.2, "Ratio (~3:1)"),           # Более мягкий ratio
            (3, 0.02, "Attack (~5ms)"),         # Чуть медленнее attack
            (4, 0.08, "Release (~80ms)"),       # Чуть медленнее release
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name, "Compressor"):
                success_count += 1
            time.sleep(0.3)  # Больше времени между изменениями
        
        print(f"   📊 Compressor: настроено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def gentle_saturator_tuning(self, device_index):
        """Мягкая настройка Saturator для jungle"""
        print(f"🔥 Настраиваю Saturator (слот {device_index}) - деликатно...")
        
        settings = [
            # Избегаем param 0
            (1, 0.08, "Drive (~3dB)"),          # Мягкий drive
            (2, 0.5, "Base (50%)"),             # Нейтральная база
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name, "Saturator"):
                success_count += 1
            time.sleep(0.3)
        
        print(f"   📊 Saturator: настроено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def gentle_reverb_tuning(self, device_index):
        """Мягкая настройка Reverb для jungle"""
        print(f"🌊 Настраиваю Reverb (слот {device_index}) - аккуратно...")
        
        settings = [
            # Избегаем param 0
            (1, 0.18, "Room Size (~18%)"),      # Небольшая комната
            (2, 0.12, "Dry/Wet (~12%)"),        # Мало влажности
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name, "Reverb"):
                success_count += 1
            time.sleep(0.3)
        
        print(f"   📊 Reverb: настроено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def gentle_chorus_tuning(self, device_index):
        """Мягкая настройка Chorus для jungle"""
        print(f"〰️ Настраиваю Chorus (слот {device_index}) - нежно...")
        
        settings = [
            # Избегаем param 0
            (1, 0.05, "Rate (~0.2Hz)"),         # Очень медленная модуляция
            (2, 0.1, "Amount (~10%)"),          # Легкий эффект
        ]
        
        success_count = 0
        for param_idx, value, name in settings:
            if self.safe_set_parameter(device_index, param_idx, value, name, "Chorus"):
                success_count += 1
            time.sleep(0.3)
        
        print(f"   📊 Chorus: настроено {success_count}/{len(settings)} параметров")
        return success_count > 0
    
    def safe_jungle_tuning(self):
        """Безопасная настройка всех jungle эффектов"""
        print("🛡️  SAFE JUNGLE AUTO-TUNER v2.0")
        print("=" * 45)
        print("⚠️  Консервативный режим - без отключения плагинов")
        
        # Проверяем доступность API
        try:
            response = requests.get(f"{BASE_URL}/state", timeout=2)
            if response.status_code != 200:
                print("❌ Bridge сервер недоступен!")
                return
        except:
            print("❌ Не могу подключиться к bridge серверу!")
            return
        
        print("✅ Подключение к Ableton установлено")
        
        # Мягкая настройка устройств
        tuning_tasks = [
            (1, "EQ Eight", self.gentle_eq_tuning),
            (2, "Compressor", self.gentle_compressor_tuning),
            (3, "Saturator", self.gentle_saturator_tuning),
            (4, "Chorus", self.gentle_chorus_tuning),
            (5, "Reverb", self.gentle_reverb_tuning)
        ]
        
        tuned_count = 0
        
        for device_index, device_name, tuner_func in tuning_tasks:
            try:
                print(f"\n🔧 {device_name} в слоте {device_index}...")
                if tuner_func(device_index):
                    tuned_count += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"   ❌ Ошибка настройки {device_name}: {e}")
        
        print(f"\n📊 ИТОГ БЕЗОПАСНОЙ НАСТРОЙКИ:")
        print(f"   Обработано устройств: {tuned_count}/{len(tuning_tasks)}")
        
        if tuned_count > 0:
            print(f"\n✅ Jungle эффекты настроены!")
            print(f"   Проверьте результат в Ableton")
        
        # Показываем рекомендации для ручной доводки
        self.show_manual_recommendations()
        
        return tuned_count
    
    def show_manual_recommendations(self):
        """Показывает рекомендации для ручной доводки"""
        print(f"\n🎯 РЕКОМЕНДАЦИИ ДЛЯ РУЧНОЙ ДОВОДКИ:")
        print("=" * 40)
        
        recommendations = {
            "EQ Eight (слот 1)": [
                "• Band 1: High-pass на 80-100Hz (убрать mud)",
                "• Band 8: Boost на 8-12kHz +2dB (яркость)",
                "• Band 3: Легкий cut на 400Hz -1dB (clarity)"
            ],
            "Compressor (слот 2)": [
                "• Threshold: -18 до -15dB (для punch)",
                "• Ratio: 3:1 до 4:1 (контроль динамики)",
                "• Attack: 1-5ms (сохранить transients)",
                "• Release: 30-100ms (быстрое восстановление)"
            ],
            "Saturator (слот 3)": [
                "• Drive: 2-5dB (аналоговое тепло)",
                "• Type: Analog Clip (музыкальность)",
                "• Base/Frequency: по вкусу"
            ],
            "Reverb (слот 5)": [
                "• Room Size: 15-25% (интимность)",
                "• Decay: 1-2s (быстрый хвост)",
                "• Dry/Wet: 10-20% (атмосфера)",
                "• PreDelay: 10-20ms (четкость)"
            ],
            "Chorus (слот 4)": [
                "• Rate: 0.2-1Hz (медленная модуляция)",
                "• Amount: 10-20% (тонкий эффект)",
                "• Для stereo width"
            ]
        }
        
        for device, tips in recommendations.items():
            print(f"\n🎛️ {device}:")
            for tip in tips:
                print(f"   {tip}")
    
    def emergency_enable_all(self):
        """Экстренное включение всех устройств"""
        print(f"\n🚨 ЭКСТРЕННОЕ ВКЛЮЧЕНИЕ ВСЕХ УСТРОЙСТВ")
        print("=" * 40)
        
        device_slots = [1, 2, 3, 4, 5]  # EQ, Comp, Sat, Chorus, Reverb
        enabled_count = 0
        
        for slot in device_slots:
            try:
                # Пытаемся включить через параметр 0 (обычно On/Off)
                if self.safe_set_parameter(slot, 0, 1.0, "Device On", f"Slot {slot}"):
                    enabled_count += 1
                time.sleep(0.2)
            except Exception as e:
                print(f"   ❌ Ошибка включения слота {slot}: {e}")
        
        print(f"\n📊 Включено слотов: {enabled_count}/{len(device_slots)}")
        return enabled_count

def main():
    """Основная функция безопасной автонастройки"""
    tuner = SafeJungleAutoTuner("1 808")
    
    try:
        # Выполняем безопасную настройку
        tuned = tuner.safe_jungle_tuning()
        
        print(f"\n💡 ВАЖНЫЕ ЗАМЕЧАНИЯ:")
        print(f"1. Эта версия использует консервативные настройки")
        print(f"2. Плагины должны остаться включенными")
        print(f"3. Доводите звук вручную по рекомендациям выше")
        print(f"4. При проблемах используйте: python plugin_recovery.py")
        
    except Exception as e:
        print(f"❌ Ошибка в safe jungle tuner: {e}")

if __name__ == "__main__":
    main()