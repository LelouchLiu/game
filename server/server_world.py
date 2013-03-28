#Model object for the server
import random
from twisted.application.service import Service
from twisted.internet.task import LoopingCall

#TCP_SERVICE_NAME = 'tcp-service-name'
#GAME_SERVICE_NAME = 'game-service-name'

#class World(SimulationTime):
class World():

	#windowSize = 400,400
	flag = True
	def __init__(self, platformClock=None, random=random, granularity=1, windowSize=[400,400]):
		pass
		#SimulationTime.__init__(self, granularity, platformClock)
		#self.random = random
		self.observers = []
		self.players = []
		self.manager = None
		#self.start()
		#self.loadLevel('level.txt')
		#lc = LoopingCall(self.update)
		#lc.start(1/60)


class GameService(Service):
	#An L{IService<twisted.application.service.IService>} which starts and stops simulation time on a L{World}.

	def __init__(self, world):
		self.world = world

	def startService(self):
		self.world.start()

	def stopService(self):
		self.world.stop()

