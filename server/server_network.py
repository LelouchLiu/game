from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor
from twisted.protocols.amp import (AMP, Command, Integer, Float, Argument, String, Boolean)
from client.network_declarations import *

class GameServer(AMP):

	#Translate AMP requests from clients into model operations and vice versa
	def __init__(self, world, clock=reactor):
		self.world = world
		self.manager = self.world.manager
		self.clock = clock
		self.players = {}
		self.client = None

	def introduce(self):
		#Return game.environment.Environment and new game.player.Player data, and start watching for new player creation.
		player = self.world.createPlayer()
		identifier = self.identifierForPlayer(player)
		#self.clock.callLater(0, self.sendExistingState)
		self.client = player
		player.manager = self.manager
		pos = player.getPosition()
		return {"granularity": self.world.granularity, "identifier": identifier, "x": pos[0], "y": pos[1]}
	Introduce.responder(introduce)	

	def playerCreated(self, player):
		#Send data about the new player to the client that this protocol is connected to with a NewPlayer command.
		self.notifyPlayerCreated(player)
		player.addObserver(self)

	def playerRemoved(self, player):
		#Send data about the removed player to the client that this protocol is connected to with a RemovePlayer command.
		identifier = self.identifierForPlayer(player)
		self.callRemote(RemovePlayer, identifier=identifier)
		del self.players[identifier]

	def notifyPlayerCreated(self, player):
		#Notify the client that a new Player has been created.
		self.callRemote(NewPlayer, self.identifierForPlayer(player), list(player.getPosition()))

	def sendExistingState(self):
		self.sendExistingPlayers()
		self.sendCreepData()

	def playerForIdentifier(self, identifier):
		return self.players[identifier]

	def identifierForPlayer(self, player):
		#Return an identifier for the given Player. If the given Player has not been given before, create a new identifier.
		self.players[id(player)] = player
		return id(player)

	def directionChanged(self, player):
		#A Player's direction has changed: Send it to the client.
		identifier = self.identifierForPlayer(player)
		direction = player.direction
		self.callRemote(SetDirectionOf, identifier, direction)

	def setMyDirection(self, direction):
		#Set the direction of the player of the client connected to this protocol.
		self.client.direction = direction
		return {}
	SetMyDirection.responder(setMyDirection)

	def setMyPosition(self, identifier, x, y):
		player = self.playerForIdentifier(identifier)
		player.worldPos = [x,y]
		print player.worldPos
		return {}
	SetMyPosition.responder(setMyPosition)	

class GameFactory(ServerFactory):

	def __init__(self, world):
		self.world = world

	def buildProtocol(self, ignored):
		return GameServer(self.world)