#Model object for the server
import random
from twisted.application.service import Service
from twisted.internet.task import LoopingCall
from client.player import *
from client.environment import *
from client.manager import *


class World(SimulationTime):
	
	resolution = 600,600
	def __init__(self, platformClock=None, random=random, granularity=1, windowSize=[600,600]):
		SimulationTime.__init__(self, granularity, platformClock)
		#self.random = random
		self.observers = []
		self.players = []
		self.manager = Manager(seconds=self.seconds)
		self.start()
		#self.loadLevel('level.txt')
		#lc = LoopingCall(self.update)
		#lc.start(1/60)

	def update(self):
		self.manager.update()

	def createPlayer(self):
		#Make a new L{Player}.
		pos = [200,200]
		player = Player(pos, self.seconds)
		player.manager = self.manager
		self.manager.addPlayer(player)
		
		for observer in self.observers:
			observer.playerCreated(player)
		self.players.append(player)
		return player
		
	def getPlayers(self):
		#Return an iterator of all Players in this World.
		return iter(self.players)

	def removePlayer(self, player):
		#Stop tracking the given Player and notify observers via the playerRemoved method.
		self.players.remove(player)
		for observer in self.observers:
			observer.playerRemoved(player)

	def addObserver(self, observer):
		#Add the given object to the list of those notified about state changes in this world.
		self.observers.append(observer)

class GameService(Service):
	#An IService<twisted.application.service.IService which starts and stops simulation time on a World.

	def __init__(self, world):
		self.world = world

	def startService(self):
		self.world.start()

	def stopService(self):
		self.world.stop()

