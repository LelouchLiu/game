import os
import copy
import pygame
import pymunk
from math import sin,cos,sqrt
from pymunk import Vec2d

class Projectile(pygame.sprite.Sprite):
	
	#temporary values
	velocity = 70
	dmg = 10
	maxRange = 600
	maxVel = 200
	mass = 10
	radius = 10
	elasticity = 0.9

	#friendlyFire=false won't hurt player, true:will 
	def __init__(self, rectPos, bodyPos, orientation, friendlyFire, seconds, identifier):
		pygame.sprite.Sprite.__init__(self)
		self.identifier = identifier
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/arrow.png"
		self.image = pygame.image.load(imgPath)
		self.origImage = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()	
		self.rect.center = rectPos
		self.lastPos = bodyPos
		self.bodyPos = bodyPos
		self.distTraveled = 0
		self.friendlyFire = friendlyFire
		self.seconds = seconds
		self.vector = Vec2d(cos(orientation), sin(orientation))
		self.rotate(orientation)
		self._setPhysics()

	def _setPhysics(self):
		#pymunk initializations
		self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius) #mass, width, height
		self.body = pymunk.Body(self.mass,  self.inertia) #Mass, Moment of inertia
		self.shape = pymunk.Circle(self.body, self.radius)
		self.body.position = pymunk.Vec2d(self.bodyPos[0], self.bodyPos[1])
		self.body._set_velocity_limit(self.maxVel)
		self.shape.elasticity = self.elasticity
		self.applyForce()

	#Apply the intial thrust force to object
	def applyForce(self):	
		thrust = self.velocity
		#multiplied by 100 because it seems to be slow
		force = pymunk.Vec2d(100 * thrust * self.vector.x, 100 *thrust * self.vector.y)
		offset = [0, 0]
		self.body.apply_impulse(force, r=offset)

	#Returns true if projectile has traveled its maximum range thus far	
	def distanceTraveled(self):
		xd = self.body.position[0] - self.lastPos[0]
		yd = self.body.position[1] - self.lastPos[1]
		self.distTraveled += sqrt(xd * xd + yd * yd)
		if self.distTraveled > self.maxRange:
			return True
		return False

	def rotate(self, orientation):
		#Why do I use 57 again? Figure that one out lol
		oldPos = copy.deepcopy(self.rect.center)
		self.image = pygame.transform.rotate(self.origImage, self.toDegrees(self.orientation))
		self.rect = self.image.get_rect(center=oldPos)
		self.body._set_angle(self.orientation)