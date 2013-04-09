from __future__ import division
import pygame
import types
import sys
from pymunk.pygame_util import draw_space
from pygame.locals import*
from twisted.python.filepath import FilePath
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from manager import *
import copy
import string


class Window(object):

	screen = None
	FPS = 60

	#Intialize window object, anything initialzed to none is updated at a later time
	def __init__(self, environment, resolution, clock=reactor, event=pygame.event):
		self.environment = environment
		self.manager = None
		self.resolution = resolution
		self.environment.addObserver(self)
		self.clock = clock
		self.controller = None
		self.event = event
		self.client = None
		self.dynamicSprites = pygame.sprite.Group()
		self.staticSprites = pygame.sprite.Group()

	
	def paint(self):
		black = 0, 0, 0
		self.screen.fill(black)
		self.drawProjectiles()
		self.drawPlayers()
		self.dynamicSprites.draw(self.screen)
		self.staticSprites.draw(self.screen)
		draw_space(self.screen, self.manager.space) #pymunk space
		pygame.display.flip()
		self.dynamicSprites.empty()


	def drawProjectiles(self):
		for proj in self.manager.projectiles:
			#add collision shit here and move projectile accordingly to player view
			self.dynamicSprites.add(proj)
	def drawPlayers(self):
		#draw players inside client.camera
		pass
				
	def drawLevel(self):
		pass
		#self.level.draw(self.screen, self.client.camera)
		
	def createLevel(self):
		#self.level = Level(self.size, None, 'level.txt')
		#self.level = None
		#if self.environment.network:
		#	self.environment.network.loadLevel('level.txt')
		self.manager = Manager(self.client.seconds)
		self.manager.addPlayer(self.client)
		self.manager.addClient(self.client)
		self.manager.resolution = self.resolution
		
		#self.level.manager = self.manager
		#self.level.screen = self.screen
		self.client.manager = self.manager
			
		
	def handleInput(self):
		#Retrieve outstanding pygame input events and dispatch them.
		for event in self.event.get():
			self._handleEvent(event)

		pygame.event.pump()
		keystate =  pygame.key.get_pressed()
		self.controller.parseKeys(keystate)	

	def _handleEvent(self, event):
		#Handle a single pygame input event.
		if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			self.stop()
		else:
			self.controller.handleEvent(event)
							
	def submitTo(self, controller):
		#Specify the given controller as the one to receive further events.
		self.controller = controller
	
	def go(self):
		#Show this window.
		#return: A Deferred that fires when this window is closed by the user.
		pygame.init()
	
		self.screen = pygame.display.set_mode(self.resolution)
		self.staticSprites.add(self.client)
		self.createLevel()
		
		self._renderCall = LoopingCall(self.paint)
		self._renderCall.start(1 / self.FPS, now=False)
		self._updateCall = LoopingCall(self.manager.update)
		self._updateCall.start(1 / self.FPS, now=False)
		self._inputCall = LoopingCall(self.handleInput)

		finishedDeferred = self._inputCall.start(.04, now=False)
		finishedDeferred.addCallback(lambda ign: self._renderCall.stop())
		finishedDeferred.addCallback(lambda ign: pygame.display.quit())
		return finishedDeferred
		
	def stop(self):
		#Stop updating this window and handling events for it.
		self.environment.stop()
		self.clock.stop()
		
		#sys.exit()
		

	def playerCreated(self, player):
		self.sprites.add(player)
		self.manager.addPlayer(player)
		
	def playerRemoved(self, player):
		view = self._playerViews.pop(player)
		self.sprites.remove(player)
		#sel.scene._items.remove(view)


class PlayerView():

	def paint(self):	
		position = self.player.getPosition()
			

