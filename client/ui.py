
from twisted.internet.protocol import ClientFactory
from twisted.protocols.policies import ProtocolWrapper, WrappingFactory
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from network import NetworkController
#from view import Window
#from controller import PlayerController


class ConnectionNotificationWrapper(ProtocolWrapper):
	#A protocol wrapper which fires a Deferred when the connection is made.

	def makeConnection(self, transport):
		#Fire the Deferred at self.factory.connectionNotification with the real protocol.
		ProtocolWrapper.makeConnection(self, transport)
		self.factory.connectionNotification.callback(self.wrappedProtocol)

class ConnectionNotificationFactory(WrappingFactory):
	#A factory which uses ConnectionNotificationWrapper.
	#connectionNotification: The Deferred which will be fired with a Protocol at some point.
	protocol = ConnectionNotificationWrapper
	def __init__(self, realFactory):
		WrappingFactory.__init__(self, realFactory)
		self.connectionNotification = Deferred()



class UI(object):
	#windowFactory: The factory that should produce things like game.view.Window.
		
	def __init__(self, reactor=reactor, windowFactory=None):	
	#def __init__(self, reactor=reactor, windowFactory=Window):
		self.reactor = reactor
		self.windowFactory = windowFactory

	def connect(self, host, port):
		clientFactory = ClientFactory()
		clientFactory.protocol = lambda: NetworkController(self.reactor)
		factory = ConnectionNotificationFactory(clientFactory)
		self.reactor.connectTCP(host, port, factory)
		return factory.connectionNotification

	def gotInitialPlayer(self, player):
		#Hook up a PlayerView and a PlayerController for the given Player.
		self.window.submitTo(PlayerController(player))

	def introduce(self, protocol):
		self.protocol = protocol
		return self.protocol.introduce()

	def gotIntroduced(self, environment):
		#Hook up a user-interface controller for the Player and display the Environment in a Window.
		self.window = self.windowFactory(environment, self.reactor)
		player = environment.initialPlayer
		if player is not None:
			self.gotInitialPlayer(player)
		environment.start()
		self.window.client = player
		#player.window = self.window
		return self.window.go()

	def start(self,host,port):
		# - Connect to the given host and port.
		# - Make introductions.
		# - Run a GUI.
		d = self.connect(host, port)
		d.addCallback(self.introduce)
		d.addCallback(self.gotIntroduced)
		return d
		
		
	