#from vector import Vector
#from projectile import *
#from force import *
import os
import pygame
#import copy
#import math
PI = 3.141592653589793238462643383

class Player(pygame.sprite.Sprite):
	
	def __init__(self, position, seconds):
		pygame.sprite.Sprite.__init__(self)
		self.lastDirectionChange = seconds()
		self.direction = [0,-1]
		self.seconds = seconds
		self.observers = []
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/player.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.worldPos = position

	def getPosition(self):
		return list(self.worldPos)

	def addObserver(self, observer):
		#Add the given object to the list of those notified about state changes in this player.
		self.observers.append(observer)
