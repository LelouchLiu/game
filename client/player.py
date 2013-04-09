import os
import pygame
import view
import math
import pymunk
import copy
from pymunk import Vec2d

PI = 3.141592653589793238462643383

class Player(pygame.sprite.Sprite):
	
	#Constants for now...
	thrust = 250
	rotationSpeed = 5
	maxVel = 200
	mass = 100
	width = height = 30
	elasticity = 1.0

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

		#pymunk initializations
		self.inertia = pymunk.moment_for_box(self.mass, self.width, self.height) #mass, width, height
		self.body = pymunk.Body(self.mass,  self.inertia) #Mass, Moment of inertia
		self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
		self.body.position = pymunk.Vec2d(position[0], position[1])
		self.body._set_velocity_limit(self.maxVel)

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


	def toRadians(self):
		#returns orientation in radians
		return float((self.orientation * PI) / 180.0)
	def updatePos(self):
		#self.worldPos[0] += self.direction[0] * self.speed
		#self.worldPos[1] += self.direction[1] * self.speed

		rad = self.toRadians()
		x = math.cos(rad)
		y = -math.sin(rad)
		thrust = self.thrust * -self.direction[1]
		force = pymunk.Vec2d(thrust * x,
				thrust * y)

		#print force
		#print x,y
		offset = [0, 0]
		
		self.body.apply_impulse(force, r=offset)
		#Below lines are temporary to show movement until environment is added
		pos = self.body.position
		#print self.body.velocity
		#print pos
		#print self.direction, pos
		#pos = Vec2d(pos.x, pos.y)
		#angle = math.degrees(self.body.angleq)
		#print angle
		#self.image = pygame.transform.rotate(self.image, angle)
		self.rect.center = (pos.x, pos.y)
		#print self.rect.center
		
		for observer in self.observers:
			observer.posChanged(self)

	#update rotation of ship
	def rotate(self):
		self.orientation += -self.direction[0] * self.rotationSpeed
		if self.orientation > 360:
			self.orientation -= 360
		elif self.orientation < 0:
			self.orientation += 360
		oldPos = copy.deepcopy(self.rect.center)
		self.image = pygame.transform.rotate(self.origImage, self.orientation)
		self.rect = self.image.get_rect(center=oldPos)
		self.body._set_angle(self.orientation)

	def fireProj(self, pos):
		proj = Projectile(self.rect.center, self.worldPos, pos, 0, self.seconds)
		self.manager.addProjectile(proj)
		#for observer in self.observers:
			#observer.createProjectile(proj)