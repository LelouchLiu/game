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
		self.client = None #can refer to client or server
		self.players = {}
		self.resolution = None
		
	def update(self):
		self.client.update()
		
	def addClient(self, client):
		self.client = client
		
	def addPlayer(self, player):
		self.players[id(player)] = player
		player.id = id(player)

	def removePlayer(self, player):
		del self.players[player.id]





				