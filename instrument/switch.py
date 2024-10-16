import pygame as pg
from enum import Enum
from typing import Callable
import copy


class SwitchShape(Enum):
    CIRCLE = 1


class SwitchGraphic:
    DEFAULT_OFF_COLOR = pg.Color(16, 16, 16)

    def __init__(self, zone: pg.Rect, on_color: pg.Color, off_color: pg.Color = DEFAULT_OFF_COLOR,
                 shape=SwitchShape.CIRCLE):
        self.rect = zone
        self.on_color = on_color
        self.off_color = off_color
        self.shape = shape

        self._color = self.off_color

    def on(self):
        self._color = self.on_color

    def off(self):
        self._color = self.off_color

    def draw(self, surface: pg.Surface):
        if self.shape == SwitchShape.CIRCLE:
            pg.draw.ellipse(surface, self._color, self.rect)


class Switch:
    def __init__(self, action: Callable, stop_action: Callable,
                 graphic: SwitchGraphic | None = None) -> None:
        self.action = action
        self.stop_action = stop_action
        self.graphic = graphic

        self.on = False

    def activate(self) -> None:
        if not self.on:
            self.on = True
            if self.graphic:
                self.graphic.on()
            self.action()

    def deactivate(self) -> None:
        if self.on:
            self.on = False
            if self.graphic:
                self.graphic.off()
            self.stop_action()

    def toggle(self) -> None:
        if not self.on:
            self.activate()
        else:
            self.deactivate()


class AudioSwitch(Switch):
    def __init__(self, sound: pg.mixer.Sound, effects: dict | None = None, graphic: SwitchGraphic | None = None) -> None:
        """
        Effects: <code>{"fadein": ms, "fadeout": ms, "maxtime": ms}</code>
        """
        super().__init__(lambda: None, lambda: None, graphic)  # we will properly initialize it later
        self.base_sound = sound
        self.sound_effects = effects
        self.graphic = graphic

        self.sound = self.base_sound
        self.init_sound()

    def init_sound(self) -> None:
        fade_in_length = 0
        fade_out_length = 0
        max_time = 0

        if self.sound_effects:
            for effect, arg in self.sound_effects.items():
                if effect == "fadein":
                    fade_in_length = int(arg)
                if effect == "fadeout":
                    fade_out_length = int(arg)
                if effect == "maxtime":
                    max_time = int(arg)

        self.action = lambda: self.sound.play(-1, max_time, fade_in_length)
        self.stop_action = lambda: self.sound.fadeout(fade_out_length)
