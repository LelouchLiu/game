import os
import pygame
import view
import math
import pymunk
from pymunk import Vec2d


#from vector import Vector
#from projectile import *
#from force import *
import copy
#import math
#PI = 3.141592653589793238462643383

class Player(pygame.sprite.Sprite):
	
	speed = 50
	rotationSpeed = 10
	
	def __init__(self, position, seconds):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/ship.gif"
		self.origImage = pygame.image.load(imgPath)
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = self.worldPos = position
		self.lastDirectionChange = seconds()
		self.direction = [0,-1]
		self.seconds = seconds
		self.observers = []
		self.orientation = 0

		self.mass = 500
		self.width = self.height = 30
		self.inertia = pymunk.moment_for_box(500, self.width, self.height) #mass, width, height
		self.elasticity = 1.0
		self.body = pymunk.Body(self.mass,  self.inertia) #Mass, Moment of inertia
		self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
		self.body.position = pymunk.Vec2d(position[0], position[1])

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
		for observer in self.observers:
			observer.directionChanged(self)

	def update(self):
		self.rotate()
		self.updatePos()

	def updatePos(self):
		#self.worldPos[0] += self.direction[0] * self.speed
		#self.worldPos[1] += self.direction[1] * self.speed

		
		#self.body.velocity = (self.direction[0] * self.speed, self.direction[1] * self.speed)
		
		#need to rotate the ship


		#Below lines are temporary to show movement until environment is added
		#pos = self.body.position
		#print self.direction, pos
		#pos = Vec2d(pos.x, pos.y)
		#angle = math.degrees(self.body.angleq)
		#print angle
		#self.image = pygame.transform.rotate(self.image, angle)
		#self.rect.center = (pos.x, pos.y)
		
		for observer in self.observers:
			observer.posChanged(self)

	#update rotation of ship
	def rotate(self):
		self.orientation += self.direction[0] * self.rotationSpeed
		oldPos = copy.deepcopy(self.rect.center)
		self.image = pygame.transform.rotate(self.origImage, self.orientation)
		self.rect = self.image.get_rect(center=oldPos)

	def fireProj(self, pos):
		proj = Projectile(self.rect.center, self.worldPos, pos, 0, self.seconds)
		self.manager.addProjectile(proj)
		#for observer in self.observers:
			#observer.createProjectile(proj)


	def rotate(self, image, angle):
		#rotate an image while keeping its center and size
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image