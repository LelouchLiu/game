import pygame
from pygame import (K_w, K_a, K_s, K_d)
from pygame.locals import*
#from vector import *

class PlayerController(object):

	def __init__(self, player):
		self.player = player
		self.downDirections = []
		#Key map is used for dynamic mapping of keys, [function to call, arg]
		self.keyMap = {'K_SPACE': (self.player.fireProj, 0)}

	def parseKeys(self, keys):
		direction = self.calculateDirection(keys)
		self.player.setDirection(direction)
		if keys[K_SPACE]:
			function = self.keyMap['K_SPACE'][0]
			arg = self.keyMap['K_SPACE'][1]
			function(arg)

	def handleEvent(self, event):
		if event.type == MOUSEBUTTONDOWN:
			self.player.alive = not self.player.alive
			#keys = pygame.mouse.get_pressed()
			#if keys[0]: #left
			#self.player.fireProj()
			#elif keys[1]: #right

	#Calculate direction given pressed keys
	def calculateDirection(self, keys):
		x = y = 0

		if keys[K_w]:
			y = -1
		elif keys[K_s]:
			y = 1
		if keys[K_a]:
			x = -1
		elif keys[K_d]:
			x = 1	

		return [x,y]