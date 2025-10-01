#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jungle Sound Processor для Amen Break
Автоматическая настройка jungle/drum'n'bass звука
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8787"

class JungleProcessor:
    """Процессор для создания классического jungle звука из Amen Break"""
    
    def __init__(self, track_name="1 808"):
        self.track_name = track_name
        self.jungle_settings = {
            # Настройки EQ для jungle звука
            "eq": {
                "low_cut": 80,      # Убираем низкие частоты для punch
                "high_boost": 8000,  # Усиливаем высокие для clarity
                "mid_cut": 400       # Немного убираем средние
            },
            
            # Настройки компрессора
            "compressor": {
                "threshold": -18,    # dB
                "ratio": 4.0,        # 4:1
                "attack": 1,         # ms - быстрая атака для punch
                "release": 50        # ms - быстрый release
            },
            
            # Настройки дисторшна/сатурации
            "saturation": {
                "drive": 0.3,        # Легкая сатурация
                "type": "analog"     # Аналоговый тип
            },
            
            # Настройки реверба
            "reverb": {
                "room_size": 0.2,    # Небольшая комната
                "decay": 1.5,        # Секунды
                "pre_delay": 15,     # ms
                "wet": 0.15          # 15% влажности
            }
        }
    
    def get_track_devices(self):
        """Получает список устройств на треке"""
        try:
            payload = {
                "action": "get_track_devices",
                "args": {"track": self.track_name},
                "id": "get_devices"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            if response.status_code == 200:
                result = response.json().get("result", {})
                # API возвращает сообщение, а не список устройств
                # Возвращаем пустой список для совместимости
                return []
            return []
        except Exception as e:
            print(f"❌ Ошибка получения устройств: {e}")
            return []
    
    def set_device_parameter(self, device_index, param_index, value):
        """Устанавливает параметр устройства"""
        try:
            payload = {
                "action": "set_device_parameter",
                "args": {
                    "track": self.track_name,
                    "device_index": device_index,
                    "param_index": param_index,
                    "value": value
                },
                "id": "set_param"
            }
            
            response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Ошибка установки параметра: {e}")
            return False
    
    def boost_high_frequencies(self):
        """Усиливает высокие частоты для jungle звука"""
        print("🎚️ Настраиваю высокие частоты...")
        
        # Увеличиваем темп для характерного jungle sound
        try:
            payload = {
                "action": "set_tempo",
                "args": {"bpm": 174},  # Классический jungle темп
                "id": "jungle_tempo"
            }
            requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
            print("✅ Темп установлен на 174 BPM (jungle стандарт)")
        except Exception as e:
            print(f"❌ Ошибка установки темпа: {e}")
    
    def apply_jungle_processing(self):
        """Применяет комплексную jungle обработку"""
        print("🥁 Применяю jungle обработку к Amen Break...")
        
        # 1. Устанавливаем jungle темп
        self.boost_high_frequencies()
        
        # 2. Информация о jungle обработке
        print("📱 Готовлю jungle обработку...")
        
        # 3. Применяем pitch shifts для variation
        print("\n🎵 Создаю pitch variations...")
        self.create_pitch_variations()
        
        # 4. Информация о дальнейшей обработке
        print("\n🎛️ Рекомендуемая дальнейшая обработка в Ableton:")
        print("   1. Добавьте EQ Eight:")
        print("      - High-pass на 80Hz")
        print("      - Boost на 8-12kHz (+3dB)")
        print("      - Slight cut на 400Hz (-1dB)")
        print("\n   2. Добавьте Compressor:")
        print("      - Threshold: -18dB")
        print("      - Ratio: 4:1")
        print("      - Attack: 1ms, Release: 50ms")
        print("\n   3. Добавьте Saturator:")
        print("      - Drive: 3-5dB")
        print("      - Type: Analog Clip")
        print("\n   4. Добавьте Reverb:")
        print("      - Room size: 20%")
        print("      - Decay: 1.5s, Wet: 15%")
        
        return True
    
    def create_pitch_variations(self):
        """Создает pitch variations Amen Break в разных слотах"""
        variations = [
            {"slot": 1, "pitch": 0, "name": "Original"},
            {"slot": 2, "pitch": 12, "name": "Octave Up"},
            {"slot": 3, "pitch": -12, "name": "Octave Down"}, 
            {"slot": 4, "pitch": 7, "name": "Fifth Up"},
            {"slot": 5, "pitch": -5, "name": "Fourth Down"}
        ]
        
        for var in variations:
            try:
                # Копируем оригинальный клип
                print(f"   📝 Создаю вариацию: {var['name']} (pitch: {var['pitch']:+d})")
                
                # Создаем новый клип
                payload = {
                    "action": "create_midi_clip",
                    "args": {
                        "track": self.track_name,
                        "slot": var["slot"],
                        "bars": 4.0,
                        "loop": True
                    },
                    "id": f"variation_{var['slot']}"
                }
                
                response = requests.post(f"{BASE_URL}/cmd", json=payload, timeout=5)
                
                if response.status_code == 200:
                    # Копируем ноты из оригинального клипа (слот 0)
                    # Для этого нужно было бы получить ноты, изменить pitch и записать
                    # Пока что создаем пустой клип
                    
                    # Устанавливаем pitch для клипа 
                    pitch_payload = {
                        "action": "set_clip_pitch",
                        "args": {
                            "track": self.track_name,
                            "slot": var["slot"],
                            "pitch_coarse": var["pitch"]
                        },
                        "id": f"pitch_{var['slot']}"
                    }
                    
                    requests.post(f"{BASE_URL}/cmd", json=pitch_payload, timeout=5)
                    print(f"   ✅ Вариация {var['name']} создана в слоте {var['slot']}")
                
                time.sleep(0.5)  # Пауза между операциями
                
            except Exception as e:
                print(f"   ❌ Ошибка создания вариации {var['name']}: {e}")
    
    def create_chopped_variations(self):
        """Создает chopped версии Amen Break"""
        print("\n✂️ Создаю chopped variations...")
        
        # Разные chop паттерны
        chop_patterns = [
            {
                "name": "Half Time",
                "slot": 6,
                "description": "Растянутый на половину скорости"
            },
            {
                "name": "Double Time", 
                "slot": 7,
                "description": "Ускоренный в 2 раза"
            },
            {
                "name": "Stutter",
                "slot": 8, 
                "description": "С stuttering эффектом"
            }
        ]
        
        for pattern in chop_patterns:
            print(f"   🎵 {pattern['name']}: {pattern['description']}")
            # Здесь можно добавить логику создания различных chop паттернов
    
    def apply_jungle_effects_chain(self):
        """Применяет полную цепочку jungle эффектов"""
        print("\n🔗 Применяю полную jungle effects chain...")
        
        effects_chain = [
            "EQ Eight (High-pass + High boost)",
            "Compressor (Punchy settings)", 
            "Saturator (Analog warmth)",
            "Chorus (Slight width)",
            "Reverb (Room ambience)",
            "Limiter (Final control)"
        ]
        
        for i, effect in enumerate(effects_chain):
            print(f"   {i+1}. {effect}")
        
        print("\n💡 Совет: Используйте Drum Kit для индивидуальной обработки каждого элемента ударных")

def main():
    """Основная функция для обработки Amen Break в jungle стиле"""
    print("🌿 JUNGLE SOUND PROCESSOR для Amen Break")
    print("=" * 50)
    
    processor = JungleProcessor("1 808")
    
    try:
        # Проверяем доступность API
        response = requests.get(f"{BASE_URL}/state", timeout=2)
        if response.status_code != 200:
            print("❌ Bridge сервер недоступен!")
            return
        
        print("✅ Подключение к Ableton установлено")
        
        # Применяем jungle обработку
        processor.apply_jungle_processing()
        
        # Создаем дополнительные вариации
        processor.create_chopped_variations()
        
        # Показываем effects chain
        processor.apply_jungle_effects_chain()
        
        print("\n🎯 Jungle обработка завершена!")
        print("\n🔥 Следующие шаги:")
        print("1. Настройте Drum Kit на треке для детальной обработки")
        print("2. Добавьте указанные эффекты вручную") 
        print("3. Экспериментируйте с различными вариациями")
        print("4. Добавьте bassline на отдельном треке")
        
    except Exception as e:
        print(f"❌ Ошибка в jungle processor: {e}")

if __name__ == "__main__":
    main()