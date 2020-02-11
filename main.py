#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import pygame

from modele import *
from ai import *
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

class RenderArea(QWidget):
    imgNum=0
    imgNumAI=0
    imgQuantity=4
    imgQuantityAI=4
    imgBombe=0
    imgQuantityBombe=6
    def __init__(self,main, parent=None):
        super(RenderArea, self).__init__(parent)
        self.initUI()
        self.main=main

    '''
    initUI
    Defini toutes les variables utilisées dans le programme
    '''
    def initUI(self):
        pygame.init()

        self.gamepadTimer = QTimer()
        self.gamepadTimer.timeout.connect(self.gamepad)
        self.gamepadTimer.start(50)

        self.freezer = False
        self.pen = Qt.NoPen
        self.brush = QBrush(Qt.SolidPattern)
        self.playerBrush = QBrush()
        self.bombBrush = QBrush()
        self.AIBrush = QBrush()
        self.menuPause1=QWidget(self)
        self.perdu1= QWidget(self)
        self.font=QFont("Roboto",25,QFont.Bold)
        self.styleSheet="QPushButton{ background-color: rgb(8,88,200); border-radius: 10px; border: 2px solid;}"
        self.stylePerdu="QWidget{background-color: rgb(0,0,0);border: 2px solid white;} QPushButton{ background-color: rgb(8,88,200); border-radius: 10px; border: 2px solid;} QLabel{font-size: 25px;}"
        self.changeTimer=QTimer()
        self.mytimerAI=QTimer()
        self.mytimer = QTimer()
        self.playerTimer = QTimer()
        self.Tab=1
        self.TabAI=0

        self.tuto()

        self.propaTimer = QTimer()

        self.key = (0, -150)

        self.timers = []
        self.bombs = []
        self.posList = []
        self.propaPosList = []
        self.propagation = []
        self.player = Joueur(QPoint(50, 50), QColor(223, 56, 56), QBrush())

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
            "sorti":QPixmap("sprites/sorti.png")
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
                QPixmap('sprites/spritessj.png').copy(166,5,19,25).scaled(50,50),#joueurUp 5
                QPixmap('sprites/spritessj.png').copy(188,5,19,25).scaled(50,50),#joueurUp 6
                QPixmap('sprites/spritessj.png').copy(209,5,19,25).scaled(50,50),#joueurUp 7
                QPixmap('sprites/spritessj.png').copy(226,5,18,25).scaled(50,50),#joueurUp 8
                QPixmap('sprites/spritessj.png').copy(60,5,19,25).scaled(50,50),  #joueurUpStop
                #gokuSSJG
                QPixmap('sprites/spritessjg.png').copy(166,5,19,25).scaled(50,50),#joueurUp 10
                QPixmap('sprites/spritessjg.png').copy(188,5,19,25).scaled(50,50),#joueurUp 11
                QPixmap('sprites/spritessjg.png').copy(209,5,19,25).scaled(50,50),#joueurUp 12
                QPixmap('sprites/spritessjg.png').copy(226,5,18,25).scaled(50,50),#joueurUp 13
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

        self.AISprite = [
            [
                QPixmap('sprites/boo.png').copy(48,208,48,49).scaled(50,50),#IAUp 0
                QPixmap('sprites/boo.png').copy(98,208,48,49).scaled(50,50),#IAUp 1
                QPixmap('sprites/boo.png').copy(48,208,48,49).scaled(50,50),#IAUp 0
                QPixmap('sprites/boo.png').copy(98,208,48,49).scaled(50,50),#IAUp 1
                QPixmap('sprites/boo.png').copy(2,208,48,49).scaled(50,50)#IAstop
            ],
            [
                QPixmap('sprites/boo.png').copy(48,15,48,49).scaled(50,50),#IADown 0
                QPixmap('sprites/boo.png').copy(144,15,48,49).scaled(50,50),#IADown 1
                QPixmap('sprites/boo.png').copy(48,15,48,49).scaled(50,50),#IADown 0
                QPixmap('sprites/boo.png').copy(144,15,48,49).scaled(50,50),#IADown 1
                QPixmap('sprites/boo.png').copy(2,15,48,49).scaled(50,50)#IAstop
            ],
            [
                QPixmap('sprites/boo.png').copy(55,77,48,49).scaled(50,50),#IALeft 0
                QPixmap('sprites/boo.png').copy(145,77,48,49).scaled(50,50),#IALeft 1
                QPixmap('sprites/boo.png').copy(55,77,48,49).scaled(50,50),#IALeft 0
                QPixmap('sprites/boo.png').copy(145,77,48,49).scaled(50,50),#IALeft 1
                QPixmap('sprites/boo.png').copy(5,77,48,49).scaled(50,50)#IAstop
            ],
            [
                QPixmap('sprites/boo.png').copy(55,144,48,49).scaled(50,50), #IARight 0
                QPixmap('sprites/boo.png').copy(144,140,48,49).scaled(50,50), #IARight 1
                QPixmap('sprites/boo.png').copy(55,144,48,49).scaled(50,50), #IARight 0
                QPixmap('sprites/boo.png').copy(144,140,48,49).scaled(50,50), #IARight 1
                QPixmap('sprites/boo.png').copy(5,144,48,49).scaled(50,50) #IAstop
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
            QPixmap("sprites/itemFreezer.png").copy(0, 0, 50, 50).scaled(50,50),
            QPixmap("sprites/itemGenkidama.png").copy(0, 0, 50, 50).scaled(50,50),
            QPixmap("sprites/itemHaricot.png").copy(0, 0, 50, 50).scaled(50,50),
            QPixmap("sprites/itemSSJ.png").copy(0, 0, 50, 50).scaled(50,50)
        ]

        #self.main.bruit.setSource(self.main.bruitage[5])
        #self.main.bruit.play()
        self.playerBrush.setTexture(self.playerSprite[self.Tab][self.imgNum])

        self.AI = []

        self.AI.append(AI(QPoint(17*50, 11*50), self.AISprite[1][2]))
        self.AI[0].setEvent(Event.playerIsAway)

        self.AI.append(AI(QPoint(50, 11*50), self.AISprite[1][2]))
        self.AI[1].setEvent(Event.playerIsAway)

        self.AI.append(AI(QPoint(17*50, 50), self.AISprite[1][2]))
        self.AI[2].setEvent(Event.playerIsAway)

        choice = random.randint(0, 2)
        print("c'est", choice, "qui a la cle")
        self.AI[choice].setKey(True)

        self.AItimer = []
        for i in range(3):
            self.AItimer.append(QTimer())

        for i in range(len(self.AI)):
            self.AItimer[i].timeout.connect(self.AIProcessEvent)
            self.AItimer[i].start(1000)

        self.createTerrain()
    
    '''
    moving
    permet de changer de sprite pour le joueur
    timer
    permet au bout d'un temps donner de lancer la fonction myprint qui va mettre un sprite du joueur en position arret dans la dernier direction connue

    C'est le meme proceder pour l'AI
    '''
    def moving(self):
        if self.imgNum<self.imgQuantity-1:
            self.imgNum+=1
        else :
            self.imgNum=self.imgQuantity-3
        self.playerBrush.setTexture(self.playerSprite[self.Tab][self.imgNum])
      
    def movingAI(self):
        if self.imgNumAI<self.imgQuantityAI-1:
            self.imgNumAI+=1
        else :
            self.imgNumAI=0
        self.AIBrush.setTexture(self.AISprite[self.TabAI][self.imgNumAI])
    
    def bombeAnime(self):
        if self.imgBombe<self.imgQuantityBombe-1:
            self.imgBombe+=1
        else :
            self.imgBombe=0 
        self.bombBrush.setTexture(self.bombeSprite[self.imgBombe])

    def timer(self):
        self.mytimer.stop()
        self.mytimer = QTimer()
        self.mytimer.timeout.connect(self.myprint)
        self.mytimer.start(500)

    def myprint(self):
        self.playerBrush.setTexture(self.playerSprite[self.Tab][self.imgQuantity])
        self.update()

    def timerAI(self):
        self.mytimerAI.stop()
        self.mytimerAI = QTimer()
        self.mytimerAI.timeout.connect(self.myprintAI)
        self.mytimerAI.start(1000)

    def myprintAI(self):
        self.AIBrush.setTexture(self.AISprite[self.TabAI][4])
        self.update()

    '''
    gamepad
    Gere la manette en bluetooth
    '''
    def gamepad(self):
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
    def keyPressEvent(self, event):
        mouvementPossible = False
        if event.key() == Qt.Key_Z:
            self.Tab=0
            if self.terrain[(self.player.getPosition().y()-50)//50][(self.player.getPosition().x())//50].getCollision()==False and ((self.player.getPosition().x())//50, (self.player.getPosition().y()-50)//50) not in self.posList: 
                if self.freezer == False:
                    self.player.moveTo("UP")
                else:
                    pass
                mouvementPossible = True
                
                             
        elif event.key() == Qt.Key_S:
            self.Tab=1
            if self.terrain[(self.player.getPosition().y()+50)//50][(self.player.getPosition().x())//50].getCollision()==False and ((self.player.getPosition().x())//50, (self.player.getPosition().y()+50)//50) not in self.posList:
                if self.freezer == False:
                    self.player.moveTo("DOWN")
                else:
                    pass
                mouvementPossible = True
                
        elif event.key() == Qt.Key_Q:
            self.Tab=2
            if self.terrain[(self.player.getPosition().y())//50][(self.player.getPosition().x()-50)//50].getCollision()==False and ((self.player.getPosition().x()-50)//50, (self.player.getPosition().y())//50) not in self.posList:
                if self.freezer == False:
                    self.player.moveTo("LEFT")
                else:
                    pass
                mouvementPossible = True

        elif event.key() == Qt.Key_D:
            self.Tab=3
            if self.terrain[(self.player.getPosition().y())//50][(self.player.getPosition().x()+50)//50].getCollision()==False and ((self.player.getPosition().x()+50)//50, (self.player.getPosition().y())//50) not in self.posList:
                if self.freezer == False:
                    self.player.moveTo("RIGHT")
                else:
                    pass
                mouvementPossible = True

        if mouvementPossible:
            self.moving()
            self.timer()


        elif event.key() == Qt.Key_Space and len(self.bombs)<self.player.getNbBombe():
            self.bombs.append(Bombe(QPoint(self.player.getPosition().x(), self.player.getPosition().y()), QColor(0, 0, 0), 1))
            self.posList.append((self.player.getPosition().x()//50, self.player.getPosition().y()//50))
            self.timers.append(QTimer())
            self.main.bruit6.play()
            self.timers[-1].singleShot(2500, self.explodeBomb)
            
        elif event.key() == Qt.Key_P:
            self.menuPause()

        if (self.player.getPosition().x(), self.player.getPosition().y()) == self.key:
            self.brush.setTexture(QPixmap("sprites/niveau1.png").scaled(30, 30))
            self.key = (0, 0)
            self.player.setCle(True)
            self.main.score+=100
            self.main.bruit11.play()
        
        if self.player.getPosition() == self.sortiePos and (self.player.getCle() == True):
            self.main.score+=1000
            for i in range(self.player.getNbVie()):
                self.main.score+=150
            self.main.bruit4.play()
            self.gagner()

        # Gestion des objets
        if type(self.terrain[(self.player.getPosition().y())//50][(self.player.getPosition().x())//50]).__name__ == "Objet":
            self.gestionObjet(self.terrain[(self.player.getPosition().y())//50][(self.player.getPosition().x())//50].getType())
            self.terrain[(self.player.getPosition().y())//50][(self.player.getPosition().x())//50] = Case(QPoint(self.player.getPosition().x(), self.player.getPosition().y()), False, self.terrainSprite["herbe"])
        self.update()

    '''
    gestionObjet
    Permet de gérer les effets des objets
    '''
    def gestionObjet(self, typeObjet):
        if typeObjet == "force":
            self.player.incForceBombe()
            if self.imgQuantity == 4:
                self.main.bruit8.play()
                self.imgNum = 6
                self.imgQuantity = 9
            elif self.imgQuantity == 9:
                self.main.bruit9.play()
                self.imgNum = 11
                self.imgQuantity = 14
        elif typeObjet == "vie":
            self.player.incVie()
        elif typeObjet == "bombe":
            self.player.incNbBombe()
        elif typeObjet == "poison":
            self.main.bruit7.play()
            self.freezer = True
            timer = QTimer()
            timer.singleShot(10000, self.removeFreezer)
            
    '''
    removeFreezer
    Permet uniquement d'enlever les effets de Freezer
    '''
    def removeFreezer(self):
        self.freezer = False
    
    '''
    drawKey
    Permet de dessiner la clé dans la fenetre
    '''
    def drawKey(self, painter):
        brush = QBrush()
        brush.setTexture(QPixmap("sprites/niveau1.png").scaled(50, 50))
        painter.setBrush(brush)
        painter.drawRect(QRect(QPoint(self.key[0], self.key[1]), QSize(50, 50)))

    '''
    drawLife
    Permet de dessiner les coeurs dans la fenetre
    '''
    def drawLife(self, painter):
        brush = QBrush()
        brush.setTexture(QPixmap("sprites/vie.png").scaled(25, 25))
        painter.setBrush(brush)
        j=2
        for i in range(self.player.getNbVie()):
            painter.drawRect(QRect(QPoint(50*j,0), QSize(25, 25)))
            j+=1

    '''
    AIProcessEvent
    Fonction qui régis le comportement de l' """IA"""
    '''
    def AIProcessEvent(self):
        for ai in self.AI:
            self.cellsAroundEvent(ai)
            ai.setEvent(self.event)
            if ai.getState() == State.move:
                choice = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                AIpos = (ai.getPosition().x(), ai.getPosition().y())
                mouvementPossible = False
                if choice == "UP" and self.terrain[(AIpos[1]-50)//50][AIpos[0]//50].getCollision() == False and ((ai.getPosition().x())//50, (ai.getPosition().y()-50)//50) not in self.posList:
                    self.TabAI=0
                    mouvementPossible = True
                if choice == "DOWN" and self.terrain[(AIpos[1]+50)//50][AIpos[0]//50].getCollision() == False and ((ai.getPosition().x())//50, (ai.getPosition().y()+50)//50) not in self.posList:
                    self.TabAI=1
                    mouvementPossible = True
                if choice == "LEFT" and self.terrain[(AIpos[1])//50][(AIpos[0]-50)//50].getCollision() == False and ((ai.getPosition().x()-50)//50, (ai.getPosition().y())//50) not in self.posList:
                    self.TabAI=2
                    mouvementPossible = True
                if choice == "RIGHT" and self.terrain[(AIpos[1])//50][(AIpos[0]+50)//50].getCollision() == False and ((ai.getPosition().x()+50)//50, (ai.getPosition().y())//50) not in self.posList:
                    self.TabAI=3
                    mouvementPossible = True
                if mouvementPossible:
                    ai.moveTo(choice)
                    self.movingAI()
                    self.timerAI()

    '''
    drawPropagation
    Permet de dessiner la propagation des bombes quand elles explosent
    '''
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
    def removePropagation(self):
        self.propagation = []
        self.propaPosList = []

    '''
    playerLooseALife
    Gere le moment où le joueur pert une vie
    '''
    def playerLooseALife(self):
        self.player.setMort(True)
        self.player.setPosition(0, -50)
        self.player.decVie()
        self.main.bruit3.play()
        if self.player.getNbVie()<= 0:
            self.perdu()
        else:
            self.playerTimer.singleShot(1500, self.replacePlayer)

    '''
    perdu
    Gere le moment où le joueur n'a plus de vie et donc la fin de la partie
    '''
    def perdu(self):
        self.main.musique.stop()
        self.main.musique.setSource(QUrl.fromLocalFile("sons/musicD.wav"))
        self.main.musique.play()
        self.player.setPosition(0, -1000)
        self.perdu1.setGeometry((self.frameGeometry().width()/2)-300,(self.frameGeometry().height()/2)-200,600,400)
        self.layout = QVBoxLayout()

        self.image=QLabel(self)
        self.image.setPixmap(QPixmap("sprites/gokuMort.png"))

        self.text=QLabel(self)
        self.text.setText("GAME OVER !")
        self.text.setAlignment(Qt.AlignCenter)

        self.retry=QPushButton("Retry",self)
        self.retry.setFixedSize(580,50)
        self.retry.setFont(self.font)
        self.retry.clicked.connect(self.menuP)
        
        self.perdu1.setStyleSheet(self.stylePerdu)
        
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.retry)
        
        self.perdu1.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.perdu1.show()

    '''
    gagner
    Gere le moment où le joueur a gagner
    '''
    def gagner(self):
        self.main.stacked.close()
        self.main.resultat()
        
    '''
    replacePlayer
    Replace le joueur après son temps de respawn
    '''
    def replacePlayer(self):
        self.player.setMort(False)
        self.player.setPosition(50, 50)
        self.main.bruit10.play()
        self.playerBrush.setTexture(QPixmap('sprites/reaparaitre.png').scaled(50,50))
        self.update()
    
    def cellsAroundEvent(self, ai):
        AIpos = (ai.getPosition().x()//50, ai.getPosition().y()//50)
        Playerpos = (self.player.getPosition().x()//50, self.player.getPosition().y()//50)

        if Playerpos[0] < AIpos[0]-2 and Playerpos[0] > AIpos[0]+2 and Playerpos[1] < AIpos[1]-2 and Playerpos[1] > AIpos[1]+2:
            ai.setEvent(Event.playerIsNear)
        else:
            ai.setEvent(Event.playerIsAway)

    '''
    drawBomb
    Dessine les bombes
    '''
    def drawBomb(self, painter):
        self.bombeAnime()
        painter.setBrush(self.bombBrush)
        for i in range(len(self.bombs)):
            painter.drawRect((QRect(self.bombs[i].getPosition(), QSize(50, 50))))

    '''
    explodeBomb
    Gere l'explosion d'une bombe
    '''
    def explodeBomb(self):
        i = 0
        # Propagation à droite
        while i < self.player.getForceBombe() and self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)+(i+1)].getCollision() == False:
            if self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)+(i+1)].getCollision() == False:
                if i+1 == self.player.getForceBombe():
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x()+((i+1)*50), self.bombs[0].getPosition().y()), False, self.propagationSprite["fin droite"]))
                else:
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x()+((i+1)*50), self.bombs[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.bombs[0].getPosition().x()+((i+1)*50))//50, (self.bombs[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation à gauche
        while i < self.player.getForceBombe() and self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)-(i+1)].getCollision() == False:
            if self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)-(i+1)].getCollision() == False:
                if i+1 == self.player.getForceBombe():
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x()-((i+1)*50), self.bombs[0].getPosition().y()), False, self.propagationSprite["fin gauche"]))
                else:
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x()-((i+1)*50), self.bombs[0].getPosition().y()), False, self.propagationSprite["gauche/droite"]))
                self.propaPosList.append(((self.bombs[0].getPosition().x()-((i+1)*50))//50, (self.bombs[0].getPosition().y())//50))
            i+=1
        i = 0
        # Propagation en bas
        while i < self.player.getForceBombe() and self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player.getForceBombe():
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["fin bas"]))
                else:
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()+((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.bombs[0].getPosition().x())//50, (self.bombs[0].getPosition().y()+((i+1)*50))//50))
            i+=1
        i = 0
        # Propagation en haut
        while i < self.player.getForceBombe() and self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)].getCollision() == False:
            if self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)].getCollision() == False:
                if i+1 == self.player.getForceBombe():
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["fin haut"]))
                else:
                    self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()-((i+1)*50)), False, self.propagationSprite["haut/bas"]))
                self.propaPosList.append(((self.bombs[0].getPosition().x())//50, (self.bombs[0].getPosition().y()-((i+1)*50))//50))
            i+=1

        self.propagation.append(Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()), False, self.propagationSprite["milieu"]))
        self.propaPosList.append((self.bombs[0].getPosition().x()//50, self.bombs[0].getPosition().y()//50))

        self.propaTimer.singleShot(400, self.removePropagation)

        i = 0
        dejaExplose = False
        # Brique à droite
        while i < self.player.getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)+(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)+(i+1)].getSortie() == True:
                    self.terrain[self.bombs[0].getPosition().y()//50][(self.bombs[0].getPosition().x()//50)+(i+1)] = Case(QPoint(self.bombs[0].getPosition().x()+(i+1)*50, self.bombs[0].getPosition().y()), False, self.terrainSprite["sorti"]) 
                elif self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)+(i+1)].getObjet().getType() != "null":
                    self.terrain[self.bombs[0].getPosition().y()//50][(self.bombs[0].getPosition().x()//50)+(i+1)] = self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)+(i+1)].getObjet()
                else:
                    self.terrain[self.bombs[0].getPosition().y()//50][(self.bombs[0].getPosition().x()//50)+(i+1)] = Case(QPoint(self.bombs[0].getPosition().x()+(i+1)*50, self.bombs[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)+(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique à gauche
        while i < self.player.getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)-(i+1)]).__name__ == "Brique":
                dejaExplose = True
                if self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)-(i+1)].getSortie() == True:
                    self.terrain[self.bombs[0].getPosition().y()//50][(self.bombs[0].getPosition().x()//50)-(i+1)] = Case(QPoint(self.bombs[0].getPosition().x()-(i+1)*50, self.bombs[0].getPosition().y()), False, self.terrainSprite["sorti"])
                elif self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)-(i+1)].getObjet().getType() != "null":
                    self.terrain[self.bombs[0].getPosition().y()//50][(self.bombs[0].getPosition().x()//50)-(i+1)] = self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)-(i+1)].getObjet()
                else:
                    self.terrain[self.bombs[0].getPosition().y()//50][(self.bombs[0].getPosition().x()//50)-(i+1)] = Case(QPoint(self.bombs[0].getPosition().x()-(i+1)*50, self.bombs[0].getPosition().y()), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.bombs[0].getPosition().y()//50)][(self.bombs[0].getPosition().x()//50)-(i+1)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en bas
        while i < self.player.getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)].getSortie() == True:
                    self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)] = Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()+(i+1)*50), False, self.terrainSprite["sorti"])
                elif self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)] = self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)] = Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()+(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.bombs[0].getPosition().y()//50)+(i+1)][(self.bombs[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1
        i = 0
        dejaExplose = False
        # Brique en haut
        while i < self.player.getForceBombe() and dejaExplose == False:
            if type(self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)]).__name__ == "Brique":
                dejaExplose = True
                if self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)].getSortie() == True:
                    self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)] = Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()-(i+1)*50), False, self.terrainSprite["sorti"])
                elif self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)].getObjet().getType() != "null":
                    self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)] = self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)].getObjet()
                else:
                    self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)] = Case(QPoint(self.bombs[0].getPosition().x(), self.bombs[0].getPosition().y()-(i+1)*50), False, self.terrainSprite["herbe"])
            elif self.terrain[(self.bombs[0].getPosition().y()//50)-(i+1)][(self.bombs[0].getPosition().x()//50)].getCollision() == True:
                dejaExplose = True
            i+=1

        self.bombs[0].setPosition(0, -50)
        self.bombs.pop(0)
        self.posList.pop(0)
        self.timers.pop(0)
        self.main.bruit0.play()
        self.update()

    '''
    drawAI
    Dessine l' """IA"""
    '''
    def drawAI(self, ai, painter):
        painter.setBrush(self.AIBrush)
        painter.drawRect(QRect(ai.getPosition(), QSize(50, 50)))

    '''
    drawPlayer
    Dessine le joueur
    '''
    def drawPlayer(self, painter):
        painter.setBrush(self.playerBrush)
        painter.drawRect(QRect(self.player.getPosition(), QSize(50, 50)))

    '''
    drawTerrain
    Dessine la map
    '''
    def drawTerrain(self, painter):
        brush = QBrush()
        for i in range(len(self.terrain)):
            for j in range(len(self.terrain[0])):
                brush.setTexture(self.terrain[i][j].getCouleur())
                painter.setBrush(brush)
                painter.drawRect(QRect(self.terrain[i][j].getPosition(), QSize(50, 50)))

    '''
    randomObjet
    Defini les taux de drop des objets
    '''
    def randomObjet(self, pos):
        choice = random.randint(0, 100)
        if choice > 16:
            return Objet(pos, "none", "null")
        elif choice > 11:
            return Objet(pos, self.items[3], "force")
        elif choice > 6:
            return Objet(pos, self.items[2], "vie")
        elif choice > 1:
            return Objet(pos, self.items[1], "bombe")
        elif choice >= 0:
            return Objet(pos, self.items[0], "poison")
    
    '''
    createTerrain
    Créée la matrice de la map
    '''
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
        
        print("la sortie est en" , j, i)
        self.terrain[i][j].setSortie(True)

        self.sortiePos= self.terrain[i][j].getPosition()

    '''
    paintEvent
    Gestionnaire de dessin de PyQt
    '''
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        self.drawTerrain(painter)
        self.drawLife(painter)

        if self.player.getMort() == False:
            self.drawPlayer(painter)

        for i in range(len(self.AI)):
            if self.AI[i].getState() != State.dead:
                self.drawAI(self.AI[i], painter)
            if self.AI[i].getPosition() == self.player.getPosition():
                self.playerLooseALife()
            if ((self.AI[i].getPosition().x())//50, (self.AI[i].getPosition().y())//50) in self.propaPosList:
                if self.AI[i].getKey()==True:
                    self.key = (self.AI[i].getPosition().x(), self.AI[i].getPosition().y())
                self.AI[i].setState(State.dead)
                self.AI[i].setPosition(QPoint(0, -100))
                self.main.score+= 200
                self.main.bruit3.play()

        if ((self.player.getPosition().x())//50, (self.player.getPosition().y())//50) in self.propaPosList:
            self.playerLooseALife()

        self.drawKey(painter)

        self.drawBomb(painter)
        self.drawPropagation(painter)

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
        self.continuer.setFont(self.font)
        self.continuer.setStyleSheet(self.styleSheet)
        self.continuer.clicked.connect(self.continuer2)
        
        self.retourMenu=QPushButton("Menu principal",self)
        self.retourMenu.setFixedSize(300,50)
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
    ouvre un fenetre de tuto qui indique la fonction de chaque items
    '''
    def tuto(self):
        self.styleTuto="QWidget{background-color: rgb(0,0,0);border: 2px solid white;} QPushButton{ background-color: rgb(8,88,200); border-radius: 10px; border: 2px solid;} QLabel{font-size: 25px;}"
        self.styleSousTuto="QWidget{background-color: rgb(0,0,0);} QLabel{font-size: 25px;}"
        self.tuto1=QWidget(self)
        self.tuto1.setGeometry((self.frameGeometry().width()/2)-240,(self.frameGeometry().height()/2)-170,800,500)
        self.layout = QVBoxLayout()
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
        self.sousLayout1=QHBoxLayout()

        self.text1=QLabel(self)
        self.text1.setText("Tutoriel :")
        self.text1.setAlignment(Qt.AlignCenter)
        self.sousLayout1.addWidget(self.text1)

        self.sousWidget1.setLayout(self.sousLayout1)

        #layout2

        self.sousLayout2=QHBoxLayout()

        self.image2=QLabel(self)
        self.image2.setFixedSize(60,80)
        self.image2.setPixmap(QPixmap("sprites/itemGenkidama.png"))

        self.text2=QLabel(self)
        self.text2.setText("Permet d'avoir plus de bombe")

        self.sousLayout2.addWidget(self.image2)
        self.sousLayout2.addWidget(self.text2)
        self.sousWidget2.setLayout(self.sousLayout2)

        #layout3

        self.sousLayout3=QHBoxLayout()

        self.image3=QLabel(self)
        self.image3.setFixedSize(60,80)
        self.image3.setPixmap(QPixmap("sprites/itemHaricot.png").scaled(50,50))

        self.text3=QLabel(self)
        self.text3.setText("Permet d'avoir de la vie")

        self.sousLayout3.addWidget(self.image3)
        self.sousLayout3.addWidget(self.text3)
        self.sousWidget3.setLayout(self.sousLayout3)

        #layout4

        self.sousLayout4=QHBoxLayout()

        self.image4=QLabel(self)
        self.image4.setFixedSize(60,80)
        self.image4.setPixmap(QPixmap("sprites/itemSSJ.png").scaled(50,50))

        self.text4=QLabel(self)
        self.text4.setText("Permet d'améliorer la force des bombes")

        self.sousLayout4.addWidget(self.image4)
        self.sousLayout4.addWidget(self.text4)
        self.sousWidget4.setLayout(self.sousLayout4)

        #layout5

        self.sousLayout5=QHBoxLayout()

        self.image5=QLabel(self)
        self.image5.setFixedSize(60,80)
        self.image5.setPixmap(QPixmap("sprites/itemFreezer.png").scaled(50,50))

        self.text5=QLabel(self)
        self.text5.setText("Il immobilise le joueur")

        self.sousLayout5.addWidget(self.image5)
        self.sousLayout5.addWidget(self.text5)
        self.sousWidget5.setLayout(self.sousLayout5)

        self.continuer6=QPushButton("Continuer",self)
        self.continuer6.setFixedSize(780,50)
        self.continuer6.setFont(self.font)
        self.continuer6.clicked.connect(self.fermerTuto)
        
        self.layout.addWidget(self.sousWidget1)
        self.layout.addWidget(self.sousWidget2)
        self.layout.addWidget(self.sousWidget3)
        self.layout.addWidget(self.sousWidget4)
        self.layout.addWidget(self.sousWidget5)
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