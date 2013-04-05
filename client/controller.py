import pygame
from pygame import (K_w, K_a, K_s, K_d)
from pygame.locals import*
#from vector import *

class PlayerController(object):

	def __init__(self, player):
		self.player = player
		self.downDirections = []

	def parseKeys(self, keys):
		direction = self.calculateDirection(keys)
		self.player.setDirection(direction)

	#def mouseButton(self, position):
	#	self.player.fireProj(position, None)
		

	def handleEvent(self, event):
		if event.type == MOUSEBUTTONDOWN:
			keys = pygame.mouse.get_pressed()
			if keys[0]: #left
				pass
			elif keys[1]: #right
				pass

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