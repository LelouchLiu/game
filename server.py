#Entry point to start the server
import sys
from twisted.internet import reactor
from twisted.application.service import MultiService
from twisted.application.service import IServiceMaker
from twisted.application.internet import TCPServer
#from server.server_network import GameFactory
#from server.server_world import *

#sys.path.append('data')

def main():
	print 'Server Started'
	#world = World(granularity=100, platformClock=reactor)
	#factory = GameFactory(world)
	reactor.listenTCP(1338, factory)	
	reactor.run()

if __name__ == '__main__':
    main()