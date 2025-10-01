# -*- coding: utf-8 -*-
# MyAgent/__init__.py — Версия 4.0 (с исправленным логированием)

from __future__ import absolute_import, print_function, unicode_literals
import logging

# --- Настройка логирования ---
# Это правильный способ писать в Log.txt Ableton
log = logging.getLogger(__name__)

from ableton.v2.control_surface import ControlSurface
from ableton.v2.control_surface.capabilities import (
    CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT,
    controller_id, inport, outport
)

UDP_IP = "127.0.0.1"
UDP_PORT = 8788

def get_capabilities():
    return {
        CONTROLLER_ID_KEY: controller_id(vendor_id=0, product_ids=[], model_name="MyAgent"),
        PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), outport(props=[SCRIPT])],
    }

class MyAgent(ControlSurface):
    def __init__(self, c_instance):
        super(MyAgent, self).__init__(c_instance)
        self._running = False
        self._sock = None
        self._thread = None

        self.show_message("MyAgent Initializing...")
        self._start_udp()

    def disconnect(self):
        self._stop_udp()
        self.show_message("MyAgent Disconnected")
        super(MyAgent, self).disconnect()

    def _start_udp(self):
        try:
            import socket, threading
            self._socket_mod = socket

            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.bind((UDP_IP, UDP_PORT))
            self._sock.settimeout(0.5)

            self._running = True
            self._thread = threading.Thread(target=self._udp_loop)
            self._thread.daemon = True
            self._thread.start()
            log.info("MyAgent: UDP server started at %s:%s", UDP_IP, UDP_PORT)
            self.show_message("MyAgent Ready")
        except Exception as e:
            log.error("MyAgent: UDP init error: %s", e, exc_info=True)
            self.show_message("MyAgent UDP FAILED")

    def _stop_udp(self):
        self._running = False
        if self._thread:
            self._thread.join(0.5)
        if self._sock:
            self._sock.close()

    def _udp_loop(self):
        while self._running:
            try:
                data, _ = self._sock.recvfrom(4096)
                if data:
                    self.schedule_message(0, self._handle_payload, data.decode("utf-8", "ignore"))
            except self._socket_mod.timeout:
                continue
            except Exception:
                self._running = False

    def _handle_payload(self, payload):
        try:
            import json
            msg = json.loads(payload)
        except Exception:
            log.error("MyAgent: Received bad JSON: %s", payload)
            return

        action = msg.get("action")
        args = msg.get("args") or {}
        fn = getattr(self, "_action_" + str(action), None)

        if callable(fn):
            try:
                fn(**args)
            except Exception as e:
                log.error("MyAgent: Handler '%s' error: %s", action, e, exc_info=True)
        else:
            log.warning("MyAgent: No handler for action '%s'", action)

    # --- Обработчики команд (с префиксом _action_) ---

    def _action_request_state(self, reply_port):
        """Собирает состояние проекта и отправляет его обратно на указанный порт."""
        log.info("MyAgent: Handling request_state, will reply to port %s", reply_port)
        try:
            state = {
                "tempo": self.song.tempo,
                "is_playing": self.song.is_playing,
                "tracks": []
            }
            for t in self.song.tracks:
                state["tracks"].append({
                    "name": t.name,
                    "is_armed": t.arm
                })
            
            import json, socket
            reply_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            reply_sock.sendto(json.dumps(state).encode('utf-8'), (UDP_IP, reply_port))
            log.info("MyAgent: Sent state back to port %s", reply_port)

        except Exception as e:
            log.error("MyAgent: Error in _action_request_state: %s", e, exc_info=True)

    def _action_play(self):
        self.song.start_playing()
        log.info("MyAgent: Action - Play")

    def _action_stop(self):
        self.song.stop_playing()
        log.info("MyAgent: Action - Stop")

    def _action_set_tempo(self, bpm):
        self.song.tempo = float(bpm)
        log.info("MyAgent: Action - Set Tempo to %s", bpm)

    def _find_track(self, track_name):
        for t in self.song.tracks:
            if t.name == track_name:
                return t
        log.error("MyAgent: Track '%s' not found.", track_name)
        return None

    def _action_create_midi_clip(self, track, slot, bars, loop):
        target_track = self._find_track(track)
        if target_track:
            clip_slot = target_track.clip_slots[slot]
            clip_slot.create_clip(bars)
            clip_slot.clip.looping = loop
            log.info("MyAgent: Created MIDI clip in track '%s', slot %s", track, slot)

    def _action_set_clip_notes(self, track, slot, notes):
        target_track = self._find_track(track)
        if target_track and target_track.clip_slots[slot].has_clip:
            try:
                # Оборачиваем изменение в Undo Step - это может быть ключом к решению
                self.song.begin_undo_step()
                clip = target_track.clip_slots[slot].clip
                notes_tuple = tuple((n['p'], n['s'], n['d'], n['v'], False) for n in notes)
                clip.set_notes(notes_tuple)
                log.info("MyAgent: Set %d notes in track '%s', slot %s", len(notes), track, slot)
            except Exception as e:
                log.error("MyAgent: Error in set_clip_notes: %s", e, exc_info=True)
            finally:
                self.song.end_undo_step()

    def _action_add_notes(self, track, slot, notes):
        import Live
        target_track = self._find_track(track)
        if target_track and target_track.clip_slots[slot].has_clip:
            try:
                self.song.begin_undo_step()
                clip = target_track.clip_slots[slot].clip
                # Используем MidiNoteSpecification, как того требует add_notes
                note_specs = [Live.Clip.MidiNoteSpecification(n['p'], n['s'], n['d'], n['v']) for n in notes]
                clip.add_notes(tuple(note_specs))
                log.info("MyAgent: Added %d notes to track '%s', slot %s", len(notes), track, slot)
            except Exception as e:
                log.error("MyAgent: Error in add_notes: %s", e, exc_info=True)
            finally:
                self.song.end_undo_step()

    def _action_launch_clip(self, track, slot):
        target_track = self._find_track(track)
        if target_track and target_track.clip_slots[slot].has_clip:
            target_track.clip_slots[slot].fire()
            log.info("MyAgent: Launched clip in track '%s', slot %s", track, slot)

    def _action_create_midi_track(self, name=None, index=None, arm=False):
        """Создаёт MIDI-дорожку. Если index не задан — добавляет в конец. Можно задать имя и включить arm."""
        try:
            tracks_len = len(self.song.tracks)
            insert_index = tracks_len if index is None else int(index)
            if insert_index < 0:
                insert_index = 0
            if insert_index > tracks_len:
                insert_index = tracks_len

            self.song.begin_undo_step()
            self.song.create_midi_track(insert_index)
            new_track = self.song.tracks[insert_index]
            if name:
                new_track.name = str(name)
            if arm:
                try:
                    new_track.arm = bool(arm)
                except Exception:
                    pass
            log.info("MyAgent: Created MIDI track at %s with name '%s' (arm=%s)", insert_index, getattr(new_track, 'name', None), arm)
        except Exception as e:
            log.error("MyAgent: Error in create_midi_track: %s", e, exc_info=True)
        finally:
            try:
                self.song.end_undo_step()
            except Exception:
                pass

    def _action_get_track_devices(self, track):
        """Получает список устройств на дорожке"""
        target_track = self._find_track(track)
        if target_track:
            try:
                devices_info = []
                for i, device in enumerate(target_track.devices):
                    device_info = {
                        "index": i,
                        "name": device.name,
                        "class_name": device.class_name,
                        "is_active": device.is_active
                    }
                    devices_info.append(device_info)
                
                log.info("MyAgent: Found %d devices on track '%s'", len(devices_info), track)
                return devices_info
            except Exception as e:
                log.error("MyAgent: Error getting devices for track '%s': %s", track, e, exc_info=True)
        return []

    def _action_get_device_parameters(self, track, device_index):
        """Получает параметры конкретного устройства"""
        target_track = self._find_track(track)
        if target_track and device_index < len(target_track.devices):
            try:
                device = target_track.devices[device_index]
                params_info = []
                
                for i, param in enumerate(device.parameters):
                    if param.is_enabled:
                        param_info = {
                            "index": i,
                            "name": param.name,
                            "value": param.value,
                            "min": param.min,
                            "max": param.max,
                            "default_value": param.default_value
                        }
                        params_info.append(param_info)
                
                log.info("MyAgent: Found %d parameters for device '%s' on track '%s'", 
                        len(params_info), device.name, track)
                return {"device_name": device.name, "parameters": params_info}
            except Exception as e:
                log.error("MyAgent: Error getting device parameters: %s", e, exc_info=True)
        return {}

    def _action_set_device_parameter(self, track, device_index, param_index, value):
        """Устанавливает значение параметра устройства"""
        target_track = self._find_track(track)
        if target_track and device_index < len(target_track.devices):
            try:
                device = target_track.devices[device_index]
                if param_index < len(device.parameters):
                    param = device.parameters[param_index]
                    if param.is_enabled:
                        self.song.begin_undo_step()
                        # Нормализуем значение к диапазону параметра
                        normalized_value = max(param.min, min(param.max, float(value)))
                        param.value = normalized_value
                        
                        log.info("MyAgent: Set parameter '%s' of device '%s' to %f on track '%s'", 
                                param.name, device.name, normalized_value, track)
                        return True
            except Exception as e:
                log.error("MyAgent: Error setting device parameter: %s", e, exc_info=True)
            finally:
                try:
                    self.song.end_undo_step()
                except Exception:
                    pass
        return False

    def _action_add_audio_effect(self, track, effect_name):
        """Добавляет аудио эффект на дорожку"""
        target_track = self._find_track(track)
        if target_track:
            try:
                self.song.begin_undo_step()
                # Добавляем эффект в конец цепи
                device_index = len(target_track.devices)
                
                # Создаем эффект (это упрощенная версия - в реальности нужно использовать browser)
                # Для полной реализации потребуется работа с Live.Browser
                log.info("MyAgent: Attempting to add effect '%s' to track '%s'", effect_name, track)
                
                # Пока что это заглушка - полная реализация требует сложной работы с браузером
                log.warning("MyAgent: add_audio_effect is a placeholder - full implementation requires browser API")
                return False
                
            except Exception as e:
                log.error("MyAgent: Error adding audio effect: %s", e, exc_info=True)
                return False
            finally:
                try:
                    self.song.end_undo_step()
                except Exception:
                    pass
        return False

    def _action_set_clip_pitch(self, track, slot, pitch_coarse=0, pitch_fine=0):
        """Изменяет pitch MIDI клипа"""
        target_track = self._find_track(track)
        if target_track and target_track.clip_slots[slot].has_clip:
            try:
                self.song.begin_undo_step()
                clip = target_track.clip_slots[slot].clip
                
                # Изменяем pitch через транспозицию клипа
                if hasattr(clip, 'pitch_coarse'):
                    clip.pitch_coarse = max(-48, min(48, int(pitch_coarse)))
                    log.info("MyAgent: Set clip pitch coarse to %d in track '%s', slot %s", 
                            pitch_coarse, track, slot)
                
                if hasattr(clip, 'pitch_fine'):
                    clip.pitch_fine = max(-50, min(50, int(pitch_fine)))
                    log.info("MyAgent: Set clip pitch fine to %d in track '%s', slot %s", 
                            pitch_fine, track, slot)
                    
                return True
            except Exception as e:
                log.error("MyAgent: Error setting clip pitch: %s", e, exc_info=True)
                return False
            finally:
                self.song.end_undo_step()
        return False

def create_instance(c_instance):
    return MyAgent(c_instance)