#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
from main import *
from multijoueur import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p = self.palette()
        p.setColor(QPalette.Window,QColor(176,224,230))
        p.setColor(QPalette.Button,QColor(53,53,53))
        p.setColor(QPalette.Highlight,QColor(142,45,197))
        p.setColor(QPalette.ButtonText,QColor(255,255,255))
        p.setColor(QPalette.WindowText,QColor(255,255,255))
        self.setPalette(p)
        self.setWindowIcon(QIcon("sprites/niveau1.png"))

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window,self).__init__(parent)
        self.initUI()

    def initUI(self):

        # création des differents sons:
        self.bruit0=QSoundEffect()
        self.bruit1=QSoundEffect()
        self.bruit2=QSoundEffect()
        self.bruit3=QSoundEffect()
        self.bruit4=QSoundEffect()
        self.bruit5=QSoundEffect()
        self.bruit6=QSoundEffect()
        self.bruit7=QSoundEffect()
        self.bruit8=QSoundEffect()
        self.bruit9=QSoundEffect()
        self.bruit10=QSoundEffect()
        self.bruit11=QSoundEffect()

        #creation de la musique du menu:
        self.musique=QSoundEffect()
        self.musique.setSource(QUrl.fromLocalFile("sons/musique.wav"))
        self.musique.setLoopCount(QSoundEffect.Infinite)
        self.musique.setVolume(0.3)
        self.musique.play()

        #creation des sliders du menu option et set du volume des sons et de la musique au lancement du jeu:
        self.volume=QSlider(Qt.Horizontal)
        self.volume.setValue(30)
        self.volumeBruit=QSlider(Qt.Horizontal)
        self.volumeBruit.setValue(40)
        SLIDER = """QSlider::groove:horizontal {border: 2px solid #A0A5B2;
                border-radius: 2px;
                height: 4px;
                background: #E8E8E8;}
            QSlider::handle:horizontal {background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #FFFFFF, stop: 0.7 #3975D7,
                stop: 1.0 #C0C0FF);
                width: 20px;
                border-top: 1px solid #FFFFFF;
                border-left: 1px solid #0000FF;
                border-right: 1px solid #0000FF;
                border-bottom: 2px solid #0000CC;
                border-radius: 2px;
                margin: -3px 0;}"""

        self.volume.setStyleSheet(SLIDER)
        self.volumeBruit.setStyleSheet(SLIDER)

        #tableau contenant tous les sons du jeu et set de chaque son:

        self.bruitage=[
            QUrl.fromLocalFile("sons/explosion.wav"), #0
            QUrl.fromLocalFile("sons/menuA.wav"), #1
            QUrl.fromLocalFile("sons/menuR.wav"), #2
            QUrl.fromLocalFile("sons/mortEnnemi.wav"), #3
            QUrl.fromLocalFile("sons/sortir.wav"), #4
            QUrl.fromLocalFile("sons/depart.wav"), #5
            QUrl.fromLocalFile("sons/bombepose.wav"), #6
            QUrl.fromLocalFile("sons/itemF.wav"), #7
            QUrl.fromLocalFile("sons/ssjSound.wav"), #8
            QUrl.fromLocalFile("sons/ssjgSound.wav"), #9
            QUrl.fromLocalFile("sons/reaparaitre.wav"), #10
            QUrl.fromLocalFile("sons/recupboule.wav") #11     
        ]

        self.bruit0.setSource(self.bruitage[0])
        self.bruit1.setSource(self.bruitage[1])
        self.bruit2.setSource(self.bruitage[2])
        self.bruit3.setSource(self.bruitage[3])
        self.bruit4.setSource(self.bruitage[4])
        self.bruit5.setSource(self.bruitage[5])
        self.bruit6.setSource(self.bruitage[6])
        self.bruit7.setSource(self.bruitage[7])
        self.bruit8.setSource(self.bruitage[8])
        self.bruit9.setSource(self.bruitage[9])
        self.bruit10.setSource(self.bruitage[10])
        self.bruit11.setSource(self.bruitage[11])

        self.setGeometry(10, 10, 950, 650)
        self.setWindowTitle('DragonBomber Z')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.font=QFont("Roboto",25,QFont.Bold)
        self.styleSheet="QPushButton{ background-color: rgb(242,107,29); color: rgb(245,226,50); border-radius: 10px; border: 2px solid;}"
        self.styleSheetRetour="QPushButton{ background-color: transparent; border: 2px solid transparent;}"
        self.styleGagner="QWidget{background-color: rgb(0,0,0);border: 2px solid white;} QPushButton{ background-color: rgb(8,88,200); border-radius: 10px; border: 2px solid;} QLabel{font-size: 25px;}"   
        cursor = QPixmap('sprites/cursor.png').scaled(40,40)       
        self.setCursor(QCursor(cursor))
        self.score=0

        #Création du menu principal:

        self.menuRetour1=QWidget(self)
        #le menu:

        self.menu=QWidget(self)
        self.menu.setGeometry((self.frameGeometry().width()/2)-100,(self.frameGeometry().height()/2),300,200)
        self.layout = QVBoxLayout()

        #bouton jouer:

        self.jouer=QPushButton("Jouer",self)
        self.jouer.setFixedSize(200,50)
        self.jouer.setFont(self.font)
        self.jouer.setStyleSheet(self.styleSheet)
        self.jouer.clicked.connect(self.menuJouer)
        
        #bouton option:
        self.option=QPushButton("Options",self)
        self.option.setFixedSize(200,50)
        self.option.setFont(self.font)
        self.option.setStyleSheet(self.styleSheet)
        self.option.clicked.connect(self.option2)
        
        #bouton quitter
        self.quitter=QPushButton("Quitter",self)
        self.quitter.setFixedSize(200,50)
        self.quitter.setFont(self.font)
        self.quitter.setStyleSheet(self.styleSheet)
        self.quitter.clicked.connect(self.quit) 

        
        self.layout.addWidget(self.jouer)
        self.layout.addWidget(self.option)
        self.layout.addWidget(self.quitter)
        
        self.menu.setLayout(self.layout)

        #image de fond du jeu:

        self.oImage=QImage("sprites/fond.jpg")
        self.sImage=self.oImage.scaled(QSize(self.frameGeometry().width(),self.frameGeometry().height()))
        p2=QPalette()
        p2.setBrush(10,QBrush(self.sImage))
        self.setPalette(p2)
        
        self.setCenter()
        self.show()


    #fonction qui permet de centrer la fenêtre au milieu de l'écran:

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #fonction qui permet de quitter le jeu:

    def quit(self):
        self.bruit1.play()
        dialog=QMessageBox(self)
        dialog.setText('Voulez-vous vraiment quitter l\'application ?')
        dialog.setIcon(QMessageBox.Question)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        ret=dialog.exec_()
        if ret==QMessageBox.Yes:
            QCoreApplication.quit()

    #fonction qui est activé en appuyant sur le bouton jouer:  

    def menuJouer(self):
        self.bruit1.play()
        self.menu.close()

        self.menuJouer1=QWidget(self)
        self.menuJouer1.setGeometry((self.frameGeometry().width()/2)-350,(self.frameGeometry().height()/2)-350,700,700)
        self.layoutJouer = QHBoxLayout()
        
        #bouton solo:

        self.niveau1=QPushButton(" Solo",self)
        self.niveau1.setLayoutDirection(Qt.RightToLeft)
        self.niveau1.setIcon(QIcon("sprites/niveau1.png"))
        self.niveau1.setIconSize(QSize(45,45))
        self.niveau1.setFixedSize(200,50)
        self.niveau1.setFont(self.font)
        self.niveau1.setStyleSheet(self.styleSheet)
        self.niveau1.clicked.connect(self.jeu)

        #bouton multi:

        self.niveau2=QPushButton(" Multi",self)
        self.niveau2.setLayoutDirection(Qt.RightToLeft)
        self.niveau2.setIcon(QIcon("sprites/niveau2.png"))
        self.niveau2.setIconSize(QSize(45,45))
        self.niveau2.setFixedSize(200,50)
        self.niveau2.setFont(self.font)
        self.niveau2.setStyleSheet(self.styleSheet)
        self.niveau2.clicked.connect(self.jeuMulti)

        self.layoutJouer.addWidget(self.niveau1)
        self.layoutJouer.addWidget(self.niveau2)

        self.menuJouer1.setLayout(self.layoutJouer)

        self.menuJouer1.show()
        self.menuRetour()

    #fonction qui crée le bouton retour:
    
    def menuRetour(self):
        self.menuRetour1=QWidget(self)
        self.menuRetour1.setGeometry(30,10,100,100)
        self.layoutRetour = QHBoxLayout()
        
        font=QFont("Roboto",25,QFont.Bold)
        self.retour=QPushButton("",self)
        self.retour.setStyleSheet(self.styleSheetRetour)
        self.retour.setIcon(QIcon("sprites/retour.png"))
        self.retour.setIconSize(QSize(95,95))
        self.retour.setFixedSize(100,100)
        self.retour.clicked.connect(self.menuRetour2)
        self.retour.setFont(self.font)
        
        self.layoutRetour.addWidget(self.retour)
        self.menuRetour1.setLayout(self.layoutRetour)
        self.menuRetour1.show()

    #fonction qui permet de revenir au menu principal en partant du menu jouer:
    def menuRetour2(self):
        self.bruit2.play()
        self.menuJouer1.close()
        self.menuRetour1.close()

        self.menu.show()

    #fonction qui permet de jouer au solo lorsqu'on appui sur le bouton solo:

    def jeu(self):
        self.bruit1.play()
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/jeux.wav"))
        self.musique.play()
        self.menuJouer1.close()
        self.menuRetour1.close()
        self.score=0

        self.stacked=QStackedWidget()

        self.jeux=RenderArea(self)
        
        self.stacked.addWidget(self.jeux)
        self.stacked.setCurrentWidget(self.jeux)
        self.setCentralWidget(self.stacked)
        self.jeux.setFocus(Qt.OtherFocusReason)

    #fonction qui permet de jouer au solo lorsqu'on appui sur le bouton multi:

    def jeuMulti(self):
        self.bruit1.play()
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/jeux.wav"))
        self.musique.play()
        self.menuJouer1.close()
        self.menuRetour1.close()

        self.stacked=QStackedWidget()

        self.jeux=RenderAreaMulti(self)
        
        self.stacked.addWidget(self.jeux)
        self.stacked.setCurrentWidget(self.jeux)
        self.setCentralWidget(self.stacked)
        self.jeux.setFocus(Qt.OtherFocusReason)

    #fonction qui affiche la victoire du mode solo:
    
    def resultat(self):
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/musicV.wav"))
        self.musique.play()

        self.gagner1=QWidget(self)
        self.gagner1.setGeometry((self.frameGeometry().width()/2)-300,(self.frameGeometry().height()/2)-200,600,400)
        self.layout = QVBoxLayout()

        self.image=QLabel(self)
        self.image.setPixmap(QPixmap("sprites/gokuVictoire.png").scaled(600,300))

        #création du texte victoire:

        self.text=QLabel(self)
        self.text.setText("Victoire !")
        self.text.setAlignment(Qt.AlignCenter)

        texte="Score :"+" "+str(self.score)

        #affichage du score:

        self.score=QLabel(self)
        self.score.setText(texte)
        self.score.setAlignment(Qt.AlignCenter)

        #bouton continuer pour fermer le résultat:

        self.continuer5=QPushButton("Continuer",self)
        self.continuer5.setFixedSize(580,50)
        self.continuer5.setFont(self.font)
        self.continuer5.clicked.connect(self.finResultat)
        
        self.gagner1.setStyleSheet(self.styleGagner)
        
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.score)
        self.layout.addWidget(self.continuer5)
        
        self.gagner1.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.gagner1.show()

        #fonction qui affiche la victoire du mode multi:

    def resultat1(self,vainqueur):
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/musicV.wav"))
        self.musique.play()

        self.gagner2=QWidget(self)
        self.gagner2.setGeometry((self.frameGeometry().width()/2)-300,(self.frameGeometry().height()/2)-200,600,400)
        self.layout = QVBoxLayout()

        self.image=QLabel(self)
        self.image.setPixmap(QPixmap("sprites/gokuVictoire.png").scaled(600,300))

        texte="Victoire du joueur "+str(vainqueur)+" !"

        #affiche le vainqueur:

        self.text=QLabel(self)
        self.text.setText(texte)
        self.text.setAlignment(Qt.AlignCenter)

        #bouton continuer pour fermer le résultat:

        self.continuer5=QPushButton("Continuer",self)
        self.continuer5.setFixedSize(580,50)
        self.continuer5.setFont(self.font)
        self.continuer5.clicked.connect(self.finResultat1)
        
        self.gagner2.setStyleSheet(self.styleGagner)
        
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.continuer5)
        
        self.gagner2.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.gagner2.show()

    #fonction qui affiche aucune victoire si tout le monde est mort du mode multi:

    def resultat2(self):
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/musicD.wav"))
        self.musique.play()

        self.gagner3=QWidget(self)
        self.gagner3.setGeometry((self.frameGeometry().width()/2)-300,(self.frameGeometry().height()/2)-200,600,400)
        self.layout = QVBoxLayout()

        self.image=QLabel(self)
        self.image.setPixmap(QPixmap("sprites/gokuVictoire.png").scaled(600,300))

        #affiche pas de gagnant:

        self.text=QLabel(self)
        self.text.setText("Pas de gagnant !")
        self.text.setAlignment(Qt.AlignCenter)

        #bouton continuer pour fermer le résultat:

        self.continuer5=QPushButton("Continuer",self)
        self.continuer5.setFixedSize(580,50)
        self.continuer5.setFont(self.font)
        self.continuer5.clicked.connect(self.finResultat2)
        
        self.gagner3.setStyleSheet(self.styleGagner)
        
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.continuer5)
        
        self.gagner3.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.gagner3.show()        

    #fonction qui ferme le résultat du solo:
    
    def finResultat(self):
        self.bruit1.play()
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/musique.wav"))
        self.musique.play()
        self.gagner1.close()
        self.menuJouer()

    #fonction qui ferme le résultat du multi si il y a un gagnant:

    def finResultat1(self):
        self.bruit1.play()
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/musique.wav"))
        self.musique.play()
        self.gagner2.close()
        self.menuJouer()
    
    #fonction qui ferme le résultat du multi si aucun gagnant:

    def finResultat2(self):
        self.bruit1.play()
        self.musique.stop()
        self.musique.setSource(QUrl.fromLocalFile("sons/musique.wav"))
        self.musique.play()
        self.gagner3.close()
        self.menuJouer()

    #fonction qui crée le menu de réglage lorsque on appui sur le bouton option:

    def option2(self):
        self.bruit1.play()

        self.option1=QWidget(self)
        self.option1.setGeometry((self.frameGeometry().width()/2)-300,(self.frameGeometry().height()/2)-200,600,400)
        self.layout = QVBoxLayout()

        self.text=QLabel(self)
        self.text.setText("Volume :")
        self.text.setAlignment(Qt.AlignCenter)
        
        self.volume.setRange(0,100)
        self.volume.valueChanged.connect(self.VolumeP)

        self.option1.setStyleSheet(self.styleGagner)

        self.textB=QLabel(self)
        self.textB.setText("Bruitage :")
        self.textB.setAlignment(Qt.AlignCenter)

        self.volumeBruit.setRange(0,100)
        self.volumeBruit.valueChanged.connect(self.VolumeB)

        self.continuer5=QPushButton("Continuer",self)
        self.continuer5.setFixedSize(580,50)
        self.continuer5.setFont(self.font)
        self.continuer5.clicked.connect(self.menuRetour3)
 
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.volume)
        self.layout.addWidget(self.textB)
        self.layout.addWidget(self.volumeBruit)
        self.layout.addWidget(self.continuer5)
        
        self.option1.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.option1.show()

    #fonction qui récupère la valeur du slider volume pour l'appliquer au son de la musique du jeu:

    def VolumeP(self):
        self.vol=self.volume.value()/100
        self.musique.setVolume(self.vol)

    #fonction qui récupère la valeur du slider volume pour l'appliquer aux bruits du jeu:

    def VolumeB(self):
        self.volB=self.volumeBruit.value()/100
        self.bruit0.play()
        self.bruit0.setVolume(self.volB)
        self.bruit1.setVolume(self.volB)
        self.bruit2.setVolume(self.volB)
        self.bruit3.setVolume(self.volB)
        self.bruit4.setVolume(self.volB)
        self.bruit5.setVolume(self.volB)
        self.bruit6.setVolume(self.volB)
        self.bruit7.setVolume(self.volB)
        self.bruit8.setVolume(self.volB)
        self.bruit9.setVolume(self.volB)
        self.bruit10.setVolume(self.volB)
        self.bruit11.setVolume(self.volB)
        
    #fonction qui permet de de fermer le menu option:

    def menuRetour3(self):
        self.bruit1.play()
        self.option1.close()
        self.menu.show()

app = Application(sys.argv)
win = Window()
sys.exit(app.exec_())
