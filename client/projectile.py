import os
import copy
import pygame
import pymunk
from math import sin,cos,sqrt
from pymunk import Vec2d

class Projectile(pygame.sprite.Sprite):
	
	#temporary values
	velocity = 300
	dmg = 10
	maxRange = 200
	maxVel = 200
	mass = 10
	width = 20
	height = 5
	elasticity = 0.9

	#friendlyFire=false won't hurt player, true:will 
	def __init__(self, rectPos, worldPos, orientation, friendlyFire, seconds, identifier):
		pygame.sprite.Sprite.__init__(self)
		self.identifier = identifier
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/arrow.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()	
		self.rect.center = rectPos
		self.rect.inflate(-3,-2)
		self.initPos = self.worldPos = worldPos
		self.friendlyFire = friendlyFire
		self.seconds = seconds
		self.lastDirectionChange = seconds()
		self.vector = Vec2d(cos(orientation), sin(orientation))

		#pymunk initializations
		self.inertia = pymunk.moment_for_box(self.mass, self.width, self.height) #mass, width, height
		self.body = pymunk.Body(self.mass,  self.inertia) #Mass, Moment of inertia
		self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
		self.body.position = pymunk.Vec2d(worldPos[0], worldPos[1])
		self.body._set_velocity_limit(self.maxVel)
		#self.body._set_angular_velocity_limit(0)
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
		xd = self.worldPos[0] - self.initPos[0]
		yd = self.worldPos[1] - self.initPos[1]
		if sqrt(xd * xd + yd * yd) >= self.maxRange:
			return True
		return False
			
	def rotate(self):
		#Why do I use 57 again? Figure that one out lol
		self.image = pygame.transform.rotate(self.image, 57 * direction(self.vector.x,-self.vector.y))
