#Used by server and client to do updates and shit

import pygame
import types
from pygame.locals import*
from twisted.python.filepath import FilePath
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class Manager():

	def __init__(self, seconds, level=None):
		self.level = level
		self.seconds = seconds
		self.client = None #can refer to an actual client or server, not really important which
		self.players = pygame.sprite.Group()
		
	def update(self):
		pass	
		#self.updateProjectiles()
		#self.updateCreeps()
		
	def addPlayer(self, player):
		#self.modelobjects[id(player)] = player
		player.id = id(player)
		self.players.add(player)


				