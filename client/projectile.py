import os
import copy
import pygame
from math import sin,cos,sqrt
from vector import *

class Projectile(pygame.sprite.Sprite):
	
	#temporary values
	speed = 50
	dmg = 10
	projRange = 200

	#wfriendlyFire=false won't hurt player true:will, vice versa for creeps,
	def __init__(self, rectPos, worldPos, targetPos, friendlyFire, seconds):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/arrow.png"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()	
		self.rect.center = rectPos
		self.rect.inflate(-3,-2)
		self.initPos = self.worldPos = worldPos
		self.getVector(targetPos)
		self.friendlyFire = friendlyFire
		self.seconds = seconds
		self.lastDirectionChange = seconds()
	
	def updatePos(self):
		now = self.seconds()
		elapsedTime = now - self.lastDirectionChange
		self.lastDirectionChange = self.seconds()
		magnitude = elapsedTime * self.speed
		self.worldPos[0] += int(self.vector.x * magnitude * self.speed)
		self.worldPos[1] += int(self.vector.y * magnitude * self.speed)
		
		#temporary
		self.rect.center = self.worldPos
		
		if self.distanceTraveled() >= self.projRange:
			return False
		else:
			return self.worldPos
					
	#returns how far the projectile has traveled thus far	
	def distanceTraveled(self):
		xd = self.worldPos[0] - self.initPos[0]
		yd = self.worldPos[1] - self.initPos[1]
		return sqrt(xd * xd + yd * yd)
			
	def rotate(self):
		self.image = pygame.transform.rotate(self.image, 57 * direction(self.vector.x,-self.vector.y))
		
	def getVector(self, target):
		xd = target[0] - self.rect.center[0]
		yd = target[1] - self.rect.center[1]
		if xd != 0 and yd!= 0:
			self.vector = Vector((xd / sqrt(xd*xd + yd*yd)), (yd / sqrt(xd*xd + yd*yd)))
		else:
			if xd == 0:
				if yd < 0:
					self.vector = Vector(0,-1)
				elif yd > 0:
					self.vector = Vector(0,1)
			elif yd == 0:
				if xd < 0:
					self.vector = Vector(-1,0)
				elif xd > 0:
					self.vector = Vector(1,0)