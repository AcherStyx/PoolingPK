# -*- coding: utf-8 -*-
# @Time    : 2022/11/2 11:14
# @Author  : Yaojie Shen
# @Project : PoolingPK-Backend
# @File    : __init__.py


class GameEnv(object):

    def control(self, inputs):
        raise NotImplementedError

    def scan(self, inputs):
        raise NotImplementedError
