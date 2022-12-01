# -*- coding: utf-8 -*-
# @Time    : 2022/10/31 09:46
# @Author  : Yaojie Shen
# @Project : PoolingPK-Backend
# @File    : poolingpk.py
import random

from . import GameEnv
from typing import *


class Element(object):
    def get_status(self) -> Dict:
        raise NotImplementedError()


class Gamer(Element):

    def __init__(self, x: int, y: int, uid):
        self.x = x
        self.y = y
        self.direction = 90
        self.uid = uid

    def get_status(self):
        return {
            "uid": self.uid,
            "x": self.x,
            "y": self.y,
            "direction": self.direction
        }


class Bullet(Element):

    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed

    def get_status(self):
        return {
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "speed": self.speed
        }


def _recursive_get_status(env_elements: Union[List, Dict, Element]):
    if isinstance(env_elements, Element):
        return env_elements.get_status()
    elif isinstance(env_elements, list):
        return [_recursive_get_status(elem) for elem in env_elements]
    elif isinstance(env_elements, dict):
        return {k: _recursive_get_status(v) for k, v in env_elements.items()}
    else:
        raise ValueError(f"Input type is {type(env_elements)} which is not supported. ({env_elements})")


class PoolingPK(GameEnv):

    def __init__(self, n_players=4):
        self.elements = {
            "gamer": [Gamer(x=random.randint(0, 300), y=random.randint(0, 300), uid=i) for i in range(n_players)],
            "bullet": [Bullet(x=random.randint(0, 300), y=random.randint(0, 300), direction=90, speed=2)]
        }
        self.direction = 0
        self.step = 0

    def control(self, inputs):
        pass

    def scan(self, inputs):
        ret = _recursive_get_status(self.elements)
        self.update()
        return ret

    def update(self):
        self.step += 1
        if self.step == 20:
            self.direction = (self.direction + 1) % 4
            self.step = 0

        for gamer in self.elements["gamer"]:
            if self.direction == 0:
                gamer.x += 1
            elif self.direction == 1:
                gamer.y -= 1
            elif self.direction == 2:
                gamer.x -= 1
            elif self.direction == 3:
                gamer.y += 1
