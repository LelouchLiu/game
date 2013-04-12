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
		#self.defineCollisionHandlers()

	#Set up collision handlers
	def defineCollisionHandlers(self):
		#collisions between a & b, 
		self.collisionTypes = {'static': 0, 'player': 1, 'projectile': 2, 'creep': 3}
		self.space.add_collision_handler(self.client.identifier, self.collisionTypes['projectile'], post_solve = self.playerCollision)
		

	def playerCollision(self, space, arbiter):
		for shape in arbiter.shapes:
			print shape.collision_type

	def update(self):
		#self.getFPS()
		self.updatePlayers()
		self.updateProjectiles()
		self.space.step(1.0/60)

	def updatePlayers(self):
		for player in self.players:
			player.updatePos()

	def updateProjectiles(self):
		for proj in self.projectiles:
			pos = proj.body.position
			proj.rect.center = (pos.x, self.flipy(pos.y))
			#proj.rotate()
			if proj.distanceTraveled():	
				self.removeProjectile(proj)
			proj.lastPos = [pos.x, pos.y]	


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
			
	def getFPS(self):
		self.clock.tick()
		print "FPS ", self.clock.get_fps()

	def setResolution(self, resolution):
		self.resolution = resolution
