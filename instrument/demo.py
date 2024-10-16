import pygame as pg
import numpy as np
import os
from typing import Callable
import copy
from constants import Constants
from waveform import Waveform
from switch import *
from tkinter import messagebox, colorchooser

# os.environ.setdefault("SDL_AUDIODRIVER", "pulseaudio")

pg.mixer.pre_init(Constants.AUDIO_FREQUENCY, channels=Constants.AUDIO_CHANNELS)  # channels = 8 with Soundcore Q20
pg.init()

window = pg.display.set_mode(Constants.MIN_SCREEN_SIZE)
clock = pg.time.Clock()

note_names = ("C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4")
note_keys = (pg.K_a, pg.K_s, pg.K_d, pg.K_f, pg.K_g, pg.K_h, pg.K_j, pg.K_k, pg.K_l, pg.K_SEMICOLON, pg.K_QUOTE, pg.K_KP_ENTER)

# notes = tuple(note_register.values())
# notes[11].play()
# switch_register = {
#     note_keys[i]: Switch(lambda: notes[i].play(100), lambda: notes[i].stop(),
#                          SwitchGraphic(pg.Rect(100 * (i % 3), 100 * (i // 3), 100, 100), pg.Color(i * 10, i * 15, i * 20)))
#     for note in notes
# }
switch_register = {}
i = 0
# for a in range(len(note_names)):
#     i = copy.deepcopy(a)
#     note = Waveform.sinewave_of_hz(Waveform.hz_of(note_names[i]), 0.5)
#     switch_register.update(
#         {
#             note_keys[i]: Switch(lambda: note.play(100), lambda: note.stop(),
#                                  SwitchGraphic(
#                                      pg.Rect(100 * (i % 3), 100 * (i // 3), 100, 100), pg.Color(i * 10, i * 15, i * 20)
#                                  ))
#         }
#     )
#     i += 1
note_6 = Waveform.sinewave_of_hz(Waveform.hz_of(note_names[6]))
switch_register.update({note_keys[6]: AudioSwitch(note_6, {"fadein": 1000, "fadeout": 1000},
                                             SwitchGraphic(
                                                 pg.Rect(0, 200, 100, 100), pg.Color(60, 90, 120)
                                             ))})
# todo I'm going to have to do the switch register manually!

# print(switch_register)
#     pg.K_a: Switch(lambda: note_register["C4"].play(100), lambda: note_register["C4"].stop(),
#                    SwitchGraphic(pg.Rect(0, 0, 100, 100), pg.Color(0, 255, 0))),
#     pg.K_s: Switch(lambda: note_register["C4"].play(100), lambda: note_register["C4"].stop(),
#                    SwitchGraphic(pg.Rect(0, 0, 100, 100), pg.Color(0, 255, 0))),
#     pg.K_d: Switch(lambda: note_register["C4"].play(100), lambda: note_register["C4"].stop(),
#                    SwitchGraphic(pg.Rect(0, 0, 100, 100), pg.Color(0, 255, 0))),
#     pg.K_f: Switch(lambda: note_register["C4"].play(100), lambda: note_register["C4"].stop(),
#                    SwitchGraphic(pg.Rect(0, 0, 100, 100), pg.Color(0, 255, 0)))
# }
# print(switch_register[pg.K_a].graphic.zone)

strangewave = Waveform.wave_of_hz(
    880, 1.0,
    lambda value: np.sin(1 - np.exp(value * 0.005)) * Constants.Signal.HI
)
strangewave.play()

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    # this is bad... do not bind events to graphics!
    window.fill(pg.color.THECOLORS["black"])

    keys = pg.key.get_pressed()
    for key, switch in switch_register.items():
        switch.graphic.draw(window)
        if keys[key]:
            switch.activate()
        else:
            switch.deactivate()
    if keys[pg.K_p]:
        messagebox.showinfo("P", "You pressed the letter p!")
        color = colorchooser.askcolor()  # gives it in the format ((r, g, b), "#hex")
        switch_register[note_keys[6]].graphic.on_color = pg.Color(color[0])
    mouse = pg.mouse.get_pressed()
    if mouse[0]:
        switch_register[note_keys[6]].graphic.rect.center = pg.mouse.get_pos()

    pg.display.flip()

    clock.tick(60)
