import pygame as pg
from enum import Enum
from typing import Callable


class SwitchShape(Enum):
    CIRCLE = 1


class SwitchGraphic:
    DEFAULT_OFF_COLOR = pg.Color(16, 16, 16)

    def __init__(self, zone: pg.Rect, on_color: pg.Color, off_color: pg.Color = DEFAULT_OFF_COLOR,
                 shape=SwitchShape.CIRCLE):
        self.zone = zone
        self.on_color = on_color
        self.off_color = off_color
        self.shape = shape

        self._color = self.off_color
        self.on = False

    def draw(self, surface: pg.Surface):
        if self.shape == SwitchShape.CIRCLE:
            pg.draw.ellipse(surface, self._color, self.zone)


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
            self.action()

    def deactivate(self) -> None:
        if self.on:
            self.on = False
            self.stop_action()

    def toggle(self) -> None:
        if not self.on:
            self.activate()
        else:
            self.deactivate()
