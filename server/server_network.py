from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor
from twisted.protocols.amp import AMP


class GameServer(AMP):

	#Translate AMP requests from clients into model operations and vice versa
	def __init__(self, world, clock=reactor):
		self.world = world
		self.manager = self.world.manager
		self.clock = clock
		#self.player = None
		


class GameFactory(ServerFactory):

	def __init__(self, world):
		self.world = world

	def buildProtocol(self, ignored):
		return GameServer(self.world)