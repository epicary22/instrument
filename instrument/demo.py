import pygame as pg
import numpy as np
import os
from typing import Callable
from constants import Constants
from switch import *

os.environ.setdefault("SDL_AUDIODRIVER", "pulseaudio")

pg.mixer.pre_init(Constants.AUDIO_FREQUENCY)
pg.init()

window = pg.display.set_mode(Constants.MIN_SCREEN_SIZE)
clock = pg.time.Clock()


def wave_of_hz(hz: float, amplitude: float, wave: Callable[[float], int | float]) -> pg.mixer.Sound:
	x = np.linspace(0, hz * 2, Constants.AUDIO_FREQUENCY)
	f_x = np.array([wave(value) * amplitude for value in x]).astype(np.int16)
	stereo_wave = np.repeat(f_x.reshape(Constants.AUDIO_FREQUENCY, 1), 2, axis=1)
	return pg.sndarray.make_sound(stereo_wave)


def squarewave_of_hz(hz: float, amplitude: float = 1.0) -> pg.mixer.Sound:
	return wave_of_hz(hz, amplitude, lambda value: Constants.Signal.HI if value % 2 < 1 else Constants.Signal.LO)


def sinewave_of_hz(hz: float, amplitude: float = 1.0) -> pg.mixer.Sound:
	return wave_of_hz(hz, amplitude, lambda value: np.sin(value * np.pi) * Constants.Signal.HI)


def c_sinewave_of_hz(hz: float, amplitude: float = 1.0) -> pg.mixer.Sound:
	return wave_of_hz(hz, amplitude, lambda value: Constants.Signal.LO + np.sin(value * np.pi) * Constants.Signal.HI * 2)


# squarewave = squarewave_of_hz(440, 0.2)
# squarewave.play()
# sinewave = sinewave_of_hz(220/np.pi, 1.0)
# sinewave.play()
# tanwave = wave_of_hz(
# 	1, 1.0, 
# 	lambda value: np.tan(value) * Constants.Signal.HI
# )
# tanwave.play()
strangewave = wave_of_hz(
	880, 1.0,
	lambda value: np.sin(1 - np.exp(value * 0.005)) * Constants.Signal.HI
)
strangewave.play()

# while 1:
# 	for event in pg.event.get():
# 		if event.type == pg.QUIT:
# 			pg.quit()
# 			raise SystemExit
#
# 	clock.tick(60)
