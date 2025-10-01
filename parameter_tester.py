#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parameter Tester - Тестирование настройки конкретных параметров
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8787"

class ParameterTester:
    """Тестер для настройки конкретных параметров устройств"""
    
    def __init__(self, track_name="1 808"):
        self.track_name = track_name
    
    def get_device_parameters(self, device_index):
        """Получаем список параметров устройства"""
        try:
            payload = {
                "action": "get_device_parameters",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index
                },
                "id": f"get_params_{device_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    return data.get("result", {})
            return None
        except Exception as e:
            print(f"❌ Ошибка получения параметров: {e}")
            return None
    
    def set_parameter(self, device_index, param_index, value, description=""):
        """Устанавливаем конкретный параметр"""
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": value
                },
                "id": f"set_param_{device_index}_{param_index}"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            success = response.status_code == 200
            
            if success:
                result = response.json()
                print(f"✅ Параметр установлен: {description}")
                print(f"   Устройство: слот {device_index}, параметр {param_index} = {value}")
                return True
            else:
                print(f"❌ Ошибка установки параметра: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    def test_saturator_bass(self, bass_value=-5):
        """Тестируем настройку Bass в Saturator"""
        print(f"🔥 ТЕСТ НАСТРОЙКИ SATURATOR BASS")
        print("=" * 40)
        
        device_index = 3  # Saturator в слоте 3
        
        # Сначала посмотрим доступные параметры
        print(f"📋 Получаю параметры Saturator (слот {device_index})...")
        params = self.get_device_parameters(device_index)
        
        if params:
            print(f"📊 Найдено параметров: {len(params)}")
            for i, (param_name, param_info) in enumerate(params.items()):
                value = param_info.get('value', 'N/A')
                min_val = param_info.get('min', 'N/A') 
                max_val = param_info.get('max', 'N/A')
                print(f"   {i}: {param_name} = {value} (range: {min_val} - {max_val})")
        
        # Ищем параметр Bass
        bass_param_index = None
        if params:
            for i, (param_name, param_info) in enumerate(params.items()):
                if 'bass' in param_name.lower() or 'base' in param_name.lower():
                    bass_param_index = i
                    print(f"\n🎯 Найден Bass параметр: индекс {i} = '{param_name}'")
                    break
        
        if bass_param_index is None:
            print(f"\n🔍 Bass параметр не найден автоматически. Пробую стандартные индексы...")
            # Пробуем известные индексы для Saturator Bass
            test_indices = [2, 3, 4]  # Обычно Bass находится в этих позициях
            
            for test_idx in test_indices:
                print(f"\n🧪 Тестирую индекс {test_idx} как Bass...")
                
                # Конвертируем -5dB в normalized значение (примерно)
                # Bass в Saturator обычно от -30 до +30, так что -5 это примерно 0.42
                normalized_value = (bass_value + 30) / 60  # -5 -> 25/60 = 0.417
                
                success = self.set_parameter(
                    device_index, 
                    test_idx, 
                    normalized_value, 
                    f"Bass = {bass_value}dB (normalized: {normalized_value:.3f})"
                )
                
                if success:
                    print(f"✅ Параметр {test_idx} установлен успешно!")
                    return True
        else:
            # Устанавливаем найденный Bass параметр
            normalized_value = (bass_value + 30) / 60
            success = self.set_parameter(
                device_index,
                bass_param_index,
                normalized_value,
                f"Bass = {bass_value}dB"
            )
            return success
        
        print(f"❌ Не удалось найти или установить Bass параметр")
        return False
    
    def show_all_saturator_params(self):
        """Показать все параметры Saturator для отладки"""
        print(f"\n🔍 ВСЕ ПАРАМЕТРЫ SATURATOR")
        print("=" * 35)
        
        params = self.get_device_parameters(3)  # Saturator в слоте 3
        
        if params:
            print(f"Тип полученных данных: {type(params)}")
            print(f"Данные: {params}")
            
            # Проверяем формат данных
            if isinstance(params, dict):
                for i, (param_name, param_info) in enumerate(params.items()):
                    if isinstance(param_info, dict):
                        value = param_info.get('value', 'N/A')
                        min_val = param_info.get('min', 'N/A')
                        max_val = param_info.get('max', 'N/A')
                        print(f"{i:2d}: {param_name:<15} = {value:<8} [{min_val} - {max_val}]")
                    else:
                        # Если param_info это строка или другой тип
                        print(f"{i:2d}: {param_name:<15} = {param_info}")
            elif isinstance(params, list):
                for i, param in enumerate(params):
                    print(f"{i:2d}: {param}")
        else:
            print("❌ Не удалось получить параметры Saturator")

def main():
    """Основная функция тестера"""
    tester = ParameterTester("1 808")
    
    print("🧪 PARAMETER TESTER")
    print("=" * 20)
    
    # Показываем все параметры Saturator
    tester.show_all_saturator_params()
    
    # Тестируем установку Bass на -5dB
    print(f"\n" + "=" * 50)
    success = tester.test_saturator_bass(-5)
    
    if success:
        print(f"\n🎉 ТЕСТ УСПЕШЕН!")
        print(f"   Saturator Bass установлен на -5dB")
        print(f"   Проверьте изменения в Ableton Live")
    else:
        print(f"\n❌ ТЕСТ НЕ ПРОЙДЕН!")
        print(f"   Нужно найти правильный индекс Bass параметра")

if __name__ == "__main__":
    main()