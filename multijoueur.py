#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import pygame

from modele import *
import sys
import time
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

class RenderAreaMulti(QWidget):
    imgNum=4
    imgQuantity=4
    imgNum2=4
    imgQuantity2=4
    imgNum3=4
    imgQuantity3=4
    imgNum4=4
    imgQuantity4=4
    imgBombe=0
    imgQuantityBombe=6
    choixBombe=0
    numObjet=0
    def __init__(self,main, parent=None):
        super(RenderAreaMulti, self).__init__(parent)
        self.initUI()
        self.main=main

    '''
    initUI
    Defini toutes les variables utilisées dans le programme
    '''
    def initUI(self):
        pygame.init()
        pygame.joystick.init()

        self.gamepadTimer1 = QTimer()
        self.gamepadTimer1.timeout.connect(self.gamepad1)
        self.gamepadTimer1.start(50)

        self.pen = Qt.NoPen
        self.brush = QBrush(Qt.SolidPattern)
        self.playerBrush = QBrush()
        self.playerBrush2 = QBrush()
        self.playerBrush3 = QBrush()
        self.playerBrush4 = QBrush()
        self.terrainBrush = QBrush()
        self.bombBrush = QBrush()
        self.menuPause1=QWidget(self)
        self.perdu1= QWidget(self)
        self.font=QFont("Roboto",25,QFont.Bold)
        self.styleSheet="QPushButton{ background-color: rgb(8,88,200); border-radius: 10px; border: 2px solid;}"
        self.stylePerdu="QWidget{background-color: rgb(0,0,0);border: 2px solid white;} QPushButton{ background-color: rgb(8,88,200); border-radius: 10px; border: 2px solid;} QLabel{font-size: 25px;}"
        self.changeTimer=QTimer()
        self.mytimer = QTimer()
        self.mytimer2 = QTimer()
        self.mytimer3 = QTimer()
        self.mytimer4 = QTimer()
        self.playerTimer = QTimer()
        self.Tab=1
        self.Tab2=1
        self.Tab3=1
        self.Tab4=1

        self.tuto()

        self.propaTimer = QTimer()


        self.timers = []
        self.bombs = []
        self.posList = []
        self.propaPosList = []
        self.propagation = []
        self.player = []
        self.player.append(Joueur(QPoint(50, 50), QColor(223, 56, 56), QBrush()))
        self.player.append(Joueur(QPoint(17*50, 11*50), QColor(223, 56, 56), QBrush()))
        self.player.append(Joueur(QPoint(50, 11*50), QColor(223, 56, 56), QBrush()))
        self.player.append(Joueur(QPoint(17*50, 50), QColor(223, 56, 56), QBrush()))

        self.propagationSprite = {
            "milieu": QPixmap("sprites/genkidama.png").copy(100, 100, 50, 50),
            "haut/bas": QPixmap("sprites/genkidama.png").copy(0, 150, 50, 50),
            "gauche/droite": QPixmap("sprites/genkidama.png").copy(150, 100, 50, 50),
            "fin haut": QPixmap("sprites/genkidama.png").copy(150, 150, 50, 50),
            "fin bas": QPixmap("sprites/genkidama.png").copy(0, 200, 50, 50),
            "fin gauche": QPixmap("sprites/genkidama.png").copy(50, 150, 50, 50),
            "fin droite": QPixmap("sprites/genkidama.png").copy(100, 150, 50, 50)
        }

        self.terrainSprite = {
            "herbe":QPixmap("sprites/namek.png").copy(0, 0, 50, 50),
            "mur":QPixmap("sprites/namek.png").copy(50, 0, 50, 50),
            "bordGauche":QPixmap("sprites/namek.png").copy(100, 0, 50, 50),
            "bordDroite":QPixmap("sprites/namek.png").copy(0, 50, 50, 50),
            "bordHaut":QPixmap("sprites/namek.png").copy(50, 50, 50, 50),
            "bordBas":QPixmap("sprites/namek.png").copy(100, 50, 50, 50),
            "jointureBasDroite":QPixmap("sprites/namek.png").copy(0, 100, 50, 50),
            "jointureBasGauche":QPixmap("sprites/namek.png").copy(50, 100, 50, 50),
            "jointureHautGauche":QPixmap("sprites/namek.png").copy(100, 100, 50, 50),
            "jointureHautDroite":QPixmap("sprites/namek.png").copy(0, 150, 50, 50),
            "rocher":QPixmap("sprites/namek.png").copy(50, 150, 50, 50),
        }

        self.playerSprite = [
            [ 
                #goku
                QPixmap('sprites/sprite.png').copy(166,5,19,25).scaled(50,50),#joueurUp 0
                QPixmap('sprites/sprite.png').copy(188,5,19,25).scaled(50,50),#joueurUp 1
                QPixmap('sprites/sprite.png').copy(209,5,19,25).scaled(50,50),#joueurUp 2
                QPixmap('sprites/sprite.png').copy(226,5,18,25).scaled(50,50),#joueurUp 3
                QPixmap('sprites/sprite.png').copy(60,5,19,25).scaled(50,50),  #joueurUpStop
                #gokuSSJ
                QPixmap('sprites/spritessj.png').copy(166,5,19,25).scaled(50,50),#joueurUp 0
                QPixmap('sprites/spritessj.png').copy(188,5,19,25).scaled(50,50),#joueurUp 1
                QPixmap('sprites/spritessj.png').copy(209,5,19,25).scaled(50,50),#joueurUp 2
                QPixmap('sprites/spritessj.png').copy(226,5,18,25).scaled(50,50),#joueurUp 3
                QPixmap('sprites/spritessj.png').copy(60,5,19,25).scaled(50,50),  #joueurUpStop
                #gokuSSJG
                QPixmap('sprites/spritessjg.png').copy(166,5,19,25).scaled(50,50),#joueurUp 0
                QPixmap('sprites/spritessjg.png').copy(188,5,19,25).scaled(50,50),#joueurUp 1
                QPixmap('sprites/spritessjg.png').copy(209,5,19,25).scaled(50,50),#joueurUp 2
                QPixmap('sprites/spritessjg.png').copy(226,5,18,25).scaled(50,50),#joueurUp 3
                QPixmap('sprites/spritessjg.png').copy(60,5,19,25).scaled(50,50)  #joueurUpStop
            ],

            [
                #goku
                QPixmap('sprites/sprite.png').copy(85,37,19,25).scaled(50,50),#joueurDown 0
                QPixmap('sprites/sprite.png').copy(106,37,19,25).scaled(50,50),#joueurDown 1
                QPixmap('sprites/sprite.png').copy(126,37,19,25).scaled(50,50),#joueurDown 2
                QPixmap('sprites/sprite.png').copy(145,37,19,25).scaled(50,50),#joueurDown 3
                QPixmap('sprites/sprite.png').copy(38,5,19,25).scaled(50,50),  #joueurDownStop
                #gokuSSJ
                QPixmap('sprites/spritessj.png').copy(85,37,19,25).scaled(50,50),#joueurDown 0
                QPixmap('sprites/spritessj.png').copy(106,37,19,25).scaled(50,50),#joueurDown 1
                QPixmap('sprites/spritessj.png').copy(126,37,19,25).scaled(50,50),#joueurDown 2
                QPixmap('sprites/spritessj.png').copy(145,37,19,25).scaled(50,50),#joueurDown 3
                QPixmap('sprites/spritessj.png').copy(38,5,19,25).scaled(50,50),  #joueurDownStop
                #gokuSSJG
                QPixmap('sprites/spritessjg.png').copy(85,37,19,25).scaled(50,50),#joueurDown 0
                QPixmap('sprites/spritessjg.png').copy(106,37,19,25).scaled(50,50),#joueurDown 1
                QPixmap('sprites/spritessjg.png').copy(126,37,19,25).scaled(50,50),#joueurDown 2
                QPixmap('sprites/spritessjg.png').copy(145,37,19,25).scaled(50,50),#joueurDown 3
                QPixmap('sprites/spritessjg.png').copy(38,5,19,25).scaled(50,50)  #joueurDownStop
            ],

            [
                #goku
                QPixmap('sprites/sprite.png').copy(80,4,19,25).scaled(50,50),#joueurLeft 0
                QPixmap('sprites/sprite.png').copy(100,4,19,25).scaled(50,50),#joueurLeft 1
                QPixmap('sprites/sprite.png').copy(122,5,19,25).scaled(50,50),#joueurLeft 2
                QPixmap('sprites/sprite.png').copy(140,4,19,25).scaled(50,50),#joueurLeft 3
                QPixmap('sprites/sprite.png').copy(3,5,19,25).scaled(50,50),   #joueurLeftStop
                #gokuSSJ
                QPixmap('sprites/spritessj.png').copy(80,4,19,25).scaled(50,50),#joueurLeft 0
                QPixmap('sprites/spritessj.png').copy(100,4,19,25).scaled(50,50),#joueurLeft 1
                QPixmap('sprites/spritessj.png').copy(122,5,19,25).scaled(50,50),#joueurLeft 2
                QPixmap('sprites/spritessj.png').copy(140,4,19,25).scaled(50,50),#joueurLeft 3
                QPixmap('sprites/spritessj.png').copy(3,5,19,25).scaled(50,50),   #joueurLeftStop
                #gokuSSJG
                QPixmap('sprites/spritessjg.png').copy(80,4,19,25).scaled(50,50),#joueurLeft 0
                QPixmap('sprites/spritessjg.png').copy(100,4,19,25).scaled(50,50),#joueurLeft 1
                QPixmap('sprites/spritessjg.png').copy(122,5,19,25).scaled(50,50),#joueurLeft 2
                QPixmap('sprites/spritessjg.png').copy(140,4,19,25).scaled(50,50),#joueurLeft 3
                QPixmap('sprites/spritessjg.png').copy(3,5,19,25).scaled(50,50)   #joueurLeftStop
            ],

            [
                #goku
                QPixmap('sprites/sprite.png').copy(0,35,19,25).scaled(50,50), #joueurRight 0
                QPixmap('sprites/sprite.png').copy(21,35,19,25).scaled(50,50), #joueurRight 1
                QPixmap('sprites/sprite.png').copy(41,34,19,25).scaled(50,50), #joueurRight 2
                QPixmap('sprites/sprite.png').copy(59,33,19,25).scaled(50,50), #joueurRight 3
                QPixmap('sprites/sprite.png').copy(20,5,19,25).scaled(50,50),  #joueurRightStop
                #gokuSSJ
                QPixmap('sprites/spritessj.png').copy(0,35,19,25).scaled(50,50), #joueurRight 0
                QPixmap('sprites/spritessj.png').copy(21,35,19,25).scaled(50,50), #joueurRight 1
                QPixmap('sprites/spritessj.png').copy(41,34,19,25).scaled(50,50), #joueurRight 2
                QPixmap('sprites/spritessj.png').copy(59,33,19,25).scaled(50,50), #joueurRight 3
                QPixmap('sprites/spritessj.png').copy(20,5,19,25).scaled(50,50),  #joueurRightStop
                #gokuSSJG
                QPixmap('sprites/spritessjg.png').copy(0,35,19,25).scaled(50,50), #joueurRight 0
                QPixmap('sprites/spritessjg.png').copy(21,35,19,25).scaled(50,50), #joueurRight 1
                QPixmap('sprites/spritessjg.png').copy(41,34,19,25).scaled(50,50), #joueurRight 2
                QPixmap('sprites/spritessjg.png').copy(59,33,19,25).scaled(50,50), #joueurRight 3
                QPixmap('sprites/spritessjg.png').copy(20,5,19,25).scaled(50,50)  #joueurRightStop
            ]
        ]

        self.bombeSprite = [
            QPixmap("sprites/genkidama.png").copy(0, 0, 50, 50),
            #QPixmap("sprites/genkidama.png").copy(50, 0, 50, 50),
            QPixmap("sprites/genkidama.png").copy(100, 0, 50, 50),
            #QPixmap("sprites/genkidama.png").copy(150, 0, 50, 50),
            QPixmap("sprites/genkidama.png").copy(0, 50, 50, 50),
            #QPixmap("sprites/genkidama.png").copy(50, 50, 50, 50),
            QPixmap("sprites/genkidama.png").copy(100, 50, 50, 50),
            QPixmap("sprites/genkidama.png").copy(0, 50, 50, 50),
            QPixmap("sprites/genkidama.png").copy(0, 0, 50, 50),
            #QPixmap("sprites/genkidama.png").copy(150, 50, 50, 50),
            #QPixmap("sprites/genkidama.png").copy(0, 100, 50, 50),
            #QPixmap("sprites/genkidama.png").copy(50, 100, 50, 50)
        ]
        
        self.items = [
            QPixmap("sprites/itemFreezer.png").copy(0, 0, 50, 50),
            QPixmap("sprites/itemGenkidama.png").copy(0, 0, 50, 50),
            QPixmap("sprites/itemHaricot.png").copy(0, 0, 50, 50),
            QPixmap("sprites/itemSSJ.png").copy(0, 0, 50, 50).scaled(50, 50)
        ]

        self.playerBrush.setTexture(QPixmap('sprites/sprite.png').copy(38,5,19,25).scaled(50,50))
        self.playerBrush2.setTexture(QPixmap('sprites/sprite.png').copy(38,5,19,25).scaled(50,50))
        self.playerBrush3.setTexture(QPixmap('sprites/sprite.png').copy(38,5,19,25).scaled(50,50))
        self.playerBrush4.setTexture(QPixmap('sprites/sprite.png').copy(38,5,19,25).scaled(50,50))

        self.createTerrain()

    '''
    moving
    permet de changer de sprite pour le joueur 1
    timer
    permet au bout d'un temps donner de lancer la fonction myprint qui va mettre un sprite du joueur 1 en position arret dans la dernier direction connue

    C'est le meme proceder pour tous les joueurs
    '''
    #Animation Joueur1
    def moving(self):
        if self.imgNum<self.imgQuantity-1:
            self.imgNum+=1
        else :
            self.imgNum=self.imgQuantity-3
        self.playerBrush.setTexture(self.playerSprite[self.Tab][self.imgNum])

    def timer(self):
        self.mytimer.stop()
        self.mytimer = QTimer()
        self.mytimer.timeout.connect(self.myprint)
        self.mytimer.start(500)

    def myprint(self):
        self.playerBrush.setTexture(self.playerSprite[self.Tab][self.imgQuantity])
        self.update()

    #Animation Joueur2
    def moving2(self):
        if self.imgNum2<self.imgQuantity2-1:
            self.imgNum2+=1
        else :
            self.imgNum2=self.imgQuantity2-3
        self.playerBrush2.setTexture(self.playerSprite[self.Tab2][self.imgNum2])

    def timer2(self):
        self.mytimer2.stop()
        self.mytimer2 = QTimer()
        self.mytimer2.timeout.connect(self.myprint2)
        self.mytimer2.start(500)

    def myprint2(self):
        self.playerBrush2.setTexture(self.playerSprite[self.Tab2][self.imgQuantity2])
        self.update()
    
    #Animation Joueur3
    def moving3(self):
        if self.imgNum3<self.imgQuantity3-1:
            self.imgNum3+=1
        else :
            self.imgNum3=self.imgQuantity3-3
        self.playerBrush3.setTexture(self.playerSprite[self.Tab3][self.imgNum3])

    def timer3(self):
        self.mytimer3.stop()
        self.mytimer3 = QTimer()
        self.mytimer3.timeout.connect(self.myprint3)
        self.mytimer3.start(500)

    def myprint3(self):
        self.playerBrush3.setTexture(self.playerSprite[self.Tab3][self.imgQuantity3])
        self.update()

    #Animation Joueur4
    def moving4(self):
        if self.imgNum4<self.imgQuantity4-1:
            self.imgNum4+=1
        else :
            self.imgNum4=self.imgQuantity4-3
        self.playerBrush4.setTexture(self.playerSprite[self.Tab4][self.imgNum4])

    def timer4(self):
        self.mytimer4.stop()
        self.mytimer4 = QTimer()
        self.mytimer4.timeout.connect(self.myprint4)
        self.mytimer4.start(500)

    def myprint4(self):
        self.playerBrush4.setTexture(self.playerSprite[self.Tab4][self.imgQuantity4])
        self.update()

    #Animation bombe
    def bombeAnime(self):
        if self.imgBombe<self.imgQuantityBombe-1:
            self.imgBombe+=1
        else :
            self.imgBombe=0 
        self.bombBrush.setTexture(self.bombeSprite[self.imgBombe])

    '''
    gamepad
    Gere la manette en bluetooth
    '''
    def gamepad1(self):
        pygame.joystick.init()
        if pygame.joystick.get_count()!=0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION:
                    hat = self.joystick.get_hat(0)
                    buttonFire = self.joystick.get_button(0)
                    if hat[1]==1:
                        self.keyPressEvent(QKeyEvent(QEvent.KeyPress, 90, Qt.NoModifier))
                    elif hat[1]==-1:
                        self.keyPressEvent(QKeyEvent(QEvent.KeyPress, 83, Qt.NoModifier))
                    elif hat[0]==-1:
                        self.keyPressEvent(QKeyEvent(QEvent.KeyPress, 81, Qt.NoModifier))
                    elif hat[0]==1:
                        self.keyPressEvent(QKeyEvent(QEvent.KeyPress, 68, Qt.NoModifier))
                    elif buttonFire==1:
                        self.keyPressEvent(QKeyEvent(QEvent.KeyPress, 32, Qt.NoModifier))

    '''
    keyPressEvent
    Le gestionnaire d'événement clavier de PyQt
    '''
    #Touches des joueurs
    def keyPressEvent(self, event):
        #Joueur1
        if self.player[0].getMort() == False:
            if event.key() == Qt.Key_Z:
                self.Tab=0
                if self.terrain[(self.player[0].getPosition().y()-50)//50][(self.player[0].getPosition().x())//50].getCollision()==False and ((self.player[0].getPosition().x())//50, (self.player[0].getPosition().y()-50)//50) not in self.posList: 
                    self.player[0].moveTo("UP")
                    self.moving()
                    self.timer()
                                
            elif event.key() == Qt.Key_S:
                self.Tab=1
                if self.terrain[(self.player[0].getPosition().y()+50)//50][(self.player[0].getPosition().x())//50].getCollision()==False and ((self.player[0].getPosition().x())//50, (self.player[0].getPosition().y()+50)//50) not in self.posList:
                    self.player[0].moveTo("DOWN")
                    self.moving()
                    self.timer()
                    
            elif event.key() == Qt.Key_Q:
                self.Tab=2
                if self.terrain[(self.player[0].getPosition().y())//50][(self.player[0].getPosition().x()-50)//50].getCollision()==False and ((self.player[0].getPosition().x()-50)//50, (self.player[0].getPosition().y())//50) not in self.posList:
                    self.player[0].moveTo("LEFT")
                    self.moving()
                    self.timer()

            elif event.key() == Qt.Key_D:
                self.Tab=3
                if self.terrain[(self.player[0].getPosition().y())//50][(self.player[0].getPosition().x()+50)//50].getCollision()==False and ((self.player[0].getPosition().x()+50)//50, (self.player[0].getPosition().y())//50) not in self.posList:
                    self.player[0].moveTo("RIGHT")
                    self.moving()
                    self.timer()

            elif event.key() == Qt.Key_Space and len(self.player[0].TabBombe)<self.player[0].getNbBombe():
                self.player[0].TabBombe.append(Bombe(QPoint(self.player[0].getPosition().x(), self.player[0].getPosition().y()), QColor(0, 0, 0), 1))
                self.posList.append((self.player[0].getPosition().x()//50, self.player[0].getPosition().y()//50))
                self.timers.append(QTimer())
                self.main.bruit6.play()
                self.choixBombe=0
                self.timers[-1].singleShot(2500, self.explodeBomb1)
        
        #Joueur2
        if self.player[1].getMort() == False:
            if event.key() == Qt.Key_T:
                self.Tab2=0
                if self.terrain[(self.player[1].getPosition().y()-50)//50][(self.player[1].getPosition().x())//50].getCollision()==False and ((self.player[1].getPosition().x())//50, (self.player[1].getPosition().y()-50)//50) not in self.posList: 
                    self.player[1].moveTo("UP")
                    self.moving2()
                    self.timer2()
                                
            elif event.key() == Qt.Key_G:
                self.Tab2=1
                if self.terrain[(self.player[1].getPosition().y()+50)//50][(self.player[1].getPosition().x())//50].getCollision()==False and ((self.player[1].getPosition().x())//50, (self.player[1].getPosition().y()+50)//50) not in self.posList:
                    self.player[1].moveTo("DOWN")
                    self.moving2()
                    self.timer2()
                    
            elif event.key() == Qt.Key_F:
                self.Tab2=2
                if self.terrain[(self.player[1].getPosition().y())//50][(self.player[1].getPosition().x()-50)//50].getCollision()==False and ((self.player[1].getPosition().x()-50)//50, (self.player[1].getPosition().y())//50) not in self.posList:
                    self.player[1].moveTo("LEFT")
                    self.moving2()
                    self.timer2()

            elif event.key() == Qt.Key_H:
                self.Tab2=3
                if self.terrain[(self.player[1].getPosition().y())//50][(self.player[1].getPosition().x()+50)//50].getCollision()==False and ((self.player[1].getPosition().x()+50)//50, (self.player[1].getPosition().y())//50) not in self.posList:
                    self.player[1].moveTo("RIGHT")
                    self.moving2()
                    self.timer2()

            elif event.key() == Qt.Key_N and len(self.player[1].TabBombe)<self.player[1].getNbBombe():
                self.player[1].TabBombe.append(Bombe(QPoint(self.player[1].getPosition().x(), self.player[1].getPosition().y()), QColor(0, 0, 0), 1))
                self.posList.append((self.player[1].getPosition().x()//50, self.player[1].getPosition().y()//50))
                self.timers.append(QTimer())
                self.main.bruit6.play()
                self.choixBombe=1
                self.timers[-1].singleShot(2500, self.explodeBomb2)

        #Joueur3
        if self.player[2].getMort() == False:
            if event.key() == Qt.Key_I:
                self.Tab3=0
                if self.terrain[(self.player[2].getPosition().y()-50)//50][(self.player[2].getPosition().x())//50].getCollision()==False and ((self.player[2].getPosition().x())//50, (self.player[2].getPosition().y()-50)//50) not in self.posList: 
                    self.player[2].moveTo("UP")
                    self.moving3()
                    self.timer3()
                                
            elif event.key() == Qt.Key_K:
                self.Tab3=1
                if self.terrain[(self.player[2].getPosition().y()+50)//50][(self.player[2].getPosition().x())//50].getCollision()==False and ((self.player[2].getPosition().x())//50, (self.player[2].getPosition().y()+50)//50) not in self.posList:
                    self.player[2].moveTo("DOWN")
                    self.moving3()
                    self.timer3()
                    
            elif event.key() == Qt.Key_J:
                self.Tab3=2
                if self.terrain[(self.player[2].getPosition().y())//50][(self.player[2].getPosition().x()-50)//50].getCollision()==False and ((self.player[2].getPosition().x()-50)//50, (self.player[2].getPosition().y())//50) not in self.posList:
                    self.player[2].moveTo("LEFT")
                    self.moving3()
                    self.timer3()

            elif event.key() == Qt.Key_L:
                self.Tab3=3
                if self.terrain[(self.player[2].getPosition().y())//50][(self.player[2].getPosition().x()+50)//50].getCollision()==False and ((self.player[2].getPosition().x()+50)//50, (self.player[2].getPosition().y())//50) not in self.posList:
                    self.player[2].moveTo("RIGHT")
                    self.moving3()
                    self.timer3()

            elif event.key() == Qt.Key_M and len(self.player[2].TabBombe)<self.player[2].getNbBombe():
                self.player[2].TabBombe.append(Bombe(QPoint(self.player[2].getPosition().x(), self.player[2].getPosition().y()), QColor(0, 0, 0), 1))
                self.posList.append((self.player[2].getPosition().x()//50, self.player[2].getPosition().y()//50))
                self.timers.append(QTimer())
                self.main.bruit6.play()
                self.choixBombe=2
                self.timers[-1].singleShot(2500, self.explodeBomb3)
        
        #Joueur4
        if self.player[3].getMort() == False:
            if event.key() == Qt.Key_Up:
                self.Tab4=0
                if self.terrain[(self.player[3].getPosition().y()-50)//50][(self.player[3].getPosition().x())//50].getCollision()==False and ((self.player[3].getPosition().x())//50, (self.player[3].getPosition().y()-50)//50) not in self.posList: 
                    self.player[3].moveTo("UP")
                    self.moving4()
                    self.timer4()
                                
            elif event.key() == Qt.Key_Down:
                self.Tab4=1
                if self.terrain[(self.player[3].getPosition().y()+50)//50][(self.player[3].getPosition().x())//50].getCollision()==False and ((self.player[3].getPosition().x())//50, (self.player[3].getPosition().y()+50)//50) not in self.posList:
                    self.player[3].moveTo("DOWN")
                    self.moving4()
                    self.timer4()
                    
            elif event.key() == Qt.Key_Left:
                self.Tab4=2
                if self.terrain[(self.player[3].getPosition().y())//50][(self.player[3].getPosition().x()-50)//50].getCollision()==False and ((self.player[3].getPosition().x()-50)//50, (self.player[3].getPosition().y())//50) not in self.posList:
                    self.player[3].moveTo("LEFT")
                    self.moving4()
                    self.timer4()

            elif event.key() == Qt.Key_Right:
                self.Tab4=3
                if self.terrain[(self.player[3].getPosition().y())//50][(self.player[3].getPosition().x()+50)//50].getCollision()==False and ((self.player[3].getPosition().x()+50)//50, (self.player[3].getPosition().y())//50) not in self.posList:
                    self.player[3].moveTo("RIGHT")
                    self.moving4()
                    self.timer4()

            elif event.key() == Qt.Key_Shift and len(self.player[3].TabBombe)<self.player[3].getNbBombe():
                self.player[3].TabBombe.append(Bombe(QPoint(self.player[3].getPosition().x(), self.player[3].getPosition().y()), QColor(0, 0, 0), 1))
                self.posList.append((self.player[3].getPosition().x()//50, self.player[3].getPosition().y()//50))
                self.timers.append(QTimer())
                self.main.bruit6.play()
                self.choixBombe=3
                self.timers[-1].singleShot(2500, self.explodeBomb4)
        
        if event.key() == Qt.Key_P:
            self.menuPause()
        
        for i in range(4):
            if self.player[i].getMort() == False and type(self.terrain[(self.player[i].getPosition().y())//50][(self.player[i].getPosition().x())//50]).__name__ == "Objet":
                self.gestionObjet(self.terrain[(self.player[i].getPosition().y())//50][(self.player[i].getPosition().x())//50].getType(),i)
                self.terrain[(self.player[i].getPosition().y())//50][(self.player[i].getPosition().x())//50] = Case(QPoint(self.player[i].getPosition().x(), self.player[i].getPosition().y()), False, self.terrainSprite["herbe"])
        self.update()
    
    '''
    gestionObjet
    Permet de gérer les effets des objets
    '''
    #Gestion objets
    def gestionObjet(self, typeObjet, player):
        if typeObjet == "force":
            self.player[player].incForceBombe()
            if player == 0:
                if self.imgQuantity == 4:
                    self.main.bruit8.play()
                    self.imgNum = 6
                    self.imgQuantity = 9
                elif self.imgQuantity == 9:
                    self.main.bruit9.play()
                    self.imgNum = 11
                    self.imgQuantity = 14

            if player == 1:
                if self.imgQuantity2 == 4:
                    self.main.bruit8.play()
                    self.imgNum2 = 6
                    self.imgQuantity2 = 9
                elif self.imgQuantity2 == 9:
                    self.main.bruit9.play()
                    self.imgNum2 = 11
                    self.imgQuantity2 = 14

            if player == 2:
                if self.imgQuantity3 == 4:
                    self.main.bruit8.play()
                    self.imgNum3 = 6
                    self.imgQuantity3 = 9
                elif self.imgQuantity3 == 9:
                    self.main.bruit9.play()
                    self.imgNum3 = 11
                    self.imgQuantity3 = 14

            if player == 3:
                if self.imgQuantity4 == 4:
                    self.main.bruit8.play()
                    self.imgNum4 = 6
                    self.imgQuantity4 = 9
                elif self.imgQuantity4 == 9:
                    self.main.bruit9.play()
                    self.imgNum4 = 11
                    self.imgQuantity4 = 14
        elif typeObjet == "bombe":
            self.player[player].incNbBombe()

    '''
    drawPropagation
    Permet de dessiner la propagation des bombes quand elles explosent
    '''
    #Dessin propagation
    def drawPropagation(self, painter):
        brush = QBrush()
        for i in self.propagation:
            brush.setTexture(i.getCouleur())
            painter.setBrush(brush)
            painter.drawRect((QRect(i.getPosition(), QSize(50, 50))))
    
    '''
    removePropagation
    Vide le tableau de propagation
    '''
    #Enlever dessin propagation
    def removePropagation(self):
        for i in self.propagation:
            i.setPosition(0, -50)
        self.propagation = []
        self.propaPosList = []

    '''
    playerLooseALife
    Gere le moment où le joueur pert une vie est donc meurt
    '''
    #Qaund le joueur perds une vie
    def playerLooseALife(self,i):
        self.main.bruit3.play()
        self.player[i].setPosition(0, -50)
        self.player[i].setMort(True)
    
    '''
    drawBomb
    Dessine les bombes pour le joueur 1
    '''
    #Dessine la bombe
    def drawBomb(self, painter):
        self.bombeAnime()
        painter.setBrush(self.bombBrush)
        for i in range(len(self.player[0].TabBombe)):
            painter.drawRect(QRect(self.player[0].TabBombe[i].getPosition(), QSize(50, 50)))

    '''
    drawBomb
    Dessine les bombes pour le joueur 2
    '''
    def drawBomb2(self, painter):
        self.bombeAnime()
        painter.setBrush(self.bombBrush)
        for i in range(len(self.player[1].TabBombe)):
            painter.drawRect(QRect(self.player[1].TabBombe[i].getPosition(), QSize(50, 50)))

    '''
    drawBomb
    Dessine les bombes pour le joueur 3
    '''
    def drawBomb3(self, painter):
        self.bombeAnime()
        painter.setBrush(self.bombBrush)
        for i in range(len(self.player[2].TabBombe)):
            painter.drawRect(QRect(self.player[2].TabBombe[i].getPosition(), QSize(50, 50)))

    '''
    drawBomb
    Dessine les bombes pour le joueur 4
    '''
    def drawBomb4(self, painter):
        self.bombeAnime()
        painter.setBrush(self.bombBrush)
        for i in range(len(self.player[3].TabBombe)):
            painter.drawRect(QRect(self.player[3].TabBombe[i].getPosition(), QSize(50, 50)))

    '''
    explodeBomb
    Gere l'explosion d'une bombe pour le joueur 1
    '''
    #Gestion explosion bombe joueur1
    def explodeBomb1(self):
        i = 0
        # Propagation à droite
        while i < self.player[0].getForceBombe() and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
            if self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
                if i+1 == self.player[0].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x()+((i+1)*50), self.player[0].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin droite"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x()+((i+1)*50), self.player[0].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[0].TabBombe[0].getPosition().x()+((i+1)*50))//50, (self.player[0].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation à gauche
        while i < self.player[0].getForceBombe() and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
            if self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
                if i+1 == self.player[0].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x()-((i+1)*50), self.player[0].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin gauche"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x()-((i+1)*50), self.player[0].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[0].TabBombe[0].getPosition().x()-((i+1)*50))//50, (self.player[0].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation en bas
        while i < self.player[0].getForceBombe() and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[0].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x(), self.player[0].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["fin bas"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x(), self.player[0].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[0].TabBombe[0].getPosition().x())//50, (self.player[0].TabBombe[0].getPosition().y()+((i+1)*50))//50))
            i+=1
        i = 0
        # Propagation en haut
        while i < self.player[0].getForceBombe() and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[0].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x(), self.player[0].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["fin haut"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x(), self.player[0].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[0].TabBombe[0].getPosition().x())//50, (self.player[0].TabBombe[0].getPosition().y()-((i+1)*50))//50))
            i+=1

        self.propagation.append(Case(QPoint(self.player[0].TabBombe[0].getPosition().x(), self.player[0].TabBombe[0].getPosition().y()), False, self.propagationSprite["milieu"]))
        self.propaPosList.append((self.player[0].TabBombe[0].getPosition().x()//50, self.player[0].TabBombe[0].getPosition().y()//50))

        self.propaTimer.singleShot(400, self.removePropagation)

        i = 0
        dejaExplose = False
        # Brique à droite
        while i < self.player[0].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)].getSortie() == True:
                    self.terrain[self.player[0].TabBombe[0].getPosition().y()//50][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)] = Case(QPoint(self.player[0].TabBombe[0].getPosition().x()+(i+1)*50, self.player[0].TabBombe[0].getPosition().y()), False, self.terrainSprite["sorti"]) 
                else:
                    if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ != "Objet" and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet().getType() != "null":
                        self.terrain[self.player[0].TabBombe[0].getPosition().y()//50][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)] = self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                    else:
                        self.terrain[self.player[0].TabBombe[0].getPosition().y()//50][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)] = Case(QPoint(self.player[0].TabBombe[0].getPosition().x()+(i+1)*50, self.player[0].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique à gauche
        while i < self.player[0].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Objet" and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)].getObjet().getType() != "null":
                    self.terrain[self.player[0].TabBombe[0].getPosition().y()//50][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)] = self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.player[0].TabBombe[0].getPosition().y()//50][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)] = Case(QPoint(self.player[0].TabBombe[0].getPosition().x()-(i+1)*50, self.player[0].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)][(self.player[0].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en bas
        while i < self.player[0].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)]).__name__ == "Objet" and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[0].TabBombe[0].getPosition().x(), self.player[0].TabBombe[0].getPosition().y()+(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en haut
        while i < self.player[0].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)]).__name__ != "Objet" and self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[0].TabBombe[0].getPosition().x(), self.player[0].TabBombe[0].getPosition().y()-(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[0].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[0].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        self.player[0].TabBombe[0].setPosition(0, -50)
        self.player[0].TabBombe.pop(0)
        self.posList.pop(0)
        self.timers.pop(0)
        self.main.bruit0.play()
        self.update()

    '''
    explodeBomb
    Gere l'explosion d'une bombe pour le joueur 2
    '''
    #Gestion explosion bombe joueur2
    def explodeBomb2(self):
        i = 0
        # Propagation à droite
        while i < self.player[1].getForceBombe() and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
            if self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
                if i+1 == self.player[1].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x()+((i+1)*50), self.player[1].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin droite"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x()+((i+1)*50), self.player[1].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[1].TabBombe[0].getPosition().x()+((i+1)*50))//50, (self.player[1].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation à gauche
        while i < self.player[1].getForceBombe() and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
            if self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
                if i+1 == self.player[1].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x()-((i+1)*50), self.player[1].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin gauche"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x()-((i+1)*50), self.player[1].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[1].TabBombe[0].getPosition().x()-((i+1)*50))//50, (self.player[1].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation en bas
        while i < self.player[1].getForceBombe() and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[1].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x(), self.player[1].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["fin bas"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x(), self.player[1].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[1].TabBombe[0].getPosition().x())//50, (self.player[1].TabBombe[0].getPosition().y()+((i+1)*50))//50))
            i+=1
        i = 0
        # Propagation en haut
        while i < self.player[1].getForceBombe() and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[1].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x(), self.player[1].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["fin haut"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x(), self.player[1].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[1].TabBombe[0].getPosition().x())//50, (self.player[1].TabBombe[0].getPosition().y()-((i+1)*50))//50))
            i+=1

        self.propagation.append(Case(QPoint(self.player[1].TabBombe[0].getPosition().x(), self.player[1].TabBombe[0].getPosition().y()), False, self.propagationSprite["milieu"]))
        self.propaPosList.append((self.player[1].TabBombe[0].getPosition().x()//50, self.player[1].TabBombe[0].getPosition().y()//50))

        self.propaTimer.singleShot(400, self.removePropagation)

        i = 0
        dejaExplose = False
        # Brique à droite
        while i < self.player[1].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ != "Objet" and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet().getType() != "null":
                    self.terrain[self.player[1].TabBombe[0].getPosition().y()//50][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)] = self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.player[1].TabBombe[0].getPosition().y()//50][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)] = Case(QPoint(self.player[1].TabBombe[0].getPosition().x()+(i+1)*50, self.player[1].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique à gauche
        while i < self.player[1].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Objet" and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)].getObjet().getType() != "null":
                    self.terrain[self.player[1].TabBombe[0].getPosition().y()//50][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)] = self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.player[1].TabBombe[0].getPosition().y()//50][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)] = Case(QPoint(self.player[1].TabBombe[0].getPosition().x()-(i+1)*50, self.player[1].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)][(self.player[1].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en bas
        while i < self.player[1].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)]).__name__ == "Objet" and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[1].TabBombe[0].getPosition().x(), self.player[1].TabBombe[0].getPosition().y()+(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en haut
        while i < self.player[1].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)]).__name__ != "Objet" and self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[1].TabBombe[0].getPosition().x(), self.player[1].TabBombe[0].getPosition().y()-(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[1].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[1].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        self.player[1].TabBombe[0].setPosition(0, -50)
        self.player[1].TabBombe.pop(0)
        self.posList.pop(0)
        self.timers.pop(0)
        self.main.bruit0.play()
        self.update()

    '''
    explodeBomb
    Gere l'explosion d'une bombe pour le joueur 3
    '''
    #Gestion explosion bombe joueur3
    def explodeBomb3(self):
        i = 0
        # Propagation à droite
        while i < self.player[2].getForceBombe() and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
            if self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
                if i+1 == self.player[2].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x()+((i+1)*50), self.player[2].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin droite"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x()+((i+1)*50), self.player[2].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[2].TabBombe[0].getPosition().x()+((i+1)*50))//50, (self.player[2].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation à gauche
        while i < self.player[2].getForceBombe() and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
            if self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
                if i+1 == self.player[2].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x()-((i+1)*50), self.player[2].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin gauche"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x()-((i+1)*50), self.player[2].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[2].TabBombe[0].getPosition().x()-((i+1)*50))//50, (self.player[2].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation en bas
        while i < self.player[2].getForceBombe() and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[2].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x(), self.player[2].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["fin bas"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x(), self.player[2].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[2].TabBombe[0].getPosition().x())//50, (self.player[2].TabBombe[0].getPosition().y()+((i+1)*50))//50))
            i+=1
        i = 0
        # Propagation en haut
        while i < self.player[2].getForceBombe() and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[2].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x(), self.player[2].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["fin haut"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x(), self.player[2].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[2].TabBombe[0].getPosition().x())//50, (self.player[2].TabBombe[0].getPosition().y()-((i+1)*50))//50))
            i+=1

        self.propagation.append(Case(QPoint(self.player[2].TabBombe[0].getPosition().x(), self.player[2].TabBombe[0].getPosition().y()), False, self.propagationSprite["milieu"]))
        self.propaPosList.append((self.player[2].TabBombe[0].getPosition().x()//50, self.player[2].TabBombe[0].getPosition().y()//50))

        self.propaTimer.singleShot(400, self.removePropagation)

        i = 0
        dejaExplose = False
        # Brique à droite
        while i < self.player[2].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ != "Objet" and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet().getType() != "null":
                    self.terrain[self.player[2].TabBombe[0].getPosition().y()//50][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)] = self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.player[2].TabBombe[0].getPosition().y()//50][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)] = Case(QPoint(self.player[2].TabBombe[0].getPosition().x()+(i+1)*50, self.player[2].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique à gauche
        while i < self.player[2].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Objet" and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)].getObjet().getType() != "null":
                    self.terrain[self.player[2].TabBombe[0].getPosition().y()//50][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)] = self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.player[2].TabBombe[0].getPosition().y()//50][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)] = Case(QPoint(self.player[2].TabBombe[0].getPosition().x()-(i+1)*50, self.player[2].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)][(self.player[2].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en bas
        while i < self.player[2].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)]).__name__ == "Objet" and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[2].TabBombe[0].getPosition().x(), self.player[2].TabBombe[0].getPosition().y()+(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en haut
        while i < self.player[2].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)]).__name__ != "Objet" and self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[2].TabBombe[0].getPosition().x(), self.player[2].TabBombe[0].getPosition().y()-(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[2].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[2].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        self.player[2].TabBombe[0].setPosition(0, -50)
        self.player[2].TabBombe.pop(0)
        self.posList.pop(0)
        self.timers.pop(0)
        self.main.bruit0.play()
        self.update()

    '''
    explodeBomb
    Gere l'explosion d'une bombe pour le joueur 4
    '''
    #Gestion explosion bombe joueur4
    def explodeBomb4(self):
        i = 0
        # Propagation à droite
        while i < self.player[3].getForceBombe() and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
            if self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == False:
                if i+1 == self.player[3].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x()+((i+1)*50), self.player[3].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin droite"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x()+((i+1)*50), self.player[3].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[3].TabBombe[0].getPosition().x()+((i+1)*50))//50, (self.player[3].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation à gauche
        while i < self.player[3].getForceBombe() and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
            if self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == False:
                if i+1 == self.player[3].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x()-((i+1)*50), self.player[3].TabBombe[0].getPosition().y()), False, self.propagationSprite["fin gauche"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x()-((i+1)*50), self.player[3].TabBombe[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.player[3].TabBombe[0].getPosition().x()-((i+1)*50))//50, (self.player[3].TabBombe[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation en bas
        while i < self.player[3].getForceBombe() and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[3].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x(), self.player[3].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["fin bas"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x(), self.player[3].TabBombe[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[3].TabBombe[0].getPosition().x())//50, (self.player[3].TabBombe[0].getPosition().y()+((i+1)*50))//50))
            i+=1
        i = 0
        # Propagation en haut
        while i < self.player[3].getForceBombe() and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player[3].getForceBombe():
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x(), self.player[3].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["fin haut"]))
                else:
                    self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x(), self.player[3].TabBombe[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.player[3].TabBombe[0].getPosition().x())//50, (self.player[3].TabBombe[0].getPosition().y()-((i+1)*50))//50))
            i+=1

        self.propagation.append(Case(QPoint(self.player[3].TabBombe[0].getPosition().x(), self.player[3].TabBombe[0].getPosition().y()), False, self.propagationSprite["milieu"]))
        self.propaPosList.append((self.player[3].TabBombe[0].getPosition().x()//50, self.player[3].TabBombe[0].getPosition().y()//50))

        self.propaTimer.singleShot(400, self.removePropagation)

        i = 0
        dejaExplose = False
        # Brique à droite
        while i < self.player[3].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)]).__name__ != "Objet" and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet().getType() != "null":
                    self.terrain[self.player[3].TabBombe[0].getPosition().y()//50][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)] = self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.player[3].TabBombe[0].getPosition().y()//50][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)] = Case(QPoint(self.player[3].TabBombe[0].getPosition().x()+(i+1)*50, self.player[3].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique à gauche
        while i < self.player[3].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)]).__name__ == "Objet" and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)].getObjet().getType() != "null":
                    self.terrain[self.player[3].TabBombe[0].getPosition().y()//50][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)] = self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.player[3].TabBombe[0].getPosition().y()//50][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)] = Case(QPoint(self.player[3].TabBombe[0].getPosition().x()-(i+1)*50, self.player[3].TabBombe[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)][(self.player[3].TabBombe[0].getPosition().x()//50)-(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en bas
        while i < self.player[3].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)]).__name__ == "Objet" and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[3].TabBombe[0].getPosition().x(), self.player[3].TabBombe[0].getPosition().y()+(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)+(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en haut
        while i < self.player[3].getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if type(self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)]).__name__ != "Objet" and self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)] = self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)] = Case(QPoint(self.player[3].TabBombe[0].getPosition().x(), self.player[3].TabBombe[0].getPosition().y()-(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.player[3].TabBombe[0].getPosition().y()//50)-(i+1)][(self.player[3].TabBombe[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        self.player[3].TabBombe[0].setPosition(0, -50)
        self.player[3].TabBombe.pop(0)
        self.posList.pop(0)
        self.timers.pop(0)
        self.main.bruit0.play()
        self.update()

    '''
    drawPlayer
    Dessine le joueur 1
    '''
    #Dessine le joueur 1
    def drawPlayer(self, painter):
        painter.setBrush(self.playerBrush)
        painter.drawRect(QRect(self.player[0].getPosition(), QSize(50, 50)))

    '''
    drawPlayer
    Dessine le joueur 2
    '''
    #Dessine le joueur 2
    def drawPlayer2(self, painter):
        painter.setBrush(self.playerBrush2)
        painter.drawRect(QRect(self.player[1].getPosition(), QSize(50, 50)))
    
    '''
    drawPlayer
    Dessine le joueur 3
    '''
    #Dessine le joueur 3
    def drawPlayer3(self, painter):
        painter.setBrush(self.playerBrush3)
        painter.drawRect(QRect(self.player[2].getPosition(), QSize(50, 50)))

    '''
    drawPlayer
    Dessine le joueur 4
    '''
    #Dessine le joueur 4
    def drawPlayer4(self, painter):
        painter.setBrush(self.playerBrush4)
        painter.drawRect(QRect(self.player[3].getPosition(), QSize(50, 50)))

    '''
    drawTerrain
    Dessine la map
    '''
    #Dessine le terrain    
    def drawTerrain(self, painter):
        for i in range(len(self.terrain)):
            for j in range(len(self.terrain[0])):
                self.terrainBrush.setTexture(self.terrain[i][j].getCouleur())
                painter.setBrush(self.terrainBrush)
                painter.drawRect(QRect(self.terrain[i][j].getPosition(), QSize(50, 50)))

    '''
    randomObjet
    Defini les taux de drop des objets
    '''
    #Probabiliter des objets
    def randomObjet(self, pos):
        choice = random.randint(0, 100)
        if choice > 20:
            return Objet(pos, "none", "null")
        elif choice > 10:
            return Objet(pos, self.items[3], "force")
        elif choice >= 0:
            return Objet(pos, self.items[1], "bombe")

    '''
    createTerrain
    Créée la matrice de la map
    '''
    #Crée le terrain
    def createTerrain(self):
        self.terrain = []
        spriteMur = self.terrainSprite["mur"]
        spriteHerbe = self.terrainSprite["herbe"]
        spriteBordGauche = self.terrainSprite["bordGauche"]
        spriteBordDroit = self.terrainSprite["bordDroite"]
        bordHaut = self.terrainSprite["bordHaut"]
        bordBas = self.terrainSprite["bordBas"]
        jointureBasDroite = self.terrainSprite["jointureBasDroite"]
        jointureBasGauche = self.terrainSprite["jointureBasGauche"]
        jointureHautGauche = self.terrainSprite["jointureHautGauche"]
        jointureHautDroite = self.terrainSprite["jointureHautDroite"]
        rocher = self.terrainSprite["rocher"]
        
        # Première ligne
        ligne = []
        ligne.append(Case(QPoint(0, 0), True, jointureHautGauche))
        for i in range(1,18):
            mur = Case(QPoint(50*i, 0), True, bordHaut)
            ligne.append(mur)
        ligne.append(Case(QPoint(50*18, 0), True, jointureHautDroite))
        
        self.terrain.append(ligne)

        # Les deux lignes suivantes
        ligne = []
        ligne.append(Case(QPoint(0, 50), True, spriteBordGauche))
        for i in range(1,3):
            ligne.append(Case(QPoint(50*i, 50), False, spriteHerbe))
        for i in range(3, 16):
            ligne.append(Brique(QPoint(50*i, 50), rocher, self.randomObjet(QPoint(50*i, 50))))
        for i in range(16,18):
            ligne.append(Case(QPoint(50*i, 50), False, spriteHerbe))
        ligne.append(Case(QPoint(50*18, 50), True, spriteBordDroit))
        self.terrain.append(ligne)

        ligne = []
        ligne.append(Case(QPoint(0, 100), True, spriteBordGauche))
        ligne.append(Case(QPoint(50, 100), False, spriteHerbe))
        for i in range(2, 17):
            if i%2==0:
                ligne.append(Case(QPoint(50*i, 100), True, spriteMur))
            else:
                ligne.append(Brique(QPoint(50*i, 100), rocher, self.randomObjet(QPoint(50*i, 100))))
        ligne.append(Case(QPoint(50*17, 100), False, spriteHerbe))
        ligne.append(Case(QPoint(50*18, 100), True, spriteBordDroit))
        self.terrain.append(ligne)
        
        for j in range(3, 10):
            ligne = []
            mur = Case(QPoint(0, 50*j), True, spriteBordGauche)
            ligne.append(mur)
            if j%2==0:
                for i in range(1, 18):
                    if i%2==0:
                        mur = Case(QPoint(50*i, 50*j), True, spriteMur)
                        ligne.append(mur)
                    else:
                        herbe = Brique(QPoint(50*i, 50*j), rocher, self.randomObjet(QPoint(50*i, 50*j)))
                        ligne.append(herbe)
            else:
                for i in range(1, 18):
                    if i==0 or i==18:
                        mur = Case(QPoint(50*i, 50*j), True, spriteMur)
                        ligne.append(mur)
                    else:
                        herbe = Brique(QPoint(50*i, 50*j), rocher, self.randomObjet(QPoint(50*i, 50*j)))
                        ligne.append(herbe)
            mur = Case(QPoint(50*18, 50*j), True, spriteBordDroit)
            ligne.append(mur)
            self.terrain.append(ligne)

        ligne = []
        ligne.append(Case(QPoint(0, 50*10), True, spriteBordGauche))
        ligne.append(Case(QPoint(50, 50*10), False, spriteHerbe))
        for i in range(2, 17):
            if i%2==0:
                ligne.append(Case(QPoint(50*i, 50*10), True, spriteMur))
            else:
                ligne.append(Brique(QPoint(50*i, 50*10), rocher, self.randomObjet(QPoint(50*i, 50*10))))
        ligne.append(Case(QPoint(50*17, 50*10), False, spriteHerbe))
        ligne.append(Case(QPoint(50*18, 50*10), True, spriteBordDroit))
        self.terrain.append(ligne)

        ligne = []
        ligne.append(Case(QPoint(0, 50*11), True, spriteBordGauche))
        for i in range(1,3):
            ligne.append(Case(QPoint(50*i, 50*11), False, spriteHerbe))
        for i in range(3, 16):
            ligne.append(Brique(QPoint(50*i, 50*11), rocher, self.randomObjet(QPoint(50*i, 50*11))))
        for i in range(16,18):
            ligne.append(Case(QPoint(50*i, 50*11), False, spriteHerbe))
        ligne.append(Case(QPoint(50*18, 50*11), True, spriteBordDroit))
        self.terrain.append(ligne)

        ligne = []
        ligne.append(Case(QPoint(0, 50*12), True, jointureBasGauche))
        for i in range(1,18):
            mur = Case(QPoint(50*i, 50*12), True, bordBas)
            ligne.append(mur)
        ligne.append(Case(QPoint(50*18, 50*12), True, jointureBasDroite))
        
        self.terrain.append(ligne)
        
        i=random.randint(1,11)
        j=random.randint(1,17)

        while type(self.terrain[i][j]).__name__ != "Brique":
            i=random.randint(1,11)
            j=random.randint(1,17)

    '''
    paintEvent
    Gestionnaire de dessin de PyQt
    '''
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        self.drawTerrain(painter)
        if self.player[0].getMort() == False:
            self.drawPlayer(painter)
        if self.player[1].getMort() == False:
            self.drawPlayer2(painter)
        if self.player[2].getMort() == False:
            self.drawPlayer3(painter)
        if self.player[3].getMort() == False:
            self.drawPlayer4(painter)
            
        for i in range(len(self.player)):
            if ((self.player[i].getPosition().x())//50, (self.player[i].getPosition().y())//50) in self.propaPosList:
                self.playerLooseALife(i)

        self.drawBomb(painter)
        self.drawBomb2(painter)
        self.drawBomb3(painter)
        self.drawBomb4(painter)
        self.drawPropagation(painter)

        vic=self.victoire()

        if vic[0]==1:
            self.gagner(vic[1]+1)
        elif vic[0]==0:
            self.pasGagner()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    '''
    victoire
    Compte le nombre de joueurs restants et determine le vainqueur
    '''
    def victoire(self):
        count=0
        winner=0
        for i in range(len(self.player)):
            if self.player[i].getMort()==False:
                count+=1
                winner=i
        return count,winner

    '''
    gagner
    Affiche la fin de la partie et le vainqueur
    '''
    def gagner(self,vainqueur):
        self.main.stacked.close()
        self.main.resultat1(vainqueur)

    def pasGagner(self):
        self.main.stacked.close()
        self.main.resultat2()

    '''
    menuPause
    ouvre un fenetre de pause pour revenir sur le menu principal
    '''
    def menuPause(self):
        self.main.bruit1.play()
        self.menuPause1.setGeometry((self.frameGeometry().width()/2)-150,(self.frameGeometry().height()/2)-100,400,200)
        self.layout = QVBoxLayout()

        self.continuer=QPushButton("Continuer",self)
        self.continuer.setFixedSize(300,50)
        self.continuer.setCursor(Qt.PointingHandCursor)
        self.continuer.setFont(self.font)
        self.continuer.setStyleSheet(self.styleSheet)
        self.continuer.clicked.connect(self.continuer2)
        
        self.retourMenu=QPushButton("Menu principal",self)
        self.retourMenu.setFixedSize(300,50)
        self.retourMenu.setCursor(Qt.PointingHandCursor)
        self.retourMenu.setFont(self.font)
        self.retourMenu.setStyleSheet(self.styleSheet)
        self.retourMenu.clicked.connect(self.menuP)
        
        self.layout.addWidget(self.continuer)
        self.layout.addWidget(self.retourMenu)
        
        self.menuPause1.setLayout(self.layout)
        self.menuPause1.show()

    def continuer2(self):
        self.main.bruit1.play()
        self.menuPause1.close()
        self.setFocus(Qt.OtherFocusReason)

    def menuP(self):
        self.main.bruit1.play()
        self.main.musique.stop()
        self.main.musique.setSource(QUrl.fromLocalFile("sons/musique.wav"))
        self.main.musique.play()
        self.main.stacked.close()
        self.main.menuJouer()

    '''
    tuto
    ouvre un fenetre de tuto qui indique les touches pour chaque joueur
    '''
    def tuto(self):
        self.styleTuto="QWidget{background-color: rgb(0,0,0);border: 2px solid white;} QPushButton{ background-color: rgb(8,88,200); border-radius: 10px; border: 2px solid;} QLabel{font-size: 25px;}"
        self.styleSousTuto="QWidget{background-color: rgb(0,0,0);} QLabel{font-size: 25px;}"
        self.tuto1=QWidget(self)
        self.tuto1.setGeometry((self.frameGeometry().width()/2)-295,(self.frameGeometry().height()/2)-220,900,600)
        self.layout = QVBoxLayout()
        
        self.sousWidget=QWidget()

        self.sousWidget1=QWidget(self)
        self.sousWidget2=QWidget(self)
        self.sousWidget3=QWidget(self)
        self.sousWidget4=QWidget(self)
        self.sousWidget5=QWidget(self)

        self.sousWidget1.setStyleSheet(self.styleSousTuto)
        self.sousWidget2.setStyleSheet(self.styleSousTuto)
        self.sousWidget3.setStyleSheet(self.styleSousTuto)
        self.sousWidget4.setStyleSheet(self.styleSousTuto)
        self.sousWidget5.setStyleSheet(self.styleSousTuto)

        #layout1
        self.sousLayout1=QVBoxLayout()

        self.text1=QLabel(self)
        self.text1.setText("Tutoriel :")
        self.text1.setAlignment(Qt.AlignCenter)
        self.sousLayout1.addWidget(self.text1)

        self.sousWidget1.setLayout(self.sousLayout1)

        #layout2

        self.sousLayout2=QVBoxLayout()

        self.text21=QLabel(self)
        self.text22=QLabel(self)
        self.text23=QLabel(self)
        self.text24=QLabel(self)
        self.text25=QLabel(self)
        self.text26=QLabel(self)

        self.text21.setText("Joueur 1 :")
        self.text22.setText("Z : haut")
        self.text23.setText("Q : gauche")
        self.text24.setText("S : bas")
        self.text25.setText("D : droite")
        self.text26.setText("Space : bombe")

        self.sousLayout2.addWidget(self.text21)
        self.sousLayout2.addWidget(self.text22)
        self.sousLayout2.addWidget(self.text23)
        self.sousLayout2.addWidget(self.text24)
        self.sousLayout2.addWidget(self.text25)
        self.sousLayout2.addWidget(self.text26)
        self.sousWidget2.setLayout(self.sousLayout2)

        #layout3

        self.sousLayout3=QVBoxLayout()

        self.text31=QLabel(self)
        self.text32=QLabel(self)
        self.text33=QLabel(self)
        self.text34=QLabel(self)
        self.text35=QLabel(self)
        self.text36=QLabel(self)

        self.text31.setText("Joueur 2 :")
        self.text32.setText("T : haut")
        self.text33.setText("F : gauche")
        self.text34.setText("G : bas")
        self.text35.setText("H : droite")
        self.text36.setText("N : bombe")

        self.sousLayout3.addWidget(self.text31)
        self.sousLayout3.addWidget(self.text32)
        self.sousLayout3.addWidget(self.text33)
        self.sousLayout3.addWidget(self.text34)
        self.sousLayout3.addWidget(self.text35)
        self.sousLayout3.addWidget(self.text36)
        self.sousWidget3.setLayout(self.sousLayout3)

        #layout4
        self.sousLayout4=QVBoxLayout()

        self.text41=QLabel(self)
        self.text42=QLabel(self)
        self.text43=QLabel(self)
        self.text44=QLabel(self)
        self.text45=QLabel(self)
        self.text46=QLabel(self)

        self.text41.setText("Joueur 3 :")
        self.text42.setText("I : haut")
        self.text43.setText("J : gauche")
        self.text44.setText("K : bas")
        self.text45.setText("L : droite")
        self.text46.setText("space : bombe")

        self.sousLayout4.addWidget(self.text41)
        self.sousLayout4.addWidget(self.text42)
        self.sousLayout4.addWidget(self.text43)
        self.sousLayout4.addWidget(self.text44)
        self.sousLayout4.addWidget(self.text45)
        self.sousLayout4.addWidget(self.text46)
        self.sousWidget4.setLayout(self.sousLayout4)

        #layout5

        self.sousLayout5=QVBoxLayout()

        self.text51=QLabel(self)
        self.text52=QLabel(self)
        self.text53=QLabel(self)
        self.text54=QLabel(self)
        self.text55=QLabel(self)
        self.text56=QLabel(self)

        self.text51.setText("Joueur 4 :")
        self.text52.setText("Flèche de haut : haut")
        self.text53.setText("Flèche de gauche : gauche")
        self.text54.setText("Flèche de bas : bas")
        self.text55.setText("Flèche de droite : droite")
        self.text56.setText("Ctrl : bombe")

        self.sousLayout5.addWidget(self.text51)
        self.sousLayout5.addWidget(self.text52)
        self.sousLayout5.addWidget(self.text53)
        self.sousLayout5.addWidget(self.text54)
        self.sousLayout5.addWidget(self.text55)
        self.sousLayout5.addWidget(self.text56)
        self.sousWidget5.setLayout(self.sousLayout5)

        #sousLayout

        self.sousLayout=QHBoxLayout()

        self.layout.addWidget(self.sousWidget1)
        self.sousLayout.addWidget(self.sousWidget2)
        self.sousLayout.addWidget(self.sousWidget3)
        self.sousLayout.addWidget(self.sousWidget4)
        self.sousLayout.addWidget(self.sousWidget5)
        self.sousWidget.setLayout(self.sousLayout)

        self.continuer6=QPushButton("Continuer",self)
        self.continuer6.setFixedSize(880,50)
        self.continuer6.setFont(self.font)
        self.continuer6.clicked.connect(self.fermerTuto)
        
        self.layout.addWidget(self.sousWidget)
        self.layout.addWidget(self.continuer6)
        
        self.tuto1.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.tuto1.show()

    '''
    tuto
    ferme la fenetre de tuto 
    '''
    def fermerTuto(self):
        self.main.bruit1.play()
        self.tuto1.close()
        self.setFocus(Qt.OtherFocusReason)