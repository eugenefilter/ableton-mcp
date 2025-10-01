#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOM-Based Parameter Calibrator - Правильная работа с параметрами через Live Object Model
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8787"

class LOMParameterCalibrator:
    """Калибратор параметров с использованием Live Object Model свойств"""
    
    def __init__(self, track_name="1 808"):
        self.track_name = track_name
    
    def get_parameter_info(self, device_index, param_index):
        """Получить полную информацию о параметре включая min/max"""
        try:
            # Сначала пробуем получить информацию о параметре
            # В нашем API пока нет прямого доступа к min/max, но можем попробовать
            
            payload = {
                "action": "get_device_parameters",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index
                },
                "id": f"param_info_{device_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                print(f"📊 Информация о параметрах устройства {device_index}:")
                print(f"   Ответ API: {result}")
                return result
            
            return None
            
        except Exception as e:
            print(f"❌ Ошибка получения информации о параметре: {e}")
            return None
    
    def calibrate_saturator_base(self):
        """Правильная калибровка Base параметра Saturator"""
        
        print(f"🎛️ КАЛИБРОВКА SATURATOR BASE С LOM")
        print("=" * 45)
        
        device_index = 3  # Saturator
        base_param_index = 5  # Мы знаем что это правильный индекс
        
        # Получаем информацию о параметре
        param_info = self.get_parameter_info(device_index, base_param_index)
        
        print(f"\n🔍 Анализ Base параметра (индекс {base_param_index}):")
        
        # Согласно документации Ableton, Base обычно имеет диапазон 0-100
        # Но может быть и в dB (-30 до +30)
        
        # Тестируем различные подходы к значениям
        test_approaches = [
            {
                "name": "Прямое dB значение", 
                "value": -5.0,
                "description": "Если параметр принимает прямые dB значения"
            },
            {
                "name": "Процентный подход",
                "value": 45.0,  # 45% от 100 может соответствовать -5dB
                "description": "Если Base это процент от 0 до 100"
            },
            {
                "name": "Нормализованный в диапазоне dB",
                "value": 25.0,  # -5dB в диапазоне -30 до +30 = 25
                "description": "Если Base в dB но с offset"
            }
        ]
        
        for approach in test_approaches:
            try:
                print(f"\n🧪 Тестирую: {approach['name']}")
                print(f"   Значение: {approach['value']}")
                print(f"   Логика: {approach['description']}")
                
                payload = {
                    "action": "set_device_parameter",
                    "args": {
                        "track": self.track_name,
                        "device_index": device_index,
                        "param_index": base_param_index,
                        "value": approach['value']
                    },
                    "id": f"calibrate_base_{approach['value']}"
                }
                
                response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        print(f"   ✅ Установлено: {approach['value']}")
                        
                        actual = input(f"   ❓ Какой Base показывает в GUI? ")
                        
                        if '-5' in actual or '5.0' in actual:
                            print(f"   🎉 НАЙДЕНО! Используйте значение: {approach['value']}")
                            return approach['value']
                        else:
                            print(f"   📝 Результат: {actual}")
                    else:
                        print(f"   ❌ API ошибка")
                else:
                    print(f"   ❌ HTTP ошибка")
                    
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        return None
    
    def reverse_engineer_parameter_mapping(self, device_index, param_index, target_display_value):
        """Обратная инженерия для поиска правильного API значения"""
        
        print(f"\n🔬 ОБРАТНАЯ ИНЖЕНЕРИЯ ПАРАМЕТРА")
        print(f"   Устройство: {device_index}, Параметр: {param_index}")
        print(f"   Цель: получить {target_display_value} в GUI")
        print("=" * 50)
        
        # Бинарный поиск правильного значения
        low = -100.0
        high = 100.0
        tolerance = 0.1
        
        for iteration in range(20):  # Максимум 20 итераций
            
            test_value = (low + high) / 2
            
            try:
                payload = {
                    "action": "set_device_parameter",
                    "args": {
                        "track": self.track_name,
                        "device_index": device_index,
                        "param_index": param_index,
                        "value": test_value
                    },
                    "id": f"reverse_eng_{iteration}"
                }
                
                print(f"\n🎯 Итерация {iteration + 1}: тестирую {test_value:.3f}")
                
                response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        
                        actual = input(f"   Какое значение показывает GUI? (или 'q' для выхода): ")
                        
                        if actual == 'q':
                            break
                        
                        try:
                            actual_float = float(actual)
                            
                            print(f"   📊 {test_value:.3f} -> GUI: {actual_float}")
                            
                            if abs(actual_float - target_display_value) <= tolerance:
                                print(f"   🎉 НАЙДЕНО! Для GUI {target_display_value}: используйте API значение {test_value:.3f}")
                                return test_value
                            elif actual_float > target_display_value:
                                # GUI слишком высокое, уменьшаем API значение
                                high = test_value
                            else:
                                # GUI слишком низкое, увеличиваем API значение
                                low = test_value
                                
                        except ValueError:
                            print(f"   ⚠️ Введите число или 'q'")
                            
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                break
        
        return None

def main():
    """Основная функция калибровки с LOM подходом"""
    
    print("🔬 LOM-BASED PARAMETER CALIBRATOR")
    print("=" * 40)
    print("Используем знания о Live Object Model для правильной калибровки")
    
    calibrator = LOMParameterCalibrator("1 808")
    
    try:
        # Проверяем подключение
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code != 200:
            print("❌ Bridge сервер недоступен!")
            return
        
        print("✅ Подключение установлено")
        
        # Калибруем Base параметр с пониманием LOM
        print(f"\n🎯 ЦЕЛЬ: Base = -5.0dB в Saturator")
        
        base_value = calibrator.calibrate_saturator_base()
        
        if not base_value:
            print(f"\n🔍 Запускаю обратную инженерию...")
            base_value = calibrator.reverse_engineer_parameter_mapping(3, 5, -5.0)
        
        if base_value:
            print(f"\n✅ КАЛИБРОВКА ЗАВЕРШЕНА!")
            print(f"   Для Base = -5.0dB используйте: {base_value}")
            
            # Обновляем jungle_auto_tuner.py
            print(f"\n📝 Обновите jungle_auto_tuner.py:")
            print(f'   {{"param": 5, "value": {base_value}}}  # Base (-5dB)')
        else:
            print(f"\n❌ Не удалось найти правильное значение")
        
    except Exception as e:
        print(f"❌ Ошибка в LOM calibrator: {e}")

if __name__ == "__main__":
    main()