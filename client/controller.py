import pygame
from pygame import (K_w, K_a, K_s, K_d)
#from vector import *
KEYS_TO_DIRECTIONS = [K_w, K_a, K_s, K_d]

class PlayerController(object):
	#downDirections: List of currently held arrow keys.
	#mouseSensitivity: A multipler for how much rotation each unit ofrelative mouse movement should result in.
	mouseSensitivity = 0.25

	def __init__(self, player):
		self.player = player
		self.downDirections = []

	def keyDown(self, key):
		if key in KEYS_TO_DIRECTIONS:
			self.downDirections.append(key)
			self.player.setDirection(self.calculateDirection(self.downDirections))

			
	def keyUp(self, key):
		if key in KEYS_TO_DIRECTIONS:
			try:
				self.downDirections.remove(key)
			except ValueError:
				pass
			else:
				self.player.setDirection(self.calculateDirection(self.downDirections))

	def mouseButton(self, position):
		self.player.fireProj(position, None)

			
	def mouseMotion(self, position, (x, y), buttons):
		self.player.turn(y * self.mouseSensitivity, x * self.mouseSensitivity)

	def calculateDirection(self, pressedKeys):
		x = 0
		y = 0
		for key in pressedKeys:
			if key == K_w:
				y = -1
			elif key == K_s:
				y = 1
			if key == K_a:
				x = -1
			elif key == K_d:
				x = 1
		return [x,y]