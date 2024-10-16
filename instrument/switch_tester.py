from switch import *
from constants import Constants
from waveform import Waveform
import pygame as pg
import sys

pg.mixer.pre_init(Constants.AUDIO_FREQUENCY)
pg.init()

window = pg.display.set_mode(Constants.MIN_SCREEN_SIZE)
clock = pg.time.Clock()

sinewave_220 = Waveform.sinewave_of_hz(Waveform.hz_of("Eb4"), 0.5)
sinewave_110 = Waveform.sinewave_of_hz(Waveform.hz_of("Bb4"), 0.5)
constant_sound = Switch(lambda: [sinewave_220.play(100), sinewave_110.stop()],
                        lambda: [sinewave_110.play(100), sinewave_220.stop()],
                        SwitchGraphic(pg.Rect(0, 0, 100, 100), pg.Color(255, 80, 220)))
crunchy_sound = Waveform.squarewave_of_hz(Waveform.hz_of("Ab4"), 0.2)
toggle_sound = Switch(lambda: crunchy_sound.play(100),
                      lambda: crunchy_sound.stop(),
                      SwitchGraphic(pg.Rect(200, 200, 100, 100), pg.Color(0, 255, 0)))

while 1:
    keys = pg.key.get_pressed()
    if keys[pg.K_g]:
        constant_sound.activate()
    else:
        constant_sound.deactivate()

    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_j:
                toggle_sound.deactivate()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_g:
                constant_sound.toggle()
            if event.key == pg.K_h:
                toggle_sound.toggle()
        if event.type == pg.QUIT:
            sys.exit()

    constant_sound.graphic.draw(window)
    toggle_sound.graphic.draw(window)

    pg.display.flip()

    clock.tick(60)
