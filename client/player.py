import os
import pygame
import view
import pymunk
import copy
from twisted.internet import reactor
from pymunk import Vec2d
from projectile import *

import sprite_sheet
from sprite_strip_anim import SpriteStripAnim

class Player(pygame.sprite.Sprite):
	
	#Constants for now...
	velocity = 50
	rotationSpeed = 0.087 #~5 degrees
	maxVel = 200
	mass = 10
	width = height = 20
	elasticity = 0.65

	def __init__(self, position, seconds, resolution):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/ship.gif"
		self.origImage = pygame.image.load(imgPath)
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.direction= Vec2d(0,-1)
		self.seconds = seconds
		self.observers = []
		self.orientation = 0
		self.coolDowns = [False]
		self.resolution = resolution
		self._setPhysics(position)
		self.alive = True

	#pymunk init
	def _setPhysics(self, pos):
		self.inertia = pymunk.moment_for_circle(self.mass, 0, self.width)
		self.body = pymunk.Body(self.mass,  self.inertia) #Mass, Moment of inertia
		self.shape = pymunk.Circle(self.body, self.width)
		self.body.position = pymunk.Vec2d(pos[0], self.flipy(pos[1]))
		self.body._set_velocity_limit(self.maxVel)
		self.body._set_angular_velocity_limit(0)
		self.shape.elasticity = self.elasticity

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
		#need to fire projectile in front of player
		if not self.coolDowns[identifier]:
			x = self.body.position[0] + (cos(self.orientation) * (self.width + 2))
			y = (self.body.position[1] + (sin(self.orientation) * (self.height + 2)))
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