import os
import copy
import pygame
import pymunk
from physical import Physical
from pymunk import Vec2d
from math import sqrt

class Projectile(pygame.sprite.Sprite, Physical):
	
	dmg = 10
	maxRange = 500
	#friendlyFire=false won't hurt player, true:will 

	def __init__(self, rectPos, bodyPos, orientation, friendlyFire, seconds, identifier, collisionType):
		pygame.sprite.Sprite.__init__(self)
		Physical.__init__(self, bodyPos, orientation, velocity=70, 
								mass=10, elasticity=0.9, shape={"circle": 10}, 
								maxVel=200, collisionType=collisionType)
		self.identifier = identifier
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/arrow.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()	
		self.rect.center = rectPos
		self.lastPos = bodyPos
		self.distTraveled = 0
		self.friendlyFire = friendlyFire
		self.seconds = seconds
		#self.rotate(orientation)
		self.applyImpulse()

	#Returns true if projectile has traveled its maximum range thus far	
	def distanceTraveled(self):
		xd = self.body.position[0] - self.lastPos[0]
		yd = self.body.position[1] - self.lastPos[1]
		self.distTraveled += sqrt(xd * xd + yd * yd)
		if self.distTraveled > self.maxRange:
			return True
		return False

	def rotate(self, orientation):
		self.image = pygame.transform.rotate(self.origImage, self.toDegrees(self.orientation))
		self.body._set_angle(self.orientation)