import os
import pygame

#from vector import Vector
#from projectile import *
#from force import *
#import copy
#import math
#PI = 3.141592653589793238462643383

class Player(pygame.sprite.Sprite):
	
	speed = 10

	def __init__(self, position, seconds):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/player.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.worldPos = position
		self.lastDirectionChange = seconds()
		self.direction = [0,-1]
		self.seconds = seconds
		self.observers = []

	#center the player when resolution is set/changed
	def center(self, resolution):
		self.rect.center = (resolution[0]/2, resolution[1]/2)

	def getPosition(self):
		return list(self.worldPos)

	def addObserver(self, observer):
		#Add the given object to the list of those notified about state changes in this player.
		self.observers.append(observer)

	def setDirection(self, dir):
		self.direction = dir

	def update(self):
		self.updatePos()

	def updatePos(self):
		self.worldPos[0] += self.direction[0] * self.speed
		self.worldPos[1] += self.direction[1] * self.speed

		#Below will change
		self.rect.centerx += self.direction[0] * self.speed
		self.rect.centery += self.direction[1] * self.speed