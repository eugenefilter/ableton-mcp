#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saturator Step-by-Step Analyzer - Пошаговый анализ каждого параметра Saturator
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

class SaturatorAnalyzer:
    """Пошаговый анализатор Saturator параметров"""
    
    def __init__(self, track_name="1 808", device_index=3):
        self.track_name = track_name
        self.device_index = device_index
        self.saturator_params = {}
    
    def test_parameter(self, param_index, test_value, param_name="Unknown"):
        """Тестирует один параметр и записывает результат"""
        
        print(f"\n🎛️ ТЕСТ ПАРАМЕТРА {param_index} ({param_name})")
        print(f"   Устанавливаю значение: {test_value}")
        
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": self.track_name,
                    "device_index": self.device_index,
                    "param_index": param_index,
                    "value": test_value
                },
                "id": f"saturator_test_{param_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print(f"   ✅ Команда отправлена")
                    time.sleep(0.3)  # Даем время на применение
                    
                    actual = input(f"   ❓ Что показывает {param_name} в Saturator? ")
                    
                    self.saturator_params[param_index] = {
                        "name": param_name,
                        "test_value": test_value,
                        "actual_result": actual
                    }
                    
                    print(f"   📝 Записано: {param_name} = {actual}")
                    return True
                else:
                    print(f"   ❌ API ошибка: {result}")
            else:
                print(f"   ❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Исключение: {e}")
        
        return False
    
    def full_saturator_analysis(self):
        """Полный анализ всех параметров Saturator"""
        
        print(f"🔍 ПОЛНЫЙ АНАЛИЗ SATURATOR")
        print(f"Устройство: слот {self.device_index}")
        print("=" * 50)
        
        # Известные параметры Saturator с тестовыми значениями
        test_params = [
            (0, 1.0, "Device On/Off"),
            (1, 5.0, "Drive"),
            (2, 50.0, "Base/Frequency/Depth?"),
            (3, 2000.0, "Frequency/Base/Width?"),
            (4, 100.0, "Width/Depth/Color?"),
            (5, -5.0, "Base (мы знаем что это Base)"),
            (6, 0.5, "Dry/Wet?"),
            (7, 1.0, "Color/Type?"),
        ]
        
        print(f"🎯 Тестируем каждый параметр по очереди:")
        print(f"   После каждого теста смотрите что изменилось в Saturator")
        
        for param_index, test_value, param_description in test_params:
            success = self.test_parameter(param_index, test_value, param_description)
            
            if not success:
                print(f"   ⚠️ Параметр {param_index} не удалось протестировать")
            
            # Пауза между тестами
            if param_index < len(test_params) - 1:
                input(f"\n   ⏸️ Нажмите Enter для следующего параметра...")
        
        print(f"\n📊 РЕЗУЛЬТАТЫ АНАЛИЗА:")
        self.print_analysis_summary()
    
    def print_analysis_summary(self):
        """Выводит сводку по всем протестированным параметрам"""
        
        print("=" * 60)
        print("📋 КАРТА ПАРАМЕТРОВ SATURATOR:")
        print("=" * 60)
        
        if not self.saturator_params:
            print("❌ Нет данных о параметрах")
            return
        
        for param_index, info in self.saturator_params.items():
            print(f"{param_index:2d}: {info['name']:<20} | Тест: {info['test_value']:<10} | Результат: {info['actual_result']}")
        
        print(f"\n🎯 РЕКОМЕНДАЦИИ ДЛЯ jungle_auto_tuner.py:")
        self.generate_jungle_recommendations()
    
    def generate_jungle_recommendations(self):
        """Генерирует рекомендации для jungle настроек"""
        
        print("=" * 50)
        
        jungle_settings = []
        
        for param_index, info in self.saturator_params.items():
            param_name = info['name']
            result = info['actual_result'].lower()
            
            # Определяем jungle значения на основе результатов
            if 'drive' in result or 'драйв' in result:
                jungle_settings.append(f'{{"param": {param_index}, "value": 5.0}}    # Drive: 5dB')
            elif 'base' in result or 'бейс' in result or '-5' in result:
                jungle_settings.append(f'{{"param": {param_index}, "value": -5.0}}   # Base: -5dB')
            elif 'frequency' in result or 'частота' in result or '2000' in result:
                jungle_settings.append(f'{{"param": {param_index}, "value": 2000}}   # Frequency: 2kHz')
            elif 'width' in result or 'ширина' in result or '100' in result:
                jungle_settings.append(f'{{"param": {param_index}, "value": 100}}    # Width: 100%')
            elif 'depth' in result or 'глубина' in result or '50' in result:
                jungle_settings.append(f'{{"param": {param_index}, "value": 50}}     # Depth: 50%')
            elif param_index == 0:  # On/Off пропускаем
                continue
        
        if jungle_settings:
            print(f"\"Saturator\": {{")
            print(f"    \"jungle_settings\": [")
            print(f"        # Пропускаем param 0 (On/Off)")
            for setting in jungle_settings:
                print(f"        {setting}")
            print(f"    ]")
            print(f"}},")
        else:
            print("❌ Не удалось определить параметры для jungle настроек")
    
    def quick_base_test(self):
        """Быстрый тест только Base параметра"""
        
        print(f"⚡ БЫСТРЫЙ ТЕСТ BASE ПАРАМЕТРА")
        print("=" * 35)
        
        # Мы знаем что Base это параметр 5
        base_param = 5
        
        test_values = [-10.0, -5.0, 0.0, 5.0, 10.0]
        
        print(f"🎯 Тестирую разные значения для Base (параметр {base_param}):")
        
        for value in test_values:
            success = self.test_parameter(base_param, value, f"Base = {value}dB")
            
            if success:
                time.sleep(1)
            else:
                break
        
        print(f"\n💡 Найдите значение которое дает нужный Base для jungle")

def main():
    """Основная функция анализатора"""
    
    print("🔬 SATURATOR STEP-BY-STEP ANALYZER")
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
    
    analyzer = SaturatorAnalyzer("1 808", 3)
    
    print(f"\n🎯 ВЫБЕРИТЕ РЕЖИМ АНАЛИЗА:")
    print(f"1. Полный анализ всех параметров")
    print(f"2. Быстрый тест только Base")
    
    try:
        choice = input("Введите номер (1 или 2): ")
        
        if choice == "1":
            analyzer.full_saturator_analysis()
        elif choice == "2":
            analyzer.quick_base_test()
        else:
            print("❌ Неверный выбор")
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️ Анализ прерван пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()