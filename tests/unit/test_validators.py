"""Тесты валидаторов."""

import pytest

from ableton_mcp.exceptions import MusicValidationError
from ableton_mcp.utils.validators import (
    validate_key,
    validate_midi_pitch,
    validate_scale,
    validate_tempo,
    validate_velocity,
)


class TestMidiPitch:
    def test_valid_pitch(self):
        assert validate_midi_pitch(60) == 60
        assert validate_midi_pitch(0) == 0
        assert validate_midi_pitch(127) == 127

    def test_invalid_pitch(self):
        with pytest.raises(MusicValidationError):
            validate_midi_pitch(-1)
        with pytest.raises(MusicValidationError):
            validate_midi_pitch(128)


class TestVelocity:
    def test_valid_velocity(self):
        assert validate_velocity(100) == 100
        assert validate_velocity(0) == 0
        assert validate_velocity(127) == 127

    def test_invalid_velocity(self):
        with pytest.raises(MusicValidationError):
            validate_velocity(-1)
        with pytest.raises(MusicValidationError):
            validate_velocity(128)


class TestTempo:
    def test_valid_tempo(self):
        assert validate_tempo(140) == 140
        assert validate_tempo(60) == 60
        assert validate_tempo(200) == 200

    def test_invalid_tempo(self):
        with pytest.raises(MusicValidationError):
            validate_tempo(59)
        with pytest.raises(MusicValidationError):
            validate_tempo(201)


class TestKey:
    def test_valid_keys(self):
        assert validate_key("A") == "A"
        assert validate_key("C#") == "C#"
        assert validate_key("Bb") == "Bb"

    def test_invalid_key(self):
        with pytest.raises(MusicValidationError):
            validate_key("X")
        with pytest.raises(MusicValidationError):
            validate_key("H")


class TestScale:
    def test_valid_scales(self):
        assert validate_scale("harmonic_minor") == "harmonic_minor"
        assert validate_scale("major") == "major"
        assert validate_scale("phrygian_dominant") == "phrygian_dominant"

    def test_invalid_scale(self):
        with pytest.raises(MusicValidationError):
            validate_scale("unknown_scale")
