#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Event(Enum):
    playerIsAway = 0
    playerIsNear = 1
    hitByBomb = 2

class State(Enum):
    move = 0
    follow = 1
    dead = 2

class AI:
    def __init__(self, position, sprite):
        self.state = State.move
        self.event = Event.playerIsAway
        self.position = position
        self.key = False
        self.sprite = sprite

    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = pos

    def getKey(self):
        return self.key

    def setKey(self, k):
        self.key = k

    def getSprite(self):
        return self.sprite

    def setEvent(self, e):
        self.event = e

    def setState(self, s):
        self.state = s

    def getState(self):
        return self.state

    def getEvent(self):
        return self.event

    def moveTo(self, direction):
        if direction=="UP":
            self.position = QPoint(self.position.x(), self.position.y()-50)
        elif direction=="DOWN":
            self.position = QPoint(self.position.x(), self.position.y()+50)
        elif direction=="LEFT":
            self.position = QPoint(self.position.x()-50, self.position.y())
        elif direction=="RIGHT":
            self.position = QPoint(self.position.x()+50, self.position.y())