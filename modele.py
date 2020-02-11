#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Case():
    def __init__(self, position, collision, couleur):
        self.collision = collision
        self.position = position
        self.couleur = couleur

    def getCollision(self):
        return self.collision

    def getPosition(self):
        return self.position

    def getCouleur(self):
        return self.couleur

    def setPosition(self, x, y):
        self.position = QPoint(x, y)

    def setCollision(self, collision):
        self.collision = collision

    def setCouleur(self, couleur):
        self.couleur = couleur

class Joueur(Case):
    def __init__(self, position, couleur, brush):
        super().__init__(position, True, couleur)
        self.cle = False
        self.mort = False
        self.nbVie = 3
        self.forceBombe = 1
        self.nbBombe = 1
        self.TabBombe=[]
        self.brush = brush

    def getBrush(self):
        return self.brush

    def setBrush(self, brush):
        self.brush = brush

    def getTabBombe(self):
        return self.TabBombe

    def getCle(self):
        return self.cle

    def getNbBombe(self):
        return self.nbBombe

    def getForceBombe(self):
        return self.forceBombe

    def incVie(self):
        self.nbVie+=1

    def incForceBombe(self):
        self.forceBombe+=1

    def incNbBombe(self):
        self.nbBombe+=1

    def setCle(self, k):
        self.cle = k

    def getMort(self):
        return self.mort

    def getNbVie(self):
        return self.nbVie

    def moveTo(self, direction):
        if direction=="UP":
            self.position = QPoint(self.position.x(), self.position.y()-50)
        elif direction=="DOWN":
            self.position = QPoint(self.position.x(), self.position.y()+50)
        elif direction=="LEFT":
            self.position = QPoint(self.position.x()-50, self.position.y())
        elif direction=="RIGHT":
            self.position = QPoint(self.position.x()+50, self.position.y())

    def decVie(self):
        self.nbVie-=1

    def setMort(self, mort):
        self.mort = mort

class Bombe(Case):
    def __init__(self, position, couleur, force):
        super().__init__(position, True, couleur)
        self.force = force

    def getForce(self):
        return self.force

class Brique(Case):
    def __init__(self, position, couleur, objet):
        super().__init__(position, True, couleur)
        self.objet = objet
        self.cassee = False
        self.sortie = False

    def getObjet(self):
        return self.objet

    def setCassee(self, cassee):
        self.cassee = cassee

    def getCassee(self):
        return self.cassee
    
    def setSortie(self, sortie):
        self.sortie = sortie

    def getSortie(self):
        return self.sortie

class Objet(Case):
    def __init__(self, position, couleur, type):
        self.couleur = couleur
        self.position = position
        self.collision = False
        self.type = type

    def getType(self):
        return self.type