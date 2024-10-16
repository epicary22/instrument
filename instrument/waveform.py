import pygame as pg
import numpy as np
import re
from typing import Callable
from constants import Constants


class Waveform:
    @staticmethod
    def wave_of_hz(hz: float, amplitude: float, wave: Callable[[float], int | float]) -> pg.mixer.Sound:
        x = np.linspace(0, hz * 2, Constants.AUDIO_FREQUENCY)
        f_x = np.array([wave(value) * amplitude for value in x]).astype(np.int16)
        stereo_wave = np.repeat(f_x.reshape(Constants.AUDIO_FREQUENCY, 1), Constants.AUDIO_CHANNELS, axis=1)
        return pg.sndarray.make_sound(stereo_wave)

    @staticmethod
    def squarewave_of_hz(hz: float, amplitude: float = 1.0) -> pg.mixer.Sound:
        return Waveform.wave_of_hz(hz, amplitude,
                                   lambda value: Constants.Signal.HI if value % 2 < 1 else Constants.Signal.LO)

    @staticmethod
    def sinewave_of_hz(hz: float, amplitude: float = 1.0) -> pg.mixer.Sound:
        return Waveform.wave_of_hz(hz, amplitude, lambda value: np.sin(value % 2 * np.pi) * Constants.Signal.HI)

    @staticmethod
    def c_sinewave_of_hz(hz: float, amplitude: float = 1.0) -> pg.mixer.Sound:
        return Waveform.wave_of_hz(hz, amplitude,
                                   lambda value: Constants.Signal.LO + np.sin(value * np.pi) * Constants.Signal.HI * 2)

    @staticmethod
    def hz_of(note_name: str) -> float:
        A_0 = 27.50000

        if re.match(r"^[A-G][#b]?\d$", note_name) is None:  # for future re use: must have an r-string
            return -1
        note = note_name[0]
        accidental = note_name[1] if len(note_name) == 3 else None
        octave = float(note_name[2] if len(note_name) == 3 else note_name[1])

        half_steps_from_a = 0
        if note == "C":
            half_steps_from_a = -9
        elif note == "D":
            half_steps_from_a = -7
        elif note == "E":
            half_steps_from_a = -5
        elif note == "F":
            half_steps_from_a = -4
        elif note == "G":
            half_steps_from_a = -2
        elif note == "A":
            half_steps_from_a = 0
        elif note == "B":
            half_steps_from_a = 2
        if accidental == "#":
            half_steps_from_a += 1
        elif accidental == "b":
            half_steps_from_a -= 1

        base_a = A_0 * 2 ** octave
        hz = base_a * np.power(2, half_steps_from_a/12)
        return hz
