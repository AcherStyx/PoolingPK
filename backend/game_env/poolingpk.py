# -*- coding: utf-8 -*-
# @Time    : 2022/10/31 09:46
# @Author  : Yaojie Shen
# @Project : PoolingPK-Backend
# @File    : poolingpk.py
import math
import random

from . import GameEnv
from typing import *

PLAYER_SPEED = 4
BULLET_SPEED = 32

BULLET_BURN_TIME = 5

COLLISION_RANGE = 50

AIR_WALL = 25


class Element(object):
    def get_status(self) -> Dict:
        raise NotImplementedError()


class Gamer(Element):

    def __init__(self, x: int, y: int, map_height: int, map_width: int, uid):
        self.x = x % map_width
        self.y = y % map_height
        self.map_height = map_height
        self.map_width = map_width
        self.direction = 0
        self.uid = uid
        self.speed = PLAYER_SPEED
        self.cooling_time = 0
        self.health = 100
        self.burn = 0

    def get_status(self):
        return {
            "uid": self.uid,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "move_direction": self.direction,
            "health": self.health
        }

    def move(self, move_direction):
        """

        :param move_direction:
        3  2  1
        4  8  0
        5  6  7
        LT x->
        y
        :return:
        """
        if self.health > 0:
            assert move_direction in list(range(9))  # only support 8 move_direction
            # case-by-case movement
            if move_direction == 0:
                self.x += self.speed
            elif move_direction == 1:
                self.x += self.speed / math.pow(2, 0.5)
                self.y -= self.speed / math.pow(2, 0.5)
            elif move_direction == 2:
                self.y -= self.speed
            elif move_direction == 3:
                self.x -= self.speed / math.pow(2, 0.5)
                self.y -= self.speed / math.pow(2, 0.5)
            elif move_direction == 4:
                self.x -= self.speed
            elif move_direction == 5:
                self.x -= self.speed / math.pow(2, 0.5)
                self.y += self.speed / math.pow(2, 0.5)
            elif move_direction == 6:
                self.y += self.speed
            elif move_direction == 7:
                self.x += self.speed / math.pow(2, 0.5)
                self.y += self.speed / math.pow(2, 0.5)
            elif move_direction == 8:
                pass
            else:
                raise RuntimeError
            self.x = AIR_WALL if self.x < AIR_WALL else self.x
            self.y = AIR_WALL if self.y < AIR_WALL else self.y
            self.x = self.map_width - AIR_WALL if self.x > self.map_width - AIR_WALL else self.x
            self.y = self.map_height - AIR_WALL if self.y > self.map_height - AIR_WALL else self.y
            self.direction = move_direction if move_direction != 8 else self.direction
            self.cooling_time += 1
        else:
            self.burn += 1

    def fire(self):
        if self.cooling_time > 10:
            self.cooling_time = 0
            return Bullet(x=self.x, y=self.y, map_height=self.map_height, map_width=self.map_width,
                          direction=self.direction)
        else:
            return None

    def hit(self):
        self.health = max(0, self.health - 5)


class Bullet(Element):

    def __init__(self, x, y, map_height: int, map_width: int, direction):
        assert direction in list(range(8))  # for bullet, direction cannot be 8
        self.x = x
        self.y = y
        self.map_height = map_height
        self.map_width = map_width
        self.move_direction = direction
        self.speed = BULLET_SPEED
        offset = 30
        if self.move_direction == 0:
            self.x += offset
        elif self.move_direction == 1:
            self.x += offset / math.pow(2, 0.5)
            self.y -= offset / math.pow(2, 0.5)
        elif self.move_direction == 2:
            self.y -= offset
        elif self.move_direction == 3:
            self.x -= offset / math.pow(2, 0.5)
            self.y -= offset / math.pow(2, 0.5)
        elif self.move_direction == 4:
            self.x -= offset
        elif self.move_direction == 5:
            self.x -= offset / math.pow(2, 0.5)
            self.y += offset / math.pow(2, 0.5)
        elif self.move_direction == 6:
            self.y += offset
        elif self.move_direction == 7:
            self.x += offset / math.pow(2, 0.5)
            self.y += offset / math.pow(2, 0.5)
        else:
            raise RuntimeError
        self.health = 100
        self.burn = 0

    def get_status(self):
        return {
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "move_direction": self.move_direction,
            "speed": self.speed,
            "health": self.health
        }

    def move(self):
        if self.health > 0:
            move_direction = self.move_direction
            if move_direction == 0:
                self.x += self.speed
            elif move_direction == 1:
                self.x += self.speed / math.pow(2, 0.5)
                self.y -= self.speed / math.pow(2, 0.5)
            elif move_direction == 2:
                self.y -= self.speed
            elif move_direction == 3:
                self.x -= self.speed / math.pow(2, 0.5)
                self.y -= self.speed / math.pow(2, 0.5)
            elif move_direction == 4:
                self.x -= self.speed
            elif move_direction == 5:
                self.x -= self.speed / math.pow(2, 0.5)
                self.y += self.speed / math.pow(2, 0.5)
            elif move_direction == 6:
                self.y += self.speed
            elif move_direction == 7:
                self.x += self.speed / math.pow(2, 0.5)
                self.y += self.speed / math.pow(2, 0.5)
            else:
                raise RuntimeError
            if self.x < 0 or self.y < 0 or self.x > self.map_width or self.y > self.map_height:
                return False  # destroy
            else:
                return True
        else:
            self.burn += 1
            return True

    def hit(self):
        self.health = 0


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

    def __init__(self, n_players=5):
        self.n_players = n_players
        self.map_height = 600
        self.map_width = 800

        self.elements = {
            "player": {str(i): Gamer(x=random.randint(0, self.map_width),
                                     y=random.randint(0, self.map_height),
                                     map_height=self.map_height,
                                     map_width=self.map_width, uid=i) for i in range(n_players)},
            "bullet": []
        }
        self.direction = [random.randint(0, 8) for _ in range(self.n_players)]  # direction for each computer
        self.step = 0

    def scan(self, inputs):
        return _recursive_get_status(self.elements)

    def update(self, command: dict = None):
        # update computer
        self.step += 1
        if self.step == 50:
            self.direction = [random.randint(0, 8) for _ in range(self.n_players)]
            self.step = 0
        for (player_id, player), direction in zip(self.elements["player"].items(), self.direction):
            if player_id == "0":
                continue
            else:
                player.move(direction)
                fire_ret = player.fire()
                if fire_ret is not None:
                    self.elements["bullet"].append(fire_ret)
        # update player
        if command is not None:
            for player_name, player_action in command.items():
                if player_name in self.elements["player"]:
                    player = self.elements["player"][player_name]
                    player.move(command["0"])
                    if command["fire"]:
                        fire_ret = player.fire()
                        if fire_ret is not None:
                            self.elements["bullet"].append(fire_ret)
                    self.elements["player"] = {i: p for i, p in self.elements["player"].items() if p.burn < 30}
        # collision
        for player_a_id, player_a in self.elements["player"].items():
            for player_b_id, player_b in self.elements["player"].items():
                if player_a_id == player_b_id:
                    continue
                else:
                    current_distance = ((player_a.x - player_b.x) ** 2 + (player_a.y - player_b.y) ** 2) ** 0.5
                    if current_distance < COLLISION_RANGE:
                        scale = COLLISION_RANGE / current_distance
                        center_x = (player_a.x + player_b.x) / 2
                        center_y = (player_a.y + player_b.y) / 2
                        player_a.x = center_x - (center_x - player_a.x) * scale
                        player_a.y = center_y - (center_y - player_a.y) * scale
                        player_b.x = center_x - (center_x - player_b.x) * scale
                        player_b.y = center_y - (center_y - player_b.y) * scale
        # update bullet
        keep_bullet = []
        for bullet in self.elements["bullet"]:
            if bullet.move():
                keep_bullet.append(bullet)
        self.elements["bullet"] = keep_bullet
        # hit
        keep_bullet = []
        for bullet in self.elements["bullet"]:
            if bullet.health == 0:
                if bullet.burn < BULLET_BURN_TIME:
                    keep_bullet.append(bullet)
            else:
                distance = []
                for player_name, player in self.elements["player"].items():
                    distance.append((player_name, ((bullet.x - player.x) ** 2 + (bullet.y - player.y) ** 2) ** 0.5))
                closest_player_name, closest_distance = min(distance, key=lambda x: x[1])
                if closest_distance < 25:
                    self.elements["player"][closest_player_name].hit()
                    bullet.hit()
                keep_bullet.append(bullet)
        self.elements["bullet"] = keep_bullet

        return _recursive_get_status(self.elements)
