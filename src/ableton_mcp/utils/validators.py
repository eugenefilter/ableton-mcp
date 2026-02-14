"""Валидация музыкальных и MIDI параметров."""

from ableton_mcp.exceptions import MusicValidationError

# Допустимые тональности
VALID_KEYS = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

# Допустимые гаммы
VALID_SCALES = [
    "major",
    "minor",
    "harmonic_minor",
    "melodic_minor",
    "dorian",
    "phrygian",
    "lydian",
    "mixolydian",
    "aeolian",
    "locrian",
    "phrygian_dominant",
    "double_harmonic",
    "whole_tone",
    "chromatic",
]


def validate_midi_pitch(pitch: int) -> int:
    """Валидация MIDI pitch (0-127).

    Args:
        pitch: MIDI номер ноты.

    Returns:
        Валидный pitch.

    Raises:
        MusicValidationError: Если pitch вне диапазона.
    """
    if not 0 <= pitch <= 127:
        raise MusicValidationError(f"MIDI pitch должен быть 0-127, получено: {pitch}")
    return pitch


def validate_velocity(velocity: int) -> int:
    """Валидация MIDI velocity (0-127).

    Args:
        velocity: Сила нажатия.

    Returns:
        Валидный velocity.

    Raises:
        MusicValidationError: Если velocity вне диапазона.
    """
    if not 0 <= velocity <= 127:
        raise MusicValidationError(f"Velocity должен быть 0-127, получено: {velocity}")
    return velocity


def validate_tempo(tempo: int) -> int:
    """Валидация темпа (60-200 BPM).

    Args:
        tempo: Темп в BPM.

    Returns:
        Валидный темп.

    Raises:
        MusicValidationError: Если темп вне диапазона.
    """
    if not 60 <= tempo <= 200:
        raise MusicValidationError(f"Темп должен быть 60-200 BPM, получено: {tempo}")
    return tempo


def validate_key(key: str) -> str:
    """Валидация тональности.

    Args:
        key: Тональность (например, "A", "C#", "Bb").

    Returns:
        Валидная тональность.

    Raises:
        MusicValidationError: Если тональность невалидна.
    """
    if key not in VALID_KEYS:
        raise MusicValidationError(
            f"Невалидная тональность: '{key}'. Допустимые: {', '.join(VALID_KEYS)}"
        )
    return key


def validate_scale(scale: str) -> str:
    """Валидация гаммы/лада.

    Args:
        scale: Название гаммы (например, "harmonic_minor").

    Returns:
        Валидная гамма.

    Raises:
        MusicValidationError: Если гамма невалидна.
    """
    if scale not in VALID_SCALES:
        raise MusicValidationError(
            f"Невалидная гамма: '{scale}'. Допустимые: {', '.join(VALID_SCALES)}"
        )
    return scale
