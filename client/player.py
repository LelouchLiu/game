import os
import pygame
import copy
from entity import Entity
from pymunk import Vec2d
import sprite_sheet
from sprite_strip_anim import SpriteStripAnim

class Player(Entity):

	def __init__(self, recPos, worldPos, seconds, resolution):
		Entity.__init__(self, recPos, worldPos, resolution, collisionType= 1)
		self.manager = None #set in view as of now
		self.identifier = 1 #temporary value, set by network
		self.seconds = seconds

	def setSprites(self):
		frames = 60 / 6
		self.sprites = {'death': SpriteStripAnim('explode.bmp', (0,0,24,24), 8, 1, True, frames)}

	def playAnim(self, anim):
		if anim in self.sprites:
			self.image = self.sprites[anim].next()
			oldPos = copy.deepcopy(self.rect.center)
			self.rect = self.image.get_rect()
			self.rect.center = oldPos
