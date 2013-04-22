from twisted.internet.task import LoopingCall, Clock
from player import Player

class SimulationTime(Clock):
	#A mechanism for performing updates to simulations such that all updates occur at the same instant.
	#If a SimulationTime.callLater is performed, when the function is called, it is guaranteed that no "time" (according to
	#SimulationTime.seconds will pass until the function returns.
	#platformClock: A provider of twisted.internet.interfaces.IReactorTime which will be used to update the model time.
	#granularity: The number of times to update the model time per second. That is, the number of "instants" per
	#second. e.g., specifying 2 would make calls to seconds() return 0 for 0.5 seconds, then 0.5 for 0.5 seconds, then 1 for 
	#0.5 seconds, and so on. This number directly represents the model frames per second.
	# _call: The result of the latest call to scheduler
	_call = None
	def __init__(self, granularity, platformClock):
		Clock.__init__(self)
		self.granularity = granularity
		self.platformClock = platformClock

	def _update(self, frames):
		#Advance the simulation time by one "tick", or one over granularity.
		self.advance(1.0 * frames / self.granularity)

	def start(self):
		self._call = LoopingCall.withCount(self._update)
		self._call.clock = self.platformClock
		self._call.start(1.0 / self.granularity, now=False)


	def stop(self):
		self._call.stop()


class Environment(SimulationTime):
	#The part of The World which is visible to a client.
	#observers: A list of objects notified about state changes of this object.
	#initialPlayer: None until an initial player is set, then whatever Player it is set to.
	#network: A NetworkController instance connected to the server for the world this environment is a view on to.
	
	initialPlayer = None
	network = None
	
	def __init__(self, *a, **kw):
		SimulationTime.__init__(self, *a, **kw)
		self.observers = []
		
	def setInitialPlayer(self, player):
		self.initialPlayer = player
		
	def setNetwork(self, network):
		#Specify a connected NetworkController instance which can be used to communicate with the server.
		self.network = network

	def addObserver(self, observer):
		self.observers.append(observer)
		
	def createPlayer(self, position):
		player = Player(position, self.seconds)
		for observer in self.observers:
			observer.playerCreated(player)
		return player
		
	def removePlayer(self, player):
		#Broadcast the removal of the given player to all registered observers.
		for observer in self.observers:
			observer.playerRemoved(player)