#Used by server and client to do updates and shit

import pygame
import types
import pymunk
from pygame.locals import*
from pygame.colors import *
from twisted.python.filepath import FilePath
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class Manager():

	def __init__(self, seconds, level=None):
		self.level = level
		self.seconds = seconds
		self.client = None #can refer to client or server
		self.players = {}
		self.projectiles = pygame.sprite.Group()
		self.resolution = None

		self.space = pymunk.Space()
		self.temp()


	def temp(self):

		
	def update(self):
		self.client.update()
		self.updateProjectiles()

	def updateProjectiles(self):
		for proj in self.projectiles:
			if not proj.updatePos():
				proj.kill()
			#add collision detection
		
	def addClient(self, client):
		self.client = client
		
	def addPlayer(self, player):
		self.players[id(player)] = player
		player.id = id(player)

	def removePlayer(self, player):
		del self.players[player.id]

	def addProjectile(self, proj):
		self.projectiles.add(proj)



				