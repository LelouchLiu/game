#Used by server and client to do updates to game world

import pygame
import types
import pymunk
import copy
from math import sin,cos,sqrt,pi
from pygame.locals import*
from pygame.color import *
from twisted.python.filepath import FilePath
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from pymunk import Vec2d


class Manager():

	def __init__(self, seconds, level=None):
		self.level = level
		self.seconds = seconds
		self.client = None #can refer to client or server
		self.players = []
		self.projectiles = pygame.sprite.Group()
		self.resolution = None
		self.space = pymunk.Space()
		self.createSpace()
		self.clock = pygame.time.Clock()

	#temporary set-up
	def createSpace(self):
		staticLines = [pymunk.Segment(self.space.static_body, (50, 50), (50, 550), 5),
						pymunk.Segment(self.space.static_body, (50, 550), (550, 550), 5),
						pymunk.Segment(self.space.static_body, (550, 550), (550, 50), 5)]
		for line in staticLines:
			line.color = THECOLORS['lightgray']
			line.elasticity = .95

		self.space.add(staticLines)
		
	def update(self):
		#self.getFPS()
		self.updatePlayers()
		self.updateProjectiles()
		self.space.step(1.0/60)

	def updatePlayers(self):
		for obj in self.players:
			
			self.updateObjPos(obj)
			self.updateObjRot(obj)	

	def updateProjectiles(self):
		for proj in self.projectiles:
			pos = proj.body.position
			proj.rect.center = (pos.x, self.flipy(pos.y))
			proj.worldPos = (pos.x, self.flipy(pos.y))
			if proj.distanceTraveled():	
				self.removeProjectile(proj)

	#update object rotation
	def updateObjRot(self, obj):
		#update objects orientation to current body orientation. Commented out for now
		#obj.orientation = obj.toDegrees(obj.body._get_angle())
		obj.orientation += -obj.direction[0] * obj.rotationSpeed
		if obj.orientation > (2 * pi):
			obj.orientation -= (2 * pi)
		elif obj.orientation < 0:
			obj.orientation += (2 * pi)
		oldPos = copy.deepcopy(obj.rect.center)
		obj.image = pygame.transform.rotate(obj.origImage, self.toDegrees(obj.orientation))
		obj.rect = obj.image.get_rect(center=oldPos)
		obj.body._set_angle(obj.orientation)

	#update object position
	def updateObjPos(self, obj):
		x = cos(obj.orientation)
		y = sin(obj.orientation)
		thrust = obj.velocity * -obj.direction[1]
		force = pymunk.Vec2d(thrust * x, thrust * y)

		#TODO: figure out the offset behind the ship. see if it is any different
		offset = [0, 0]
		obj.body.apply_impulse(force, r=offset)
		pos = obj.body.position
		obj.rect.center = (pos.x, self.flipy(pos.y))

		#for observer in obj.observers:
			#observer.posChanged(obj)
		
	def addClient(self, client):
		self.client = client
		
	def addPlayer(self, player):
		self.players.append(player)
		self.space.add(player.body, player.shape)

	#def removePlayer(self, player):
		#del self.players[player.id]

	def addProjectile(self, proj):
		self.projectiles.add(proj)
		self.space.add(proj.body, proj.shape)

	def removeProjectile(self, proj):
		proj.kill()
		self.space.remove(proj.body, proj.shape)

	def flipy(self, y):
	#Used to flip y coordinate, pymunk and pygame are inverted :/
		return -y + self.resolution[1]

	def toRadians(self, angle):
		return angle * pi / 180.0

	def toDegrees(self, angle):
		return angle * 180 / pi
			
	def getFPS(self):
		self.clock.tick()
		print "FPS ", self.clock.get_fps()
