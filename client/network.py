from twisted.protocols.amp import (AMP, Command, Integer, Float, Argument, String, Boolean)
from environment import *
from player import *
from network_declarations import *

class NetworkController(AMP):
	#A controller which responds to AMP commands to make state changes to local model objects.
	#modelObjects: A dict mapping identifiers to model objects.
	#clock: A provider of IReactorTime which will be used to update the model time.
	environment = None

	def __init__(self, clock):
		self.modelObjects = {}
		self.clock = clock

	def addModelObject(self, identifier, modelObject):
		#Associate a network identifier with a model object.
		self.modelObjects[identifier] = modelObject
		modelObject.addObserver(self)
		

	def sendMessage(self, message, id):
		self.callRemote(SendMessage, message=message, id=id )
	
	def createInitialPlayer(self, environment, identifier, position):
		#Create this client's player as the initial player in the given environment and add it to the model object mapping.
		player = environment.createPlayer(position, speed)
		player.id = identifier
		environment.setInitialPlayer(player)
		self.addModelObject(identifier, player)


	def introduce(self):
		#Greet the server and register the player model object which belongs to this client 
		#and remember the identifier with which it responds.
		d = self.callRemote(Introduce)
		def cbIntroduce(box):
			granularity = box['granularity']
			self.environment = Environment(granularity, self.clock)
			self.environment.setNetwork(self)
			pos = [box['x'],box['y']]
			self.createInitialPlayer(self.environment, box['identifier'], pos)
			return self.environment
		d.addCallback(cbIntroduce)
		return d

	def objectByIdentifier(self, identifier):
		#Look up a pre-existing model object by its network identifier.
		#@type identifier: C{int}
		#@raise KeyError: If no existing model object has the given identifier.
		return self.modelObjects[identifier]

	def identifierByObject(self, modelObject):
		#Look up the network identifier for a given model object.
		#@raise ValueError: If no network identifier is associated with the given model object.
		#@rtype: L{int}
		for identifier, object in self.modelObjects.iteritems():
			if object is modelObject:
				return identifier
		raise ValueError("identifierByObject passed unknown model objects")
		

	def newPlayer(self, identifier, pos):
		#Add a new Player object to the Environment and start tracking its identifier on the network.
		player = self.environment.createPlayer(pos)
		self.modelObjects[identifier] = player
		return {}
	NewPlayer.responder(newPlayer)


	def removePlayer(self, identifier):
		#Remove an existing Player object from the Environment and stop tracking its identifier on the network.
		self.environment.removePlayer(self.objectByIdentifier(identifier))
		del self.modelObjects[identifier]
		return {}
	RemovePlayer.responder(removePlayer)