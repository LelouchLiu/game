import os
import pygame
import view
import pymunk
import copy
from math import sin,cos,sqrt
from entity import Entity
from twisted.internet import reactor
from pymunk import Vec2d
from projectile import *

import sprite_sheet
from sprite_strip_anim import SpriteStripAnim

class Player(pygame.sprite.Sprite, Physical):

	def __init__(self, recPos, worldPos, seconds, resolution):
		pygame.sprite.Sprite.__init__(self)
		Physical.__init__(self, worldPos, orientation=0, velocity=50, mass=10,
							elasticity=0.65, shape={"circle": 20}, maxVel=200, angularVel=0.087)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/ship.gif"
		self.origImage = pygame.image.load(imgPath)
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = recPos
		self.direction= Vec2d(0,-1)
		self.seconds = seconds
		self.observers = []
		self.coolDowns = [False]
		self.resolution = resolution
		self.alive = True

	#sprite init
	def setSprites(self):
		frames = 60 / 6
		self.sprites = {'death': SpriteStripAnim('explode.bmp', (0,0,24,24), 8, 1, True, frames)}

	def isAlive(self):
		return self.alive

	#center the player when resolution is set/changed
	def center(self, resolution):
		self.rect.center = (resolution[0]/2, resolution[1]/2)

	def getPosition(self):
		return list(self.worldPos)

	def addObserver(self, observer):
		#Add the given object to the list of those notified about state changes in this player.
		self.observers.append(observer)

	def setDirection(self, direction):
		self.direction = direction
		for observer in self.observers:
			observer.directionChanged(self)

	def resetCoolDown(self, identifier=None):
		self.coolDowns[identifier] = False

	#fire projectile of given id
	def fireProj(self, identifier):
		#need to fire projectile in front of entity
		if not self.coolDowns[identifier]:
			x = self.body.position[0] + (cos(self.orientation) * (self.radius + 2))
			y = (self.body.position[1] + (sin(self.orientation) * (self.radius + 2)))
			proj = Projectile([x, self.flipy(y)], [x, y], self.orientation, 
								0, self.seconds, identifier)
			self.manager.addProjectile(proj)
			self.coolDowns[identifier] = True
			reactor.callLater(.25, self.resetCoolDown, identifier=identifier)
		#for observer in self.observers:
			#observer.createProjectile(proj)

	#Used to flip y coordinate, pymunk and pygame are inverted :/
	def flipy(self, y):
		return -y + self.resolution[1]